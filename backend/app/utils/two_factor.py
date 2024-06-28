import pyotp
from flask_jwt_extended import create_access_token
from app.models.user import User

import pyotp

class TwoFactorAuth:
    @staticmethod
    def generate_totp_secret():
        return pyotp.random_base32()

    @staticmethod
    def verify_totp(secret, token):
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    @staticmethod
    def login_with_2fa(username, password, totp_token):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if TwoFactorAuth.verify_totp(user.totp_secret, totp_token):
                access_token = create_access_token(identity=user.id)
                return access_token
        return None