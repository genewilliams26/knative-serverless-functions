#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
vm-exists() determines whether or not a VM exists in the given VCenter


## Usage
curl -H "Content-Type application/json" -X POST http://vm-exists-functions.apps.<k8s-cluster>.<domain-name>/vmExists -d '{"vcenter": "vct1.<domain-name>","target_vm":"<Server-Name>"}'


## Input
vcenter - fully qualified vcenter name
vm_target - name of VM to determine



## Output
A lower case string that represents a boolean - if "true", the VM exists, else "false"


## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
