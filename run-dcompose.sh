cd ~/sensordash

docker-compose stop && docker-compose rm -f

cd ~
#clone from github
git clone git@github.com:SandroNardi/sensordash.git
#move in directory
cd ~/sensordash
#docker compose
docker compose up -d