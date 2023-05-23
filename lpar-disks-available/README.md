#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
lpar-disks-available() queries all VIOs returning a boolean representing whether at least one in scope disk is available and a list of VIOs having free disk available along with their corresponding list of disks.


## Usage
curl -H "Content-Type application/json" -X POST http://lpar-disks-available-functions.apps.<k8s-cluster>.<domain-name>/lparDisksAvailable -d '{"vios":[],"frames":["<Frame>6003"],"hmc":""}'



## Input
 - vios[]
 - frames[]
 - hmc


## Output
 - boolean disksAvailable 
 - string freeDisks


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
