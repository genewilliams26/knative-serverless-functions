#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
decom-puppet()  performs  "puppetserver ca clean --certname <fq_hostname>" 


## Usage
curl -H "Content-Type application/json" -X POST http://decom-puppet-functions.apps.<k8s-cluster>.<domain-name>/decomPuppet -d '{"fq_pup_client":"servername.<domain-name>","fq_pup_server":"<IP-Addr>"}'


Required secrets:
 - sshaccount
 - sshpassword
 

## Required Inputs
 - fq_pup_client
 - fq_pup_server


## Output
 - standard out of remote SSH call


## Limitations
Caller must have a clear network path to apps.<cluster>.<domain-name>


## Release Notes
v1. Initial Release
