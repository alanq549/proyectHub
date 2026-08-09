# src/modules/history/routes.py
from flask import Blueprint
from src.modules.history.history_controller import HistoryController

history_bp = Blueprint('history', __name__)
controller = HistoryController()

@history_bp.route('/', methods=['GET'])
def get_history():
    return controller.get_history()