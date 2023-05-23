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


def is_dup( vm_name, vc ):
    ret = True
    obj = {}
    si = SmartConnectNoSSL( host=vc, user=account + "@<domain-name>", pwd=password, port=443 )
    content = si.content
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for managed_object_ref in container.view:
        obj.update({managed_object_ref: managed_object_ref.name})
    if vm_name not in obj:
        ret = False

    return ret

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/getUniqueHostname', methods=['POST'])

def getUniqueHostname():
    json_req = request.get_json(force=True)
    vc = json_req['vcenter']
    dup = True
    while dup:
        static_str_a = 'lab'
        static_str_b = 'ss'
        alpha_a_sz = 5
        alpha_b_sz = 5
        numeric_sz = 4

        tmp_alpha = string.ascii_lowercase
        gen_alpha_a = ''.join( random.choice(tmp_alpha) for i in range(alpha_a_sz) )
        tmp_alpha = string.ascii_lowercase
        gen_alpha_b = ''.join( random.choice(tmp_alpha) for i in range(alpha_b_sz) )
        tmp_numeric = string.digits
        gen_numeric = ''.join( random.choice(tmp_numeric) for i in range(numeric_sz) )

        hname = static_str_a + '-' + static_str_b + '-' + gen_alpha_a + '-' + gen_alpha_b + '-' + gen_numeric

        if not is_dup( hname, vc ):
            dup = False

    return hname

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
