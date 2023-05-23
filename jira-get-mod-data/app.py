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

def getJiraBuildData( options, itcm_num, fields_facts, idalko_url_base ):
    # connect
    jira = JIRA( options, basic_auth=(account, password) )
    allfields = jira.fields()
    nameMap = {field['name']:field['id'] for field in allfields}
    issue = jira.issue( itcm_num )
    output = "{"

    for jira_field, jira_fact in fields_facts.items():
        val = getattr( issue.fields, nameMap[jira_field] )
        if jira_fact == 'memory':
            val_list = str(val).split('.')
            val = val_list[0]
        output += '"' + str( jira_fact ).strip() + '":"' + str( val ).strip() + '",'

    # idalko table data
    issue_id = issue.id
    network_info_count = 0
    if getattr( issue.fields, nameMap["Network Information"] ):
        network_info_count = int(getattr( issue.fields, nameMap["Network Information"] ))
    storage_info_count = 0
    if getattr( issue.fields, nameMap["Storage Information"] ):
        storage_info_count = int(getattr( issue.fields, nameMap["Storage Information"] ))
    iam_info_count = 0
    if getattr( issue.fields, str(nameMap["IAM Processing"]) ):
        iam_info_count = int(getattr( issue.fields, str(nameMap["IAM Processing"]) ))

    if network_info_count > 0:
        grid_id = "16538"
        endpoint = idalko_url_base + str(grid_id) + '/issue/' + str(issue_id)
        res = requests.get(endpoint, auth=( account, password ), verify=False)
        ip_addr = str( res.json()["values"][0]["ipaddress"] )
        gw_addr = str( res.json()["values"][0]["gateway"] )
        sm_addr = str( res.json()["values"][0]["subnetmask"] )
        vlan_id = str( res.json()["values"][0]["vlan"] )
        ip_settings = '"IPAddress":"' + ip_addr + '","gateway":"' + gw_addr + '","netmask":"' + sm_addr + '","vlan":"' + vlan_id + '"'
        output += str(ip_settings)

    if storage_info_count > 0:
        filesystems = '"additionalFilesystems":['
        grid_id = "20623"
        endpoint = idalko_url_base + str(grid_id) + '/issue/' + str(issue_id)
        res = requests.get(endpoint, auth=( account, password ), verify=False)
        for x in range(0, storage_info_count):
            mount_point = res.json()["values"][x]["filesystem"]
            float_size = res.json()["values"][x]["requestedchange"]
            size = str(int(float_size))
            filesystems += '{"mount_point":"' + mount_point + '","size":"' + size + '"}'
            if x < (storage_info_count-1):
                filesystems += ','
                filesystems += ']'
                output += str(filesystems)

    if iam_info_count > 0:
        iam_records = '"IAMRecords":['
        grid_id = "22011"
        endpoint = idalko_url_base + str(grid_id) + '/issue/' + str(issue_id)
        res = requests.get(endpoint, auth=( account, password ), verify=False)
        for x in range(0, iam_info_count):
            ad_group = ""
            ad_group += str(res.json()["values"][x]["adgroup"])
            ent_owner = ""
            ent_owner += str(res.json()["values"][x]["entowner"])
            iam_records += '{"ad_group":"' + ad_group + '","ent_owner":"' + ent_owner + '"}'
            if x < (iam_info_count-1):
                iam_records += ','
                iam_records += ']'
                output += ',' + str(iam_records)

    return output

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/getBuildData', methods=['POST'])
def getBuildData():
    # json input
    json_req = request.get_json(force=True)
    jira_fqdn = json_req['jira_fqdn']
    itcm_num = json_req['itcm_num']

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
    idalko_url_base = "https://" + jira_fqdn + ":443/rest/idalko-igrid/1.0/grid/"
    options = {'server': jira_url_base, 'verify': False }

    fields_facts={
        'Designated NERC Test System':'DNTSFlag',
        'NERC Classification':'NERCClassification',
        'Cores':'CPU',
        'RAM':'memory',
        'Description':'description',
        'Co-location Rule':'locationRule',
        'System Type':'systemType',
        'Storage Information':'storageTable',
        'IT Ops Owner':'opsOwner',
        'Fulfillment Owner':'fulfillmentOwner',
        'Business Owner':'businessOwner',
        'Dev Owner':'devOwner',
        'Frame':'frame',
        'Domain':'domain',
        'BES Cyber System':'BESCyberAsset',
        'OU':'OU',
        'OS Platform':'osPlatform',
        'OS':'OS',
        'SOC1 Impacting?':'SSAE16Impact',
        'vCenter Folder':'vcenterFolder',
        'vCenter':'vcenter',
        'Monitoring Required':'monitoringRequired',
        'Location':'datacenter',
        'Infrastructure Implementation Type':'INFImplementationType',
        'Host Cluster':'hostCluster',
        'Functional Environment':'functionalEnvironment',
        'Environment':'environment',
        'Designated POD':'designatedPod',
        'Backup Schedule':'backupSchedule',
        'Datastore Cluster':'datastoreCluster',
        'Asset Name':'assetName',
        'Asset Description':'assetDescription',
        'CPU Pool':'CPUPool',
        'Business Application':'businessApp',
        'Business Service':'businessService',
        'Business Function':'businessFunction',
        'New IAM Role Required?':'IDMRole',
        'New AD Group Required?':'securityGroupAdmin',
        'Virtual Cores':'virtualCPU',
        'Building and Data Center':'building'
    }

    if len( result_detail ) > 0:
        result = '{"response": "error: ' + result_detail + '"}'
    else:
        result = getJiraBuildData( options, itcm_num, fields_facts, idalko_url_base )

    result += "}"
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
