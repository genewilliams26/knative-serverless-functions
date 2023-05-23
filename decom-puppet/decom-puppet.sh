#!/bin/bash
tstamp=`date --iso-8601=seconds`

# deactivate cert
curl -X POST --tlsv1 --cacert /etc/puppetlabs/puppet/ssl/certs/ca.pem --cert /etc/puppetlabs/puppet/ssl/certs/${node}.pem --key /etc/puppetlabs/puppet/ssl/private_keys/${node}.pem \
  -H "Accept: application/json" -H "Content-Type: application/json" -d "{\"command\":\"deactivate node\",\"version\":3,\"payload\":{\"certname\":\"${node}\",\"producer_timestamp\":\"${tstamp}\"}}" \
  https://puppet.<domain-name>:8081/pdb/cmd/v1

# delete cert ('clean')
curl -X DELETE --tlsv1 --cacert /etc/puppetlabs/puppet/ssl/certs/ca.pem --cert /etc/puppetlabs/puppet/ssl/certs/${node}.pem \
  --key /etc/puppetlabs/puppet/ssl/private_keys/${node}.pem -H "Accept: application/json" https://puppet.<domain-name>:8140/puppet-ca/v1/certificate_status/${node}
