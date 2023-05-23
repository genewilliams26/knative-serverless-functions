#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
jira-get-vm-build-date() receives the Jira ticket number of an ITCM VM build request, queries the Jira API for that ticket's data, and filters/formats the necessary JSON for an automated build..


## Usage
curl -H "Content-Type application/json" -X POST http://jira-get-vm-build-data-functions.apps.<k8s-cluster>.<domain-name>/getBuildData -d '{"itcm_num": "ITCM-135555", "jira_fqdn": "jiratest.<domain-name>"}'


## Input
itcm-num - ITCM Jira ticket ID 
jira_fqdn - fully qualified domain name of Jira API



## Output
JSON payload of required fields for an <Organization> VM build


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
