# Cirun-task-server
Server for Cirun task made in Flask, the github api has been used to authenticate a user
and fetch the repos by passing on the username

###  Getting Started
1. Clone this repo: `git clone https://github.com/jason7531/Cirun-task-server.git`
2. Change the repo directory: `cd Cirun-task-server`
3. Setting up virtualenv: `virtualenv ENV && source ENV/bin/activate`
4. Install dependencies with pip: `pip install -r requirements.txt`
5. Add following things to your `.env`:
 * Set `CLIENT_ID` and `CLIENT_SECRET` to the values obtained from github
6. Run the app: `python app.py` 
7. Acess the server on: `http://localhost:4000/handleLogin` 

### API Doc
URL                                  | Method | Body                  | Description
-------------------------------------|--------|-----------------------|---------------------------------------
http://localhost:4000/handleLogin    | GET    | N/A                   | Redirects to the login page of github
http://localhost:4000/callback       | POST   | payload automatically passed after putting in credentials   | Handles the authentication 
http://localhost:4000/index          | GET    | N/A                   | Returns the user info
http://localhost:4000/user/`username`| GET    | N/A                   | Returns an array of repos

### `http://localhost:4000/index` Response Sample : 

![index reponse](/images/image1.jpeg?raw=true "JSON Response to /index")

### `http://localhost:4000/user/<username>` Response Sample :
![user reponse](/images/image2.jpeg?raw=true "JSON Response to /user/username")



