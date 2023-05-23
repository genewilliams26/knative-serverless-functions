#!/bin/bash
curl -X DELETE -k -u '<User>:xxxxxxxxx' -H "Content-Type: text/plain" https://puppetfiles.apps.$cluster.<domain-name>/puppetfiles/v1/delete/$server
