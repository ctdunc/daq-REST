from flask_restful import Resource, reqparse

class AnalogInputChannels(Resource):
    def get(self, task_id, channel_id):
        print(task_id, channel_id)
        return 0
