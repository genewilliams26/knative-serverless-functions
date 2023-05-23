#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
mem-check-availability() checks for availability of sufficient Memory for LPAR creation.


## Usage
curl -H "Content-Type application/json" -X POST http://mem-check-availability-functions.apps.<k8s-cluster>.<domain-name>/checkMemAvailability -d '{"hmc":"<HMC-Server>7001.<domain-name>","frame":"<Frame>6003","memory":"64"}'



## Input
 - frame
 - hmc
 - memory


## Output
a boolean, 'true' meaning there is enough Memory for the specified values


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
