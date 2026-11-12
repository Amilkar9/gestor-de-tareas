from flask import Blueprint, current_app, jsonify, request

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")


def _serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
    }


@api_bp.get("/tasks")
def list_tasks():
    use_cases = current_app.config["task_use_cases"]
    tasks = use_cases.list_tasks()
    return jsonify([_serialize_task(task) for task in tasks])


@api_bp.post("/tasks")
def create_task():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title", "")
    description = payload.get("description", "")

    use_cases = current_app.config["task_use_cases"]

    try:
        task = use_cases.create_task(title, description)
        return jsonify(_serialize_task(task)), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api_bp.patch("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    use_cases = current_app.config["task_use_cases"]

    try:
        task = use_cases.toggle_task(task_id)
        return jsonify(_serialize_task(task))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


@api_bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    use_cases = current_app.config["task_use_cases"]

    try:
        use_cases.delete_task(task_id)
        return jsonify({"message": "Tarea eliminada correctamente."})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


def register_routes(app):
    app.register_blueprint(api_bp)
