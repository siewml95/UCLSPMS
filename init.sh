sudo pip3 install -r requirements.txt 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata project/fixtures/init.json
python3 manage.py runserver