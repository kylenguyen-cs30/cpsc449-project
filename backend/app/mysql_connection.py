import logging
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()
logger = logging.getLogger(__name__)


def init_mysql(app):
    # Initialize database
    db.init_app(app)

    # push an application context
    app.app_context().push()

    # import models

    with app.app_context():
        from app.database_model import User, PublicCrum, PrivateCrum

        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                db.create_all()
                print("MySQL database tables created successfully")
                logging.info("MySQL database tables created succesfully")
                break
            except OperationalError as e:
                retry_count += 1
                if retry_count == max_retries:
                    print(
                        f"Failed to connect to mysql database after {max_retries} attempts"
                    )
                    raise e
                print(
                    f"MYSQL database connection attempt {retry_count} failed, retrying..."
                )
                time.sleep(5)
