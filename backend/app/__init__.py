import logging
import os
from app.mongo_connection import init_mongo, mongo
from app.mysql_connection import init_mysql, db
from flask import Flask
from datetime import timedelta
from flask_cors import CORS
from sqlalchemy.exc import OperationalError


logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
    app.config["SESSION_COOKIE_SECURE"] = True  # Only send cookie over HTTPS
    app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JavaScript access to cookies
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Restrict cross-site requests
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

    # CORS
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
        ],
        supports_credentials=True,
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Credentials",
        ],
    )

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MONGO_URI"] = os.getenv("MONGODB_URL")

    # Initialize database
    init_mysql(app)
    init_mongo(app)

    # register blueprints
    from app.routes import crumbl_blueprint
    from app.crumbls_order import crumbl_order

    app.register_blueprint(crumbl_blueprint)
    app.register_blueprint(crumbl_order, url_prefix="/order")

    return app
