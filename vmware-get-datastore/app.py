import os
import requests
from flask import Flask, request

accountsecret = open("/var/secret/vmwareaccount/vmwareaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/vmwarepassword/vmwarepassword", "r")
password = passwordsecret.readline().strip()

def getVmTemplate(vcenter, OS, domain):
    import atexit
    import json
    from pyVmomi import vim, vmodl
    from pyVim import connect

    result = []

    # Get vim objects of a given type.
    def get_vim_objects(content, vim_type):
        return [item for item in content.viewManager.CreateContainerView(content.rootFolder, [vim_type], recursive=True).view]

    try:
        si = connect.SmartConnectNoSSL(host=vcenter, user=account, pwd=password,port=443)

    except:
       result += ("Something went wrong whey trying to connect to " + str(vcenter))

    content = si.RetrieveContent()

    for vm in get_vim_objects(content, vim.VirtualMachine):
        if vm.config.template:
            if not "b" in str(domain).lower():
                if str(OS).lower() in str(vm.name).lower() and "current" in str(vm.name).lower() and not "bes" in str(vm.name).lower():
                    result.append(vm.name)
                elif str(OS).lower() in str(vm.name).lower() and not "backup" in str(vm.name).lower() and not "old" in str(vm.name).lower() and not "test" in str(vm.name).lower() and not "inf" in str(vm.name).lower()  and not "bes" in str(vm.name).lower():
                    result.append(vm.name)
            else:
                if str(OS).lower() in str(vm.name).lower() and "current" in str(vm.name).lower() and "bes" in str(vm.name).lower():
                    result.append(vm.name)
                elif str(OS).lower() in str(vm.name).lower() and not "backup" in str(vm.name).lower() and not "old" in str(vm.name).lower() and not "test" in str(vm.name).lower() and not "inf" in str(vm.name).lower()  and "bes" in str(vm.name).lower():
                    result.append(vm.name)

    if len(result) > 1:
        result.insert(0,"ERROR")

    atexit.register(connect.Disconnect, si)

    jsonStr = json.dumps(result)

    return jsonStr

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when colling the function
@app.route('/getTemplate', methods=['POST'])
def getTemplate():
    req_data = request.get_json(force=True)

    vcenter = req_data["vcenter"]
    OS = req_data["OS"]
    domain = req_data["domain"]

    flask_result = getVmTemplate(vcenter, OS, domain)

    return flask_result

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=int(os.environ.get('PORT', 8080)))