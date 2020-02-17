from niflaskmx import handle_daq_error, \
        check_task_exists, \
        get_persisted_task,\
        TASKS
from niflaskmx.response import INVALID_TASK_RESPONSE, \
        INVALID_CHANNEL_TYPE_RESPONSE, \
        INVALID_CHANNEL_RESPONSE
from flask import Response 
from flask_restful import Api, Resource, reqparse
import nidaqmx

#TODO: define success_message (probably in responses).
success_message = 0

task_parser = reqparse.RequestParser()
task_parser.add_argument("function", help="This field cannot be blank.\
        Consult the documentation for a complete list of operations.", required=True)
task_parser.add_argument("kwargs", help="Argument should correspond to operation.")

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
        global TASKS
        # Check existence
        if not check_task_exists(task_id):
            return INVALID_TASK_RESPONSE
        
        # Get task from global list
        task = TASKS[task_id]
        
        # Parse Data from input form
        data = task_parser.parse_args()
        func = data["function"]
        kwargs = data["kwargs"] if data["kwargs"] is not None else dict()
        try:
            val = getattr(task, func)(**kwargs)
            print(val)
        except AttributeError as e:
            print(e)
        return 0

class Tasks(Resource):
    def get(self):
        return list(TASKS.keys())

