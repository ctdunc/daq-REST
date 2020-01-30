# Declare global task variable to track existing tasks and id's
from flask import Response
import nidaqmx
TASKS = {}
_nisys = nidaqmx.system.System.local()

def handle_daq_error(daqmxerror):
    code = daqmxerror.error_code
    error = daqmxerror.error_type

    text = "Error code: "+str(code)+". "+str(error)+"."
    return Response(text, status=500)

def load_task(nisys, task_id):
    index = _nisys.tasks.task_names.index(task_id)
    try:
        task = nisys.tasks[index].load()
        return task
    except nidaqmx.errors.DaqError as e:
        raise e

def get_persisted_task(task_id):
    try:
        index = _nisys.tasks.task_names.index(task_id)
        return _nisys.tasks[index]
    except Exception:
        return None

def check_task_exists(task_id):
    if task_id in TASKS:
        return True
    else:
        return False


# Load tasks from MAX on server start.
def _init_load_tasks():
    global TASKS
    task_names = _nisys.tasks.task_names
    for i in range(len(task_names)):
        name, task = task_names[i], _nisys.tasks[i]
        TASKS[name] = task.load()

_init_load_tasks()
