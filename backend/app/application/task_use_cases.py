from app.domain.task import Task
from app.domain.task_repository import TaskRepositoryPort
from app.domain.task_service import TaskService


class TaskUseCases:
    def __init__(self, repository: TaskRepositoryPort, task_service: TaskService):
        self.repository = repository
        self.task_service = task_service

    def create_task(self, title: str, description: str) -> Task:
        self.task_service.validate_task(title, description)
        task = Task(title=title.strip(), description=(description or "").strip())
        return self.repository.save(task)

    def list_tasks(self) -> list[Task]:
        return self.repository.list_all()

    def toggle_task(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise ValueError("La tarea no existe.")

        task.completed = not task.completed
        return self.repository.update(task)

    def delete_task(self, task_id: int) -> None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise ValueError("La tarea no existe.")

        self.repository.delete(task_id)
