#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
get-frame-type() retrieves the Frame Type value from the HMC server for LPAR creation/modification.


## Usage
curl -H "Content-Type application/json" -X POST http://get-frame-atype-functions.apps.<k8s-cluster>.<domain-name>/getFrameType -d '{"hmc":"<HMC-Server>7001.<domain-name>","frame":"<Frame>6003"}'



## Input
 - hmc
 - frame


## Output
 - frameType 
 - IOType


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
