import os
import sys
import json
import requests
from flask import Flask, request

accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/decomJirafacts', methods=['POST'])

def decomJirafacts():
    json_req = request.get_json(force=True)
    fq_hostname = json_req['fq_hostname']
    base_url = "https://puppetfiles.apps." + cluster + ".<domain-name>/puppetfiles/v1/delete"
    with session.delete(base_url, data='') as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
            print('   ' + data)
    result = '{"response":"' + str(data) + '"}'
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
