import json
import os
import requests
from requests.auth import HTTPBasicAuth
import paramiko
from flask import Flask, request

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/parseStgData', methods=['POST'])

def parseStgData():
    # json input
    json_req = request.get_json(force=True)
    mountpoint = json_req['values'][0]['filesystem']
    diskSize = json_req['values'][0]['requestedsize']['value']
    owner = json_req['values'][0]['owner']
    filesystemType = str( json_req['values'][0]['id'] )
    
    if mountpoint == "" or diskSize == "":
        arrayEmpty = "true"
    else:
        arrayEmpty = "false"
    
    result = '{"mountpoint":"' + mountpoint + '","diskSize":"' + diskSize + '","owner":"' + owner + '","filesystemType":"' + filesystemType + '","arrayEmpty":"' + arrayEmpty + '"}'

    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
