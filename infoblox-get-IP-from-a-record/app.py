from flask import Flask, request
import requests
import json
 
accountsecret = open("/var/secret/sshaccount/sshaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/sshpassword/sshpassword", "r")
password = passwordsecret.readline().strip()

requests.packages.urllib3.disable_warnings() # Disable SSL warnings in requests #

def searchIbx(infobloxHost, recordType, fqdn, account, password):
    url = "https://" + infobloxHost + "/wapi/v2.11.2/record:" + recordType + "?name=" + fqdn.lower()

    return requests.request("GET", url, auth=(account, password), verify=False)

def getAddress(infobloxHost, fqdn, account, password):
    # Set default values to avoid not defined errors.
    result = ""

    # fqdn check.
    if ".com" in fqdn.lower():
        try:
            recordType = "a"

            hostname_result = searchIbx(infobloxHost, recordType, fqdn, account, password)

        # Return any errors returned while trying to connect to the infoblox.
        except Exception as error_message:
            result = "error: " + str(error_message)

            return result

        # Return the status code if not 200.
        if hostname_result.status_code != 200:
            result = str(hostname_result.status_code)
            return result

        # Return error if A record not found. Then look for Host records with the same fqdn.
        if hostname_result.text == "[]":
            recordType = "host"

            hostname_result = searchIbx(infobloxHost, recordType, fqdn, account, password)

            # Return error if A or Host records not found.
            if hostname_result.text == "[]":
                result = "error: " + fqdn + " A or Host record not found."

                return result

            else:
                # Convert the text into json so it's easier to work with.
                hostname_responses = json.loads(hostname_result.text)

                # If more than one A recoreds are found there are duplicates and an error will be returned.
                if len(hostname_responses) > 1:
                    result = "error: multiple A records found for " + fqdn + "."

                    return result
                
                else:
                    # If more than one IP addresses are found an error will be returned.
                    if len(hostname_responses[0]["ipv4addrs"]) > 1:
                        result = "error: multiple IP addresses found in Host record for " + fqdn + "."

                        return result
                    else:

                        result = hostname_responses[0]["ipv4addrs"][0]["ipv4addr"]
                        return result

        else:
            # Convert the text into json so it's easier to work with.
            hostname_responses = json.loads(hostname_result.text)

            # IIf more than one A recoreds are found there are duplicates and an error will be returned.
            if len(hostname_responses) > 1:
                result = "error: multiple A records found for " + fqdn + "."

                return result
            
            else:
                result = hostname_responses[0]["ipv4addr"]
                return result

    else:
        result = "error: must use FQDN format."

        return result

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when colling the function
@app.route('/getIpAddress', methods=['POST'])
def getIpAddress():
    req_data = request.get_json(force=True)

    fqdn = req_data['fqdn']
    infobloxHost = req_data['infobloxHost']

    flask_result = getAddress(infobloxHost, fqdn, account, password)

    return flask_result 

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))