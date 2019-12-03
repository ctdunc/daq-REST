from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
app = Flask(__name__)
api = Api(app)

import auth
from auth.auth import UserLogin, UserPassReset, UserLogout
api.add_resource(UserLogin, "/auth/login")
api.add_resource(UserPassReset, "/auth/reset_password")
api.add_resource(UserLogout, "/auth/logout")
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)


app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return auth.models.RevokedTokenModel.check_blacklisted(jti)

if __name__ == "__main__":
    Flask.run(app, debug=True)
