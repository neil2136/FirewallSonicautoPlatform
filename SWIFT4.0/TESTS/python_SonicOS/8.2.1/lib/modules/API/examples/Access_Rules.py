import os,sys
import json
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print(suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + "../"
        print(root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

from utm import Firewall
from modules.API.Access_Rule import Access_Rule

ip = '10.5.192.37'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

url = '/api/sonicos/address-objects'

access_rule_ip_version="ipv4"
from_zone="WAN"
to_zone="LAN"
source_address_type="any"
source_address="any"
source_port_type="any"
source_port="any"
service_type="any"
service="any"
destination_address_type="name"
destination_address="test_object"
name="testing"
enable=False
action="deny"
schedule="test_schedule"
users_included_type="all"
users_included="all"
users_excluded_type="none"
users_excluded="none"

Accessrule=Access_Rule(fw)
def test_create_access_rule_ipv4():
    access_rule={
    "access_rules": [
        {
            "ipv4": {
                "name": "testing",
                "enable": False,
                "from": "WAN",
                "to": "LAN",
                "action": "deny",
                "source": {
                    "address": {
                        "any": True
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "any": True
                },
                "destination": {
                    "address": {
                        "name": "test_object"
                    }
                },
                "schedule": {
                    "name": "test_schedule"
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "None"
            }
        }
    ]
}
    #urilist_object = {"content_filter": {"uri_list_object": [{"name": "", "uri": [{"uri":"dd"}], "keyword": [{"uri":"ddd"},{"uri":"dddf"}]}]}}
    url='/api/sonicos/access-rules/ipv4'
    response=Accessrule.config_accessrule(**access_rule)
    print (response)


def test_delete_accessrule_using_name():
        url="/api/sonicos/access-rules/ipv4/name/testing"
        response=Accessrule.delete_accessrule(url)
        return response








test_create_access_rule_ipv4()
test_delete_accessrule_using_name()