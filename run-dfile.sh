cd ~
# stop container
docker stop $(docker ps -aqf "name=^sensordash$")
#clone from github
git clone git@github.com:SandroNardi/sensordash.git
#move in directory
cd sensordash
#build docker image in the folder
docker build --tag sensordash .
# run docker container passing apikey
docker run --env API_KEY_RO -d -p 5000:5000 sensordash