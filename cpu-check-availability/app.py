import os
import sys
import ssl
import requests
import json
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
@app.route('/checkCPUAvailability', methods=['POST'])

def checkCPUAvailability():
    result = {"output": "error"}
    json_req = request.get_json(force=True)
    frame = json_req['frame']
    hmc = json_req['hmc']
    req_cpu = json_req['CPU']
    procpool = json_req['CPUPool']

    cpus = []
    cpuout = ""
    if "Default" not in procpool:
        cpucommand = "lssyscfg -r prof -m " + frame + " -F shared_proc_pool_name,desired_proc_units | grep " + procpool
        poolcommand = "lshwres -r procpool -m " + frame + " -F name,max_pool_proc_units | grep " + procpool
    else:
        cpucommand = "lssyscfg -r prof -m " + frame + " -F shared_proc_pool_name,desired_proc_units"
        poolcommand = "lshwres -r proc -m " + frame + " --level sys -F curr_avail_sys_proc_units"
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hmc, username=account, password=password, port="22")

        stdin, stdout, stderr = client.exec_command(cpucommand)
        cpuout = stdout.read().decode('ascii')

    finally:
        client.close()

    cpuoutlist = cpuout.split('\n')
    for item in cpuoutlist:
        if item != "":
            cpus.append(float(item.split(',')[1]))

    cpu_used = sum(cpus)
    poolout = ""
    try:
        client2 = paramiko.SSHClient()
        client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client2.connect(hostname=hmc, username=account, password=password, port="22")

        stdin2, stdout2, stderr2 = client2.exec_command(poolcommand)
        poolout = stdout2.read().decode('ascii')

    finally:
        client2.close()

    if "Default" not in procpool:
        poolsize = float(poolout.split(',')[1])
        remaining_cpu = poolsize - cpu_used
    else:
        remaining_cpu = float(poolout.strip('\n'))

    if req_cpu == "":
        req_cpu = 0.0

    if float(req_cpu) <= remaining_cpu:
        available_cpu = "true"
    else:
        available_cpu = "false"

    result = '{ "CPUAvailable": ' + available_cpu + ' }'
    return( result )

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
