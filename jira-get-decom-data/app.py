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
x=0

def getJiraDecomData( options, itcm_num, fields_facts ):
    # connect
    jira = JIRA( options, basic_auth=(account, password) )
    allfields = jira.fields()
    nameMap = {field['name']:field['id'] for field in allfields}
    issue = jira.issue( itcm_num )
    output = "{"

    for jira_field, jira_fact in fields_facts.items():
        val = getattr( issue.fields, nameMap[jira_field] )
        output += '"' + str( jira_fact ).strip() + '":"' + str( val ).strip() + '",'

    return output

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/getDecomData', methods=['POST'])
def getDecomData():
    # json input
    json_req = request.get_json(force=True)
    jira_fqdn = json_req['jiraUrl']
    itcm_num = json_req['ITCMNum']

    # initialize variables
    result = '{'
    result_detail = ""

    # input validation
    if itcm_num[:5].upper() != "ITCM-":
        result_detail = "AUTOMATION_DATA_MISMATCH itcm_num prefix"
    elif len(itcm_num) < 8 or len(itcm_num) > 12:
        result_detail = "AUTOMATION_DATA_MISMATCH  itcm_num length"
    elif "<domain-name>" not in jira_fqdn:
        result_detail = "AUTOMATION_DATA_MISMATCH  jira_fqdn domain"
    elif "jira" not in jira_fqdn:
        result_detail = "AUTOMATION_DATA_MISMATCH  jira_fqdn hostname"
    elif len(jira_fqdn) < 14 or len(jira_fqdn) > 18:
        result_detail = "AUTOMATION_DATA_MISMATCH  jira_fqdn length"

    # constants
    jira_url_base = 'https://' + jira_fqdn
    options = {'server': jira_url_base, 'verify': False }

    fields_facts={
        'Asset Name':'hostName',
        'Functional Environment':'functionalEnvironment'
    }

    if len( result_detail ) > 0:
        result = '{"response": "error: ' + result_detail + '"}'
    else:
        result = getJiraDecomData( options, itcm_num, fields_facts )

    result += "}"
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
