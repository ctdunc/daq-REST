curl 127.0.0.1:5000/daqmx/task/newtask -X PUT
curl 127.0.0.1:5000/daqmx/task/newtask/ai_channels/add_ai_voltage_chan -H "Content-Type: application/json"\
    -X PUT -d '{"channels":"Dev1/ai3"}'
curl 127.0.0.1:5000/daqmx/task/newtask/ai_channels -X GET

