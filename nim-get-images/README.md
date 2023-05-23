#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
nim-get-images() retrieves the Frame Type value from the HMC server for LPAR creation/modification.


## Usage
curl -H "Content-Type application/json" -X POST http://nim-get-images-functions.apps.<k8s-cluster>.<domain-name>/getNimImages -d '{"NIMhostname":"<NIM-Server>16.<domain-name>","OS":"AIX 7.1.1"}'



## Input
 - NIMhostname
 - OS


## Output
 - mksysb 
 - spot
 - bosinst


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
