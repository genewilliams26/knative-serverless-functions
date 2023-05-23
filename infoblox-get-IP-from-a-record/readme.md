## infoblox-get-ip-from-a-record v1.0.2

#### Table of Contents

1. [Description](#description)
1. [Requirements](#requirements)
1. [Usage](#usage)
1. [Example](#example)
1. [Reference](#reference)
1. [Variables](#variables)
1. [Release Notes](#releasenotes)

## Description <a name="description"></a>

This function will return the IP address of an A or Host record. If there are any errors "error: " will be in the front of the error message.

## Requirements <a name="requirements"></a>

* Flask
* requests
* json

## Usage <a name="usage"></a>

This function will be called by orchestration.

## Example <a name="example"></a>

            curl -H "Content-Type application/json" -X POST http://infoblox-get-ip-from-a-record-functions.apps.<k8s-cluster>.<domain-name>/getIpAddress -d '{"fqdn": "<WinRM-Server>.<domain-name>", "infobloxHost": "infoblox.<domain-name>"}'

## Reference <a name="reference"></a>

* https://wiki.<domain-name>/pages/viewpage.action?spaceKey=CIA&title=Create+An+Openshift+Serverless+Function

## Variables <a name="variables"></a>

* fqdn - FQDN to look for in DNS.
* infobloxHost - FQDN of the infoblbox server to connect to.

## Release Notes <a name="releasenotes"></a>

Initial release v1.0.2