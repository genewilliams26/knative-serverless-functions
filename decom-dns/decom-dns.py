import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

fq_hostname = "<LPAR>004.<domain-name>"
ipv4addr = "<IP-Addr>"

account = '<User>'
password = '<password>'

header = "Content-Type:application/json"
url_base = "https://tgrid.<domain-name>/wapi/v2.1"
a_record_get = '/record:a?name='
ptr_record_get = '/record:ptr?ipv4addr='

response = requests.get( url_base + a_record_get + fq_hostname, auth=(account, password), verify=False )
s = str( response.json() ).split()[1]
a_record_id = s[1:len(s)-2]

response = requests.get( url_base + ptr_record_get + ipv4addr, auth=(account, password), verify=False )
s = str( response.json() ).split()[1]
ptr_record_id = s[1:len(s)-2]

response = requests.delete( url_base + '/' + a_record_id, auth=(account, password), verify=False )
response = requests.delete( url_base + '/' + ptr_record_id, auth=(account, password), verify=False )
response = requests.delete( url_base + '/request', auth=(account, password), verify=False, json='[{"method": "STATE:ASSIGN","data":{"host_name":"' + fq_hostname + '"}},{"method":"GET","object": "record:host","data": {"name":"##STATE:host_name:##"},"assign_state": {"host_ref": "_ref"},"enable_substitution": true,"discard": true},{ "method": "DELETE", "object": "##STATE:host_ref:##","enable_substitution": true,"discard": true},{"method": "STATE:DISPLAY"}]' )

