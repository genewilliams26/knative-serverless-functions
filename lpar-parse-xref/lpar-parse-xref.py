import os
import sys
import json
import requests
import csv
from scp import SCPClient
import paramiko

account = '<User>'
password = '<password>'

def createSSHClient(server, port, user, pw):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, pw)
    return client

json_req = json.loads( sys.argv[1] )
refenceTablePath = json_req['refenceTablePath']
frame = json_req['frame']
toolkit = "<Toolkit-Server>.<domain-name>"
result = {"output":"error"}

ssh = createSSHClient(toolkit, 22, account, password)
scp = SCPClient(ssh.get_transport())

try:
    scp.get(r'' + refenceTablePath, r'/tmp/reference_table.csv')
finally:
    scp.close()

xref_file = csv.reader(open('/tmp/reference_table.csv', 'r'))
frameinfo = ""
for row in xref_file:
    if frame == row[1]:
        frameinfo = row
result = '{[{"vios":["' + frameinfo[6] + '","' + frameinfo[7] + '"},{"frames":["' + frameinfo[15] + '","' + frameinfo[16] + '","' + frameinfo[17] + '","' + frameinfo[18] + '"}]}'

print( json.dumps(result).strip(' "').rstrip() )
