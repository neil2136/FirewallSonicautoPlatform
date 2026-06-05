from utm import Firewall

'''
firewall
a.AccessRule
b.ContentFilterObject
  uri_list_object,uri_list_group,cfs_action_object,add_cfs_profile_object
c.ContentFilterPolicies
d.ActionObject
e.MatchObject
f.EmailObject
g.BandwidthObject
h.AppControl
i.AppRule 
'''

from modules.CLI.firewall import AccessRuleCli
from modules.CLI.firewall import ContentFilterObjectCli
from modules.CLI.firewall import ContentFilterPoliciesCli
from modules.CLI.firewall import ActionObjectCli
from modules.CLI.firewall import MatchObjectCli
from modules.CLI.firewall import EmailObjectCli
from modules.CLI.firewall import BandwidthObjectCli
from modules.CLI.firewall import AppControlCli
from modules.CLI.firewall import AppRuleCli

ip = '192.168.168.168'
port = '2033'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

access_rule_obj = AccessRuleCli(fw)
content_filter_obj = ContentFilterObjectCli(fw)
cfs_policy_obj = ContentFilterPoliciesCli(fw)
action_object_obj = ActionObjectCli(fw)
match_object_obj = MatchObjectCli(fw)
email_object_obj = EmailObjectCli(fw)
bandwidth_object_obj = BandwidthObjectCli(fw)
app_control_obj = AppControlCli(fw)
app_rule_obj = AppRuleCli(fw)


access_rule_ipv4_dict = {
    'name': 'test test test',
    'from': 'WAN',
    'to': 'LAN',
    'action': 'allow',  # "allow,deny,discard"
    'src_name': 'X1 Subnet',
    # 'src_group': 'All WAN IP',
    'dst_name': 'X0 IP',
    # 'dst_group': 'test_group',
    'service_name': 'Citrix TCP (Session Reliability)',
    'users_included': 'administrator',
    'users_excluded_group': 'SonicWALL Read-Only Admins',
    # 'service_group':
    'logging': False,
    'tcp_timeout': 20,
    'connection_limit_src': 124,
    'qos_dscp': {'explicit': 5 },
    'schedule_days_SU-M':{'time1': '00:00','time2': '00:15'},
    'comment': 'test test test'
}

access_rule_ipv4_dict_1 = {
    'from': 'WAN',
    'to': 'LAN',
    'action': 'allow',  # "allow,deny,discard"
    'src_name': 'X1 Subnet',
    # 'src_group': 'All WAN IP',
    'dst_name': 'X0 IP',
    # 'dst_group': 'test_group',
    'service_name': '6over4',
    # 'service_group':'yuuu'
    "comment": 'test access rule ipv4'
}

access_rule_ipv4_dict_1_edit = {
    'from': 'WAN',
    'from_new': 'DMZ',
    'to': 'LAN',
    "enable": False,
    'action': 'allow',  # "allow,deny,discard"
    'action_new': 'deny',
    'src_name': 'X1 Subnet',
    'src_name_new': 'X2 Subnet',
    # 'src_group': 'All WAN IP',
    'dst_name': 'X0 IP',
    'dst_group_new': 'All X0 Management IP',
    'service_name': '6over4',
    'service_name_new': 'Address Mask Reply',
    'schedule_days_SU-SA_new':True,
    # 'service_group':
}

access_rule_ipv4_dict_2 = {
    'from': 'DMZ',
    'to': 'LAN',
    'action': 'deny',
    'src_name': 'X2 Subnet',
    'dst_group': 'All X0 Management IP',
    'service_name': 'Address Mask Reply',
    'schedule_days_SU-SA':True,
}

access_rule_ipv6_dict = {
    'from': 'LAN',
    'to': 'WAN',
    'action': 'allow',
    'src_group': 'LAN IPv6 Subnets',
    'version': 'v6'
}

show_access_rule_dict = {
    'from': 'DMZ',
    'to': 'WAN',
    # 'version': 'ipv4',
    # 'type': 'custom'

}

access_rule_dict_edit_uuid = {
    'version': 'ipv4',
    'uuid': '',
    'from_new': 'LAN',
    "to_new": 'WAN',
    'action_new': 'deny',
    'src_name_new': 'X2 Subnet',
    'dst_group_new': 'All X0 Management IP',
    'service_name_new': 'Address Mask Reply',
    'schedule_days_SU-SA_new': True,
}

