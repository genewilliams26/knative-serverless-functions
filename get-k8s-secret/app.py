import os
import sys
import json
import requests
from flask import Flask, request

passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
sshpassword = passwordsecret.readline().strip()
passwordsecret = open("/var/secret/vmwarepassword/vmwarepassword", "r")
vmwarepassword = passwordsecret.readline().strip()

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/getK8sSecret', methods=['POST'])

def getK8sSecret():
    json_req = request.get_json(force=True)
    account = json_req['account']

    if account == '<User>':
        result = '{"answer":"' + sshpassword + '"}'
    elif account == 'scorchprod':
        result = '{"answer":"' + vmwarepassword + '"}'
    else:
        result = '{"answer":"input not supported"}'
       
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
