#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
lpar-rootvg-add() determines whether or not a VM exists in the given VCenter


## Usage
curl -H "Content-Type application/json" -X POST http://lpar-rootvg-add-functions.apps.<k8s-cluster>.<domain-name>/lparRootVGadd -d '{"frame": "<Frame>2006"}'


## Input
frame - LPAR's frame


## Output
0 if successful, 1 if not

## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
