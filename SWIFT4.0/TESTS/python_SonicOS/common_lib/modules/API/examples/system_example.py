import sys
import os
from pprint import pprint
sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')

from utm import Firewall

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

###################### StatusApi ##########################
from modules.API.system import StatusApi
#status = StatusApi(fw)

#out = status.show_status()
#pprint(out)
#out = status.show_version()
#pprint(out)

###################### LicenseApi #########################
from modules.API.system import LicenseApi
#license = LicenseApi(fw)

#out = license.show_license()
#print(out)
#out = license.show_license_setting()
#pprint(out)

#keys=[{'key': 'sly-asia-wag-lard-hero-sled'},
#      {'key': 'rosy-cray-bee-bah-mule-lit'},
#      {'key': 'melt-egg-is-trod-rout-line'}]
#out = license.update_license_setting(keys)
#print(out)

#out = license.sync_license()
#print(out)

###################### AdminApi ###########################
from modules.API.system import AdminApi
admin = AdminApi(fw)

#out = admin.show_admin_setting()
#pprint(out)

#admin_info = {
#    'admin': {
#        'preempt_action': 'logout'
#    },
#   'gms_management': {
#        'ipsec_tunnel': {
#           'authentication_key': '4e6319ec55f0bcc88f53696d6b212e4f',
#            'behind_nat_device': {},
#            'encryption_key': 'ad8969dd3acc0fe3',
#            'encryption_type': 'des-md5',
#            'heartbeat_status_only': False,
#            'spi': 'C0EAE4E1FD8C',
#            'syslog_server_port': 514
#        }
#    }
#   # 'http_port': 88,
#}
#out = admin.conf_admin(**admin_info)
#pprint(out)

#admin_info = {
#    'admin': {
#        'preempt_action': 'logout'
#    },
#    'gms_management': {}
#}
#out = admin.edit_admin(**admin_info)
#pprint(out)

#out = admin.unbind_totp_key()
#pprint(out)

#fw1 = Firewall(ip, user='admin', password='Admin@123456789', supported_config_mode='api')
#admin1 = AdminApi(fw1)
#out = admin1.change_password(new_pass='password', old_pass='Admin@123456789')
#pprint(out)

###################### SNMPApi ###########################
from modules.API.system import SNMPApi
snmp = SNMPApi(fw)

# base_option = {
#     "system_name": "sonicwall",
#     "system_contact": "test@test.com",
#     "system_location": "Shanghai",
#     "asset_number": "12345678",
#     "get_community_name": "public",
#     "trap_community_name": "public",
#     "host_1": "10.103.201.162",
#     "host_2": "10.2.2.2",
#     "host_3": "10.3.3.3",
#     "host_4": "10.4.4.4",
# }
# out = snmp.snmp_base_settings(**base_option)
# pprint(out)

# advance_option = {
#     'engine_id': '80002225032CB8ED9D3C20',
#     'increase_subsystem_priority': False,
#     'mandatory': False,
# }
# out = snmp.snmp_advance_settings(**advance_option)
# pprint(out)

# view_option = {
#     "view_name": 'custom_view',
#     "oid_list": ['1.2.3', '1.2.4', '1.2.5', '1.2.6']  # oid list under one name, like ['2.3','2.4']
# }
# out = snmp.snmp_view_add(**view_option)
# pprint(out)
# out = snmp.snmp_view_delete(**view_option)
# pprint(out)

# user_option = {
#     'user_name': 'UserTest',
#     'user_security': 'authentication_and_privacy',  # None, authentication_only, authentication_and_privacy
#     'user_auth_method': 'md5',                      # md5, sha1, must set for authentication_only, authentication_and_privacy
#     'user_auth_key': '12345678',                    # key length in [8, 32], must set for user_auth_method
#     'user_encrypt_method': 'aes',                   # aes, des, must set for authentication_and_privacy
#     'user_priv_key': 'abcdefg',                     # key length in [8, 32], must set for user_encrypt_method
#     'user_group': 'group1',
# }
# out = snmp.snmp_user_add(**user_option)
# pprint(out)
# user_edit = {
#     'user_name': 'UserTest',
#     'user_new_name': 'UserNew',
#     'user_security': ''
# }
# out = snmp.snmp_user_edit(**user_edit)
# pprint(out)
# out = snmp.snmp_user_delete(name='UserTest')
# pprint(out)

