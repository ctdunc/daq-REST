from flask_restful import Resource, reqparse

exchange_parser = reqparse.RequestParser()
implements_parser = reqparse.RequestParser()

# TODO: run_parser.add_argument(<metadata filters>)
class Runs(Resource):
    def get(self):
        # TODO: perform DB search, potentially with 
        # args = run_parser.parse_args()

        return 0

class Run(Resource):
    def get(self, run):
        # TODO: perform DB search, potentially with 
        # args = run_parser.parse_args()

        return 0

class RunExchange(Resource):
    def get(self):
        # TODO

        return 0

class RunImplements(Resource):
    def get(self):
        # TODO:

        return 0

    def put(self):
        # TODO: run analysis code at this endpoint

        return 0

