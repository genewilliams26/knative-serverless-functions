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
@app.route('/getNimImages', methods=['POST'])

def getNimImages():
    result = {"output": "error"}
    json_req = request.get_json(force=True)
    nim = json_req["NIMhostname"]
    osVer = json_req["OS"]

    version = osVer.split()[1].replace('.', "") + "00"
    #if "7.1" in osVer:
    #    version = "7100"
    #elif "6.1" in osVer:
    #    version = "6100"

    getMksysb = "sudo lsnim -t mksysb"
    getSpot = "sudo lsnim -t spot"
    getBosinst = "sudo lsnim -t bosinst_data | grep Gold | awk '{print $1}'"

    mksysb = ""
    spot = ""
    sysbout = ""
    spotout = ""
    bosinstOut = ""
    bosinst = ""

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=nim, username=account, password=password, port="22")

        stdin, stdout, stderr = client.exec_command(getMksysb)
        sysbout = stdout.read().decode('ascii').split('\n')
        stdin, stdout, stderr = client.exec_command(getSpot)
        spotout = stdout.read().decode('ascii').split('\n')
        stdin, stdout, stderr = client.exec_command(getBosinst)
        bosinst = stdout.read().decode('ascii').split('\n')

    finally:
        client.close()

    for line in sysbout:
        if "Gold" in line and version in line:
            mksysb = line.split()[0]

    for lines in spotout:
        if "Gold" in lines and version in lines:
            spot = lines.split()[0]

    result = { "mksysb": mksysb, "spot": spot, "bosinst": bosinst[0] }
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
