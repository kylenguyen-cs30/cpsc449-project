import os

from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# from flask_migrate import Migrate, migrate

# db = SQLAlchemy()
# migrate = Migrate()


def create_app():
    app = Flask(__name__)

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

    # NOTE: Enable Database later
    #
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    #     "DATABASE_URL", "postgresql://admin:password@db/cpsc449_project"
    # )
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # db.init_app(app)
    # migrate.init_app(app, db)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "my-default-secret-key")

    from app.routes import crumbl_blueprint

    app.register_blueprint(crumbl_blueprint)
    return app
