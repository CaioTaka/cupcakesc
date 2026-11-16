import json
import uuid
from datetime import datetime, timezone

from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, session, url_for

from app.models.database import get_db

orders_bp = Blueprint("orders", __name__, url_prefix="/order")


def format_brl(cents):
    amount = f"{cents / 100:,.2f}"
    return "R$ " + amount.replace(",", "X").replace(".", ",").replace("X", ".")


def cart_totals(items):
    subtotal = sum(item["unit_price_cents"] * item["quantity"] for item in items)
    shipping = current_app.config["SHIPPING_CENTS"] if items else 0
    return subtotal, shipping, subtotal + shipping


def order_progress(created_at):
    created = datetime.fromisoformat(created_at).replace(tzinfo=timezone.utc)
    elapsed = max(0, int((datetime.now(timezone.utc) - created).total_seconds()))
    accepted = current_app.config["ORDER_AUTO_ACCEPT_SECONDS"]
    prep_end = accepted + current_app.config["PREPARATION_SECONDS"]
    delivered = prep_end + current_app.config["DELIVERY_ESTIMATE_SECONDS"]
    if elapsed < accepted:
        return "recebido"
    if elapsed < prep_end:
        return "em_preparo"
    if elapsed < delivered:
        return "saiu_para_entrega"
    return "entregue"


def order_state(created_at):
    created = datetime.fromisoformat(created_at).replace(tzinfo=timezone.utc)
    elapsed = max(0, int((datetime.now(timezone.utc) - created).total_seconds()))
    accept_seconds = current_app.config["ORDER_AUTO_ACCEPT_SECONDS"]
    prep_seconds = current_app.config["PREPARATION_SECONDS"]
    delivery_seconds = current_app.config["DELIVERY_ESTIMATE_SECONDS"]
    prep_ends = accept_seconds + prep_seconds
    delivery_ends = prep_ends + delivery_seconds
    if elapsed < accept_seconds:
        return {"status": "recebido", "label": "Pedido recebido", "message": "Seu pedido será aceito automaticamente em instantes.", "countdown_label": "Confirmação automática", "remaining": accept_seconds - elapsed, "stage": 1}
    if elapsed < prep_ends:
        return {"status": "em_preparo", "label": "Pedido aceito · em preparo", "message": "A confeitaria está preparando seus cupcakes.", "countdown_label": "Previsão para sair da loja", "remaining": prep_ends - elapsed, "stage": 2}
    if elapsed < delivery_ends:
        return {"status": "saiu_para_entrega", "label": "Saiu para entrega", "message": "O motoboy está a caminho.", "countdown_label": "Previsão de entrega", "remaining": delivery_ends - elapsed, "stage": 3}
    return {"status": "entregue", "label": "Pedido entregue", "message": "Pedido concluído. Obrigado!", "countdown_label": "Status", "remaining": 0, "stage": 4}


@orders_bp.get("/history")
def history():
    browser_id = session.get("demo_browser_id")
    orders = []
    if browser_id:
        db = get_db()
        rows = db.execute(
            "SELECT id, total_cents, payment_method, status, created_at FROM orders WHERE browser_id = ? ORDER BY id DESC",
            (browser_id,),
        ).fetchall()
        status_names = {
            "recebido": "Pedido recebido",
            "em_preparo": "Em preparo",
            "saiu_para_entrega": "Saiu para entrega",
            "entregue": "Entregue",
        }
        for row in rows:
            order = dict(row)
            current_status = order_progress(order["created_at"])
            if order["status"] != current_status:
                db.execute("UPDATE orders SET status = ? WHERE id = ?", (current_status, order["id"]))
            order["status"] = current_status
            order["status_display"] = status_names[current_status]
            order["total_display"] = format_brl(order["total_cents"])
            order["payment_display"] = {"credit": "Crédito", "debit": "Débito", "pix": "Pix"}.get(order["payment_method"], "Não informado")
            orders.append(order)
        db.commit()
    return render_template("order_history.html", orders=orders)


