## vmware-get-datastore v1.0.3

#### Table of Contents

1. [Description](#description)
1. [Requirements](#requirements)
1. [Usage](#usage)
1. [Example](#example)
1. [Reference](#reference)
1. [Variables](#variables)
1. [Release Notes](#releasenotes)

## Description <a name="description"></a>

This function will return the datastore cluster that is available to the ESXi server based on the host cluster the ESXi server is a member of.

It will return a JSON string with a single result, error for duplicates or, error for no datstore clusters found.

## Requirements <a name="requirements"></a>

* gunicorn
* Flask
* pyVmomi
* pyVim

## Usage <a name="usage"></a>

This function will be called by orchestration.

## Example <a name="example"></a>

            curl -H "Content-Type application/json" -X POST http://vmware-get-datastore-functions.apps.<k8s-cluster>.<domain-name>/getDatastore -d '{"vcenter": "vct1.<domain-name>", "hostName": "<Server-Name>"}'

## Reference <a name="reference"></a>

* https://wiki.<domain-name>/pages/viewpage.action?spaceKey=CIA&title=Create+An+Openshift+Serverless+Function
* https://wiki.<domain-name>/display/CIA/Find+Active+vCenter+Servers

## Variables <a name="variables"></a>

* vcenter - FQDN of the vcenter server. See reference section for more info.
* hostName - ESXi server name.

## Release Notes <a name="releasenotes"></a>

Initial release v.1.0.3