import sys
import json
import paramiko
from threading import Thread
import requests
from flask import Flask, request

clusterenvsecret = open("/var/secret/clusterenv/clusterenv", "r")
clusterenv = clusterenvsecret.readline().strip()


app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/validateTasks', methods=['POST'])

def validateTasks():
    json_req = request.get_json(force=True)
    server_name = json_req['svr']
    ipv4addr = json_req['ipv4addr']

    if clusterenv == 'dev' or clusterenv == 'test':
        fq_pup_server = "<VM>0005a.<domain-name>"
    else:
        fq_pup_server = "<Puppet-Server>.<domain-name>"

    count = 0
    status = 1
    while( count < 10 and status == 1 ):
        dns_ck = 
        vm_ck = 
        ad_ck = 
        puppet_ck = 
        _ck = 


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
