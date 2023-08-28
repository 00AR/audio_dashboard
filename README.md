# audio_dashboard

## Steps to setup project

Clone the Repository:

``` git clone https://github.com/00AR/audio_dashboard.git ```

To install the dependencies, open audio_dashboard directory in the terminal and run the command:

``` python -m pip install requirements.txt ```

Database environment variables
```
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT
```

## Working
The app is made of two models: Audio and User. The User model stores user data and is used for authenitcation. The Audio model is used to store the meta data of the uploaded audio files. The user can login in using his user name. The app has two pages: login and dashboard. In the login page user can enter his username and submits, the application checks whether a user with the input username exists in the database if it exists, the user id is stored in the session if the user does not exists a user a created with the input username and the new user is stored in the session. This is dummy login feature and is not intended to be used in actual production environment. Authenticated user can access the dashboard page, which has a table of the file uploaded by the user, and a file input form where user can upload new audio files. 
The uploaded files are checked whether they are audio files (mp3 and not html or other files), and their duration is checked whether it is less than 10 minutes. I have used mutagen library to extract the meta data of the audio file, and store the meta data in the database. The play audio functionality is added by simply returning the audio file and the browser do the task of playing. 