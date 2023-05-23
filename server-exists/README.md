#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
server-exists() determines whether or not a server exists at <Organization>


## Usage
curl -H "Content-Type application/json" -X POST http://server-exists-functions.apps.<k8s-cluster>.<domain-name>/serverExists -d '{"hmc": "<HMC-Server>7001.<domain-name>","server":"<Toolkit-Server>"}'


## Input
hmc - fully qualified HMC name
server - name of server to check



## Output
A lower case string that represents a boolean - if "true", the LPAR exists, else "false"


## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
