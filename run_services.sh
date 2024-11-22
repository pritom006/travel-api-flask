#!/bin/bash

# Set the PYTHONPATH for the project
export PYTHONPATH=$PYTHONPATH:/home/w3e17/travel-api

# Run the destination service
python /home/w3e17/travel-api/destination_service/src/app.py



echo "Starting Destination Service..."
cd destination_service
source venv/bin/activate
python src/app.py &
deactivate
cd ..

echo "Starting User Service..."
cd user_service
source venv/bin/activate
python src/app.py &
deactivate
cd ..

echo "Starting Auth Service..."
cd auth_service
source venv/bin/activate
python src/app.py &
deactivate
cd ..

echo "All services are running!"
