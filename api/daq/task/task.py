from daq import handle_daq_error, \
        check_task_exists, \
        get_persisted_task,\
        TASKS
from daq.response import INVALID_TASK_RESPONSE, \
        INVALID_CHANNEL_TYPE_RESPONSE, \
        INVALID_CHANNEL_RESPONSE
from flask import Response 
from flask_restful import Api, Resource, reqparse
import nidaqmx

#TODO: define success_message (probably in responses).
success_message = 0

task_parser = reqparse.RequestParser()
task_parser.add_argument("operation", help="This field cannot be blank.\
        Consult the documentation for a complete list of operations.", required=True)
task_parser.add_argument("argument", help="Argument should correspond to operation.")

class Task(Resource):
    def get(self,  task_id):
        # TODO: get more info about task, maybe take a form here.
        return(task_id)

    def put(self, task_id):
        # Creates new nidaqmx task.
        global TASKS
        try:
            task = nidaqmx.Task(new_task_name=task_id)
            TASKS[task_id] = task
            return success_message
        except nidaqmx.errors.Error as e:
            return handle_daq_error(e)
         
    def delete(self, task_id):
        # TODO: add option to not delete from persisted task list.
        """
        Closes temporary task, and deletes from NI-MAX configuration
        """
        global TASKS

        # Check if task exists
        if not check_task_exists(task_id):
            return INVALID_TASK_RESPONSE
        # Delete task from NI-MAX.
        try:
            get_persisted_task(task_id).delete()
        except nidaqmx.errors.Error as e:
            return handle_daq_error(e)
        except Exception as e:
            # pass if get_persisted_task returns None, meaning task is not persisted.
            print(e)
            pass

        # Close task in memory
        try:
            TASKS[task_id].close()
            del TASKS[task_id]
        except nidaqmx.errors.Error as e:
            return handle_daq_error(e)
        except Exception as e:
            return e
        return 0
    
    def post(self, task_id): 
        """
        TODO: Other functions besides creation  (! indicates high priority, - indicates low priority, x indicates complete)
            xis_task_done
            !close [USE DELETE METHOD]
            xread
            -register_done_event
            !register_every_n_samples_acquired_into_buffer_event (requires impl of such events)
            -register_every_n_samples_transferred_from_buffer_event
            -register_signal_event
            -save
            !start
            !stop 
            -write
        """

        data = task_parser.parse_args()
        print(data)
        op = data["operation"]
        arg = data["argument"]
        if not arg:
            arg = dict()
        with load_task(task_id) as task:
            if op == "is_task_done":
                try:
                    task.is_task_done()
                except nidaqmx.errors.Error as e:
                    return handle_daq_error(e)
            elif op == "read":
                num_per_c = arg.get("number_of_samples_per_channel", 1)
                timeout = arg.get("timeout", 10.0)
                try:
                    data = task.read(number_of_samples_per_channel=num_per_c, timeout=timeout)
                    return data
                except nidaqmx.errors.Error as e:
                    return handle_daq_error(e)
        return 0

class Tasks(Resource):
    def get(self):
        return list(TASKS.keys())

