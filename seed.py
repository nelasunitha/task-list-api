from app import create_app, db
from app.models.task import Task
from datetime import datetime


my_app = create_app()
with my_app.app_context():
   db.session.add_all([
    Task(title="Go on my daily walk 🏞", description="Notice something new every day", completed_at=None),
    Task(title="Team Meeting", description="Attend the weekly team sync-up meeting", completed_at=datetime(2024, 10, 2, 9, 0)),
    Task(title="Code Review", description="Review code for recent pull requests", completed_at=datetime(2024, 10, 3, 11, 15)),
    Task(title="Client Call", description="Discuss requirements with the client", completed_at=datetime(2024, 10, 4, 15, 0)),
    Task(title="Update Documentation", description="Add details to the API documentation", completed_at=datetime(2024, 10, 5, 10, 30)),
    Task(title="Research on Tech Trends", description="Research new technology trends for the next project", completed_at=datetime(2024, 10, 6, 13, 0)),
    Task(title="Design New Feature", description="Design wireframes for new app feature", completed_at=datetime(2024, 10, 7, 16, 45)),
    Task(title="Team Outing", description="Organize a fun team-building outing", completed_at=datetime(2024, 10, 8, 18, 0)),
    Task(title="Debugging Issue #123", description="Fix the bug reported in issue #123", completed_at=datetime(2024, 10, 9, 12, 0)),
    Task(title="Final Presentation", description="Prepare the slides for the final presentation", completed_at=datetime(2024, 10, 10, 9, 0))
])
   db.session.commit()
