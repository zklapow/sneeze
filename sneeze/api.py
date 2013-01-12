import requests
import json

import os

tokenpath = path = os.path.join(os.path.expanduser('~'), '.sneeze_token')


class API(object):
    baseurl = "https://api.github.com"
    def __init__(self, project, user=None, password=None, token=None):
        # Handle different authorization methods
        if token:
            auth = "token %s" % token
            self.session = requests.Session()
            self.session.headers = {'Authorization': auth}
        elif user and password:
            self.session = requests.Session()
            self.session.auth = (user, password)
            self.user = user
            self.password = password
        else:
            with open(tokenpath, 'r') as tokenfile:
                token = tokenfile.read()
                auth = "token %s" % token
                self.session = requests.Session()
                self.session.headers = {'Authorization': auth}

        self.project = project

    def create_issue(self, **kwargs):
        # TODO: is owner the same as user?
        url = "{baseurl}/repos/{repo}/issues".format(baseurl=self.baseurl, repo=self.project)
        data= json.dumps(kwargs)
        print(data)
        return self.session.post(url, data = data)

    def generate_oauth(self):
        """Get a github OAUTH token and write it to a file"""

        url = "{baseurl}/authorizations".format(baseurl=self.baseurl)
        data = {'scopes': ['public_repo'],
                'client_id': '92e0cb1b8a65c1d6e354',
                'client_secret': 'd058a0cda5851dd3c85bc53c1fb026f64cfdd2ea'
               }

        resp = self.session.post(url, data=json.dumps(data))
        resp = resp.json()

        token = resp['token']

        with open(tokenpath, 'w+') as tokenfile:
            tokenfile.write(token)
        return token
