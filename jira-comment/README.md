#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
jira-transition() currently only transitions Jira ITCM server build issues


## Usage
curl -H "Content-Type application/json" -X POST http://jira-transition-functions.apps.<k8s-cluster>.<domain-name>/jiraTansition -d '{"itcm_num": "ITCM-155263", "jira_fqdn": "jiratest.<domain-name>", "desired_state":"success"}'


## Input
itcm-num - ITCM Jira ticket ID 
jira_fqdn - fully qualified domain name of Jira API
desired_state - either "success" or "failure"


## Output
either {"response":"successful"} or {"response": <error from function and jira>}


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
