## vmware-get-portgroup v1.0.8

#### Table of Contents

1. [Description](#description)
1. [Requirements](#requirements)
1. [Usage](#usage)
1. [Example](#example)
1. [Reference](#reference)
1. [Variables](#variables)
1. [Release Notes](#releasenotes)

## Description <a name="description"></a>

This function will return the port group on the virtual distributed switch from a provided vlan.

It will return a string with a single result, "error: duplicate" if multiple port groups are found, "error: no matches" if there are no port groups found, or "error: unkown" for any other list length.

## Requirements <a name="requirements"></a>

* gunicorn
* Flask
* pyVmomi
* pyVim

## Usage <a name="usage"></a>

This function will be called by orchestration.

## Example <a name="example"></a>

            curl -H "Content-Type application/json" -X POST http://vmware-get-portgroup-functions.apps.<k8s-cluster>.<domain-name>/getPortgroup -d '{"vcenter": "vct1.<domain-name>", "vlan": "440", "cluster": "DCESX01"}'

## Reference <a name="reference"></a>

* https://wiki.<domain-name>/pages/viewpage.action?spaceKey=CIA&title=Create+An+Openshift+Serverless+Function
* https://wiki.<domain-name>/display/CIA/Find+Active+vCenter+Servers

## Variables <a name="variables"></a>

* vcenter - FQDN of the vcenter server. See reference section for more info.
* vlan - Vlan number to get the port group for.
* cluster - ESX host cluster of the vCenter server.

## Release Notes <a name="releasenotes"></a>

Initial release v.1.0.8