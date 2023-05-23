#### Table of Contents

1. [Description](#description)
2. [Usage - How to call this function](#usage)
3. [Input](#input)
4. [Output](#output)
5. [Limitations - OS compatibilty](#limitations)
6. [Release Notes](#release_notes)


## Description
get-k8s-secret() returns the password of the given secret name.


## Usage
curl -H "Content-Type application/json" -X POST http://get-k8s-secret-functions.apps.<k8s-cluster>.<domain-name>/getK8sSecret -d '{"account":"<User>"}'


Required secrets:
 - sshpassword
 - vmwarepassword
 

## Required Inputs
 - account


## Output
 - associated secret


## Limitations
Caller must have a clear network path to apps.<cluster>.<domain-name>


## Release Notes
v1. Initial Release
