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
@app.route('/checkMemAvailability', methods=['POST'])

def checkMemAvailability():
    result = {"output": "error"}
    json_req = request.get_json(force=True)
    frame = json_req['frame']
    hmc = json_req['hmc']
    req_mem = json_req['memory']

    memcommand = " lshwres -r mem -m " + frame + " --level sys -F curr_avail_sys_mem"
    memout = ""
    try:
        client3 = paramiko.SSHClient()
        client3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client3.connect(hostname=hmc, username=account, password=password, port="22")

        stdin3, stdout3, stderr3 = client3.exec_command(memcommand)
        memout = stdout3.read().decode('ascii')

    finally:
        client3.close()

    remaining_mem = int(memout.strip('\n'))

    if req_mem == "":
        req_mem = 0

    if int(req_mem) <= remaining_mem:
        available_mem = "true"
    else:
        available_mem = "false"

    result = '{ "memoryAvailable": ' + available_mem + ' }'
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
