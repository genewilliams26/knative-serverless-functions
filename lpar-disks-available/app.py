import os
import sys
import ssl
import json
import requests
import paramiko
import collections
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
@app.route('/lparDisksAvailable', methods=['POST'])

def lparDisksAvailable():
    result = {"output": "error"}
    json_req = request.get_json(force=True)
    vios = json_req["vios"]
    frames = json_req["frames"]
    hmc = json_req["hmc"]
    vioinfo = []
    unusedserials = []
    for frame in frames:
        x = frames.index(frame)
        vio1 = ((x + 1) * 2) - 2
        vio2 = ((x + 1) * 2) - 1
        vionums = [vio1, vio2]

        for i in vionums:
            availdiskscommand = "viosvrcmd -m " + frame + " -p " + vios[i] + " -c \'lsdev -type disk\' | grep hdisk | grep -v SAS | grep -v Defined"
            lsvpdcommand =  "viosvrcmd -m " + frame + " -p " + vios[i] + " -c \'lsdev -vpd\' | grep -A 7 hdisk"
            lsmapcommand = "viosvrcmd -m " + frame + " -p " + vios[i] + " -c \'lsmap -all\' | grep Backing"
            availout = ""
            lsvpdout = ""
            lsmapout = ""

            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=hmc, username=account, password=password, port="22")

                stdin, stdout, stderr = client.exec_command(availdiskscommand)
                availout = stdout.read().decode('ascii').split('\n')

            finally:
                client.close()

            try:
                client2 = paramiko.SSHClient()
                client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client2.connect(hostname=hmc, username=account, password=password, port="22")

                stdina, stdouta, stderra = client2.exec_command(lsvpdcommand)
                lsvpdout = stdouta.read().decode('ascii')

            finally:
                client2.close()

            try:
                client3 = paramiko.SSHClient()
                client3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client3.connect(hostname=hmc, username=account, password=password, port="22")

                stdina, stdouta, stderra = client3.exec_command(lsmapcommand)
                lsmapout = stdouta.read().decode('ascii').split('\n')

            finally:
                client3.close()

            availout = filter(None, availout)
            availabledisks = []
            for x in availout:
                if x != "" or x != None:
                    availabledisks.append(x.split()[0])

            lsvpd = lsvpdout.split('\n\n')
            newlsvpd = []
            for thing in lsvpd:
                if "hdisk" in thing:
                    f = lsvpd.index(thing)
                    serial = ""
                    if lsvpd[f + 1] != "" or lsvpd != None:
                        serial = lsvpd[f + 1].split('\n')[3]
                        newlsvpd.append(lsvpd[f].split()[0] + " " + serial.split('.')[-1])

            lsmapout = filter(None, lsmapout)
            lsmap = []
            for backed in lsmapout:
                if backed != "" or x != None:
                    lsmap.append(backed.split()[2])

            freeserials = []
            for disk in availabledisks:
                if disk not in lsmap:
                    for ds in newlsvpd:
                        if disk == ds.split()[0]:
                            freeserials.append(ds.split()[1])
                            unusedserials.append(ds.split()[1])
            vio = {"name": vios[i], "freedisks": freeserials}
            vioinfo.append( vio )
    counter = collections.Counter(unusedserials)
    unused = []
    for serial in counter:
        c = counter[serial]
        if int(c) >= len(vios):
            unused.append(serial)
    disksavailable = "false"
    if len(unused) >= 1:
        disksavailable = "true"
    result = {"disksAvailable": disksavailable}
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
