from flask import Blueprint, jsonify
from models.user import Admin

admin_bp = Blueprint('admin', __name__)
admin = Admin("admin_user")

@admin_bp.route('/complaints', methods=['GET'])
def view_complaints():
    # Викликаємо метод перегляду скарг
    admin.view_complaints()
    return jsonify({"status": "Complaints viewed"})

@admin_bp.route('/recommendations', methods=['POST'])
def setup_recommendations():
    # Викликаємо метод налаштування рекомендацій
    admin.setup_recommendations()
    return jsonify({"status": "Recommendations setup complete"})
