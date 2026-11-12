import sqlite3
from typing import Optional

from app.domain.task import Task
from app.domain.task_repository import TaskRepositoryPort


class SqliteTaskRepository(TaskRepositoryPort):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize()

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save(self, task: Task) -> Task:
        with self._get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (title, description, completed, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (task.title, task.description, int(task.completed), task.created_at.isoformat()),
            )
            task.id = cursor.lastrowid
            return task

    def list_all(self) -> list[Task]:
        with self._get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM tasks ORDER BY created_at DESC"
            ).fetchall()
            return [self._row_to_task(row) for row in rows]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        with self._get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()

            if row is None:
                return None
            return self._row_to_task(row)

    def update(self, task: Task) -> Task:
        with self._get_connection() as connection:
            connection.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, completed = ?
                WHERE id = ?
                """,
                (task.title, task.description, int(task.completed), task.id),
            )
        return task

    def delete(self, task_id: int) -> None:
        with self._get_connection() as connection:
            connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> Task:
        from datetime import datetime, timezone

        created_at = datetime.fromisoformat(row["created_at"])
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            completed=bool(row["completed"]),
            created_at=created_at,
        )
