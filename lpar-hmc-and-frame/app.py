import os
import sys
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
@app.route('/getLparFrameAndHmc', methods=['POST'])

def getLparFrameAndHmc():
    result = {"output": "error"}
    json_req = request.get_json(force=True)
    lpar = json_req["lpar"]

    command = "lsrsrc IBM.MCP"
    output = ""

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=lpar, username=account, password=password, port="22")

        stdin, stdout, stderr = client.exec_command("lsrsrc IBM.MCP")
        output = stdout.read().decode('ascii')

    finally:
        client.close()

    hmcinfo = output[output.find('resource 1')+len('resource 1'):output.find('NodeNameList')].split('\n')
    hmc2info = output[output.find('resource 2')+len('resource 2'):-1].split('\n')

    hmc = ""
    hmcip = ""
    hmc2 = ""
    hmc2ip = ""

    for x in range(0, len(hmcinfo)):
        if hmcinfo[x].find('KeyToken') != -1:
            hmc = hmcinfo[x].split('=')[1].strip('"').lstrip('"').strip()
            hmc = hmc[1:]
        if hmcinfo[x].find('HMCIPAddr') != -1:
            hmcip = hmcinfo[x].split('=')[1].strip('\"').lstrip('\"').strip()
            hmcip = hmcip[1:]

    for x in range(0, len(hmc2info)):
        if hmc2info[x].find('KeyToken') != -1:
            hmc2 = hmc2info[x].split('=')[1].strip('"').lstrip('"').strip()
            hmc2 = hmc2[1:]
        if hmc2info[x].find('HMCIPAddr') != -1:
            hmc2ip = hmc2info[x].split('=')[1].strip('\"').lstrip('\"').strip()
            hmc2ip = hmc2ip[1:]
    f = open(os.devnull, "w")
    sys.stderr = f
    if hmc[-1] != '1':
        hmc,hmcip,hmc2,hmc2ip = hmc2,hmc2ip,hmc,hmcip

    command = "uname -u"
    output = ""

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=lpar, username=account, password=password, port="22")

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('ascii')

    finally:
        client.close()

    result = '{"hmc": ' + hmc + ', "hmcip": ' + hmcip + ', "hmc2": ' + hmc2 + ', "hmc2ip": ' + hmc2ip + ', "frame_serial": ' + output.strip() + '}'
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
