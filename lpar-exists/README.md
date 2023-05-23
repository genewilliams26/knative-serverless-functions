#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
lpar-exists() determines whether or not a LPAR exists under the given HMC


## Usage
curl -H "Content-Type application/json" -X POST http://lpar-exists-functions.apps.<k8s-cluster>.<domain-name>/lparExists -d '{"hmc": "<HMC-Server>7001.<domain-name>","lpar":"<Toolkit-Server>"}'


## Input
hmc - fully qualified HMC name
lpar - name of LPAR to determine



## Output
A lower case string that represents a boolean - if "true", the LPAR exists, else "false"


## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
