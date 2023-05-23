#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
decom-jirafacts() deletes the jira.yaml and ldap.yaml of given servername.


## Usage
curl -H "Content-Type application/json" -X POST http://decom-jirafacts-functions.apps.<k8s-cluster>.<domain-name>/decomJirafacts -d '{"fq_hostname":"<LPAR>004.<domain-name>"}'


Required secrets:
 - sshaccount
 - sshpassword
 

## Required Inputs
 - fq_hostname


## Output
 - 0 or 1


## Limitations
Caller must have a clear network path to apps.<cluster>.<domain-name>


## Release Notes
v1. Initial Release
