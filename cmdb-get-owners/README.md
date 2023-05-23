#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
cmdb-get-owners() gets dev and IT Ops owners from CMDB, given the Environment and the Business Application.


## Usage
curl -H "Content-Type application/json" -X POST http://cmdb-get-owners-functions.apps.<k8s-cluster>.<domain-name>/cmdbGetOwners -d '{"environment":"dev","businessApp":"XXX"}'


Required secrets:
 - cmdbapiaccount
 - cmdbapipw
 - k8senv
 

## Required Inputs
 - environment
 - businessApp


## Output
 - {"owner":"user"} 


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
