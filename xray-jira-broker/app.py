import os
import paramiko
import requests
import json
import urllib3
from git import Repo
from git import Git
from jira import JIRA
from requests.auth import HTTPBasicAuth
from flask import Flask, request
 
accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()




# receive riskData




xraySshSecret = open("/var/secret/sshaccount/xray-stash-sshkey", "r")
xraySshKey = xraySshSecret.readline().strip()

urllib3.disable_warnings()
jira_fqdn = 'deliverydev.<domain-name>'

# constants
repo_url = stash.<domain-name>
repo_name = reported-xray-risks
svc = "jira api"
jira_url_base = 'https://' + jira_fqdn
options = {'server': jira_url_base, 'verify': False }
keyFileName = "/tmp/.key"

def getReportedRisks():
    try:
        keyFile = open( keyFileName, "w")
        n = keyFile.write( xraySshKey )
        keyFile.close()
        git_ssh_cmd = 'ssh -i %s' % keyFileName
        Repo.clone_from(repo_url, os.path.join(os.getcwd(), repo_name),env=dict(GIT_SSH_COMMAND=git_ssh_cmd))

    finally:
        Repo.close()

def createRiskIssue( riskData ):
    try:
        jira = JIRA( options, basic_auth=(account, password) )
        new_issue = jira.create_issue(project='ITDS', summary='Test issue from knative function', description=riskData, issuetype={'name': 'Risk'})
    finally:
        jira.close()

def checkRisk( proposedRiskRecord ):
    try:
        rtn = False
        with open( keyFileName ) as f:
            if proposedRiskRecord in f.read():
                rtn = True
        return rtn
        
def main():
    try:
        getReportedRisks()
        proposedRiskRecord = buildProposedRiskRecord( riskData )
        isReported = checkRisk()
        if not isReported: 
            new_issue = jira.create_issue(project='ITDS', summary='Test issue from knative function', description=riskData, issuetype={'name': 'Risk'})
        else:
            print( proposedRiskRecord + ' has already been reported.' )
 
app = Flask(__name__)

# route to enforce web browser
@app.route('/')
def default():
    return "Please specify parameters"
 
# calling route 
@app.route('/checkFile', methods=['POST'])
def checkFile():
    req_data = request.get_json(force=True)
 
    hostname = req_data['hostname']
    directory = req_data['directory']
     
    result = main()
    return result
 
 
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
