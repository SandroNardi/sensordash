# Sensordash
Provide a minimal flask web page with humidity info about meraki sensors

## Get from GH
```bash
#clone from github
git clone git@github.com:SandroNardi/sensordash.git
cd sensordash
```
## Deploy with Gunicorn
run **bash run-gunicorn.sh**

requre pyton > 3.9
```bash
#move to home
cd ~
# kill running proces
pkill -f "gunicorn"
#remove old directory
rm -rf sensordash
#clone from github
git clone git@github.com:SandroNardi/sensordash.git
#move in directory
cd sensordash
#venv create and activate
python3 -m venv deploy
source deploy/bin/activate
#install pip requirements
pip3 install -r requirements.txt 
#run with gunicorn
gunicorn -b 0.0.0.0:5000 app:app &
```
## Deploy with Docker file
run **bash run-dfile.sh**
```bash
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
```
## Deploy with Docker Compose

```bash
cd ~/sensordash

docker-compose stop && docker-compose rm -f

cd ~
#clone from github
git clone git@github.com:SandroNardi/sensordash.git
#move in directory
cd ~/sensordash
#docker compose
docker compose up -d
```
