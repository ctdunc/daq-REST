from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# start flask app
app = Flask(__name__)

# Blueprint Imports
from auth.auth import auth_bp

# register api blueprints
app.register_blueprint(auth_bp)

# configure json web tokens
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return auth.models.RevokedTokenModel.check_blacklisted(jti)

if __name__ == "__main__":
    Flask.run(app, debug=True)
