import os,sys
import json
import time
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

ip = '10.5.192.38'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')



Accessrule=Access_Rule(fw)

url='/access-rules/ipv4'
def test_post_access_rule_ipv4():
    access_rule = {
            'name': 'test1',
            'enable': True,
            'from': 'WAN',
            'to': 'LAN',
            'action': 'deny',
            'source': {
                'address': {
                    'any': True},
                'port': {
                    'any': True}},
            'service': {
                    'name': '6over4'},
            'destination': {
                'address': {
                    'any': True}},
            'schedule': {
                'always_on': True},
            'users': {
                'included': {
                    'all': True},
                'excluded': {
                    'none': True}},
            'comment': 'testin from automation framework',
            'fragments': True,
            'logging': True,
            'sip': False,
            'h323': False,
            'flow_reporting': False,
            'botnet_filter': False,
            'geo_ip_filter': False,
            'packet_monitoring': False,
            'management': False,
            'max_connections': 100,
            'priority': {
                'auto': True},
            'tcp': {'timeout': 15,
                    'urgent': False},
            'udp': {'timeout': 30},
            'connection_limit': {
                'source': {},
                'destination': {}},
            'dpi': True,
            'dpi_ssl': {
                'client': True,
                'server': True},
            'quality_of_service': {
                'dscp': {
                    'map': True},
                'class_of_service':
                {'map': True}}}
    #urilist_object = {"content_filter": {"uri_list_object": [{"name": "", "uri": [{"uri":"dd"}], "keyword": [{"uri":"ddd"},{"uri":"dddf"}]}]}}
    response=Accessrule.config_accessrule(**access_rule)
    print (response)
    print("-----------------------------------test_post_access_rule_ipv4 completed---------------------------------------------------------")


def test_delete_accessrule_using_name():
    url="/access-rules/ipv4/name/test1"
    response=Accessrule.delete_accessrule(url)
    print(response)
    print("-----------------------------------test_delete_accessrule_using_name---------------------------------------------------------")
def test_delete_accessrule_using_body():
    access_rule = {
    "access_rules": [
        {
            "ipv4": {
        'name': 'test1',
        'enable': True,
        'from': 'WAN',
        'to': 'LAN',
        'action': 'deny',
        'source': {
                'address': {
                    'any': True},
                'port': {
                    'any': True}},
        'service': {
                'name': '6over4'},
        'destination': {
            'address': {
                'any': True}},
        'schedule': {
            'always_on': True},
        'users': {
            'included': {
                'all': True},
            'excluded': {
                'none': True}},
        'comment': 'testin from automation framework',
            'fragments': True,
            'logging': True,
            'sip': False,
            'h323': False,
            'flow_reporting': False,
            'botnet_filter': False,
            'geo_ip_filter': False,
            'packet_monitoring': False,
            'management': False,
            'max_connections': 100,
            'priority': {
                'auto': True},
            'tcp': {'timeout': 15,
                    'urgent': False},
            'udp': {'timeout': 30},
            'connection_limit': {
                'source': {},
                'destination': {}},
            'dpi': True,
            'dpi_ssl': {
                'client': True,
                'server': True}}}]}
    url = "/access-rules/ipv4"
    response=Accessrule.delete_accessrule(url,data=access_rule)
    print(response)
    print("-----------------------------------test_delete_accessrule_using_body---------------------------------------------------------")

def test_get_accessrule_using_name():
    url="/access-rules/ipv4/name/test1"
    response=Accessrule.get_accessrule(url)
    print("-----------------------------------test_get_accessrule_using_name---------------------------------------------------------")

def test_put_access_rule_ipv4():
    access_rule = {
            'name': 'test1',
            'enable': False,
            'from': 'WAN',
            'to': 'LAN',
            'action': 'deny',
            'source': {
                'address': {
                    'any': True},
                'port': {
                    'any': True}},
            'service': {
                    'name': '6over4'},
            'destination': {
                'address': {
                    'any': True}},
            'schedule': {
                'always_on': True},
            'users': {
                'included': {
                    'all': True},
                'excluded': {
                    'none': True}},
            'comment': 'testin from automation framework',
            'fragments': True,
            'logging': True,
            'sip': False,
            'h323': False,
            'flow_reporting': False,
            'botnet_filter': False,
            'geo_ip_filter': False,
            'packet_monitoring': False,
            'management': False,
            'max_connections': 100,
            'priority': {
                'auto': True},
            'tcp': {'timeout': 15,
                    'urgent': False},
            'udp': {'timeout': 30},
            'connection_limit': {
                'source': {},
                'destination': {}},
            'dpi': True,
            'dpi_ssl': {
                'client': True,
                'server': True},
            'quality_of_service': {
                'dscp': {
                    'map': True},
                'class_of_service':
                {'map': True}}}
    response=Accessrule.put_accessrule(**access_rule)
    print(response)
    print("-----------------------------------test_put_access_rule_ipv4---------------------------------------------------------")










test_post_access_rule_ipv4()
test_get_accessrule_using_name()
test_put_access_rule_ipv4()
test_get_accessrule_using_name()
test_delete_accessrule_using_name()
test_post_access_rule_ipv4()
#time.sleep(10)
test_delete_accessrule_using_body()
###################### AccessRuleIPv4Api #####################
'''
from modules.API.accessrule import AccessRuleIPv4Api
fw = Firewall(Parameter.FIREWALL,
              user='admin',
              password='password',
              supported_config_mode='api')

addressObjectsApi = AddressobjectsApi(fw)

access_rule_option = {
    'name': 'test_wan_lan',
    'from': 'WAN',
    'to': 'LAN',
    'source_addr': {'any': True},
    'dst_addr': {'any': True},
    'service': {'group': 'Ping'},
    'action': 'allow',
}
output = accessRuleApi.add_ipv4_access_rule(**access_rule_option)
access_rule_option = {
    'name': 'test_wan_lan',
    'from': 'WAN',
    'to': 'LAN',
    'source_addr': {'any': True},
    'dst_addr': {'any': True},
    'service': {'name': 'FTP Data'},
    'action': 'allow',
}
output = accessRuleApi.edit_ipv4_access_rule(**access_rule_option)
rc = accessRuleApi.del_ipv4_access_rule('test_wan_lan')
'''
