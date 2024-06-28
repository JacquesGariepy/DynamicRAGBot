from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.bot import Bot
from app.services.bot_service import BotService
from app.services.bot_action_service import BotActionService
from app import db, limiter

bp = Blueprint('bot', __name__, url_prefix='/api/bot')
bot_service = BotService()
bot_action_service = BotActionService()

@bp.route('/', methods=['GET'])
@jwt_required()
def get_bots():
    user_id = get_jwt_identity()
    bots = Bot.query.filter_by(owner_id=user_id).all()
    return jsonify([bot.to_dict() for bot in bots]), 200

@bp.route('/', methods=['POST'])
@jwt_required()
@limiter.limit("10 per day")
def create_bot():
    user_id = get_jwt_identity()
    data = request.json
    new_bot = bot_service.create_bot(user_id, data['name'], data.get('config', {}))
    return jsonify(new_bot.to_dict()), 201

@bp.route('/<string:bot_id>', methods=['GET'])
@jwt_required()
def get_bot(bot_id):
    user_id = get_jwt_identity()
    bot = Bot.query.filter_by(id=bot_id, owner_id=user_id).first_or_404()
    return jsonify(bot.to_dict()), 200

@bp.route('/<string:bot_id>/start', methods=['POST'])
@jwt_required()
def start_bot(bot_id):
    user_id = get_jwt_identity()
    bot = Bot.query.filter_by(id=bot_id, owner_id=user_id).first_or_404()
    bot_service.start_bot(bot)
    return jsonify({'message': 'Bot started successfully'}), 200

@bp.route('/<string:bot_id>/stop', methods=['POST'])
@jwt_required()
def stop_bot(bot_id):
    user_id = get_jwt_identity()
    bot = Bot.query.filter_by(id=bot_id, owner_id=user_id).first_or_404()
    bot_service.stop_bot(bot)
    return jsonify({'message': 'Bot stopped successfully'}), 200

@bp.route('/<string:bot_id>', methods=['DELETE'])
@jwt_required()
def delete_bot(bot_id):
    user_id = get_jwt_identity()
    bot = Bot.query.filter_by(id=bot_id, owner_id=user_id).first_or_404()
    db.session.delete(bot)
    db.session.commit()
    return jsonify({'message': 'Bot deleted successfully'}), 200

@bp.route('/<string:bot_id>/action', methods=['POST'])
@jwt_required()
def perform_bot_action(bot_id):
    user_id = get_jwt_identity()
    bot = Bot.query.filter_by(id=bot_id, owner_id=user_id).first_or_404()
    
    data = request.json
    action_type = data.get('action_type')
    params = data.get('params', {})

    try:
        result = bot_action_service.perform_action(bot.id, action_type, params)
        return jsonify({'result': result}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400