import os
import sys
import ssl
import json
import requests
import paramiko
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
@app.route('/decomPuppet', methods=['POST'])

def decomPuppet():
    result = {"output": "error"}
    json_req = request.get_json(force=True)
    node = json_req["fq_pup_client"]
    svr = json_req["fq_pup_server"]

    cmd = "sudo puppetserver ca clean --certname " + node
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=svr, username=account, password=password, port="22")

        stdin, stdout, stderr = client.exec_command( cmd )
        result = stdout.read().decode('ascii').split('\n')
    finally:
        client.close()

    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