# access_option = {
#     'access_name': 'AccessTest',
#     'access_security': 'authentication_only',   # None, authentication_only, authentication_and_privacy
#     'access_view': 'root',                      # view oid: root, system,...
#     'access_group': 'group1'
# }
# out = snmp.snmp_access_add(**access_option)
# pprint(out)
# access_edit = {
#     'access_name': 'AccessTest',
#     'access_new_name': 'AccessNew',              # new access name need to be changed
#     'access_security': '',   
#     'access_view': 'system'                 
# }
# out = snmp.snmp_access_add(**access_edit)
# pprint(out)
# out = snmp.snmp_access_delete(name='AccessNew')
# pprint(out)


#out = snmp.show_snmp()
#pprint(out)
#out = snmp.enable_snmp()
#pprint(out)
#out = snmp.disable_snmp()
#pprint(out)
#snmp_edit = {
#    'host_1': '1.2.3.4',
#    'snmp3': {
#        'increase_subsystem_priority': True
#    }
#}
#out = snmp.edit_snmp(**snmp_edit)
#pprint(out)

#out = snmp.show_snmp_group()
#pprint(out)
#out = snmp.add_snmp_group('test 1')
#pprint(out)
#group = {
#    'name': 'test'
#}
#out = snmp.delete_snmp_group(**group)
#pprint(out)

#out = snmp.show_snmp_user()
#pprint(out)
#user = {
#    'name': 'test11',
#    'group': '',
#    'security_level': {'authentication_and_privacy': True}, # empty or
#                                                            # 'authentication_only': True or
#                                                            # 'authentication_and_privacy'
#    # # # If security_level is not empty, authentication must be set
#    'authentication': {
#        'md5': '4,ea161c510f4feeb9cfc998fe06f2352b7ec0e2d4225fa598857a972d92aff7936108551db1fe2b12'
#    },
#
#    # # # If security_level is authentication_and_privacy, encryption must be set
#     'encryption': {
#         'aes': '4,623ed0a407436cba9e97d958b880c023b6d915d2ce5c60007b1a9906013072ebaa354215f58db0e6'
#     },
#}
#out = snmp.add_snmp_user(**user)
#pprint(out)
#user = {
#    'name': 'test11',
#    'group': 'test 1',
#    'security_level': {},
#}
#out = snmp.edit_snmp_user(**user)
#pprint(out)
#out = snmp.delete_snmp_user('test11')
#pprint(out)

#out = snmp.show_snmp_view()
#pprint(out)
#view = {
#    'name': 'CorpSNMPViewList',
#    'oid': '1.3.6.1.2.1.32'
#}
#out = snmp.add_snmp_view(**view)
#pprint(out)
#view = {
#    'name': 'CorpSNMPViewList',
#    'oid': '1.3.6.1.2.1.32'
#}
#out = snmp.delete_snmp_view(**view)
#pprint(out)

#out = snmp.show_snmp_access()
#pprint(out)
#access = {
#    'master_group': 'test 1',
#    'name': 'test2',
#    'read_view': 'IP',   # root, system, interfaces, IP, ICMP, TCP, UDP, ifMIB
#    'security_level': {'authentication_and_privacy': True} # empty or 'authentication_only': True or
#                                                           # 'authentication_and_privacy': True
#}
#out = snmp.add_snmp_access(**access)
#pprint(out)
#access = {
#    'master_group': 'test 1',
#    'name': 'test2',
#    'read_view': 'system', # root, system, interfaces, IP, ICMP, TCP, UDP, ifMIB
#    'security_level': {'authentication_and_privacy': True} # empty or 'authentication_only': True or
#                                                           # 'authentication_and_privacy': True
#}
#out = snmp.edit_snmp_access(**access)
#pprint(out)
#out = snmp.delete_snmp_access('test2')
#pprint(out)

###################### SettingApi #########################
from modules.API.system import SettingApi
setting = SettingApi(fw)

#out = setting.show_firmware()
#pprint(out)
#fw_info = {
#    'auto': {
#        'update': False
#    },
#}
#out = setting.edit_firmware(**fw_info)
#pprint(out)
#out = setting.backup_firmware()
#pprint(out)


###################### ScheduleApi ########################
from modules.API.system import ScheduleApi
schedule = ScheduleApi(fw)

