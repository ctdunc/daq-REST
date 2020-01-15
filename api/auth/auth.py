from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_raw_jwt
from auth.models import UserModel, RevokedTokenModel

# Create argument parser for authentication endpoint
auth_parser = reqparse.RequestParser()
auth_parser.add_argument("username", help = "This field cannot be blank", required = True)
auth_parser.add_argument("password", help = "This field cannot be blank", required = True)
auth_parser.add_argument("newPassword")

# Create authentication blueprint and api
auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)

def generate_token(username, message=''):
    access_token = create_access_token(identity = username)
    refresh_token = create_refresh_token(identity = username)

    return {"message": "Logged in as {}. ".format(username)+message,\
            "access_token": access_token,\
            "refresh_token": refresh_token}
            

class UserLogin(Resource):
    def post(self):
        data = auth_parser.parse_args()
        current_user = UserModel.find_by_username(data['username']) 

        if not current_user:
            return {'message': 'User {} doesn\'t exist!'.format(data['username'])}
        print(current_user['Hashed'])
        if current_user['Hashed']:
            if UserModel.verify_hash(data['password'], current_user['Password']):

                return generate_token(data['username'])
                # create token
            else:
                # return invalid credentials
                print("hash")
                return 0
        else:
            if  data['password'] == current_user['Password']:
                return generate_token(data['username'], message="Your password is not secure! Please reset it ASAP.")
            else:
                # return invalid credentials
                print("nohash")
                return 0


class UserPassReset(Resource):
    @jwt_required
    def post(self):
        data = auth_parser.parse_args()
        newpass = UserModel.generate_hash(data['newPassword'])
        UserModel.reset_password(data['username'], newpass)

class UserLogout(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti'] 
        RevokedTokenModel.add(jti)

auth_api.add_resource(UserLogin, "/login")
auth_api.add_resource(UserPassReset, "/reset_password")
auth_api.add_resource(UserLogout, "/logout")
