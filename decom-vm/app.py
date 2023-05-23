import os
import sys
import json
import requests
from flask import Flask, request

accountsecret = open("/var/secret/vmwareaccount/vmwareaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/vmwarepassword/vmwarepassword", "r")
password = passwordsecret.readline().strip()
clusterenvsecret = open("/var/secret/clusterenv/clusterenv", "r")
clusterenv = clusterenvsecret.readline().strip()

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/decomJirafacts', methods=['POST'])

def decomJirafacts():
    json_req = request.get_json(force=True)
    server_name = json_req['server_name']
    # vsvr_host = json_req['vsvr_host']

    cmd = "ansible-playbook -i /home/<User>/.g/decom/decom-vm-inv.yml -e \"server_name=" + server_name + "\" /home/<User>/.g/decom/decom-ad.yml"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if clusterenv == 'dev' or clusterenv == 'test':
            ssh.connect(hostname='<LPAR>0005a.<domain-name>', username=account, password=password, port="22")
        else:
            ssh.connect(hostname='<Puppet-Server>.<domain-name>', username=account, password=password, port="22")
        stdin, stdout, stderr = ssh.exec_command( cmd )
        frames = stdout.read().decode('ascii').split('\n')
        frames = list(filter(None, frames))

    finally:
        ssh.close()
        del ssh, stdin, stdout, stderr

    # return json.dumps(result).strip(' "').rstrip()
    return 0

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
