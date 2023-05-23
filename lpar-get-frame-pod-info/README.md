#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
lpar-get-frame-pod-info() determines whether or not a VM exists in the given VCenter


## Usage
curl -H "Content-Type application/json" -d '{"frame": "<Frame>6001"}' -X POST http://lpar-get-frame-pod-info-functions.apps.<k8s-cluster>.<domain-name>/getFramePodInfo 


## Input
frame - name of the frame


## Output
wfaSVM, wfaArray, and FRAMEvioServers in JSON format

## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
