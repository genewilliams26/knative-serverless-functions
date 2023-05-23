import json
import os
import requests
from requests.auth import HTTPBasicAuth
import paramiko
from flask import Flask, request

accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

app = Flask(__name__)

def getTowerProjectList(towerurl):
    headers = {'Content-Type': 'application/json'}
    tower = requests.get(
        towerurl, 
        auth=HTTPBasicAuth(username=account, password=password),
        headers=headers,
        verify=False,
        )
    return tower.json()


def getProjectOrgs(orgArray, towerUrl):
    orgDict = {}
    orgOutput = ""
    for i in orgArray:
        orgAdmin = ""
        if i is not None and i != "None":
            headers = {'Content-Type': 'application/json'}
            tower = requests.get(
                towerUrl + "/api/v2/organizations/" + i +"/", 
                auth=HTTPBasicAuth(username=account, password=password),
                headers=headers,
                verify=False,
            )
            orgOutput = tower.json()
            orgName = str(orgOutput['name'])

            toweradmins = requests.get(
                towerUrl + "/api/v2/organizations/" + i +"/admins/", 
                auth=HTTPBasicAuth(username=account, password=password),
                headers=headers,
                verify=False,
            )
            adminOutput = toweradmins.json()
            if len(adminOutput['results']) > 0:
                if adminOutput['results'][0]['username']:
                    orgAdmin = str(adminOutput['results'][0]['username'])
            
            orgInfo = {}
            orgInfo['organization'] = orgName
            orgInfo['organization_admin'] = orgAdmin
            orgDict[i] = orgInfo
    return orgDict

@app.route('/')
def default():
    return "Please specify Tower Url Parameter"

# route used to call the function
@app.route('/getTowerProjects', methods=['POST'])
def getTowerProjects():
    json_req = request.get_json(force=True)
    towerUrl = json_req["tower"]

    output = getTowerProjectList(towerUrl + "/api/v2/projects/")

    results = output['results']
    orgArray = []
    for x in results:
        if str(x['organization']) not in orgArray and str(x['organization']) is not "None" and str(x['organization']) is not None:
            orgArray.append(str(x['organization']))

    orgArray.sort()

    thisOrgDict = getProjectOrgs(orgArray, towerUrl)

    projectDict = {}
    for y in results:
        if str(y['organization']) != "None":
            projectDict[y['name']] = thisOrgDict[str(y['organization'])]
    
    return projectDict

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
