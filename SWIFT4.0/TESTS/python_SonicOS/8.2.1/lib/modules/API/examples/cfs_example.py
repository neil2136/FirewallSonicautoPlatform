import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print(suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + "../../"
        print(root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

from utm import Firewall
from modules.API.CFS import CFSURIListObjects

ip = '10.5.192.21'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
print(fw)
url = '/api/sonicos/content-filter/uri-list-objects'
CFSURIObject = CFSURIListObjects(fw)

def urilistobject():
    urilist_object = {"name": "Test_URI_Object",
                      "uri": ["[2001:df5:4c00:7192::227]/sonic/test", "Juniper.com"], "keyword": ["Routers", "Firewall"]}
    urilist_object_edit = {"name": "Test_URI_Object", "uri": ["Cisco.com"], "keyword": ["Switch"]}

    rc = CFSURIObject.create_uriobject(url=url, **urilist_object)
    if rc:
        print('Config URI list object success')
    else:
        print('Config URI list object fail')
    get_response = CFSURIObject.retrieve_URIlistobj("Test_URI_Object")
    print(get_response)
    put_response = CFSURIObject.put_uriobject(url, "Test_URI_Object", **urilist_object_edit)
    if put_response:
        print('Modifying URI list object success')
    else:
        print('Modifying URI list object fail')
    get_response = CFSURIObject.retrieve_URIlistobj("Test_URI_Object")
    print(get_response)
    del_response = CFSURIObject.delete_uriobject("Test_URI_Object")
    print(del_response)

urilistobject()