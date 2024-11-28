import logging
import time
import os

from flask import Flask
from datetime import timedelta
from app.database_model import db
from flask_cors import CORS
from sqlalchemy.exc import OperationalError


logger = logging.getLogger(__name__)


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

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Import models
    from app.database_model import User, PublicCrum

    with app.app_context():
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                db.create_all()
                print("Database tables created succesfully")
                logging.info("Database tables created successfully")
                break
            except OperationalError as e:
                retry_count += 1
                if retry_count == max_retries:
                    print(f"Failed to connect to database after {max_retries} attempts")
                    raise e
                print(f"Database connection attempt {retry_count} failed, retrying...")
                time.sleep(5)

    # register blueprints
    from app.routes import crumbl_blueprint

    app.register_blueprint(crumbl_blueprint)

    return app
