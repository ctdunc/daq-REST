import inspect
from flask import Response
from flask_restful import Resource, reqparse
from niflaskmx import handle_daq_error, check_task_exists, TASKS
from niflaskmx.response import INVALID_TASK_RESPONSE, INVALID_CHANNEL_TYPE_RESPONSE, INVALID_CHANNEL_RESPONSE
import nidaqmx

_supported_chan_types = ["ai_channels", "di_channels"]
# Get module functions to support
_analog_input_funcs = [
    tup[0] for tup in
    inspect.getmembers(
        nidaqmx._task_modules.ai_channel_collection.AIChannelCollection, 
        inspect.isfunction
        )
    if tup[0].startswith('add')
]
_digital_input_funcs = [
    tup[0] for tup in
    inspect.getmembers(
        nidaqmx._task_modules.di_channel_collection.DIChannelCollection,
        inspect.isfunction
        )
    if tup[0].startswith('add')
]

_chan_put_parser = reqparse.RequestParser()
_chan_put_parser.add_argument("channels", help="This field cannot be blank.", required=True)
_chan_put_parser.add_argument("kwargs", help="Any keyword arguments that should be passed to nidaqmx function")

class InputChannelsGetter(Resource):
    def get(self, task_id, channel_type):
        # Gets input channels of task
        global TASKS
        channels = getattr(TASKS[task_id], channel_type).channel_names

        """
        OLD
        nisys = nidaqmx.system.System.local()
        with load_task(nisys, task_id) as task:
            return [(chan.name, chan.description) for chan in getattr(task, channel_type)]
        """
        return channels

class InputChannelsFunction(Resource):
    def put(self, task_id, channel_type, function):
        """
        task_id:        name of nidaqmx.Task object
        channel_type:   type of channel
        function:       which function the channel is supposed to fulfill (e.g. add_ai_voltage_chan).
        """
        global TASKS
        # Post channel(s) to add with kwargs
        if not check_task_exists(task_id):
            return INVALID_TASK_RESPONSE
        if channel_type not in _supported_chan_types:
            return INVALID_CHANNEL_TYPE_RESPONSE
        task = TASKS[task_id]

        data = _chan_put_parser.parse_args()
        channels = data["channels"]
        kwargs = data["kwargs"] if data["kwargs"] is not None else dict()
       
        for channel in channels:
            try:
                added_chan = getattr(getattr(task, channel_type), function)(channels, **kwargs)
                added_chan.description = function
            except nidaqmx.errors.Error as e:
                return handle_daq_error(e)
         
        """
        OLD
        nisys = nidaqmx.system.System.local()
        # Check correct channel type
        if channel_type not in _supported_chan_types:
            return INVALID_CHANNEL_TYPE_RESPONSE
        data = _chan_put_parser.parse_args()
        channels = data["channels"]
        kwargs = data["kwargs"]

        if kwargs == None:
            kwargs = dict()

        with load_task(nisys, task_id) as task:
            added_chan = getattr(getattr(task, channel_type), function)(channels, **kwargs)
            added_chan.description = function

            # TODO: maybe throw a confirmation dialog on stuff like this?
            task.save(overwrite_existing_task=True)
        """
        return 0
