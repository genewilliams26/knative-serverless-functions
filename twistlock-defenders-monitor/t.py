import os
import re
import sys
import json

file = open( '/etc/resolv.conf', 'r')
for line in file:
    if re.search( 'k8s\.<domain-name>', line ):
        pattern = r'(^.*?)(..)(k8s\.<domain-name>.*$)'
        replacement = r'\2'
        cluster_indicator = re.sub( pattern, replacement, line ).replace("\n", "")
        if cluster_indicator == 'ev' or cluster_indicator == 'st' or cluster_indicator == 'ms':
            console_cluster = '<k8s-cluster>'
            expected_defenders = 18
        elif cluster_indicator == 'pt' or cluster_indicator == 'pb':
            console_cluster = cluster_indicator + 'k8s'
            expected_defenders = 6
        else:
            console_cluster = cluster_indicator + 'k8s'
            expected_defenders = 3



