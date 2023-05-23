#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)

## Description
The get-hmc-from-lpar function derives the Harware Management Console name and IP Address from the client LPAR.  


## Usage
curl -H "Content-Type application/json" -X POST http://get-hmc-from-lpar-functions.apps.<k8s-cluster>.<domain-name>/getHMCfromLPAR -d '{"lpar": "<LPAR>.<domain-name>"}'


## Requirements
This function requires the use of secrets and the following secrets must be supplied
serviceaccount - the account used for orchestration tasks
accountpassword - the password for the service account

## Limitaions
This function runs agains the IBM AIX LPARs

## Release Notes
v1. Initial Release of function