@orders_bp.get("/checkout")
def checkout():
    items = session.get("cart", [])
    if not items:
        return redirect(url_for("main.cart"))

    subtotal, shipping, total = cart_totals(items)
    display_items = []
    for item in items:
        display_items.append({
            "name": item["name"],
            "quantity": item["quantity"],
            "line_total": format_brl(item["unit_price_cents"] * item["quantity"]),
        })

    return render_template(
        "checkout.html",
        items=display_items,
        subtotal_display=format_brl(subtotal),
        shipping_display=format_brl(shipping),
        total_display=format_brl(total),
        pickup_address=current_app.config["PICKUP_ADDRESS"],
        delivery_address=current_app.config["DELIVERY_ADDRESS"],
        pix_key=current_app.config["PIX_DEMO_KEY"],
    )


@orders_bp.post("/confirm")
def confirm_order():
    items = session.get("cart", [])
    if not items:
        return redirect(url_for("main.cart"))

    subtotal, shipping, total = cart_totals(items)
    browser_id = session.get("demo_browser_id")
    if not browser_id:
        browser_id = uuid.uuid4().hex
        session["demo_browser_id"] = browser_id

    order_snapshot = [
        {
            "name": item["name"],
            "quantity": item["quantity"],
            "unit_price_cents": item["unit_price_cents"],
            "flavors": item.get("flavors", []),
        }
        for item in items
    ]
    payment_method = request.form.get("payment_method", "credit")
    if payment_method not in {"credit", "debit", "pix"}:
        payment_method = "credit"

    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO orders (browser_id, customer_name, items_json, total_cents, payment_method, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            browser_id,
            current_app.config["DEMO_CUSTOMER_NAME"],
            json.dumps(order_snapshot, ensure_ascii=False),
            total,
            payment_method,
            "recebido",
        ),
    )
    db.commit()
    order_id = cursor.lastrowid
    session["cart"] = []
    return redirect(url_for("orders.track_order", order_id=order_id))


@orders_bp.get("/<int:order_id>")
def track_order(order_id):
    browser_id = session.get("demo_browser_id")
    if not browser_id:
        abort(404)

    db = get_db()
    order = db.execute(
        "SELECT * FROM orders WHERE id = ? AND browser_id = ?",
        (order_id, browser_id),
    ).fetchone()
    if order is None:
        abort(404)

    state = order_state(order["created_at"])
    status = state["status"]

    if order["status"] != status:
        db.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        db.commit()

    previous_orders = [dict(row) for row in db.execute(
        """
        SELECT id, total_cents, payment_method, status, created_at
        FROM orders
        WHERE browser_id = ? AND id <> ?
        ORDER BY id DESC
        LIMIT 5
        """,
        (browser_id, order_id),
    ).fetchall()]

    for previous in previous_orders:
        previous["total_display"] = format_brl(previous["total_cents"])
        previous["status_display"] = {
            "recebido": "Recebido",
            "em_preparo": "Em preparo",
            "saiu_para_entrega": "Saiu para entrega",
            "entregue": "Entregue",
        }.get(previous["status"], previous["status"])
        previous["payment_display"] = {"credit": "Crédito", "debit": "Débito", "pix": "Pix"}.get(previous["payment_method"], "Não informado")

    items = json.loads(order["items_json"])
    for item in items:
        item["line_total_display"] = format_brl(item["unit_price_cents"] * item["quantity"])

    return render_template(
        "order_status.html",
        order=order,
        items=items,
        total_display=format_brl(order["total_cents"]),
        payment_display={"credit": "Crédito", "debit": "Débito", "pix": "Pix"}.get(order["payment_method"], "Não informado"),
        status_label=state["label"],
        status_message=state["message"],
        countdown_label=state["countdown_label"],
        remaining_seconds=state["remaining"],
        stage=state["stage"],
        is_delivered=(status == "entregue"),
        previous_orders=previous_orders,
        delivery_address=current_app.config["DELIVERY_ADDRESS"],
    )


@orders_bp.get("/<int:order_id>/progress")
def progress(order_id):
    browser_id = session.get("demo_browser_id")
    if not browser_id:
        abort(404)
    db = get_db()
    order = db.execute("SELECT * FROM orders WHERE id = ? AND browser_id = ?", (order_id, browser_id)).fetchone()
    if order is None:
        abort(404)
    state = order_state(order["created_at"])
    if order["status"] != state["status"]:
        db.execute("UPDATE orders SET status = ? WHERE id = ?", (state["status"], order_id))
        db.commit()
    return jsonify({
        "status": state["status"],
        "label": state["label"],
        "message": state["message"],
        "countdown_label": state["countdown_label"],
        "remaining": state["remaining"],
        "stage": state["stage"],
        "delivered": state["status"] == "entregue",
    })
