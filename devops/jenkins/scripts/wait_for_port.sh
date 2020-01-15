#!/bin/bash

attempt_counter=0
SERVICE_IP=$1
SERVICE_PORT=$2
SERVICE="http://$SERVICE_IP:$SERVICE_PORT"
max_attempts=$3

until $(curl --output /dev/null --silent --head --fail $SERVICE); do
    if [ ${attempt_counter} -eq ${max_attempts} ];then
      echo "Max attempts reached"
      exit 1
    fi

    printf '.'
    attempt_counter=$(($attempt_counter+1))
    sleep 1
done

echo "Connection $SERVICE to found"
