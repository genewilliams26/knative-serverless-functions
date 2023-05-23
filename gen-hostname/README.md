#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
gen-hostname() generates a hostname verified to be unique in the given vcenter.


## Usage
curl -H "Content-Type application/json" -X POST http://gen-hostname-functions.apps.<k8s-cluster>.<domain-name>/getUniqueHostname -d '{"vcenter": "vct1.<domain-name>"}'


## Input
vcenter - fully qualified vcenter name



## Output
the generated hostname, a single string (not JSON) 


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
