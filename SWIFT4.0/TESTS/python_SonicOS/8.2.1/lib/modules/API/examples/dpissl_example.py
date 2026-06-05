import sys
import os
#sys.path.append(os.environ["SONICOS_HOME"]+'/6.5.4/python_lib')
sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
from utm import Firewall
from modules.API.dpissl import ServersslApi
from modules.API.dpissl import ClientsslApi
ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

dpisslserver = ServersslApi(fw)
dpisslclient = ClientsslApi(fw)
#server_dict = {
#    'enable': True,
#    'application_firewall': True,
#    'intrusion_prevention': True,
#    'gateway_anti_virus': True,
#    'gateway_anti_spyware': True,
#    #'include_address': 'host1',
#    #'include_address_type': 'name',
#}
#server_dict = {
#    'enable': True,
#    'application_firewall': True,
#    'intrusion_prevention': True,
#    'gateway_anti_virus': True,
#    'gateway_anti_spyware': True,
#    'exclude_address': 'host1',
#    'exclude_address_type': 'name',
#    'exclude_user': 'user1',
#    'exclude_user_type': 'name',
#}
#server_dict = {
#    'enable': True,
#    'application_firewall': True,
#    'intrusion_prevention': True,
#    'gateway_anti_virus': True,
#    'gateway_anti_spyware': True,
#    'exclude_address': None,
#    'exclude_address_type': None,
#    'exclude_user': None,
#    'exclude_user_type': None,
#    #'include_user': True,
#    #'include_user_type': 'all',
#    #'include_address': True,
#    #'include_address_type': 'all',
#}
# server_dict = {
#    'enable': False,
#    'application_firewall': True,
#    'intrusion_prevention': True,
#    'gateway_anti_virus': True,
#    'gateway_anti_spyware': True,
#    'exclude_address': 'host1',
#    'exclude_address_type': 'name',
#    'exclude_user': 'user1',
#    'exclude_user_type': 'name',
#    'include_user': True,
#    'include_user_type': 'all',
#    'include_address': True,
#    'include_address_type': 'all',
# }
# rc = dpisslserver.config_general_settings(**server_dict)
#print(rc)

#server_dict = {
#    'ssl_server': 'X0 IP',
#    'ssl_server_type': 'name',
#    'certificate': 'ca1',
#    'cleartext': False,
#}
# rc = dpisslserver.add_sslserver(**server_dict)
# if rc:
#    print('Add dpissl server success')
#else:
#    print('Add dpissl server fail')
#server_dict = {
#    'ssl_server': 'X0 IP',
#    'ssl_server_type': 'name',
#    'certificate': 'ca1',
#    'cleartext': False,
#}
##rc = dpisslserver.del_sslserver(**server_dict)
#if rc:
#    print('Del dpissl server success')
#else:
#    print('Del dpissl server fail')
#
#server_dict = {
#    'ssl_server': 'X0 IP',
#    'ssl_server_type': 'name',
#    'certificate': 'ca1',
#    'cleartext': True,
#}
#rc = dpisslserver.del_sslserver(**server_dict)
#if rc:
#    print('Del dpissl server success')
#else:
#    print('Del dpissl server fail')
#
#server_dict = {
#    'ssl_server': 'X0 IP',
#    'ssl_server_type': 'name',
#    'certificate': 'ca1',
#    'cleartext_new': True,
#}
# rc = dpisslserver.edit_sslserver(**server_dict)
#if rc:
#    print('Edit dpissl server success')
#else:
#    print('Edit dpissl server fail')
#rc = dpisslserver.get_sslserver_config()
#print(rc)
#rc = dpisslserver.del_all_servers()
#print(rc)



#client_dict = {
#    'enable': True,
#    'application_firewall': True,
#    'intrusion_prevention': False,
#    'gateway_anti_virus': False,
#    'gateway_anti_spyware': False,
#    'content_filter': False,
#    'auth_server_for_decrypted_connections': False,
#    'deployment_server_domains': False,
#    'bypass_decryption': True,
#    'audit_built_in_exclusion': False,
#    'authenticate_server': False,
#    'open_failed_connections': True,
#}
#rc = dpisslclient.config_general_settings(**client_dict)
#if rc:
#    print('Edit dpissl client success')
#else:
#    print('Edit dpissl client fail')

#cert_dict = {
#    'certificate':'2048-bit',
#}
#rc = dpisslclient.config_cert(**cert_dict)
#print(rc)
#client_dict = {
#    'exclude_address': 'host1',
#    'exclude_address_type': 'name',
#    'exclude_user': None,
#    'exclude_user_type': None,
    #'include_user': True,
    #'include_user_type': 'all',
    #'include_address': True,
    #'include_address_type': 'all',
	 'cfs_category_unavailable':False,   # checkbox "Exclude connection if Content Filter Category is not available"
#}
#rc = dpisslclient.config_objects(**client_dict)
#print(rc)


#client_dict = {
#    'common_name': 'test1',
#    'common_name_action': 'skip_content_filter_exclusion',
#}
#rc = dpisslclient.add_common_name(**client_dict)
#print(rc)


#client_dict = {
#    'common_name': "test111",
#    'common_name_action': "skip_authentication",
#}
#rc = dpisslclient.add_common_name(**client_dict)
#print(rc)

#client_dict = {
#    'common_name': 'test222',
#    'common_name_action': 'exclude',
#    'exclude_type': 'disable_authenticate_server',
#}
#rc = dpisslclient.add_common_name(**client_dict)
#print(rc)

client_dict = {
    'common_name': 'test222',
    'common_name_action': 'exclude',
    'exclude_type': 'disable_authenticate_server',
}
rc = dpisslclient.delete_common_name(**client_dict)
print(rc)

#rc = dpisslclient.get_sslclient_config()
#print(rc)

#rc = dpisslclient.del_all_common_names()
#print(rc)

##############################currently not support on our dut
#client_dict = {
#    'common_name': 'test222',
#    'common_name_action': 'exclude',
#    'exclude_type': 'disable_authenticate_server',
#    'common_name_action_new': "skip_authentication",
#}
#rc = dpisslclient.edit_common_name(**client_dict)
#print(rc)

#client_dict = {
#    'selected': 'include',
#    'category': ["1. Violence/Hate/Racism","2. Intimate Apparel/Swimsuit"]
#}
#rc = dpisslclient.cfs_category_based_exclusion_inclusion(**client_dict)
#print(rc)

#client_dict = {
#    'selected': 'include',
#    'category': ["all"]
#}
#rc = dpisslclient.cfs_category_based_exclusion_inclusion(**client_dict)
#print(rc)

#################verify on postman,can get but cannot put,dts221640
#client_dict = {
#    'selected': 'exclude'
#}
#rc = dpisslclient.cfs_category_based_exclusion_inclusion(**client_dict)
#print(rc)
###############
