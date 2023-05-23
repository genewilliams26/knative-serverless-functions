import os
import sys
import json
import paramiko
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
@app.route('/lparExists', methods=['POST'])

def lparExists():
    json_req = request.get_json(force=True)
    hmc = json_req['hmc']
    lpar = json_req['lpar']
    obj = {}

    command_frame = "lssyscfg -r sys -F name"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=hmc, username=account, password=password, port="22")
        stdin, stdout, stderr = ssh.exec_command(command_frame)
        frames = stdout.read().decode('ascii').split('\n')
        frames = list(filter(None, frames))

        result = "false"
        for frame in frames:
            command_lpar = "lssyscfg -r lpar -F name -m " + frame
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hmc, username=account, password=password, port="22")

            stdin, stdout, stderr = ssh.exec_command(command_lpar)
            lpars = stdout.read().decode('ascii')
            if lpar in lpars:
                result = frame + '.' + lpar
                break
    finally:
        ssh.close()
        del ssh, stdin, stdout, stderr

    return json.dumps(result).strip(' "').rstrip()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
