import os
import sys
import json
import requests
from flask import Flask, request

accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

fq_hostname = "<LPAR>004.<domain-name>"
ipv4addr = "<IP-Addr>"

header = "Content-Type:application/json"
url_base = "https://tgrid.<domain-name>/wapi/v2.1"
a_record_get = '/record:a?name='
ptr_record_get = '/record:ptr?ipv4addr='

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/decomDNS', methods=['POST'])

def decomDNS():
    json_req = request.get_json(force=True)
    fq_hostname = json_req['fq_hostname']
    ipv4addr = json_req['ip_addr']


    response = requests.get( url_base + a_record_get + fq_hostname, auth=(account, password), verify=False )
    s = str( response.json() ).split()[1]
    a_record_id = s[1:len(s)-2]

    response = requests.get( url_base + ptr_record_get + ipv4addr, auth=(account, password), verify=False )
    s = str( response.json() ).split()[1]
    ptr_record_id = s[1:len(s)-2]

    a_response = requests.delete( url_base + '/' + a_record_id, auth=(account, password), verify=False )
    ptr_response = requests.delete( url_base + '/' + ptr_record_id, auth=(account, password), verify=False )
    host_response = requests.delete( url_base + '/request', auth=(account, password), verify=False, json='[{"method": "STATE:ASSIGN","data":{"host_name":"' + fq_hostname + '"}},{"method":"GET","object": "record:host","data": {"name":"##STATE:host_name:##"},"assign_state": {"host_ref": "_ref"},"enable_substitution": true,"discard": true},{ "method": "DELETE", "object": "##STATE:host_ref:##","enable_substitution": true,"discard": true},{"method": "STATE:DISPLAY"}]' )

    ns_cmd = "nslookup " + fq_hostname + "; nslookup " + ipv4addr + ";"
    ns_result = os.system("bash -c '%s'" % ns_cmd)
    print( ns_result )

    result = '{"a_response":"' + str(a_response) + '","ptr_response":"' + str(ptr_response) + '","host_response":"' + str(host_response) + '"}'
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
