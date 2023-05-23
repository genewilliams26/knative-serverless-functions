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
@app.route('/getFrameType', methods=['POST'])

def getFrameType():
    result = {"output": "error"}
    json_req = request.get_json(force=True)
    hmc = json_req["hmc"]
    frame = json_req["frame"]

    gettype = "lssyscfg -r sys -m " + frame + " -F type_model"
    typeout = ""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hmc, username=account, password=password, port="22")

        stdin, stdout, stderr = client.exec_command(gettype)
        typeout = stdout.read().decode('ascii').split('\n')

    finally:
        client.close()

    getIOtype = "lssyscfg -r sys -m " + frame + " -F virtual_io_server_capable"
    typeIOout = ""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hmc, username=account, password=password, port="22")

        stdin, stdout, stderr = client.exec_command(getIOtype)
        typeIOout = stdout.read().decode('ascii').split('\n')

    finally:
        client.close()

    frametype = typeout[0]
    ioType = typeIOout[0]
    result = { "frameType": frametype, "IOType": ioType }
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
