#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
run-powershell() runs a remote poweershell command


## Usage
curl -H "Content-Type application/json" -X POST http://run-powershell-functions.apps.<k8s-cluster>.<domain-name>/vmExists -d '{"target": "<WinRM-Server>.<domain-name>","cmd":"hostname;pwd"}'


## Input
target - Fully qualified server name
cmd - Command to run remotely



## Output
Standard out, standard error from powershell command


## Limitations
Caller must have a clear network path to the cluster, and access granted to run remote powershell on the target


## Release Notes
v1. Initial Release
