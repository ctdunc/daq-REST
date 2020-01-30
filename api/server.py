from flask import Flask
from flask_restful import Api

# from flask_jwt_extended import JWTManager

# start flask app
app = Flask(__name__)
api = Api(app)

"""
# add authentication resources
from auth.auth import UserLogin, UserPassReset, UserLogout
AUTH_PFX = "/auth"
api.add_resource(UserLogin, AUTH_PFX+"/login")
api.add_resource(UserPassReset, AUTH_PFX+"/reset_password")
api.add_resource(UserLogout, AUTH_PFX+"/logout")
"""
# add daqmx resources
from daq.task.task import Task, Tasks
from daq.task.channel import InputChannelsGetter, InputChannelsFunction
# from daq.task.channel import AnalogInputChannel

DAQMX_PFX = "/daqmx"
TASK_PFX = "/task"

api.add_resource(Task, DAQMX_PFX+TASK_PFX+"/<task_id>")
api.add_resource(Tasks, DAQMX_PFX+"/tasks")
api.add_resource(InputChannelsGetter, DAQMX_PFX+TASK_PFX+"/<task_id>/<channel_type>")
api.add_resource(InputChannelsFunction, DAQMX_PFX+TASK_PFX+"/<task_id>/<channel_type>/<function>")
# api.add_resource(AnalogInputChannel, DAQMX_PFX+TASK_PFX+"/<task_id>/ai_channels/<channel_id>")
# configure json web tokens
"""
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return auth.models.RevokedTokenModel.check_blacklisted(jti)
"""
if __name__ == "__main__":
    Flask.run(app, debug=True)
