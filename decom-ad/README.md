#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
decom-ad() deletes the computer object and AD group (if unique) for server being decommissioned.


## Usage
curl -H "Content-Type application/json" -X POST http://decom-ad-functions.apps.<k8s-cluster>.<domain-name>/decomJirafacts -d '{"ad_group":"<VM> Admins", "server_name":"<VM>.<domain-name>"}'


Required secrets:
 - vmwareaccount
 - vmwarepassword
 

## Required Inputs
 - ad_goup
 - server_name


## Output
 - 0 or 1


## Limitations
Caller must have a clear network path to apps.<cluster>.<domain-name>


## Release Notes
v1. Initial Release
