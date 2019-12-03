from flask_restful import Resource, reqparse

# TODO: Aaron,  you're gonna want to edit this file and add your own resources.
class Devices(Resource):
    def get(self):
        # TODO: Return List of Devices
        return 0

class Device(Resource):
    def get(self):
        # TODO: returns json-fmt device state
        
        return 0
    def put(self):
        # TODO attempt to start task with appropriate arguments. Return error if busy.
        # TODO: dry-run flag.
        return 0

