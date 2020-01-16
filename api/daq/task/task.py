from flask import Response 
from flask_restful import Api, Resource, reqparse
from daq import TASKS, handle_daq_error
import nidaqmx

def _task_exists(task_id):
    if task_id in TASKS:
        return True
    else:
        return False

class Task(Resource):
    def get(self,  task_id):
        return(task_id)

    def put(self, task_id):
        # Creates new nidaqmx task.
        try:
            task = nidaqmx.Task(new_task_id=task_id)
            TASKS[task_id] = task
            return 0
        except nidaqmx.error.Error as error:
            return handle_daq_error(e)

    def delete(self, task_id):
        try:
            with TASKS[task_id] as task:
                task.close()
            del TASKS[task_id]
            return 0
        except nidaqmx.error.Error as e:
            return handle_daq_error(e)
    
    def post(self, task_id): """
        TODO: Other functions besides creation 
            -is_task_done
            -close
            -read
            -register_done_event
            -register_every_n_samples_acquired_into_buffer_event
            -register_every_n_samples_transferred_from_buffer_event
            -register_signal_event
            -save
            -start
            -stop
            -write
        """
        # Check
        return 0

class Tasks(Resource):
    def get(self):
        return TASKS.keys()

