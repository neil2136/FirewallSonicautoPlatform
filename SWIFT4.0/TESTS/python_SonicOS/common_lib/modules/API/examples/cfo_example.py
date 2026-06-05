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
from modules.API.cfo import CfoGroupApi
from modules.API.cfo import CfoActionApi
from modules.API.cfo import CfoProfilesApi
from modules.API.cfo import CfoObjectApi



ip = '10.5.92.25'   # Device IP address

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
print(fw)


######## CFO Group###################

obj_cfo= CfoObjectApi(fw)
############ Enabling the Flow Server ###################

def uri_list_obj():
    obj = {
        'object_name': 'obj4',
        'url_name':['aaa.com','bbb.com'],
        'keyword':['vvv','vip']

  }

    rc = obj_cfo.configure_cfo_object(**obj)
    if rc:
            print('URI List object Configured ')
    else:
            print("12323232")
            print('#####Error while configuring URI List Obj##################')

uri_list_obj()

######## CFO Group###################

grp_cfo= CfoGroupApi(fw)
############ Enabling the Flow Server ###################

def uri_list_grp():
    grp = {
        'grp_name': 'grp1',
        'obj_name': ['obj1','obj2']

  }

    rc = grp_cfo.edit_cfo_group(**grp)
    if rc:
            print('URI List Group Configured ')
    else:
            print("12323232")
            print('#####Error while configuring URI List Group##################')

#uri_list_grp()


######## ACTION####################3333

profile_cfo= CfoProfilesApi(fw)
############ Enabling the Flow Server ###################

def cfo_profile():
    pro_obj = {
        'profile_name':'pro3',
        'smart_filter':True
        #'uri_list_allowed':'obj1',
        #'uri_list_forbidden':'obj2',
        #"search_order": "allowed-first",
        #"forbidden_operation": "block",
        #'consent_req':True,
        #'user_idle_timeout': 11,
        #'option_page_url': '192.12',
        #'mandatory_page_url':  '192.121',
        #'mandatory_addr': True,
        #'customer_insertion': True,
        #'entry':[{'domain':'youtube.com','key': 'YouTube-Restrict','value':'Strict'}]




  }

    act_res = profile_cfo.edit_cfo_profile(**pro_obj)
    if act_res:
            print('Action_obj Configured ')
    else:
            print('#####Error while configuring Action_Obj##################')

#cfo_profile()
#################################ACtion###################################33
action_cfo= CfoActionApi(fw)

def cfo_action():
    actn_obj = {
        'action_name': 'ac1',
        'wipe_cookies': False,
        'flow_reporting': True,
        'default_block': True,
        'password': 'sonicwall',
        'pass_active_time': '68',
        'pass_page_custom': '',
        'confirm_active_time': '67',
        'confirm_page_custom':''


  }

    act_res = action_cfo.configure_cfo_action(**actn_obj)
    if act_res:
            print('Action_obj Configured ')
    else:
            print('#####Error while configuring Action_Obj##################')

#cfo_action()

