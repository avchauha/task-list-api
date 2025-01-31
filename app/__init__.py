from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        # Set up configurations for production environment
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "RENDER_DATABASE_URI")
        app.config["SLACK_API_TOKEN"] = os.environ.get("SLACK_API_TOKEN")
        app.config["SLACK_API_URL"] = os.environ.get("SLACK_API_URL")
        app.config["SLACK_CHANNEL"] = os.environ.get("SLACK_CHANNEL")
    else:
        # Set up configurations for testing environment
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")
        app.config["SLACK_API_TOKEN"] = os.environ.get("SLACK_API_TOKEN_TEST")
        app.config["SLACK_API_URL"] = os.environ.get("SLACK_API_URL")
        app.config["SLACK_CHANNEL"] = os.environ.get("SLACK_CHANNEL_TEST")

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here

    from .tasks_routes import tasks_bp
    app.register_blueprint(tasks_bp)
    from . goals_routes import goals_bp
    app.register_blueprint(goals_bp)

    return app
