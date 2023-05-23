#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
lpar-parse-xref() returns all info from the LPAR XREF table for a given frame


## Usage
curl -H "Content-Type application/json" -X POST http://lpar-parse-xref-functions.apps.<k8s-cluster>.<domain-name>/lparParseXref -d '{"refenceTablePath": "/app/toolkit/power_systems_xref_table.csv", "frame": "<Frame>2001"}'


## Input
hmc - fully qualified HMC name
lpar - name of LPAR to determine



## Output
A lower case string that represents a boolean - if "true", the LPAR parse-xref, else "false"


## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
