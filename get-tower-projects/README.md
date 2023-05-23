#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
get-tower-project() retrieves the retrieves the projects currently in an Ansible Tower instance and the corresponding organization for that project


## Usage
curl -H "Content-Type application/json" -X POST http://get-tower-projects-functions.apps.<k8s-cluster>.<domain-name>/getTowerProjects -d '{"tower": "http://<VM>0030.<domain-name>"}'



## Input
 - tower 


## Output
 - Project
 - organization name


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release