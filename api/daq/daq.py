from flask import Blueprint
from flask_restful import Api, Resource, reqparse

daq_bp = Blueprint('daqmx', __name__)
daq_api = Api(daq_bp)



class Device(Resource):


    def get(self):
        return 0