#out = schedule.show_schedules()
#pprint(out)
#out = schedule.get_schedule('Guest Cycle Quota Update')
#pprint(out)
#sdu = {
#    'name': 'test',
#    'occurs': {
#        'recurring': {  # once, recurring, mixed
#            'recurring': [{'end': '00:20',
#                           'fri': False,
#                           'mon': True,
#                           'sat': False,
#                           'start': '00:15',
#                           'sun': True,
#                           'thu': True,
#                           'tue': True,
#                           'wed': True}]
#        }
#    },
#}
#sdu = {
#    'name': 'test1',
#    'occurs': {
#        'once': {
#            'event': {
#                'end': '2019:11:02:00:00',
#                'start': '2019:11:01:00:00'
#            }
#        }
#    },
#}
#out = schedule.add_schedule(**sdu)
#pprint(out)
#sdu = {
#    'name': 'test',
#    'occurs': {
#        'once': {
#            'event': {
#                'end': '2019:11:02:00:00',
#                'start': '2019:11:01:00:00'
#            }
#        }
#    },
#}
#out = schedule.edit_schedule(**sdu)
#pprint(out)
#out = schedule.delete_schedule('test')
#pprint(out)
#sdu = {
#    'name': 'test1',
#    'occurs': {
#        'mixed': {  # once, recurring, mixed
#            'event': {
#                'end': '2019:11:02:00:00',
#                'start': '2019:11:01:00:00'
#            },
#            'recurring': [{'end': '00:20',
#                           'fri': False,
#                           'mon': True,
#                           'sat': False,
#                           'start': '00:15',
#                           'sun': True,
#                           'thu': True,
#                           'tue': True,
#                           'wed': True}]
#        }
#    },
#}
#out = schedule.edit_schedules(**sdu)
#pprint(out)
#sdu = {
#    'name': 'test1',
#    'occurs': {
#        'once': {
#            'event': {
#                'end': '2000:01:01:00:01',
#                'start': '2000:01:01:00:00'
#            }
#        }
#    }
#}
#out = schedule.delete_schedules(**sdu)
#pprint(out)
#out = schedule.get_from_uuid('00000000-0000-0005-0c00-c0eae488b08a')
#pprint(out)
#sdu = {
#    'occurs': {
#        'recurring': {
#            'recurring': [{'end': '00:20',
#                           'mon': True,
#                           'start': '00:15',
#                           'sun': True,
#                           'thu': False,
#                           'tue': True,
#                           'wed': True}]
#        }
#    },
#    'uuid': '00000000-0000-0005-0c00-c0eae488b08a'
#}
#out = schedule.edit_from_uuid(**sdu)
#pprint(out)
#out = schedule.delete_from_uuid('00000000-0000-0005-0c00-c0eae488b08a')
#pprint(out)

###################### PacketmonitorApi ###################
from modules.API.system import PacketmonitorApi
packet = PacketmonitorApi(fw)

#out = packet.show_packmon_setting()
#pprint(out)
#pc_info = {
#    'display_filter': {
#        'bidirectional': True,
#        'destination_ips': '',
#        'destination_ports': '',
#        'ip_types': 'ICMP,TCP',
#    }
#}
#out = packet.conf_packmon(**pc_info)
#pprint(out)
#out = packet.show_pack_statistics()
#pprint(out)
#out = packet.clear_packets()
#pprint(out)
#out = packet.packets_to_ftp()
#pprint(out)
#out = packet.monitor_all()
#pprint(out)
#out = packet.monitor_default()
#pprint(out)
#out = packet.start_capture()
#pprint(out)
#out = packet.stop_capture()
#pprint(out)
#out = packet.start_mirror()
#pprint(out)
#out = packet.stop_mirror()
#pprint(out)
out = packet.export_captured_packets('html')   # eg: html,text,libpcap,pcapng,app-data
pprint(out)
###################### DiagnosticApi ######################
from modules.API.system import DiagnosticApi
diag = DiagnosticApi(fw)

#out = diag.get_icmp_conf()
#pprint(out)
#icmp = {
#    'flood': {'protection': True}
#}
#out = diag.conf_icmp(**icmp)
#pprint(out)
#out = diag.get_icmp_statistics()
#pprint(out)
#out = diag.delete_icmp_statistics()
#pprint(out)
#out = diag.show_tsr_conf()
#pprint(out)
#tsr = {
#    'arp_cache': True,
#    'atp_cache': False,
#    'debug_info': True,
#    'dhcp_bindings': False,
#    'ip_stack_info': False,
#    'vpn_keys': True
#}
#out = diag.conf_tsr(**tsr)
#pprint(out)
#out = diag.send_tsr()
#pprint(out)
#out = diag.export_tsr(server='192.168.168.169', user='root', password='password')
#pprint(out)

host, sever_type = '1.2.4.8', 'dns3'
#servers_info = {
#    'gw': (0, 0, 0),
#    'dns1': (1, 1, 0),
#    'dns2': (1, 1, 1),
#    'dns3': (1, 1, 2),
#    'ntp1': (2, 2, 0),
#    'ntp2': (2, 2, 1),
#    'msw': (4, 3, 0),
#    'lm': (4, 4, 0),
#    'cfs': (6, 5, 0),
#}
# resp = diag.connect_server_by_type(host, sever_type)

