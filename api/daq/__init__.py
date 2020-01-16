# Declare global task variable to track existing tasks and id's
from flask import Response
TASKS = {}

# DAQmx Error handling 

def handle_daq_error(daqmxerror):
    code = daqmxerror.error_code
    error = daqmxerror.error_type

    text = "Error code: "+str(code)+". NI-DAQmx says:"+str(error)+"."
    return Response(text, status=500)
    

