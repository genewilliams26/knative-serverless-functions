#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
decom-ad() deletes the given VM from VMware


## Usage
curl -H "Content-Type application/json" -X POST http://decom-vm-functions.apps.<k8s-cluster>.<domain-name>/decomVM -d '{"server_name":"<VM>.<domain-name>"}'


Required secrets:
 - vmwareaccount
 - vmwarepassword
 

## Required Inputs
 - server_name


## Output
 - 0 or 1


## Limitations
Caller must have a clear network path to apps.<cluster>.<domain-name>


## Release Notes
v1. Initial Release
