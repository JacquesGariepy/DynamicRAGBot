from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db, limiter
from app.utils.two_factor import TwoFactorAuth

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        if user.totp_secret:
            if 'totp_token' not in data:
                return jsonify({"msg": "TOTP token required"}), 400
            if not TwoFactorAuth.verify_totp(user.totp_secret, data['totp_token']):
                return jsonify({"msg": "Invalid TOTP token"}), 401
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@bp.route('/register', methods=['POST'])
@limiter.limit("3 per hour")
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@bp.route('/enable_2fa', methods=['POST'])
@jwt_required()
def enable_2fa():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    secret = TwoFactorAuth.generate_totp_secret()
    user.totp_secret = secret
    db.session.commit()
    return jsonify({"secret": secret}), 200