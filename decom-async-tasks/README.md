#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
decom-async-tasks() decommissions several attributes of a server simultaneously: VM/LPAR, DNS, AD, Puppet, SCCM/Satellite, JiraFacts.
NOTE: this function is designed to be called by the Jenkins pipeline, decom-server-pipeline, which does NOT include a controlled timeout or grace period for server decommission.

## Usage
curl -H "Content-Type application/json" -X POST http://decom-async-tasks-functions.apps.<k8s-cluster>.<domain-name>/vmExists -d '{"target_server":"<VM>.<domain-name>"}'


## Input
target_server - Fully qualified name of the server to decommission



## Output
Boolean RC 


## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
