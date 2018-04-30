# Student Project Platform
This is the final year project for Ming Liang Siew for MEng Computer Science (International Programme). This project allow Academic Staffs/External Clients to post project and allow Students to show interest in project

## Requirements
Python3.5
Virtualenv (Recommended)
MySQL (Recommended) 
## Gmail Credential

Replace content of client_secret.json with that of json file obtained from Gmail API. Then , type in
```
python quickstart.py
```
Read here for more information,
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets

## Enter Environment Variable
Enter the variables in .env


Go to https://www.uclapi.com/ and request these two variables
UCLAPI_CLIENT_ID and  UCLAPI_CLIENT_SECRET

For Amazon S3 services,  request for these three variables
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME

For production mode, get these MySQL variable

SQL_NAME - Name of MySQL account
SQL_USER -  User of MySQL
SQL_PASSWORD - Password of MySQL user
SQL_HOST - Name of MySQL host


## Install System
```
pip install -r requirements.txt 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createcachetable
```



## Create SuperUser for Adminstrator
```
python manage.py createsuperuser
```
Then, go to /admin and enter the credential to login as admin


## Running as development
```
python3 manage.py collectstatic
python3 manage.py runserver
```


## Working Product
https://djmatch.herokuapp.com

## Testing
There are three possible Web browsers to test on. Chrome, Mozilla and PhantomJS. But you need to install the driver for each broswer.

First, change the DRIVER variable in .env file. CHROME for Chrome browser, MOZILLA for Mozilla browser and finally PHANTOMJS for PhantomJs browser
```
python3 manage.py test
```