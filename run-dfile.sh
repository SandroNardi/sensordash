#build docker image in the folder
docker build --tag sensordash .
# run docker container passing apikey
docker run --env API_KEY_RO -d -p 5000:5000 sensordash