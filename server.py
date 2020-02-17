from flask import Flask
from flask_restful import Api

# start flask app
app = Flask(__name__)
api = Api(app)

# add daqmx resources
from niflaskmx.task.task import Task, Tasks
from niflaskmx.task.channel import InputChannelsGetter, InputChannelsFunction
# from daq.task.channel import AnalogInputChannel

DAQMX_PFX = "/daqmx"
TASK_PFX = "/task"

api.add_resource(Task, DAQMX_PFX+TASK_PFX+"/<task_id>")
api.add_resource(Tasks, DAQMX_PFX+"/tasks")
api.add_resource(InputChannelsGetter, DAQMX_PFX+TASK_PFX+"/<task_id>/<channel_type>")
api.add_resource(InputChannelsFunction, DAQMX_PFX+TASK_PFX+"/<task_id>/<channel_type>/<function>")
# api.add_resource(AnalogInputChannel, DAQMX_PFX+TASK_PFX+"/<task_id>/ai_channels/<channel_id>")
# configure json web tokens

if __name__ == "__main__":
    Flask.run(app, debug=True)
