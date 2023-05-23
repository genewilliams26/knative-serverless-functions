## vmware-get-template v1.0.33

#### Table of Contents

1. [Description](#description)
1. [Requirements](#requirements)
1. [Usage](#usage)
1. [Example](#example)
1. [Reference](#reference)
1. [Variables](#variables)
1. [Release Notes](#releasenotes)

## Description <a name="description"></a>

This function will return the VMWare template that matches the OS provided. It will not return backup templates. It will return ERROR if no templates are found or if there are duplicates found.

## Requirements <a name="requirements"></a>

* gunicorn
* Flask
* requests
* pyVmomi
* pyVim

## Usage <a name="usage"></a>

This function will be called by orchestration.

## Example <a name="example"></a>

            curl -H "Content-Type application/json" -X POST http://vmware-get-template-functions.apps.<k8s-cluster>.<domain-name>/getTemplate -d '{"vcenter": "vct1.<domain-name>", "OS": "2019", "domain": "org", "cluster": "<ESX-Cluster"}'

## Reference <a name="reference"></a>

* https://wiki.<domain-name>/pages/viewpage.action?spaceKey=CIA&title=Create+An+Openshift+Serverless+Function
* https://wiki.<domain-name>/display/CIA/Find+Active+vCenter+Servers

## Variables <a name="variables"></a>

* vcenter - FQDN of the vcenter server. See reference section for more info.
* OS - Operating system of the template to get.
* domain - org, orgBdev, etc. To detime if the template for the BES domains should be returned.
* cluster - ESX cluster.

## Release Notes <a name="releasenotes"></a>

* v1.0.19 - - Initial release.
* v1.0.20 - 5/5/2022 - Account for cluster being added to template name.
* v1.0.33 - 5/12/2022 - Remove BES check from template. BES 2019 templates are being used everywhere. Also removed option for any cluster other than ems or esx.