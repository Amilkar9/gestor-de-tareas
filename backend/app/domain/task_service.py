class TaskService:
    def validate_task(self, title: str, description: str) -> None:
        cleaned_title = (title or "").strip()
        if not cleaned_title:
            raise ValueError("El título es obligatorio.")

        if len(cleaned_title) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres.")

        if description is None:
            raise ValueError("La descripción no puede ser nula.")
