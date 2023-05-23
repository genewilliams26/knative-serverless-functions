import sys
import atexit
import json
from pyVmomi import vim, vmodl
from pyVim import connect
import os
import requests
from requests.auth import HTTPBasicAuth
from jira import JIRA
#import paramiko
#from flask import Flask, request

import cProfile
import pstats

import pchelper

## add threading and blocking support
from threading import Thread, Lock
#create lock instance
lock = Lock()

requests.packages.urllib3.disable_warnings() # Disable SSL warnings in requests #

#make the assumption we are ok.
exception_occured = False

# For py only code.
account ='scorchprod'
password =''

# Get VM objects.
def get_vim_objects(content, vim_type):
    return [item for item in content.viewManager.CreateContainerView(content.rootFolder, [vim_type], recursive=True).view]

# Look for templates.
def find_template(OS, vm, cluster):
    if str(OS).lower() in str(vm).lower() and "current" in str(vm).lower() and str(cluster).lower() in str(vm).lower():
        result.append(vm)
    elif str(OS).lower() in str(vm).lower() and str(cluster).lower() in str(vm).lower():
        result.append(vm)

    return result

"""
# For function code.
accountsecret = open("/var/secret/vmwareaccount/vmwareaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/vmwarepassword/vmwarepassword", "r")
password = passwordsecret.readline().strip()
"""

