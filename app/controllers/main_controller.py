from flask import Blueprint, current_app, jsonify, redirect, render_template, request, session, url_for

main_bp = Blueprint("main", __name__)


def format_brl(cents):
    amount = f"{cents / 100:,.2f}"
    return "R$ " + amount.replace(",", "X").replace(".", ",").replace("X", ".")


def get_cupcake(flavor_id):
    return next((item for item in current_app.config["CUPCAKES"] if item["id"] == flavor_id), None)


def get_cart():
    return session.setdefault("cart", [])


def cart_count():
    return sum(item.get("quantity", 0) for item in session.get("cart", []))


@main_bp.get("/")
def home():
    return render_template("home.html")


@main_bp.post("/demo-login")
def demo_login():
    return redirect(url_for("main.catalog"))


@main_bp.get("/catalog")
def catalog():
    combos = current_app.config["COMBOS"]
    cupcakes = current_app.config["CUPCAKES"]
    for item in combos + cupcakes:
        item["price_display"] = format_brl(item["price_cents"])
    return render_template("catalog.html", combos=combos, cupcakes=cupcakes)


@main_bp.get("/profile")
def profile():
    return render_template("profile.html")


@main_bp.route("/combos/<int:units>", methods=["GET", "POST"])
def choose_combo(units):
    combo = next((item for item in current_app.config["COMBOS"] if item["units"] == units), None)
    if combo is None:
        return redirect(url_for("main.catalog"))

    cart_items = get_cart()
    raw_edit_index = request.form.get("edit_index") if request.method == "POST" else request.args.get("edit")
    edit_index = None
    editing_item = None

    if raw_edit_index not in (None, ""):
        try:
            edit_index = int(raw_edit_index)
        except ValueError:
            return redirect(url_for("main.cart"))
        if edit_index < 0 or edit_index >= len(cart_items):
            return redirect(url_for("main.cart"))
        candidate = cart_items[edit_index]
        if candidate.get("kind") != "combo" or candidate.get("name") != combo["name"]:
            return redirect(url_for("main.cart"))
        editing_item = candidate

    cupcakes = current_app.config["CUPCAKES"]
    quantities = {item["id"]: 0 for item in cupcakes}
    error = None

    if request.method == "GET" and editing_item:
        for flavor in editing_item.get("flavors", []):
            if flavor.get("id") in quantities:
                quantities[flavor["id"]] = max(0, int(flavor.get("quantity", 0)))

    if request.method == "POST":
        try:
            quantities = {
                item["id"]: max(0, int(request.form.get("flavor_" + item["id"], "0")))
                for item in cupcakes
            }
        except (TypeError, ValueError):
            error = "Revise as quantidades escolhidas."
        if error is None and sum(quantities.values()) != units:
            error = "Escolha exatamente " + str(units) + " cupcakes para esta caixa."

        if error is None:
            flavors = [
                {"id": item["id"], "name": item["name"], "quantity": quantities[item["id"]]}
                for item in cupcakes if quantities[item["id"]] > 0
            ]
            updated_item = {
                "kind": "combo",
                "units": units,
                "name": combo["name"],
                "quantity": 1,
                "unit_price_cents": combo["price_cents"],
                "flavors": flavors,
            }
            if edit_index is not None:
                updated_item["quantity"] = editing_item.get("quantity", 1)
                cart_items[edit_index] = updated_item
            else:
                get_cart().append(updated_item)
            session.modified = True
            return redirect(url_for("main.cart"))

    for item in cupcakes:
        item["price_display"] = format_brl(item["price_cents"])
    combo["price_display"] = format_brl(combo["price_cents"])
    return render_template(
        "combo_select.html",
        combo=combo,
        cupcakes=cupcakes,
        quantities=quantities,
        error=error,
        editing=edit_index is not None,
        edit_index=edit_index,
        editing_quantity=editing_item.get("quantity", 1) if editing_item else 1,
    )


@main_bp.post("/cart/add/<flavor_id>")
def add_single(flavor_id):
    cupcake = get_cupcake(flavor_id)
    if cupcake is None:
        return redirect(url_for("main.catalog"))

    cart = get_cart()
    existing = next((item for item in cart if item["kind"] == "single" and item["flavor_id"] == flavor_id), None)
    if existing:
        existing["quantity"] += 1
    else:
        cart.append({
            "kind": "single",
            "flavor_id": cupcake["id"],
            "name": cupcake["name"],
            "quantity": 1,
            "unit_price_cents": cupcake["price_cents"],
        })
    session.modified = True
    return redirect(url_for("main.catalog"))


def cart_context():
    items = get_cart()
    combos = current_app.config["COMBOS"]
    for item in items:
        item["line_total_cents"] = item["unit_price_cents"] * item["quantity"]
        item["unit_price_display"] = format_brl(item["unit_price_cents"])
        item["line_total_display"] = format_brl(item["line_total_cents"])
        if item["kind"] == "combo":
            item["units"] = next((combo["units"] for combo in combos if combo["name"] == item["name"]), 0)
    subtotal = sum(item["line_total_cents"] for item in items)
    shipping = current_app.config["SHIPPING_CENTS"] if items else 0
    return {
        "items": items,
        "subtotal_display": format_brl(subtotal),
        "shipping_display": format_brl(shipping),
        "total_display": format_brl(subtotal + shipping),
    }


@main_bp.get("/cart")
def cart():
    return render_template("cart.html", **cart_context())


@main_bp.post("/cart/change/<int:item_index>/<action>")
def change_cart_item(item_index, action):
    cart_items = get_cart()
    if item_index < 0 or item_index >= len(cart_items):
        return redirect(url_for("main.cart"))
    if action == "remove":
        cart_items.pop(item_index)
    elif action == "increase":
        cart_items[item_index]["quantity"] += 1
    elif action == "decrease":
        cart_items[item_index]["quantity"] -= 1
        if cart_items[item_index]["quantity"] <= 0:
            cart_items.pop(item_index)
    session.modified = True
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        messages = {
            "increase": "Quantidade aumentada.",
            "decrease": "Quantidade reduzida.",
            "remove": "Item removido do carrinho.",
        }
        return jsonify(
            html=render_template("cart_content.html", **cart_context()),
            cart_count=cart_count(),
            message=messages.get(action, "Carrinho atualizado."),
        )
    return redirect(url_for("main.cart"))


@main_bp.post("/cart/clear")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("main.cart"))


@main_bp.app_context_processor
def inject_cart_count():
    return {"cart_count": cart_count()}
