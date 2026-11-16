"""Start the demo with a WSGI server for short remote evaluation sessions."""

import os
import secrets

from waitress import serve

from app import create_app


app = create_app(
    {
        # A fresh signing key protects browser sessions for this run only.
        "SECRET_KEY": secrets.token_urlsafe(48),
        # Quick Tunnels present HTTPS to visitors.
        "SESSION_COOKIE_SECURE": True,
    }
)


if __name__ == "__main__":
    port = int(os.environ.get("CUPCAKESC_PORT", "5000"))
    print(f"Cupcakes C remoto em http://127.0.0.1:{port}")
    print("Mantenha este terminal aberto durante os testes.")
    serve(app, host="127.0.0.1", port=port, threads=4)
