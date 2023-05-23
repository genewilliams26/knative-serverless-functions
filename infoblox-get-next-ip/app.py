import os
from flask import Flask, request
import requests
import json
import ipaddress

accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

requests.packages.urllib3.disable_warnings() # Disable SSL warnings in requests #

# Get vim objects of a given type.
def NextIp(infobloxHost, subnet, name, passw):
    # Set default values to avoid not defined errors.
    result = ""

    # Ensure the subnet does not have any host bits set.
    try:
        ipaddress.ip_network(subnet, strict=True)
    except ValueError as error:
        result = "ERROR: " + error

        return result

    # infobloxHost FQDN check.
    if infobloxHost.lower().find(".com") != -1:
        try:
            subnet_url = "https://" + infobloxHost + "/wapi/v1.2/network?network=" + subnet

            subnet_result = requests.request("GET", subnet_url, auth=(name, passw), verify=False)

            if subnet_result.text == '[]':
                result = "ERROR: " + subnet + " Network not found on " + infobloxHost + "."

                return result
        except:
            result = "ERROR: Failed to connect with URL " + subnet_url + "."

            return result

        # Change the subnet_result text to json so it's easier to work with.
        subnet_responses = json.loads(subnet_result.text)

        if len(subnet_responses) > 1:
            result = "ERROR: Duplicate Networks returned"

            return result
        else:
            for subnet_response in subnet_responses:
                # Get the network id from the _ref.
                try:
                    nextIp_url = "https://" + infobloxHost + "/wapi/v1.2/" + subnet_response["_ref"] + "?_function=next_available_ip"

                    # Split subnet to get the first 3 octects from the subnet to build the excluded list.
                    subnet_split = subnet.split(".")

                    excludIps = []

                    # create list of IP's to use in request. Network team requires IP's .0 - .20 and .250 - .255 to be reserved.
                    for n in range(0,21):
                        excludIps.append(str(subnet_split[0]) + "." + str(subnet_split[1]) + "." + str(subnet_split[2]) + "." + str(n))

                    for n in range(250,256):
                        excludIps.append(str(subnet_split[0]) + "." + str(subnet_split[1]) + "." + str(subnet_split[2]) + "." + str(n))

                    nextIp_result = requests.request("POST", nextIp_url, auth=(name, passw), verify=False, data=json.dumps({"exclude":excludIps}))

                    if nextIp_result.status_code != 200:
                        result = "ERROR: " + str(nextIp_result.status_code) + " " + json.loads(nextIp_result.text)["text"]

                        return result
                except:
                    result = "ERROR: Failed to connect with URL " + subnet_url + "."

                    return result

                # Change the nextIp_result text to json so it's easier to work with.
                nextIp_responses = json.loads(nextIp_result.text)

                if len(nextIp_responses["ips"]) > 1:
                    result = "ERROR: Duplicate IP returned"

                    return result
                else:
                    result = nextIp_responses["ips"][0]

                    return result

    else:
        result = "ERROR: infobloxHost must be in FQDN format."

        return result

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when colling the function
@app.route('/getNextIp', methods=['POST'])

def getNextIp():
    req_data = request.get_json(force=True)

    infobloxHost = req_data['infobloxHost']
    subnet = req_data['subnet']

    flask_result = NextIp(infobloxHost, subnet, account, password)

    return flask_result 

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))