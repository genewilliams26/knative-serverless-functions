#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
jira-get-vm-decom-data() receives the Jira ticket number of an ITCM VM decom request, queries the Jira API for that ticket's data, and filters/formats the necessary JSON for an automated decom..


## Usage
curl -H "Content-Type application/json" -X POST http://jira-get-vm-decom-data-functions.apps.<k8s-cluster>.<domain-name>/getDecomdData -d '{"ITCMNum": "ITCM-130580", "jiraUrl": "jiratest.<domain-name>"}'


## Input
ITCMNum - ITCM Jira ticket ID 
jiraUrl - fully qualified domain name of Jira API



## Output
JSON format:
   - hostName (ensure lowercase)
   - functionalEnvironment

## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
