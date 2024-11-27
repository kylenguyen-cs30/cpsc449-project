import os

from flask import Flask
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # TODO: MATTHEW please add your works here.
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

    # Session cookie security settings
    app.config["SESSION_COOKIE_SECURE"] = True  # Only send cookie over HTTPS
    app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JavaScript access to cookies
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Restrict cross-site requests

    # Set a session lifetime for automatic logout of inactive users
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
    # PERF: CORS no need enable yet
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

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "my-default-secret-key")

    from app.routes import crumbl_blueprint

    app.register_blueprint(crumbl_blueprint)
    return app
