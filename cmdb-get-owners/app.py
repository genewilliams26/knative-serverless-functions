import os
import json
import requests
from flask import Flask, request

accountsecret = open("/var/secret/cmdbapiaccount/cmdbapiaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/cmdbapipw/cmdbapipw", "r")
password = passwordsecret.readline().strip()
clusterenvsecret = open("/var/secret/clusterenv/clusterenv", "r")
clusterenv = clusterenvsecret.readline().strip()

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/cmdbGetOwners', methods=['POST'])

def cmdbGetOwners():
    json_req = request.get_json(force=True)
    e = json_req['environment']
    ba = json_req['businessApp']
    ucmdb_id = ""

    if clusterenv == 'dev':
        apiurl = 'https://<API-Server>.<domain-name>:8443/rest-api'
    elif clusterenv == 'test':
        apiurl = 'https://<API-Server>.<domain-name>:8443/rest-api'
    else:
        apiurl = 'https://cmdb.<domain-name>:8443/rest-api'

    targ_env = str(e).lower()
    if targ_env == "dev" or targ_env == "dvts":
        target_type = "org_dev_primary"
    else:
        target_type = "org_itops_primary"

    # next line due to openshift not excepting key/value secrets with question marks
    ucmdb_login = {
        "username": account,
        "password": password,
        "clientContext": 1
    }
    r = requests.post( apiurl + '/authenticate', json=ucmdb_login,verify=False)
    tok = json.loads(r.text)
    r = requests.post( apiurl + '/topology','BA_OWNER',verify=False,headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(tok['token'])})
    cmdb_data = r.json()

    for ci in cmdb_data["cis"]:
        s = ci["properties"]["display_label"]
        if s == ba:
            ucmdb_id = ci["ucmdbId"]
            break

    for relation in cmdb_data["relations"]:
        s = relation["end2Id"]
        t = relation["type"]
        if s == ucmdb_id and t == target_type:
            owner_id = relation["end1Id"]
            break

    for ci in cmdb_data["cis"]:
        s = ci["ucmdbId"]
        if s == owner_id:
            owner = ci["properties"]["display_label"]
            break

    res = '{"owner":"' + owner.lower() + '"}'
    return res

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
