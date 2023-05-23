#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
decom-dns() removes A, PTR, and Host records for the received fully qualified hostname and IP address.


## Usage
curl -H "Content-Type application/json" -X POST http://decom-dns-functions.apps.<k8s-cluster>.<domain-name>/decomDNS -d '{"fq_hostname":"<LPAR>004.<domain-name>","ip_addr":"<IP-Addr>"}'


Required secrets:
 - sshaccount
 - sshpassword
 

## Required Inputs
 - fq_hostname
 - ip_addr


## Output
 - 'Success' or 'Failure'  


## Limitations
Caller must have a clear network path to apps.<cluster>.<domain-name>


## Release Notes
v1. Initial Release
