from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")



@tasks_bp.post("")
def create_task():
  request_body = request.get_json()

  if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
  title = request_body["title"]
  description = request_body["description"]
  completed_at = request_body.get("completed_at")

  new_task = Task(title=title, description=description, completed_at=completed_at)

  db.session.add(new_task)
  db.session.commit()

  response = {"task": new_task.to_dict()}
  return response, 201


@tasks_bp.get("")
def get_all_tasks():
  query = db.select(Task)
  description_param = request.args.get("description")
  if description_param:
    query = query.where(Task.description.ilike(f"%{description_param}%")).order_by(Task.id)

  title_param = request.args.get("title")
  if title_param:
    query = query.where(Task.title.ilike(f"%{title_param}%")).order_by(Task.id)


  query = query.order_by(Task.id)
  tasks = db.session.scalars(query)

  tasks_response = [task.to_dict() for task in tasks]

  return tasks_response, 200


@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
  task = validate_task(task_id)


  return {"task": task.to_dict()}


@tasks_bp.put("/<task_id>")
def update_task(task_id):
  task = validate_task(task_id)
  request_body = request.get_json()

  task.title = request_body["title"]
  task.description = request_body.get("description")
  task.completed_at = request_body.get("completed_at")

  db.session.commit()
  response = {"task": task.to_dict()}
  return response, 200


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
  task = validate_task(task_id)

  db.session.delete(task)
  db.session.commit()
  response = {
    "details": f'Task {task_id} "{task.title}" successfully deleted'
    }
  return response, 200

def validate_task(task_id):
  try:
      task_id = int(task_id)
  except ValueError:
        response = {"details": f"Task {task_id} invalid"}
        abort(make_response(response, 404))

  task = Task.query.get(task_id)

  if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))

  return task