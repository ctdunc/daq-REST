# Create sample task
curl 127.0.0.1:5000/daqmx/task/newtask -X put
curl 127.0.0.1:5000/daqmx/task/newtask -H "Content-Type: application/json" \
    -X post -d '{"operation":"read"}'

