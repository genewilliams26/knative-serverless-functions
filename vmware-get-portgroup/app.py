import os
import json
from flask import Flask, request

accountsecret = open("/var/secret/vmwareaccount/vmwareaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/vmwarepassword/vmwarepassword", "r")
password = passwordsecret.readline().strip()

def getPortgroup(vcenter, vlan, cluster):
    import atexit
    from pyVmomi import vim
    from pyVim import connect

    result = []

    # Get vim objects of a given type.
    def get_vim_objects(content, vim_type):
        return [item for item in content.viewManager.CreateContainerView(content.rootFolder, [vim_type], recursive=True).view]

    si = connect.SmartConnectNoSSL(host=vcenter, user=account, pwd=password,port=443)

    content = si.RetrieveContent()

    # Get the virtual switches in vCenter.
    for DistSwitch in get_vim_objects(content, vim.DistributedVirtualSwitch):
        # Get portgroups in the virual switch.
        for portgroup in DistSwitch.portgroup:
            # Get the hosts for each prot group. This is to check if the cluster matches.
            for host in portgroup.host:
                if str(portgroup.config.defaultPortConfig.vlan.vlanId) == vlan and host.parent.name.lower() == cluster.lower():
                    # Omit infoblox port groups.
                    if not "infoblox" in portgroup.name.lower():
                        result.append(str(portgroup.name))

    # Remove duplicate results from the list.
    result = list(set(result))

    """
    Return a string with a single result, "error: duplicate" if multiple port groups are found, "error: no matches" if there are no port groups found, 
    or "error: unkown" for any other list length.
    """
    if len(result) == 1:
        result = str(result[0])
    elif len(result) == 0:
        result = "error: no matches"
    elif len(result) >= 2:
        result = "error: duplicate"  
    else:
        result = "error: unkown"

    jsonStr = json.dumps(result)

    return jsonStr

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when colling the function
@app.route('/getPortgroup', methods=['POST'])
def getTemplate():
    req_data = request.get_json(force=True)

    vcenter = req_data["vcenter"]
    vlan = req_data["vlan"]
    cluster = req_data["cluster"]

    flask_result = getPortgroup(vcenter, vlan, cluster)

    return flask_result

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=int(os.environ.get('PORT', 8080)))