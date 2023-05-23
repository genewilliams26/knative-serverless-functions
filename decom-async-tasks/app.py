import sys
import json
import paramiko
from threading import Thread
import requests
from flask import Flask, request

clusterenvsecret = open("/var/secret/clusterenv/clusterenv", "r")
clusterenv = clusterenvsecret.readline().strip()


def async_decom_vm(session, vsvr_host, server_name):
    base_url = "https://decom-vm-functions.apps.<k8s-cluster>.<domain-name>/decomVM"
    payload = '{"vcenter":"' + vsvr_host + '","server_name":"' + vsvr + '"}'
    with session.post(base_url, data=payload) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
            print('   ' + data)
    return data

def async_decom_dns( session, ipv4addr, server_name ):
    base_url = "https://decom-dns-functions.apps.<k8s-cluster>.<domain-name>/decomDNS"
    payload = '{"fq_hostname":"' + server_name + '","ip_addr":"' + ipv4addr + '"}'
    with session.post(base_url, data=payload) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
            print('   ' + data)
    return data

def async_decom_ad( session, vsvr_host, server_name ):
    base_url = "https://decom-ad-functions.apps.<k8s-cluster>.<domain-name>/decomAD"
    payload = '{"vcenter":"' + vsvr_host + '","server_name":"' + svr + '"}'
    with session.post(base_url, data=payload) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
            print('   ' + data)
    return data

def async_decom_puppet( session, fq_pup_server, server_namer ):
    base_url = "https://decom-puppet-functions.apps.<k8s-cluster>.<domain-name>/decomPuppet"
    payload = '{"fq_pup_server":"' + fq_pup_server + '","fq_pup_client":"' + server_name + '"}'
    with session.post(base_url, data=payload) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
            print('   ' + data)
    return data

def async_decom_jirafacts(session, server_name):
    base_url = "https://decom-jirafacts-functions.apps.<k8s-cluster>.<domain-name>/decomJirafacts"
    payload = '{"fq_hostname":"' + server_name + '"}'
    with session.post(base_url, data=payload) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
            print('   ' + data)
    return data


app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/runTasksParallel', methods=['POST'])

def runTasksParallel():
    json_req = request.get_json(force=True)
    svr = json_req['svr']
    ipv4addr = json_req['ipv4addr']
    vsvr_host = json_req['vsvr_host']

    if clusterenv == 'dev' or clusterenv == 'test':
        fq_pup_server = "<VM>0005a.<domain-name>"
    else:
        fq_pup_server = "<Puppet-Server>.<domain-name>"


    Thread( target=async-decom-vm, args=(vsvr_host, svr) ).start()
    Thread( target=async-decom-dns, args=(ipv4addr, svr) ).start()
    Thread( target=async-decom-ad, args=(vsvr_host, svr) ).start()
    Thread( target=async-decom-puppet, args=( fq_pup_server, svr) ).start()
    Thread( target=async-decom-jirafacts, args=(svr) ).start()

    return 0

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
