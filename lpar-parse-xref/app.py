import os
import sys
import json
import requests
import csv
from scp import SCPClient
import paramiko
from flask import Flask, request

accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

def createSSHClient(server, port, user, pw):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, pw)
    return client

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/lparParseXref', methods=['POST'])

def lparParseXref():
    json_req = request.get_json(force=True)
    refenceTablePath = json_req['refenceTablePath']
    frame = json_req['frame']
    toolkit = "<Toolkit-Server>.<domain-name>"

    result = {"output": "error" }

    ssh = createSSHClient(toolkit, 22, account, password)
    scp = SCPClient(ssh.get_transport())

    try:
        scp.get(r'' + refenceTablePath, r'/tmp/reference_table.csv')
    finally:
        scp.close()

    xref_file = csv.reader(open('/tmp/reference_table.csv', 'r'))

    frameinfo = ""
    for row in xref_file:
        if frame == row[1]:
            frameinfo = row

    frames = []
    for i in range(15, 18):
        if frameinfo[i] != "":
            frames.append(frameinfo[i])

    vios = []
    for i in range(19, 26):
        if frameinfo[i] != "":
            vios.append(frameinfo[i])

    allAttributes = {
                "hmc": frameinfo[0],
                "CEC1": frameinfo[2],
                "CEC2": frameinfo[3],
                "CEC3": frameinfo[4],
                "CEC4": frameinfo[5],
                "vios1": frameinfo[6],
                "vios2": frameinfo[7],
                "NIMFrontendIP": frameinfo[8],
                "NIMBackendIP": frameinfo[9],
                "clientNIM": frameinfo[10],
                "clientGateway": frameinfo[11],
                "clientVLAN": frameinfo[12],
                "hmc1": frameinfo[13],
                "hmc2": frameinfo[14],
                "frame1": frameinfo[15],
                "frame2": frameinfo[16],
                "frame3": frameinfo[17],
                "frame4": frameinfo[18],
                "frame1VIO1Name": frameinfo[19],
                "frame1VIO2Name": frameinfo[20],
                "frame2VIO1Name": frameinfo[21],
                "frame2VIO2Name": frameinfo[22],
                "frame3VIO1Name": frameinfo[23],
                "frame3VIO2Name": frameinfo[24],
                "frame4VIO1Name": frameinfo[25],
                "frame4VIO2Name": frameinfo[26],
                "diskType": frameinfo[31],
                "diskSize": frameinfo[32],
                "environment": frameinfo[33]
             }

    res = '{' + str(allAttributes).replace("{","").replace("}","") + ',' + '"frames":' + str(frames) + ',' + '"vios":' + str(vios) + '}'
    res.replace(" ", "")
    return res

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