# access_rule_obj.restore_access_rule()
# access_rule_obj.add_access_rule(**access_rule_ipv4_dict)
# access_rule_obj.add_access_rule(**access_rule_ipv4_dict_1)
# access_rule_obj.edit_access_rule(**access_rule_ipv4_dict_1_edit)
# access_rule_obj.edit_access_rule_by_uuid(**access_rule_dict_edit_uuid)
# output = access_rule_obj.show_access_rules(**show_access_rule_dict)
# print(output)
# access_rule_obj.del_access_rule(**access_rule_ipv4_dict_2)
# access_rule_obj.add_access_rule(**access_rule_ipv6_dict)
# access_rule_obj.del_access_rule(**access_rule_ipv6_dict)
# access_rule_obj.list_access_rule_cli()


uri_list_object_dict = {
    'name': 'test-object1',
    'keyword': ['baidu', 'google', 'yahoo'],
    'uri': ['www.baidu.com', 'www.google.com', 'www.yahoo.com'],
}
uri_list_object_dict1 = {
    'name': 'test-object2',
    'keyword': ['baidu', 'google', 'yahoo'],
    'uri': ['www.baidu.com', 'www.google.com', 'www.yahoo.com'],
}
# content_filter_obj.del_uri_list_object()  # delete all uri list if name not specified
# content_filter_obj.add_uri_list_object(**uri_list_object_dict)
# content_filter_obj.add_uri_list_object(**uri_list_object_dict1)
# all = content_filter_obj.show_uri_list_object()  # show all uri list if name not specified
# test = content_filter_obj.show_uri_list_object('test-object1')  # show uri list with name

# content_filter_obj.del_uri_list_object('test-object1','test-object2')  # delete uri list with name
# print(all)
# print(test)

uri_list_group_dict1 = {
    'name': 'test group1',
}
uri_list_group_dict = {
    'name': 'test group',
    'object_list': ['test-object1', 'test-object2'],
    'group_list': ['test group1'],
}

# content_filter_obj.del_uri_list_group()  # delete all uri list if name not specified
# content_filter_obj.add_uri_list_group(**uri_list_group_dict1)
# content_filter_obj.add_uri_list_group(**uri_list_group_dict)
# print('sophie')
# content_filter_obj.show_uri_list_group()   # show all uri list if name not specified
# content_filter_obj.show_uri_list_group('test group')   # show  uri group with name
# content_filter_obj.del_uri_list_group('test group','test group1')   # delete uri group with name


cfs_action_object_dict = {
    'name': 'cfs-action1',
    # 'action': 'block',
    'action': 'passphrase',  # block, confirm, passphrase
    # 'page': 'block test',
    'page': 'passphrase test',
    'password': "password",
    'active_time': 10,
}

cfs_action_object_dict_edit = {
    'name': 'cfs-action1',
    'name_new': 'cfs-action1-edit',
    'action': 'block',
    #'action': 'passphrase',  # block, confirm, passphrase
    'page': 'block test',
    #'page': 'passphrase test',
    'password': "password",
    #'active_time': 10,
}

# content_filter_obj.del_cfs_action_object()
# content_filter_obj.add_cfs_action_object(**cfs_action_object_dict)
# content_filter_obj.show_cfs_action_object()
# content_filter_obj.edit_cfs_action_object(**cfs_action_object_dict_edit)
# content_filter_obj.show_cfs_action_object('cfs-action1-edit')
# content_filter_obj.del_cfs_action_object('cfs-action1-edit')

cfs_profile_object_dict = {
    'name': 'cfs-profile',
    'allowed_uri_list': 'test-object1',
    'forbidden_uri_list': 'test-object2',
    'search_order': 'forbidden-first',  # forbidden-first or allowed-first
    'forbidden_operation': 'block',
    'allowed_category_list': ['1. Violence/Hate/Racism', '2. Intimate Apparel/Swimsuit'],
    'bwm_category_list': ['17. Education', '19. Cultural Institutions'],
    'confirm_category_list': ['21. Online Brokerage and Trading', '23. Government'],
    'blocked_category_list': ['28. Hacking/Proxy Avoidance Systems', '48. Multimedia'],
    'passphrase_category_list': ['60. Radicalization and Extremism', '9. Illegal Skills/Questionable Skills'],
    'https-filtering': True,
    'consent':{
        'enable': True,
        'user-idle-timeout': 10,
        'optional_page_url': 'www.baidu.com',
        'mandatory_page_url': 'www.baidu.com',
        'mandatory_address_name':'Default Active WAN IP'
    },
    'custom_header_insertion': True,
    'custom_header_entry':{
        'domain':'test',
        'key': 'test',
        'value': 'test'
    }
}

cfs_profile_object_dict_edit = {
    'name': 'cfs-profile',
    'name_new': 'cfs-profile_edit',
    'allowed_uri_list': 'test-object2',
    'forbidden_uri_list': 'test-object1',
    'search_order': 'allowed-first',  # forbidden-first or allowed-first
    'forbidden_operation': 'passphrase',
    'allowed_category_list': ['1. Violence/Hate/Racism', '2. Intimate Apparel/Swimsuit'],
    'bwm_category_list': ['17. Education', '19. Cultural Institutions'],
    'confirm_category_list': ['21. Online Brokerage and Trading', '23. Government'],
    'blocked_category_list': ['28. Hacking/Proxy Avoidance Systems', '48. Multimedia'],
    'passphrase_category_list': ['60. Radicalization and Extremism', '9. Illegal Skills/Questionable Skills'],
}

