from pathlib import Path

from flask import Flask
from flask_cors import CORS

from app.application.task_use_cases import TaskUseCases
from app.domain.task_service import TaskService
from app.infrastructure.api.routes import register_routes
from app.infrastructure.persistence.sqlite_task_repository import SqliteTaskRepository


def create_app():
    app = Flask(__name__)
    CORS(app)

    db_path = Path(__file__).resolve().parent.parent / "data" / "tasks.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    repository = SqliteTaskRepository(str(db_path))
    use_cases = TaskUseCases(repository, TaskService())

    app.config["task_use_cases"] = use_cases
    register_routes(app)

    return app
