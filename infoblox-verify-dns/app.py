import os
from flask import Flask, request
import requests
import json
 
accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

requests.packages.urllib3.disable_warnings() # Disable SSL warnings in requests #

def confirmDNS(fqdn, IPAddress, account, password):
    # Set variables to global to allow use accross the function
    global result
    global pushIP
    global pushDNS
    global ip_ddress
    global hostname
    global ptr_address
    global a_address

    # Set default values to avoid not defined errors.
    result = {}
    ip_address = ""
    hostname = ""
    pushIP = ""
    pushDNS = ""
    ptr_address = ""
    a_address = ""

    # fqdn check.
    if fqdn.lower().find(".com") != -1:
        try:
            url = "https://infoblox.<domain-name>/wapi/v2.11.2/record:a?name=" + fqdn.lower()

            hostname_result = requests.request("GET", url, auth=(account, password), verify=False)

        except Exception as error_message:
            result["status"] = error_message

            return result

        if hostname_result.status_code != 200:
            result["status"] = str(hostname_result.status_code)
            return result

        # Return True if A record not found.
        if hostname_result.text == "[]":
            pushDNS = True
        else:
            # Convert the text into json.
            hostname_responses = json.loads(hostname_result.text)

            # If more than one result is found there are duplicates and we will return hostname with thee last duplicate.
            if len(hostname_responses) > 1:
                for hostname_response in hostname_responses:
                    if hostname_response["name"] != fqdn.lower() or hostname_response["ipv4addr"] != IPAddress:
                        result["status"] = "failDNS"

            # For a single record found, ensure it matches the input data.
            else:
                for hostname_response in hostname_responses:
                    if hostname_response["name"] != fqdn.lower() and hostname_response["ipv4addr"] != IPAddress:
                        result["status"] = "failDNS"
                    elif hostname_response["name"] == fqdn.lower() and hostname_response["ipv4addr"] == IPAddress:
                        hostname = True
                    elif hostname_response["name"] == fqdn.lower() and hostname_response["ipv4addr"] != IPAddress:
                        result["status"] = "failDNS"

        # IP address check.
        try:
            url = "https://infoblox.<domain-name>/wapi/v2.11.2/search?address=" + IPAddress

            IPAddress_result = requests.request("GET", url, auth=(account, password), verify=False)

        except Exception as error_message:
            result["status"] = error_message

            return result

        if IPAddress_result.status_code != 200:
            result["status"] = str(IPAddress_result.status_code)

            return result

        # Return True if IP Address not found.
        if IPAddress_result.text == "[]":
            pushIP = True
        else:
            # Convert the text into json.
            IPAddress_responses = json.loads(IPAddress_result.text)

            # If more than one result is found there are duplicates and we will return IPddress with a value.
            if len(IPAddress_responses) > 2:
                result["status"] = "failDNS"

            else:
                # For a single record found, ensure it matches the input data. IP search returns A and PTR records.
                for IPAddress_response in IPAddress_responses:
                    if IPAddress_response["_ref"].find("record:ptr/") != -1:
                        # Return True if IP address is not in use or the name and IP of the duplicate.
                        ptr_ip = IPAddress_response["_ref"].split(":")[2].replace(".in-addr.arpa/default","").split(".")

                        ip_final = ptr_ip[3] + "." + ptr_ip[2] + "." + ptr_ip[1] + "." + ptr_ip[0]

                        if ip_final != IPAddress or IPAddress_response["ptrdname"] != fqdn.lower():
                            result["status"] = "failDNS"
                        elif ip_final == IPAddress and IPAddress_response["ptrdname"] == fqdn.lower():
                            ptr_address = True

                    elif IPAddress_response["_ref"].find("record:a/") != -1:
                        if IPAddress_response["ipv4addr"] != IPAddress or IPAddress_response["name"] != fqdn.lower():
                            result["status"] = "failDNS"
                        elif IPAddress_response["ipv4addr"] == IPAddress and IPAddress_response["name"] == fqdn.lower():
                            a_address = True

        if ptr_address == True and a_address == True:
            ip_address = True

        # If the IP and hostnames checks both result to True then return passDNS.
        if ip_address == True and hostname == True and len(result) == 0:
            result["status"] = "passDns"

            return result

        # If there are no matches for the A record or IP address then return pushDNS.
        elif pushIP == True and pushDNS == True and len(result) == 0:
            result["status"] = "pushDNS"

            return result

        # Return the results of the issues found with IP or DNS name.
        else:
            return result

    else:
        #result = "Hostname must be in FQDN format."
        result["status"] = "failDNS"

        return result

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when colling the function
@app.route('/verifyDns', methods=['POST'])
def verifyDns():
    req_data = request.get_json(force=True)

    fqdn = req_data['fqdn']
    IPAddress = req_data['IPAddress']

    flask_result = confirmDNS(fqdn, IPAddress, account, password)

    return flask_result 

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))