###################### TimeApi ############################
from modules.API.system import TimeApi
time = TimeApi(fw)

#out = time.show_time()
#pprint(out)
#time_info = {
#    'use_ntp': True,
#    'ntp_update_interval': 120
#}
#out = time.edit_time(**time_info)
#pprint(out)
time_json = {
    "time": {
        "use_ntp": False,
        "time": "10:00:39",
        "date": "2020:04:23",
        "time_zone": "pacific-time",
        "daylight_savings": True,
        "universal": False,
        "international_format": False,
        "only_custom_ntp": False,
        "ntp_update_interval": 60
    }
}
rc = time.set_time(**time_json)
time_json = {
    "time": {
        "use_ntp": True
    }
}
time.set_time(**time_json)
#out = time.show_ntp_server()
#pprint(out)
#server = {
#    'name': 'test3',
#    'md5': {
#        'key_number': 8,
#        'password': '4,9004e94212aa01bea4c3df3f84be1df4265bf7f188980992708e636afad88269825267ff13fea8f4',
#        'trust_key_no': 8
#    }
#}
#out = time.add_ntp_server(**server)
#pprint(out)
#server = {
#    'name': 'test3',
#    'no_auth': True,
#    'md5': {
#    }
#}
#out = time.edit_ntp_server(**server)
#pprint(out)
#out = time.delete_ntp_server('test3')
#pprint(out)

###################### RestartApi ############################
from modules.API.system import RestartApi
restart = RestartApi(fw)

#out = restart.restart_now()
#pprint(out)
#out = restart.restart_at('20190905000000') # YYYY-MM-DD-hh-mm-ss, '-' can be all kinds non-word.
#pprint(out)                                # also can be empty
#out = restart.restart_in(4, 'days') # para1 is an int, para2 can be days, hours, minutes
#pprint(out)

###################### CertificateApi ############################
from modules.API.system import CertificateApi
cert = CertificateApi(fw)

out = cert.show_certs()
pprint(out)
#out = cert.show_imported_certs() # # # Not work
#pprint(out)
#out = cert.show_builtin_certs() # # # Not work
#pprint(out)
#out = cert.show_cert('ComSign CA')
#pprint(out)
#ca = {
#    "alias": "test_ca",
#    "distinguished_name": {
#        "element1": {
#            "country": "AF",
#            #"state": "string",
#            #"locality": "string",
#            #"organization": "string"
#        },
#        "element2": {
#            #"country": "string",
#            "state": "US",
#            #"locality": "string",
#            #"organization": "string",
#            #"department": "string"
#        },
#        "element3": {
#            "locality": "SH",
#            #"organization": "string",
#            #"department": "string",
#            #"group": "string",
#            #"team": "string"
#        },
#        "element4": {
#            "organization": "SNWL",
#            #"department": "string",
#            #"group": "string",
#            #"team": "string",
#            #"common_name": "string",
#            #"serial": "string",
#            #"email": "string"
#        },
#        "element5": {
#            "department": "DEV",
#            #"group": "string",
#            #"team": "string",
#            #"common_name": "string",
#            #"serial": "string",
#            #"email": "string"
#        },
#        "element6": {
#            "group": "SONICCOS",
#            #"team": "string",
#            #"common_name": "string",
#            #"serial": "string",
#            #"email": "string"
#        },
#        "element7": {
#            "team": "AUTO",
#            #"common_name": "string",
#            #"serial": "string",
#            #"email": "string"
#        },
#        "element8": {
#            "common_name": "CN",
#            #"serial": "string",
#            #"email": "string"
#        }
#    },
#    "alternate_name": {
#        "domain_name": "sonicwall.com",
#        #"email": "string",
#        #"ipv4_address": "string"
#    },
#    "signature_algorithm": "sha-1", # md5 | sha-1 | sha-256 | sha-384 | sha-512
#    "key": {
#      "type": "rsa", # rsa | ecdsa
#      "size": 2048 # 1024 | 1536 | 2048 | 4096
#    },
#    "generate": True
#}
#out = cert.generate_req(**ca)
#pprint(out)
#out = cert.no_enrollment() # # # Not work
#pprint(out)
#out = cert.export_req_ftp('192.168.168.169', 'root', 'password', 'test_ca')
#pprint(out)
#out = cert.export_req_scp('192.168.168.169', 'root', 'password', 'test_ca')
#pprint(out)

out = cert.import_cert_local(cert_path="@/tmp/vsftpd_2k.p12", name="test", password="password")
pprint("---------------")
pprint(out)
pprint("---------------")
