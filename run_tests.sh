#!/bin/bash

IMAGE_NAME="psor-test-env"
CONTAINER_NAME="psor-test-container"
IP_TO_BLOCK="192.168.1.100"

echo "--- Building Docker test image: $IMAGE_NAME ---"
docker build -t $IMAGE_NAME .

echo "--- Running test container: $CONTAINER_NAME ---"
docker run -d --privileged --name $CONTAINER_NAME $IMAGE_NAME tail -f /dev/null

echo "--- Waiting for container to start up... ---"
sleep 5

echo "--- Enabling firewall inside the container ---"
docker exec $CONTAINER_NAME ufw enable

echo "--- Executing the remediation engine inside the container ---"
docker exec $CONTAINER_NAME python3 engine.py

echo "--- Verifying the firewall rule was added ---"
if docker exec $CONTAINER_NAME ufw status | grep -q "$IP_TO_BLOCK"; then
  echo "SUCCESS: Firewall rule for $IP_TO_BLOCK found."
else
  echo "FAILURE: Firewall rule for $IP_TO_BLOCK was NOT found."
fi

echo "--- Cleaning up test container ---"
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

echo "--- Test complete ---"
