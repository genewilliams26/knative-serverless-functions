## infoblox-get-next-ip v1.0.1

#### Table of Contents

1. [Description](#description)
1. [Requirements](#requirements)
1. [Usage](#usage)
1. [Example](#example)
1. [Reference](#reference)
1. [Variables](#variables)
1. [Release Notes](#releasenotes)

## Description <a name="description"></a>

This fuction will return the next available IP if there are no errors. If there are errors, it will return an error message indicating what the failure is. The network team requires IP's .0 - .20 and .250 - .255 to be reserved for their use. These IP's will not be returned.

## Requirements <a name="requirements"></a>

* os
* Flask
* requests
* json
* ipaddress

## Usage <a name="usage"></a>

This function will be called by orchestration.

## Example <a name="example"></a>

            curl -H "Content-Type application/json" -X POST http://infoblox-get-next-ip-functions.apps.<k8s-cluster>.<domain-name>/getNextIp -d '{"infobloxHost": "infoblox.<domain-name>", "subnet": "<IP-Addr>/22"}'

## Reference <a name="reference"></a>

* https://wiki.<domain-name>/pages/viewpage.action?spaceKey=CIA&title=Create+An+Openshift+Serverless+Function

## Variables <a name="variables"></a>

* subnet = The network, in CIDR notation, where the next available IP will be retrieved.
* infobloxHost = The FQDN of the Infoblox host to connect to.

## Release Notes <a name="releasenotes"></a>

Initial release v1.0.1