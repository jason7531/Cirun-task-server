from flask import Flask, json, jsonify, redirect, \
    render_template, url_for
from flask import session as login_session
from flask.helpers import make_response
from flask import request
from flask_cors import CORS, cross_origin

import requests
import random
import string
# stored in credentials.py
from credentials import client_id, client_secret

app = Flask(__name__)
# To enable CORS with the credentials
CORS(app, supports_credentials=True)
app.secret_key = 'super secret key'

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
request_url = 'https://api.github.com'

# initiates the authorization process and redirects to the github login page


@app.route('/handleLogin', methods=["GET"])
def handleLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    if login_session['state'] == state:

        fetch_url = authorization_base_url + \
            '?client_id=' + client_id + \
            '&state=' + login_session['state'] + \
            '&scope=user%20repo%20public_repo' + \
            '&allow_signup=true'
        return redirect(fetch_url)
    else:
        return jsonify(invalid_state_token="invalid_state_token")

# authenticates the user based on the credentials entered


@app.route('/callback', methods=['GET', 'POST'])
def handle_callback():

    if request.args.get('state') != login_session['state']:

        response = make_response(json.dumps('Invalid state parameter!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if 'code' in request.args:

        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': request.args['code']
        }
        headers = {'Accept': 'application/json'}
        req = requests.post(token_url, params=payload, headers=headers)
        resp = req.json()

        if 'access_token' in resp:
            login_session['access_token'] = resp['access_token']

            return redirect('http://localhost:3000/repos')
        else:
            return jsonify(error="Error retrieving access_token"), 404
    else:
        return jsonify(error="404_no_code"), 404

# returns user info such as github username which can be used to further fetch repos


@app.route('/index', methods=["GET"])
def index():

    if 'access_token' not in login_session:
        return 'Never trust strangers', 404

    access_token_url = 'https://api.github.com/user'
    r = requests.get(access_token_url, headers={
                     'Authorization': 'token '+login_session['access_token']})
    try:
        resp = r.json()
        gh_profile = resp['html_url']
        username = resp['login']
        avatar_url = resp['avatar_url']
        bio = resp['bio']
        name = resp['name']

        return jsonify(
            gh_profile=gh_profile,
            gh_username=username,
            avatar_url=avatar_url,
            gh_bio=bio,
            name=name
        )

    except AttributeError:
        app.logger.debug('error getting username from github, whoops')
        return "I don't know who you are; I should, but regretfully I don't", 500

# returns repos of the user


@app.route('/user/<string:username>')
def getRepos(username):
    if not 'access_token' in login_session:
        invalid_access_token = "Access token has expired or not in session"
        app.logger.error(invalid_access_token)
        return jsonify(invalid_access_token=invalid_access_token)
    if not username:
        return jsonify(username_not_give="Github username needed to fetch \
                                         repos")
    url = request_url + \
        '/users/{username}/repos?per_page=500'.format(username=username)
    headers = {'Accept': 'application/json'}
    try:
        req = requests.get(url, headers=headers, timeout=4)
    except (requests.exceptions.Timeout) as e:
        return jsonify("connection timed out")

    if req.status_code == 200:
        resp = req.json()
        try:
            app.logger.debug("Try to get repository names from response")
            repo_info = []
            for each_repo in resp:
                repo_dict = {}
                repo_dict['repo_name'] = each_repo['full_name']
                repo_dict['repo_link'] = each_repo['html_url']
                repo_dict['description'] = each_repo['description']
                repo_dict['owner_fullname'] = each_repo['owner']['login']
                repo_dict['html_url'] = each_repo['html_url']
                repo_info.append(repo_dict)
            app.logger.debug(
                "Successfully fetched repository info from response")
            return jsonify(
                repo_count=len(repo_info),
                repo_info=repo_info
            ), 200
        except (TypeError, AttributeError, KeyError) as e:
            app.logger.error(e)
            return jsonify(no_user_found="no user found"), 404
    else:
        res = req.json()['message']
        return jsonify(error=res)


if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0',)
