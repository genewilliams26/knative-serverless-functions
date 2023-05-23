import os
import re
import sys
import requests
import json
from requests.structures import CaseInsensitiveDict
from flask import Flask, request

accountsecret = open("/var/secret/tladminaccount/tladminaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/tladminpassword/tladminpassword", "r")
password = passwordsecret.readline().strip()

file = open( '/etc/resolv.conf', 'r')
for line in file:
    if re.search( 'k8s\.<domain-name>', line ):
        pattern = r'(^.*?)(..)(k8s\.<domain-name>.*$)'
        replacement = r'\2'
        cluster_indicator = re.sub( pattern, replacement, line ).replace("\n", "")
        if cluster_indicator == 'ev' or cluster_indicator == 'st' or cluster_indicator == 'ms':
            console_cluster = '<k8s-cluster>'
            defenders_expected = 18
        elif cluster_indicator == 'pt' or cluster_indicator == 'pb':
            console_cluster = cluster_indicator + 'k8s'
            defenders_expected = 6
        else:
            console_cluster = cluster_indicator + 'k8s'
            defenders_expected = 3

app = Flask(__name__)

@app.route('/')
def default():
    return "Please specify parameters"
@app.route( '/checkDefenders', methods=['POST'] )

def checkDefenders():
    needs_attention = []

    url = "https://twistlock-console.apps." + console_cluster + ".<domain-name>/api/v1/authenticate"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    payload = '{"username":"' + account + '","password":"' + password + '"}'
    resp = requests.post(url, headers=headers, data=payload,  verify=False)
    resp_targ = json.loads( resp.text )
    token = resp_targ['token']

    url = "https://twistlock-console.apps." + console_cluster + ".<domain-name>/api/v1/defenders/summary"
    hdr = {'Authorization': "Bearer " + token}
    resp = requests.get(url, headers=hdr, verify=False).json()
    defender_count = resp[0]['connected']

    if defender_count != defenders_expected:
        needs_attention.append( console_cluster )

    if len( needs_attention ) == 0:
        msg = "200"
    else:
        msg = "Error: Incorrect number of Twistlock Defenders for Twistlock Console(s) on the following clusters:  "
        for i in needs_attention:
            msg += i + "  ";

    return msg

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

