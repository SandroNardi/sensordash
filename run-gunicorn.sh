#move to home
cd ~
# kill running proces
pkill -f "gunicorn"
#remove old directory
rm -rf sensordash
#clone from github
git clone git@github.com:SandroNardi/sensordash.git
#move in directory
cd ~/sensordash
#venv create and activate
python3 -m venv deploy
source deploy/bin/activate
#install pip requirements
pip3 install -r requirements.txt 
#run with gunicorn
gunicorn -b 0.0.0.0:5000 app:app &