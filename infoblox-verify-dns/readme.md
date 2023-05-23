## infoblox-verify-dns v1.0.14

#### Table of Contents

1. [Description](#description)
1. [Requirements](#requirements)
1. [Usage](#usage)
1. [Example](#example)
1. [Reference](#reference)
1. [Variables](#variables)
1. [Release Notes](#releasenotes)

## Description <a name="description"></a>

This function will return status JSON strings that indicate failDNS, passDNS, and pushDNS. PassDNS means the DNS name and IP are found in DNS. PushDNS means the DNS name and IP were not found in DNS. FailDNS means there are duplictates of the DNS name, IP, or both. FailDNS will all be returned if the either the name or the IP combination don't match what's provided for a record that is found. Exception may also be returned as status.

## Requirements <a name="requirements"></a>

* os
* Flask
* requests
* json

## Usage <a name="usage"></a>

This function will be called by orchestration.

## Example <a name="example"></a>

            curl -H "Content-Type application/json" -X POST http://infoblox-verify-dns-functions.apps.<k8s-cluster>.<domain-name>/verifyDns -d '{"fqdn": "<VM>.<domain-name>", "IPAddress": "<IP-Addr>"}'

## Reference <a name="reference"></a>

* https://wiki.<domain-name>/pages/viewpage.action?spaceKey=CIA&title=Create+An+Openshift+Serverless+Function

## Variables <a name="variables"></a>

* fqdn - FQDN to look for in DNS.
* IPaddress - IP address to look for in DNS.

## Release Notes <a name="releasenotes"></a>

Initial release v1.0.14