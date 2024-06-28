from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.chatbot_service import ChatbotService
from app import limiter

bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')
chatbot_service = ChatbotService()

@bp.route('/message', methods=['POST'])
@jwt_required()
@limiter.limit("100 per day")
def process_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    message = data.get('message')
    language = data.get('language', 'en')

    if not message:
        return jsonify({"error": "No message provided"}), 400

    response = chatbot_service.process_message(user_id, message, language)
    return jsonify({"response": response})