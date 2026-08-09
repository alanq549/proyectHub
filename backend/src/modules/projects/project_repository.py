# src/modules/projects/project_repository.py
from extensions.db import db
from src.models.project import Project

class ProjectRepository:

    @classmethod
    def get_all(cls, user_id=None, call_id=None, status=None):
        query = Project.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        if call_id:
            query = query.filter_by(call_id=call_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Project.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, project_id):
        return Project.query.get(project_id)

    @classmethod
    def get_by_call_and_user(cls, call_id, user_id):
        return Project.query.filter_by(call_id=call_id, user_id=user_id).first()

    @classmethod
    def get_by_call(cls, call_id):
        return Project.query.filter_by(call_id=call_id).first()

    @classmethod
    def create(cls, project_data):
        project = Project(
            title=project_data.get('title'),
            description=project_data.get('description'),
            status=project_data.get('status', 'draft'),
            user_id=project_data.get('user_id'),
            call_id=project_data.get('call_id')
        )
        db.session.add(project)
        db.session.commit()
        return project

    @classmethod
    def update(cls, project, update_data):
        if 'title' in update_data:
            project.title = update_data['title']
        if 'description' in update_data:
            project.description = update_data['description']
        if 'status' in update_data:
            project.status = update_data['status']
        if 'call_id' in update_data:
            project.call_id = update_data['call_id']
            
        db.session.commit()
        return project

    @classmethod
    def delete(cls, project):
        db.session.delete(project)
        db.session.commit()
        return True