def getJiraBuildData( options, itcm_num, fields_facts, idalko_url_base ):
    #lock the thread.
    lock.acquire()

    global result; result = []

    # return error when unable to reach jira
    try:
        jira = JIRA( options, basic_auth=(account, password) )
    except:
        lock.release()
        return f"Unable to connect to jira",500

    allfields = jira.fields()
    domain_base = ""
    nameMap = {field['name']:field['id'] for field in allfields}
    issue = jira.issue( itcm_num )
    output = "{"
    default_mounts = ["os", "/", "c", "c:", "c:\\"]

    ## enable code profiles so we can find bottlenecks in the code logs.
    profile = cProfile.Profile()
    profile.enable()

    bldg = ""
    for jira_field, jira_fact in fields_facts.items():
        if not jira_field == 'Application Role':
            val = getattr( issue.fields, nameMap[jira_field] )

        if jira_fact == 'memory':
            val_list = str(val).split('.')
            val = val_list[0]

        # Get the base domain for OU and Tier 
        if jira_field == 'Domain':
            domain_base = val.replace( ".com", "" )

        if jira_field == 'NERC Yes/No' or 'NERC Classification' in jira_field:
            t = str( val ).strip()
            if t == 'None' or t == 'NONE':
                val = 'no'
            else:
                val = 'yes'

        # Set the env_grup variable for use in the groupName variable and the env_ou for use in the OU variable.
        # Values from table 3.6.1 in the Asset Naming Sandard.docx.
        if jira_field == 'Functional Environment' in jira_field:
            # reduce chance of a case issue
            val = val.upper()
            if val == 'IMM TEST':
                env_group = "IM"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'OTS TEST':
                env_group = "IT"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'DEV' or val == 'VENDOR':
                env_group = "DV"; env_ou = "DEV"; top_environment = "DEV"
            elif val == 'FAT':
                env_group = "FT"; env_ou = "ITEST"; top_environment = "TEST"
            elif val == 'IFAT':
                env_group = "IF"; env_ou = "ITEST"; top_environment = "TEST"
            elif val == 'IMM1' or val == 'IMM2':
                env_group = "IM"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'ITEST':
                env_group = "IT"; env_ou = "ITEST"; top_environment = "TEST"
            elif val == 'LAB':
                env_group = "LB"; env_ou = "DEV"; top_environment = "DEV"
            elif val == 'MBE':
                env_group = "MB"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'MAS1' or val == 'MAS2':
                env_group = "MS"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'MOTE':
                env_group = "MT"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'MVE1' or val == 'MVE2' or val == 'MVE3':
                env_group = "MV"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'OTS1' or val == 'OTS2' or val == 'OTS3' or val == 'OTS4' or val == 'OTS5':
                env_group = "OT"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'PROD':
                env_group = "PR"; env_ou = "PROD"; top_environment = "PROD"
            elif val == 'DST' or val == 'STAGE':
                env_group = "SG"; env_ou = "ITEST"; top_environment = "TEST"
            elif val == 'SOTE':
                env_group = "ST"; env_ou = "PROD"; top_environment = "MSE"
            elif val == 'DVTS':
                env_group = "TS"; env_ou = "DEV"; top_environment = "DEV"
            elif val == 'CERT':
                env_group = "CT"; env_ou = "PROD"; top_environment = "MSE"
            # add failure for unknown enviroment group and return it.
            else:
                lock.release()
                return f"Unknown Environment {val}",400

        # Set the Environment variable for use.
        if jira_field == 'Environment' in jira_field:
            val = top_environment

        # Get the asset name to use in the groupName var for windows servers.
        if jira_field == 'Asset Name' in jira_field:
            asset_name = val.upper()

        # Format Business Application value to standard, alhpanumeric characters only.
        if jira_field == 'Business Application' in jira_field:
            busi_app_formated = (val.replace(' ','').replace('[^A-Za-z0-9]', '').split('-'))[1]

            """ Will be used in future.
            # Set the OU value for the computer account.
            if domain_base.lower().find("b") != -1:
                if val.lower().find("citrix") != -1:
                    output += '"OU":"OU=Server ' + os_platform.lower().replace("windows ","") + ',OU=' + cityVal + ',OU=Citrix,OU=Tier 1,DC=' + domain_base + ",DC=com" + '",'
                else:
                    output += '"OU":"OU=' + cityVal + ',OU=Servers,OU=Tier 1,DC=' + domain_base + ",DC=com" + '",'
            else:
                if val.lower().find("citrix") != -1:
                    output += '"OU=Server ' + os_platform.lower().replace("windows ","") + ',OU":"OU=' + env_ou + ',OU=Server ' + os_platform.lower().replace("windows ","") + ',OU=' + cityVal + ',OU=Citrix,OU=Servers,DC=' \
                    + domain_base + ",DC=com" + '",'
                else:
                    output += '"OU":"OU=' + env_ou + ',OU=Server ' + os_platform.lower().replace("windows ","") + ',OU=' + cityVal + ',OU=Windows,OU=Servers,DC=' \
                    + domain_base + ",DC=com" + '",'
            """

        # Determine Entitlement from $OSFamily and set the os_platform value to get the template.
        if jira_field == 'OS Platform' in jira_field:
            os_platform = val

            if val.lower().find("windows") != -1:
                access_type = 'WindowsAdmin'
            elif val.lower().find("rhel") != -1:
                access_type = 'LinuxLogon'
            elif val.lower().find("aix") != -1:
                access_type = 'AIXLogon'

            # Set the groupanme value.
            if val.lower().find("windows") != -1:
                output += '"groupName":"' + (asset_name.upper() + " Admins") + '",'
            else:
                output += '"groupName":"' + (busi_app_formated + "_" +  access_type + "_" + env_group) + '",'

        if jira_field == 'Location':
            t = str( val ).strip()
            if t[0].upper() == 'T':
                cityVal = 'Taylor'
            else:
                cityVal = 'Bastrop'

            # Set bldg value if the OS is AIX.
            if str(os_platform).lower().find("aix") != -1:
                bldg = t[0].upper() + 'CC' + t[1]

        if jira_field == 'vCenter' in jira_field:
            # Set vCenter value so it can be used to connect to vCenter if the OS is not AIX.
            if str(os_platform).lower().find("aix") == -1:
                v_center = val + ".<domain-name>"

                # Set bldg value which is used for the datacenter value based on the vCenter value if the OS is not AIX.
                if val == 'vct3':
                    bldg = 'TCC3'
                elif val == 'vct3ems':
                    bldg = 'TCC3'
                elif val == 'vct1ems':
                    bldg = 'TCC1EMS'
                elif val == 'vct1block':
                    bldg = 'TCC1_T1LOWR_BK01'
                elif val == 'vct1':
                    bldg = 'TCC1'
                elif val == 'vct3rail':
                    bldg = 'T3D1'
                elif val == 'vct1rail':
                    bldg = 'T1D1'
                elif val == 'vclab':
                    bldg = 'Lab'
                elif val == 'vcb1ems':
                    bldg = 'BCC1'
                elif val == 'vcb1':
                    bldg = 'BCC1'
                elif val == 'vcb1rail':
                    bldg = 'B1D1'
                #elif val == 'vct3block':
                #    bldg = 'TCC3'
                #elif val == 'vct3grid':
                #    bldg = 'TCC3'
                #elif val == 'vcb1block':
                #    bldg = 'TCC3'
                #elif val == 'vcb1grid':
                #    bldg = 'TCC3'

        if jira_field == 'Host Cluster' in jira_field:
            # Set host_cluster value so it can be used to get the template if the OS is not AIX.
            if str(os_platform).lower().find("aix") == -1:
                host_cluster = val
                # Get vim objects of a given type.
                try:
                    si = connect.SmartConnectNoSSL(host=v_center, user=account, pwd=password,port=443)
                except:
                    lock.release()
                    return f"Unable to connect to {v_center}",500

                content = si.RetrieveContent()

                if "windows" in str(os_platform).lower() and "r2" not in str(os_platform).lower():
                    # Get the last element of the split variable, should be the OS year.
                    os_formated = str(os_platform).lower().split()[-1]
                elif "r2" in str(os_platform).lower():
                    # For 2012 R2 OS get the second element of the split variable. Should be the OS year.
                    os_formated = str(os_platform).lower().split()[1]
                else:
                    os_formated = str(os_platform).lower().replace(" ", "")

                vm_properties = ["name","config.template"]                

                root_folder = si.content.rootFolder
                view = pchelper.get_container_view(si, obj_type=[vim.VirtualMachine])
                vm_data = pchelper.collect_properties(si,
                                      view_ref=view,
                                      obj_type=vim.VirtualMachine,
                                      path_set=vm_properties,
                                      include_mors=True)                
                for vm in vm_data:
                    if vm["config.template"] and not "backup" in str(vm["name"]).lower() and not "old" in str(vm["name"]).lower() and not "inf" in str(vm["name"]).lower():
                         if "esx" in str(host_cluster).lower():
                             result = find_template(os_formated, vm["name"], host_cluster)
                         elif "ems" in str(host_cluster).lower():
                             result = find_template(os_formated, vm["name"], host_cluster)

                if len(result) > 1:
                    #result.insert(0,"ERROR: Duplicate templates found.")
                    output += '"template":"ERROR: Duplicate templates found. ' + ','.join(result) + "." + '",'
                elif len(result) == 0:
                    #result.insert(0,"ERROR: No template found.")
                    output += '"template":"ERROR: No template found.",'
                else:
                    output += '"template":"' + ''.join(result) + '",'
            else:
                output += '"template":"None",'

        output += '"' + str( jira_fact ).strip() + '":"' + str( val ).strip() + '",'
    output += '"building":"' + str( bldg ).strip() + '","city":"' + str( cityVal ).strip() + '",'

    # idalko table data
    issue_id = issue.id
    network_info_count = 0
    if getattr( issue.fields, nameMap["Network Information"] ):
        network_info_count = int(getattr( issue.fields, nameMap["Network Information"] ))
    storage_info_count = 0
    if getattr( issue.fields, nameMap["Storage Information"] ):
        storage_info_count = int(getattr( issue.fields, nameMap["Storage Information"] ))

    grid_id = "16538"
    endpoint = idalko_url_base + str(grid_id) + '/issue/' + str(issue_id)
    # add some failure logic 
    try:
        res = requests.get(endpoint, auth=( account, password ), verify=False)
    except:
        lock.release()
        return f"Unable to connect to {endpoint}",500

    ip_addr = str( res.json()["values"][0]["ipaddress"] )
    gw_addr = str( res.json()["values"][0]["gateway"] )
    sm_addr = str( res.json()["values"][0]["subnetmask"] )
    vlan_id = str( res.json()["values"][0]["vlan"] )
    ip_settings = '"IPAddress":"' + ip_addr + '","gateway":"' + gw_addr + '","netmask":"' + sm_addr + '","vlan":"' + vlan_id + '"'
    output += str(ip_settings)

    filesystems = ',"additionalFilesystems":['
    grid_id = "20623"
    endpoint = idalko_url_base + str(grid_id) + '/issue/' + str(issue_id)
    # added some failure logic
    try:
        res = requests.get(endpoint, auth=( account, password ), verify=False)
    except:
        lock.release()
        return f"Unable to connect to {endpoint}",500

    count = len( res.json()["values"] )
    if count == 0:
        filesystems += ']'
    else:
        int_count = 0 # Set variable to know how many times the for loop has ran.
        for x in range(0, count):
            mount_point = res.json()["values"][x]["filesystem"]
            if mount_point.lower() in default_mounts:
                d = 0
            else:
                float_size = res.json()["values"][x]["requestedchange"]
                size = str(int(float_size))
                if int_count > 0:
                    filesystems += ',{"mount_point":"' + mount_point + '","size":"' + size + '"}'
                else:
                    filesystems += '{"mount_point":"' + mount_point + '","size":"' + size + '"}'
                int_count += 1 # Only increment if non-OS drives are found.

        filesystems += ']'

    output += str(filesystems)

    # Disconnect from vCenter if OS is not AIX.
    if str(os_platform).lower().find("aix") == -1:
        atexit.register(connect.Disconnect, si)

    profile.disable()
    ps = pstats.Stats(profile).sort_stats('cumtime')
    ps.print_stats()

    lock.release()
    return output

