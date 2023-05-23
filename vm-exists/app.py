import os
import ssl
import random
import string
import requests
from pyVim.connect import SmartConnectNoSSL
from pyVmomi import vim
from flask import Flask, request

accountsecret = open("/var/secret/vmwareaccount/vmwareaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/vmwarepassword/vmwarepassword", "r")
password = passwordsecret.readline().strip()

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/vmExists', methods=['POST'])

def vmExists():
    json_req = request.get_json(force=True)
    vc = json_req['vcenter']
    vm_target = json_req['vm_target']
    obj = {}
    si = SmartConnectNoSSL( host=vc, user=account+'@<domain-name>', pwd=password, port=443 )
    content = si.content
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

    is_there = False
    for managed_object_ref in container.view:
        obj.update({managed_object_ref: managed_object_ref.name})
        if vm_target.lower() == str(managed_object_ref.name).strip().lower():
          is_there = True

    if is_there:
        rtn = "true"
    else:
        rtn = "false"

    return rtn

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