# content_filter_obj.del_cfs_profile_object()
# content_filter_obj.add_cfs_profile_object(**cfs_profile_object_dict)
# content_filter_obj.show_cfs_profile_object()
# content_filter_obj.edit_cfs_profile_object(**cfs_profile_object_dict_edit)
# content_filter_obj.show_cfs_profile_object('cfs-profile_edit')
# content_filter_obj.del_cfs_profile_object('cfs-profile_edit')

cfs_policy_object_dict = {
    'name': 'cfs-policy',
    'src_zone': 'WAN',
    'dst_zone': 'LAN',
    'profile': 'CFS Default Profile',
    'action': 'CFS Default Action',
    'users_included': 'guests',
    # 'users_included_group': '',
    'users_excluded': 'administrator',
    '#users_excluded_group': "Limited Administrators",
    "src_addr_excluded_name" :"Default Active WAN IP",
    # "src_addr_excluded_group":"",
    # "src_addr_included_name" :"",
    "src_addr_included_group":"All Interface IP",
    'schedule_days_M-T':'00:00'
}

cfs_policy_object_dict_edit = {
    'name': 'cfs-policy',
    'name_new': 'cfs-action1-edit',
    'src_zone': 'LAN',
    'dst_zone': 'WAN',
    'profile': 'cfs-profile',
    'action': 'CFS Default Action',
    "enable": False,
}

# cfs_policy_obj.del_cfs_policy_object()
# cfs_policy_obj.add_cfs_policy_object(**cfs_policy_object_dict)
# cfs_policy_obj.show_cfs_policy_object()
# cfs_policy_obj.edit_cfs_policy_object(**cfs_policy_object_dict_edit)
# cfs_policy_obj.show_cfs_policy_object('cfs-action1-edit')
# cfs_policy_obj.del_cfs_policy_object('cfs-action1-edit')


# action should be in block-smtp-error-reply, disable-email-attachment, email-add-text, ftp-notification-reply
#,http-block-page ,http-redirect

action_object_dict = {
    'name': 'action object test',
    'action': 'block-smtp-error-reply',
    'content': 'action object test  action object test action object test',
}

action_object_dict_edit = {
    'name': 'action object test',
    'name_new': 'action object test edit',
    'action': 'disable-email-attachment',
    'content': 'action object test  action object test action object test 111 22',
}

# action_object_obj.del_action_object()
# action_object_obj.add_action_object(**action_object_dict)
# action_object_obj.show_action_object()
#action_object_obj.edit_action_object(**action_object_dict_edit)
#action_object_obj.show_action_object('action object test edit')
# action_object_obj.del_action_object('action object test edit')

match_object_obj_dict = {
    'name': 'match object test',
    'type': 'file-content',
    'content-entry': ['test1', 'test 123', 'test 456'],
    'match-type': 'partial',
    'input-representation': 'alphanumeric',
    #'negative-matching': True,
}

# match_object_obj.del_match_object()
# match_object_obj.add_match_object(**match_object_obj_dict)
# match_object_obj.show_match_object()
# match_object_obj.show_match_object('match object test')
# match_object_obj.del_match_object('match object test')

email_object_obj_dict = {
    'name': 'email object test',
    'content-entry': ['test1@qq.com', 'test 123', 'test 456'],
    'match-type': 'partial',  # exact, partial, regex
}

# email_object_obj.del_email_object()
# email_object_obj.add_email_object(**email_object_obj_dict)
# email_object_obj.show_match_object()
# email_object_obj.show_match_object('email object test')
# email_object_obj.del_email_object('email object test')


bandwidth_object_obj_dict = {
    'name': 'bandwith object test',
    'maximum_kbps': 123,  # only one of maximum_kbps, maximum_mbps can be specified
    #'maximum_mbps': 234,
    'guaranteed_kbps': 123, # only one of guaranteed_kbps, guaranteed_kbps can be specified
    #'guaranteed_kbps': 234,
    'per_ip_kbps': 100, # only one of per_ip_kbps, per_ip_kbps can be specified
    #'per_ip_kbps': 234,
    'action': 'delay',  # delay,drop
    'priority': 'high', # realtime,highest,high,medium-high,medium,medium-low,low,lowest
    'comment': 'test test test',
}

