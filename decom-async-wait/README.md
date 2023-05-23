#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
decom-async-wait()  waits for a specified time for asynchronous decom tasks to complete

## Usage
curl -H "Content-Type application/json" -X POST http://decom-async-wait-functions.apps.<k8s-cluster>.<domain-name>/validateTasks -d '{"server_name":"<VM>.<domain-name>"}'


## Input



## Output
Boolean RC 


## Limitations
Caller must have a clear network path to the cluster


## Release Notes
v1. Initial Release