#lets try and catch exceptions we have not seen yet.
def uncaught_exception(exctype, value, tb):
    global exception_occured
    exception_occured = True
# tell python all untested exceptions come here
sys.excepthook = uncaught_exception

"""
# For function code. 
#app = Flask(__name__)

#when flask gets an unhandled exception set the crash flag!
@app.errorhandler(500)
def handle_internal_server_error(e):
    # code failure some place. 
    global exception_occured
    exception_occured = True
    return ('server side exception'), 500

# For function code. Simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

@app.route('/health', methods=['GET'])
def health():
    # tell liveness and readiness our current health state
    global exception_occured
    if exception_occured == False:
        return "OK",200
    else:
        return "Unhealthy",500

# The route used when calling the function
@app.route('/getBuildData', methods=['POST'])
"""

def getBuildData(argv): # For py only code.
#def getBuildData(): # For function code.
    # json input
    json_req = json.loads(argv) # For py only code.
    #json_req = request.get_json(force=True) # For function code.
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
        'SOC1 Impacting?':'SSAE16Impact',
        'NERC Classification':'NERCClassification',
        'Cores':'CPU',
        'NERC Yes/No':'IsNERC',
        'RAM':'memory',
        'Co-location Rule':'locationRule',
        'System Type':'systemType',
        'Storage Information':'storageTable',
        'IT Ops Owner':'opsOwner',
        'Fulfillment Owner':'fulfillmentOwner',
        'Asset Name':'assetName',
        'Business Owner':'businessOwner',
        'Dev Owner':'devOwner',
        'Frame':'frame',
        'BES Cyber System':'BESCyberAsset',
        'Domain':'domain',
        'Functional Environment':'functionalEnvironment',
        'Business Application':'businessApp',
        'OS Platform':'OS',
        'Location':'datacenter',
        'OU':'OU',
        'vCenter Folder':'vcenterFolder',
        'vCenter':'vcenter',
        'Monitoring Required':'monitoringRequired',
        'Infrastructure Implementation Type':'INFImplementationType',
        'Host Cluster':'hostCluster',
        'Environment':'top_environment',
        'Designated POD':'designatedPod',
        'Backup Schedule':'backupSchedule',
        'Datastore Cluster':'datastoreCluster',
        'Asset Description':'assetDescription',
        'CPU Pool':'CPUPool',
        'Business Service':'businessService',
        'Business Function':'businessFunction',
        'Virtual Cores':'virtualCPU',
        'Application Role':'appRole'
    }

    if len(result_detail) > 0:
        result = '{"response": "error: ' + result_detail + '"}'
    else:
        result = getJiraBuildData( options, itcm_num, fields_facts, idalko_url_base )

    # see if we got an error code back
    if result[1] == 400 or result[1] == 500:
        return result

    result += "}"
    return result

# For py only code.
result = getBuildData(sys.argv[1])
print(result)

# For function code.
#if __name__ == "__main__":
#   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))