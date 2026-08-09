from flask import Blueprint
from src.modules.projects.project_controller import ProjectController

projects_bp = Blueprint('projects', __name__)
controller = ProjectController()

@projects_bp.route('/', methods=['GET'])
def get_projects():
    return controller.get_projects()

@projects_bp.route('/<int:id>', methods=['GET'])
def get_project_by_id(id):
    return controller.get_project_by_id(id)

@projects_bp.route('/', methods=['POST'])
def create_project():
    return controller.create_project()

@projects_bp.route('/<int:id>', methods=['PUT'])
def update_project(id):
    return controller.update_project(id)

@projects_bp.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    return controller.delete_project(id)