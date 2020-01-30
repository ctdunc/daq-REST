from flask import Response

INVALID_TASK_RESPONSE = Response("The specified task is not valid.", status=500)

INVALID_CHANNEL_RESPONSE = Response("The specified channel is not valid", status=500)
INVALID_CHANNEL_TYPE_RESPONSE = Response("The specified channel type is not valid", status=500)
