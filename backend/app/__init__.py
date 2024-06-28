from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    limiter.init_app(app)

    from app.routes import auth_bp, bot_bp, rag_bp, admin_bp, chatbot_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(bot_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(chatbot_bp)

    return app