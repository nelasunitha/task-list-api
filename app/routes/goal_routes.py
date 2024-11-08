from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from ..db import db
from datetime import datetime

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")



@goals_bp.post("")
def create_goal():
  request_body = request.get_json()

  try:
     new_goal = Goal.from_dict(request_body)

  except KeyError:
     response = {"details": "Invalid data"}
     abort(make_response(response, 400))

  db.session.add(new_goal)
  db.session.commit()

  response = {"goal": new_goal.to_dict()}
  return response, 201


@goals_bp.get("")
def get_all_goals():
  query = db.select(Goal)

  title_param = request.args.get("title")
  sort = request.args.get("sort", "asc")  # Default to ascending order

  query = db.select(Goal)

  if title_param:
      query = query.where(Goal.title.ilike(f"%{title_param}%"))

  if sort == "desc":
      query = query.order_by(Goal.title.asc())

  goals = db.session.scalars(query)
  goals_response = [goal.to_dict() for goal in goals]

  return goals_response, 200


@goals_bp.get("/<goal_id>")
def get_single_goal(goal_id):
  goal = validate_goal(goal_id)


  return {"goal": goal.to_dict()}


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
  goal = validate_goal(goal_id)
  request_body = request.get_json()

  goal.title = request_body["title"]


  db.session.commit()
  response = {"goal": goal.to_dict()}
  return response, 200

@goals_bp.patch("/<goal_id>/mark_complete")
def mark_goal_complete(goal_id):
    goal = validate_goal(goal_id)
    goal.completed_at = datetime.now()
    db.session.commit()

    return {"goal": goal.to_dict()}, 200

@goals_bp.patch("/<goal_id>/mark_incomplete")
def mark_goal_incomplete(goal_id):
    goal = validate_goal(goal_id)
    goal.completed_at = None

    db.session.commit()

    return {"goal": goal.to_dict()}, 200


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
  goal = validate_goal(goal_id)

  db.session.delete(goal)
  db.session.commit()
  response = {
    "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }
  return response, 200

def validate_goal(goal_id):
  try:
      goal_id = int(goal_id)
  except ValueError:
        response = {"details": f"Goal {goal_id} invalid"}
        abort(make_response(response, 404))

  goal = db.session.get(Goal,goal_id)

  if not goal:
        response = {"message": f"goal {goal_id} not found"}
        abort(make_response(response, 404))

  return goal
