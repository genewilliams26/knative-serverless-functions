#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
parse-storage-data() receives and parses the storage table from an ITCM Jira ticket, returning a JSON payload containing mountpoint, diskSize, owner, and filesystemType.


## Usage
curl -H "Content-Type application/json" -X POST http://parse-storage-data-functions.apps.<k8s-cluster>.<domain-name>/parseStgData -d '{"startAt":0,"maxResults":10,"total":1,"values":[{"owner":"serviceaccount","requestedsize":{"name":"32","value":"32"},"issueId":433990,"lun":null,"numberofdevices":1.0,"modified":1,"id":331409,"requestedchange":32.0,"filesystem":"/app"}]}


## Input
JSON payload consisting of a full response from an ITCM Jira Idalko stoge table like the one shown above in 'Usage'


## Output
a simplified presentation of 4 key elements from the input: mountpoint, diskSize, owner, and filesystemType, in the form of a single JSON payload


## Limitations
Caller must have a clear network path to apps.<k8s-cluster>.<domain-name>


## Release Notes
v1. Initial Release
