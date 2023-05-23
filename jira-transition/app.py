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

def transitionIssue( options, itcm_num, desired_state, msg ):
    rc = 1
    jira = JIRA( options, basic_auth=(account, password) )
    issue = jira.issue(itcm_num)
    transitions = jira.transitions(issue)
    if desired_state == "success":
        jira.transition_issue(issue, '1011')
        rc = 0
        jira.add_comment(issue, msg)
    else:
        jira.transition_issue(issue, '911')
        rc = 0
        jira.add_comment(issue, msg)
    return "0"

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/jiraTransition', methods=['POST'])
def jiraTansition():
    # json input    ex: '{"jira_fqdn":"jiratest.<domain-name>","itcm_num":"ITCM-135555","desired_state":"success","msg":"Build failed"}'
    json_req = request.get_json(force=True)
    jira_fqdn = json_req['jira_fqdn']
    itcm_num = json_req['itcm_num']
    desired_state = json_req['desired_state']
    msg = json_req['msg']

    # constants
    jira_url_base = 'https://' + jira_fqdn
    options = {'server': jira_url_base, 'verify': False }

    # input validation
    result_detail = ""
    if itcm_num[:5].upper() != "ITCM-":
        result_detail = "error: itcm_num prefix"
    elif "jira" not in jira_fqdn:
        result_detail = "error: jira_fqdn hostname"

    if len( result_detail ) > 0:
        result = '{"response":"error:"' + result_detail + '"}'
    else:
        result = '{"response":"'
        ret = transitionIssue( options, itcm_num, desired_state, msg )
        result += ret + '"}'

    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
