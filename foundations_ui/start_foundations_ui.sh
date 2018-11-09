#!/bin/bash


function trap_ctrlc ()
{

    kill $API_PID
    echo 'Closing API server'

    exit 2
}

# initialise trap to call trap_ctrlc function when signal 2 (SIGINT) or 15 (SIGTERM) is received
trap "trap_ctrlc" 2 15 

npm install 

python run_api_server.py &
API_PID=$!
echo 'api server started'

yarn start