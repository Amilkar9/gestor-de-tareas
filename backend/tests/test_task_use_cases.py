import pytest

from app.domain.task import Task
from app.domain.task_service import TaskService
from app.application.task_use_cases import TaskUseCases


class InMemoryTaskRepository:
    def __init__(self):
        self.tasks = []
        self._next_id = 1

    def save(self, task):
        task.id = self._next_id
        self._next_id += 1
        self.tasks.append(task)
        return task

    def list_all(self):
        return list(self.tasks)

    def get_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task):
        for index, current in enumerate(self.tasks):
            if current.id == task.id:
                self.tasks[index] = task
                return task
        raise ValueError("Task not found")

    def delete(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]


@pytest.fixture
def use_cases():
    repository = InMemoryTaskRepository()
    service = TaskService()
    return TaskUseCases(repository, service)


def test_create_task(use_cases):
    task = use_cases.create_task("Estudiar para examen", "Revisar apuntes de arquitectura")

    assert task.id == 1
    assert task.title == "Estudiar para examen"
    assert task.completed is False


def test_toggle_task(use_cases):
    use_cases.create_task("Preparar presentación", "Hacer 3 diapositivas")

    task = use_cases.toggle_task(1)

    assert task.completed is True
    assert use_cases.list_tasks()[0].completed is True


def test_delete_task(use_cases):
    use_cases.create_task("Revisar código", "Refactorizar un método")

    use_cases.delete_task(1)

    assert use_cases.list_tasks() == []
