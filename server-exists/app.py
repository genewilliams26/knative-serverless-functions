import sys
import os
import json
import paramiko
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
from flask import Flask, request

def fetch(session, vsvr_host, vsvr):
    if vsvr_host[0:1] == 's':
        base_url = "http://lpar-exists-functions.apps.<k8s-cluster>.<domain-name>/lparExists"
        payload = '{"hmc":"' + vsvr_host + '","lpar":"' + vsvr + '"}'
    else:
        base_url = "http://vm-exists-functions.apps.<k8s-cluster>.<domain-name>/vmExists"
        payload = '{"vcenter":"' + vsvr_host + '","vm_target":"' + vsvr + '"}'
    with session.post(base_url, data=payload) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(base_url))
            print('   ' + data)
        return data

async def get_data_asynchronous():
    vsvr_host_list = [
        'vct1.<domain-name>',
        'vcb1.<domain-name>',
        'vct3.<domain-name>',
        '<HMC-Server>7001.<domain-name>',
        '<HMC-Server>5001.<domain-name>',
        '<HMC-Server>3001.<domain-name>',
        '<HMC-Server>3001.<domain-name>'
    ]
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            print( "vsvr_host: " + vsvr_host + "   svr: " + svr )
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, vsvr_host, svr)
                )
                for vsvr_host in vsvr_host_list
            ]
            for response in await asyncio.gather(*tasks):
                pass

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/serverExists', methods=['POST'])

def serverExists():
    json_req = request.get_json(force=True)
    svr = json_req['svr']

    result = "false"
    r = os.system("ping -c 1 " + svr + ".<domain-name> > /dev/null 2>&1")
    if r == 0:
        print( "true" )
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(get_data_asynchronous())
        if future == "true":
            result = "true"
        loop.run_until_complete(future)
        print( result )

    return rtn

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
