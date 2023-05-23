import os
import ssl
import json
import string
import requests
import winrm
from winrm.protocol import Protocol
from flask import Flask, request
#from pypsrp.client import Client
#from pypsrp.shell import Process, SignalCode, WinRS
#from pypsrp.wsman import WSMan

accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

def callFunction(session, frame):
    base_url = "http://lpar-get-frame-pod-info-functions.apps.<k8s-cluster>.<domain-name>/getFramePodInfo"
    payload = '{"frame":"' + frame + '"}'
    with session.post(base_url, data=payload) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
            print('   ' + data)
        return data

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/lparRootVGadd', methods=['POST'])

def lparRootVGadd():
    json_req = request.get_json(force=True)
    frame = json_req['frame']
    pshSvr = json_req['pshSvr']

    with requests.Session() as session:
        frameInfoStr = callFunction(session, frame)
    frameInfo = json.loads(frameInfoStr)
    print( str(frameInfo) )

    cmd0 = "$credential = New-Object System.Management.Automation.PsCredential('" + account + "', (ConvertTo-SecureString " + password + " -AsPlainText -Force));"
    cmd1 = "d:\\director\\powershell\\netapp\\test-NETAPP-POSH-LPAR-rootVGadd.ps1 -credential $credential -Cluster " + str(frameInfo["wfaArray"]) + " -vServerName " + str(frameInfo["wfaSVM"]) + " -vioList ["
    for vioSvr in frameInfo["FRAMEvioServers"]:
        cmd1 += "'" + str(vioSvr) + "',"
    cmd1 = cmd1[:-1]
    cmd1 += "];"
    cmd = cmd0 + cmd1


    p = Protocol(
        endpoint='https://<WinRM-Server>.<domain-name>:5986/wsman',
        transport='ntlm',
        username=r'org\<User>',
        password='<password>',
        server_cert_validation='ignore')
    shell_id = p.open_shell()
    command_id = p.run_command(shell_id, cmd)
    std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)
    #s = winrm.Session('<WinRM-Server>.<domain-name>', auth=HTTPBasicAuth('<Organization>\<User>', '<password>'))
    #r = s.run_ps( cmd )
    print( p.std_out )

    #wsman = WSMan(pshSvr, ssl=False, auth="basic", encryption="never", username=account, password=password)
    #with wsman, WinRS(wsman) as shell:
        #process = Process(shell, "powershell", [cmd0 + cmd1])
    #with Client(pshSvr, username=account, password=password) as client:
    #    stdout, stderr, rc = client.execute_cmd("powershell.exe " + cmd0 + cmd1 )

    return r.std_out

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