# bandwidth_object_obj.del_bandwidth_object()
# bandwidth_object_obj.add_bandwidth_object(**bandwidth_object_obj_dict)
# bandwidth_object_obj.show_bandwidth_object()
# bandwidth_object_obj.show_bandwidth_object('bandwith object test')
# bandwidth_object_obj.del_bandwidth_object('bandwith object test')

app_control_global_dict = {
    "enable": True,
    "log-all": True,
    "log-filename": True,
    "log-redundancy": 10,
}
app_control_obj_category_dict = {
    'category': '',  # put an integer if want use category id , or put category name here
    'application': '', # put an integer if want use application id , or put application name here
    'signature': '', # put an integer if want use signature id , or put signature name here
    'log': True, # True or False
    'block': True, # True or False
    'InIP_group': 'LAN Subnets',
    #'InIP_name': 'X0 Subnet',
    #'InIP_all': '',
    'ExIP_group': '',
    'ExIP_name': 'X0 Subnet',
    'ExIP_all': '',
}
app_control_obj_category_dict_1 = {
    'category': 'PROTOCOLS',  # put an integer if want use category id , or put category name here
    'application': 'ICMP', # put an integer if want use application id , or put application name here
    'signature': '5193', # put an integer if want use signature id , or put signature name here
    'log': True,  # True or False
    'block': True,  # True or False
    'InIP_group': 'LAN Subnets',
    'ExIP_name': 'X0 Subnet',
}

app_control_obj_category_dict_2 = {
    'category': 'PROTOCOLS',  # put an integer if want use category id , or put category name here
    'log': True, # True or False
    'block': True, # True or False
}

app_control_obj_category_dict_3 = {
    'category': 'PROTOCOLS',  # put an integer if want use category id , or put category name here
    'application': 'ICMP', # put an integer if want use application id , or put application name here
    'log': True, # True or False
    'block': False, # True or False
}
exclude_list_dict = {
    'type': 'ips'
}
exclude_list_dict_1 = {
    'type': 'ao',
    #'ao_name': 'X0 Subnet', # ao_name,ao_group only one can be specified
    'ao_group': 'LAN Subnets',

}
show_app_control_dict = {
    'category': 'EMAIL-APPS',
    'application': 'Horde',

}

# app_control_obj.reset_ac()
# app_control_obj.config_ac_global(**app_control_global_dict)

#app_control_obj.config_ac(**app_control_obj_category_dict_1)
#app_control_obj.enable_exclude_list(**exclude_list_dict_1)
# app_control_obj.show_app_control()
# app_control_obj.show_app_control(**show_app_control_dict)

app_setting_dict = {
    "enable": True,
    "log-redundancy": 12
}
app_rule_obj_dict = {
    'name': 'app rule',
    'type': 'ftp_client_download',
    'src_addr_group': '',  # only can specify one of src_addr_group, src_addr_name
    #'src_addr_name': '',
    'dst_addr_group': '',  # only can specify one of dst_addr_group, dst_addr_name
    #'dst_addr_name': '',
    'excl_addr_group': '', # only can specify one of excl_addr_group, excl_addr_name
    #'excl_addr_name': '',
    'src_service': '',
    'dst_service': '',
    'match_object': 'ftp_match_obj1',
    'action-object': '',
    'log_individual': True,
    'log_redundancy': 'global', # specify this parameter as digit if want to specify redundancy interval ,else set as 'global'
    'direction_advanced_from': 'WAN', # only can specify one of direction_advanced_** ,direction_basic
    'direction_advanced_to': 'any',
    #'direction_basic': 'both',
    'logging': True,

}

app_rule_obj_dict_1 = {
    'name': 'app rule 1',
    'type': 'ftp_client_download',
    'src_addr_group': 'LAN Subnets',
    'dst_addr_name': 'X1 Subnet',
    'excl_addr_name': 'X0 IP',
    'match_object': 'ftp_match_obj1',
    'action_object': 'Reset/Drop',
    'log_individual': True,
    'log_redundancy': '2',
    'direction_advanced_from': 'WAN',
    'direction_advanced_to': 'LAN',
    'logging': True,

}

app_rule_obj_dict_2 = {
    'name': 'app rule 2',
    'type': 'ftp_client_download',
    'dst_service': 'FTP Control',
    'match_object': 'ftp_match_obj1',
    'action_object': 'Reset/Drop',
    'log_individual': True,
    'log_redundancy': 'global',
    'direction_basic': 'both',
    'logging': True,
}

app_rule_obj.config_app_setting(**app_setting_dict)
# app_rule_obj.add_app_rule(**app_rule_obj_dict_1)
# app_rule_obj.add_app_rule(**app_rule_obj_dict_2)
# app_rule_obj.show_app_rule()
# app_rule_obj.show_app_rule('app rule 1')
# app_rule_obj.del_app_rule('app rule 1', 'app rule 2')
# app_rule_obj.del_app_rule()



