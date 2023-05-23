import os
import string
import requests
from pypsrp.powershell import PowerShell, RunspacePool
from pypsrp.wsman import WSMan
from flask import Flask, request

accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/runPowershell', methods=['POST'])

def runPowershell():
    json_req = request.get_json(force=True)
    cmd = json_req['cmd']
    target = json_req['target']

    wsman = WSMan(target, username=account, password=password, cert_validation=False)

    with RunspacePool(wsman) as pool:
        ps = PowerShell(pool)
        ps.add_cmdlet("Get-PSDrive").add_parameter("Name", "C")
        ps.invoke()

    return ps.output[0]

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
