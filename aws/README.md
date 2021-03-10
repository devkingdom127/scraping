#Steps to run
python3 -m venv env
source env/bin/activate
#If you do not have flask installed
python -m pip install Flask==1.1.1

#Steps to run
python app.py


To Do
<ul>
<li>Make a search file which will call post on /search with term or category, affiliates coming in as well</li>
<li>Append affiliates based on which search pass it into the function.. Create utils for this based on which one</li>
<li>Call each search based on a list</li>
<li>Join items together if name matches</li>
<li>Respond with list</li>
</ul>



python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
python3 pip install -r requirements.txt

run with
./script.sh


#run on server
nohup gunicorn -w 4 app:app --bind 0.0.0.0 > log.txt 2>&1 &

#see running
jobs -l