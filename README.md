# Cirun-task-server
Server for Cirun task made in Flask, the github api has been used to authenticate a user
and fetch the repos by passing on the username

###  `python app.py`
starts the flask server at the mentioned port (i.e. 4000) 

*All the apis require secret key and credentials, To set up a secret, go to your Repository Settings page, then select Secrets. Your secret's name will be used in your workflow to reference the data, and you can place the secret itself in the value. To use that secret, you can reference it using the secrets context within your workflow

*Make sure to use the call back url to handle the authentication as its a mandatory part of the process

*CORS and set_credentials have been allowed to mantain smooth communication between client and backend as the client is hostend on another server



