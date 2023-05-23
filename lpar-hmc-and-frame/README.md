#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
lpar-hmc-and-frame() retrieves the Frame serial number and HMC info for a given LPAR.


## Usage
curl -H "Content-Type application/json" -X POST http://lpar-hmc-and-frame-functions.apps.<k8s-cluster>.<domain-name>/getLparFrameAndHmc -d '{"lpar":"<LPAR>.<domain-name>"}'



## Input
 - LPAR

 
## Output
 - hmc
 - frame


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
