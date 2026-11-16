from flask import Flask

from app.config import Config
from app.models.database import init_app as init_database


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    from app.controllers.main_controller import main_bp
    from app.controllers.order_controller import orders_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(orders_bp)

    init_database(app)
    return app
