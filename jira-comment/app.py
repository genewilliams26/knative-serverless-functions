import sys
import json
import os
import requests
from requests.auth import HTTPBasicAuth
from jira import JIRA
import paramiko
from flask import Flask, request

accountsecret = open("/var/secret/vmwareaccount/vmwareaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/vmwarepassword/vmwarepassword", "r")
password = passwordsecret.readline().strip()

def commentIssue( options, itcm_num, msg ):
    rc = 1
    jira = JIRA( options, basic_auth=(account, password) )
    issue = jira.issue(itcm_num)
    jira.add_comment(issue, msg)

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/jiraComment', methods=['POST'])
def jiraComment():
    # json input    ex: '{"jira_fqdn":"jiratest.<domain-name>","itcm_num":"ITCM-135555","comment":"test comment"}'
    json_req = request.get_json(force=True)
    jira_fqdn = json_req['jira_fqdn']
    itcm_num = json_req['itcm_num']
    comment = json_req['comment']

    # constants
    jira_url_base = 'https://' + jira_fqdn
    options = {'server': jira_url_base, 'verify': False }
    commentIssue( options, itcm_num, comment )

    return "0"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
