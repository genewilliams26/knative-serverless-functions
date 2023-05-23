#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
twistlock-defenders-monitor() determines if any Twistlock Defender agents are down


## Usage
curl -H "Content-Type application/json" -X POST http://twistlock-defenders-monitor-functions.apps.<k8s-cluster>.<domain-name>/checkDefenders


## Input
No inputs


## Output
"200" if all defenders are up, or a list of clusters with defenders not responding

## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
