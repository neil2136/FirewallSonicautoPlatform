import re
import os
import copy
import time
import subprocess
import requests
import json
from collections import OrderedDict
from pprint import pprint
from utm import is_Firewall_up
from runner.settings import logger

def encode_url(url: str):
    if ' ' in url:
        url = url.replace(' ', '%20')
    if '//' in url:
        url = url.replace('//', '%2f%2f')
    return url

def encode_http_url(url: str):  # used for def import_crl_urlper    add by JLian
    if ' ' in url:
        url = url.replace(' ', '%20')
    if ":" in url:
        url = url.replace(':', '%3A')
    if '/' in url:
        url = url.replace('/', '%2F')
    return url

class StatusApi:
    '''SystemApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/reporting/status/system'

    def show_status(self):
        return self.fw.api_get(self.url)

    def show_version(self):
        url = 'api/sonicos/version'
        return self.fw.api_get(url)

    def show_security_services(self):
        url = 'api/sonicos/reporting/status/security-services'
        return self.fw.api_get(url)

class LicenseApi:
    '''LicenseApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/license'

    def show_license(self):
        url= 'api/sonicos/reporting/license'
        return self.fw.api_get(url)

    def show_license_setting(self):
        url = self.url + '/base'
        return self.fw.api_get(url)
    
    def show_license_register(self):
        url = 'api/sonicos/license/registration-code'
        return self.fw.api_get(url)
    
    def show_license_security_services(self):
        url = 'api/sonicos/reporting/license/security-services'
        return self.fw.api_get(url)    

    def update_license_setting(self, msg=False, keys=[]):
        url = self.url + '/base'
        input_json = {'license': {'upgrade': []}}
        input_json['license']['upgrade'] = keys
        if len(keys):
            return self.fw.api_put(url, msg, input_json)
        else:
            return self.fw.api_put(url)

    def sync_license(self, msg=False):
        url = self.url + '/synchronize'
        return self.fw.api_post(url, msg)


class AdminApi:
    '''AdminApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/administration'
        self.non_config_url = 'api/sonicos/non-config-mode'
        self.config_url = 'api/sonicos/config-mode'
        self.start_mgmt = 'api/sonicos/start-management'
        
        self.init_admin_json = {
            "administration": {
                # "firewall_name": "",
                "local_user_lockout": False,
                # "log_without_lockout": True,
                # "http_port": 80,
                "firewall_domain_name": "",
                "idle_logout_time": 60,
                "inter_admin_messaging": {},
                "multiple_admin": False,
                "enhanced_audit_logging": False,
                # "wireless_controller_mode": "normal-firewall",
                "dashboard_as_starting_page": False,
                "tls_and_above": False,
                "out_of_band_management": False,
                "https_port": 443,
                "admin": {
                    "name": "admin",
                    "one_time_password": {
                        # "totp": True
                    },
                    "preempt_action": "goto-non-config",
                    "preempt_inactivity_timeout": 10
                },
                "password": {
                    "enforce_character_difference": False,
                    "minimum_length": 8,
                    "aging": {
                        # "duration": 0
                    },
                    "complexity": {
                        # "type": "alpha-and-numeric",
                        # "upper_case": 0,
                        # "lower_case": 0,
                        # "digital": 0,
                        # "symbolic": 0
                    },
                    "uniqueness": {
                        # "count": 0
                    },
                    "constraints_apply_to": {
                        "builtin_admin": True,
                        "full_admins": True,
                        "limited_admins": True,
                        "local_users": True,
                        "guest_admins": True,
                        # "system_admins": True,
                        # "crypto_admins": True,
                        # "audit_admins": True
                    }
                },
                "gms_management": {
                    # 'ipsec_tunnel': {
                    #     'authentication_key': '4e6319ec55f0bcc88f53696d6b212e4f',
                    #     'behind_nat_device': {},
                    #     'encryption_key': 'ad8969dd3acc0fe3',
                    #     'encryption_type': 'des-md5',
                    #     'heartbeat_status_only': False,
                    #     'spi': 'C0EAE4E1FD8C',
                    #     'syslog_server_port': 514
                    # }
                },
                "user_lockout": {
                    "enable": False,
                    "failures_rate": 5,
                    "failures_duration": 1,
                    "lockout_duration": 5
                 },
                "web_management": {
                    "allow_http": False,
                    "certificate": {'use_self_signed': True},
                    "cert_common_name": "192.168.168.168",
                    "client_certificate_check": False,
                    # "client_certificate_issuer": "",
                    # "ocsp_check": {
                    #     "responder_URL": ""
                    # },
                    "default_table_size": 50,
                    "refresh_interval": 10,
                    "tooltip": {
                        "form_delay": 2000,
                        "button_delay": 3000,
                        "text_delay": 500
                    }
                },
               # "override_download_url": {
               #     "sonicpoint": {
               #         "n": "",
               #         "nv": "",
               #         "ndr": "",
               #         "ac": ""
               #     }
               # },
                "language_override": {
                    "english": True
                },
                "ssh": {
                    "port": 22
                }
            }
        }
        self.init_pwd_json = {
            "administration": {
                "admin_password": {
                    "old": "",
                    "new": ""
                }
            }
        }
    def show_admin_setting(self):
        url = self.url + '/global'
        return self.fw.api_get(url)

    def conf_admin(self, msg=False, **kwargs):
        url = self.url + '/global'
        input_json = {}
        pprint(kwargs)
        # input_json = copy.deepcopy(self.init_admin_json)
        input_json = self.show_admin_setting()
        input_json['administration'].update(kwargs)

        if "enforce_http_host_check" in kwargs:
            input_json['administration']["enforce_http_host_check"] = kwargs["enforce_http_host_check"]
        if 'firewall_name' not in kwargs.keys():
            out = self.show_admin_setting()
            input_json['administration']['firewall_name'] = out['administration']['firewall_name']
        if 'language_override' in kwargs.keys() and not kwargs['language_override']:
            input_json['administration']['language_override'].clear()
        if 'http_port' in kwargs.keys():
            input_json['administration']['http_port'] = kwargs['http_port']
        if 'ssh_port' in kwargs.keys():
            input_json['administration']['ssh']['port'] = kwargs['ssh_port']
        if 'force_through_interface' in kwargs.keys() and 'any' in input_json['administration']['force_through']:
            del input_json['administration']['force_through']['any']
            input_json['administration']['force_through']['interface'] = kwargs['force_through_interface']
        elif 'force_through_interface' in kwargs.keys() and 'interface' in input_json['administration']['force_through']:
            input_json['administration']['force_through']['interface'] = kwargs['force_through_interface']
        elif 'force_through_any' in kwargs.keys():
             input_json['administration']['force_through']['any'] = kwargs['force_through_any']
        return self.fw.api_put(url, msg, data=input_json)
    
    def conf_admin_update(self, msg=False, **kwargs):
        url = self.url + '/global'
        json_input = copy.deepcopy(kwargs)
        return self.fw.api_put(url, msg, data=json_input)

    def edit_admin(self, msg=False, **kwargs):
        url = self.url + '/global'
        input_json = self.show_admin_setting()
        input_json.update(kwargs)
        if 'language_override' in kwargs.keys() and not kwargs['language_override']:
            input_json['administration']['language_override'].clear()
        if 'web_management' in kwargs['administration'].keys():
            if 'allow_http' in kwargs['administration']['web_management'].keys() and \
               not kwargs['administration']['web_management']['allow_http'] and 'http_port' in input_json['administration'].keys():
                input_json['administration'].pop('http_port')
            if 'certificate' in kwargs['administration']['web_management'].keys():
                input_json['administration']['web_management']['certificate'] = {'name':kwargs['administration']['web_management']['certificate']}
            if 'client_certificate_check' in kwargs['administration']['web_management'].keys() and \
               not kwargs['administration']['web_management']['client_certificate_check']:
                if 'client_certificate_issuer' in input_json['administration']['web_management'].keys():
                    input_json['administration']['web_management'].pop('client_certificate_issuer')
                if 'ocsp_check' in input_json['administration']['web_management'].keys():
                    input_json['administration']['web_management'].pop('ocsp_check')
        if 'user_lockout' in kwargs['administration'].keys() and not kwargs['administration']['user_lockout']:
            input_json['administration']['user_lockout'].clear()
        if 'gms_management' in kwargs['administration'].keys() and not kwargs['administration']['gms_management']:
            input_json['administration']['gms_management'].clear()
        if 'password' in kwargs['administration'].keys() and 'complexity' in kwargs['administration']['password'].keys() and \
           not kwargs['administration']['password']['complexity']:
            input_json['administration']['complexity'].clear()
        if 'password' in kwargs['administration'].keys() and 'complexity' in kwargs['administration']['password'].keys() and \
           not kwargs['administration']['password']['constraints_apply_to']:
            input_json['administration']['complexity'].clear()
        if 'admin' in kwargs['administration'].keys() and \
           'one_time_password' in kwargs['administration']['admin'].keys() and not kwargs['administration']['admin']['one_time_password']:
            input_json['administration']['admin']['one_time_password'].clear()
        return self.fw.api_put(url, msg, data=input_json)

    def unbind_totp_key(self, msg=False):
        url = self.url + '/unbind-totp-key'
        return self.fw.api_post(url, msg)
    
    def unbind_totp_key_with_name(self,name,msg=False):
        url = self.url + '/unbind-totp-key' + '/' + name
        return self.fw.api_post(url, msg)
    
    def change_password(self, msg=False, **kwargs):
        url = self.url + '/password'
        input_json = {}
        input_json = copy.deepcopy(self.init_pwd_json)
        # input_json['administration'].update(kwargs)
        input_json['administration']['admin_password']['old'] = kwargs['old_pwd']
        input_json['administration']['admin_password']['new'] = kwargs['new_pwd']
        pprint(input_json)
        return self.fw.api_post(url, msg, data=input_json)
        
    def set_non_config_mode(self,msg=False):
        res = self.fw.api_post(self.non_config_url, msg,data={})
        return res
        
    def set_config_mode(self,msg=False):
        res = self.fw.api_post(self.config_url, msg,data={})
        return res


    def set_mgmt_mode(self, msg=False):
        res = self.fw.api_post(self.start_mgmt, msg, data={})
        return res


class SNMPApi:
    '''SNMPApi Class'''
    default_options = {
        ### ----- view settings -----
        'view_name': '',
        'oid_list': [],                 # oid list under one name, like ['2.3','2.4']
        ### ----- user settings -----
        'user_name': '',
        # 'user_new_name': '',          # new user name need to be changed
        'user_security': '',            # None, authentication_only, authentication_and_privacy
        'user_auth_method': 'md5',      # md5, sha1, only for AO, AP
        'user_auth_key': '',            # key length in [8, 32], only for user_auth_method
        'user_encrypt_method': 'aes',   # aes, des, only for AP
        'user_priv_key': '',            # key length in [8, 32], only for user_encrypt_method
        'user_group': '',
        ### ----- access settings -----
        'access_name': '',
        # 'access_new_name': '',        # new access name need to be changed
        'access_security': '',          # None, authentication_only, authentication_and_privacy
        'access_view': '',              # view oid: root, system,...
        'access_group': ''
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/snmp'
        self.url_base = self.url + '/base'
        self.url_view = self.url + '/views'
        self.url_user = self.url + '/users'
        self.url_access = self.url + '/accesses'
        self.init_snmp_json = {
            'snmp': {
                'asset_number': '',
                'get_community_name': 'public',
                'host_1': '',
                'host_2': '',
                'host_3': '',
                'host_4': '',
                'snmp3': {
                    'engine_id': '8000222503C0EAE488B08A',
                    'increase_subsystem_priority': False,
                    'mandatory': False
                },
                'system_contact': '',
                'system_location': '',
                'system_name': '',
                'trap_community_name': ''
            }
        }

        self.init_user_json = {
            'snmp' : {
                'user' : {
                    'name' : 'name',
                    'security_level' : {},
                    'group' : ''
                }
            }
        }
        self.init_view_json = {
            'snmp': {
                'view': [
                    {
                        'name': '',
                        'oid': ''
                    }
                ]
            }
        }

        self.init_user_json_new = {
            'snmp': {
                'user': [
                    {
                        'name': '',
                        'security_level': {},
                        # 'authentication': {'md5': ''}, ### only for authentication_only and authentication_and_privacy
                        # 'encryption': {'aes': ''},     ### only for authentication_and_privacy
                        'group': ''
                    }
                ]
            }
        }

        self.init_access_json = {
            'snmp': {
                'access': [
                    {
                        'name': '',
                        'security_level': {},
                        'read_view': '',
                        'master_group': ''
                    }
                ]
            }
        }

    ### New version configs rewritten by Celia, recommend to use this #
    ### ------------------------ Base configure
    def snmp_base_settings(self, msg=False, **kwargs):
        json_input = dict(self.show_snmp())
        if 'snmp' not in json_input.keys():
            logger.error('ERROR: Fail to get snmp base setting!')
            json_input = copy.deepcopy(self.init_snmp_json)
        json_input['snmp'].update(kwargs)
        return self.fw.api_put(self.url_base, msg, data=json_input)
        
    def snmp_config(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        config = self.fw.api_put(self.url_base, msg, data=json_input)
        return config

    def snmp_advance_settings(self, msg=False, **kwargs):
        json_input = dict(self.show_snmp())        
        if 'snmp' not in json_input.keys():
            logger.error('ERROR: Fail to get snmp base setting!')
            json_input = copy.deepcopy(self.init_snmp_json)
        elif 'snmp3' not in json_input['snmp'].keys():
            logger.error('ERROR: Fail to get snmp advance setting!')
            json_input['snmp']['snmp3'] = copy.deepcopy(self.init_snmp_json['snmp']['snmp3'])
        json_input['snmp']['snmp3'].update(kwargs)
        return self.fw.api_put(self.url_base, msg, data=json_input)

    ### ------------------------ Group: edit
    def snmp_group_edit(self, msg=False, name='', new_name=''):
        # input a new group name
        init_json = {'snmp': {}}
        if not (name and new_name):
            logger.info("Please input group name and new name!")
            return False
        url = self.url + '/groups/name/' + name
        init_json['snmp'] = {'group': [{'name': new_name}]}
        if msg:
            rc, msg = self.fw.api_put(url, msg=True, data=init_json)
            return rc, msg
        rc = self.fw.api_put(url, msg=False, data=init_json)
        return rc

    ### ------------------------ View: add, delete
    def build_json_view(self, **kwargs):
        logger.info(f"kwargs to build view json: {kwargs}")
        json_input = copy.deepcopy(self.init_view_json)
        try:
            path = json_input['snmp']['view']
            # config oid(including multiple oids) and name
            oid_list = kwargs['oid_list']
            if len(oid_list):
                path[:] = []
                for i in range(len(oid_list)):
                    new_oid = {
                        'name': kwargs['view_name'],
                        'oid': oid_list[i]
                    }
                    path.append(new_oid)
            json_input['snmp']['view'] = path
        except KeyError as e:
            logger.error(f"Invalid key '{e}': In building JSON for SNMP view!")
        logger.info("SNMP view json obtained: ")
        logger.info(json_input)
        return json_input

    def snmp_view_add(self, msg=False, **kwargs):
        # json = {"snmp":{"view":[{"name":"test2","oid":"1.2.3"},{"name":"test2","oid":"1.2.4"}]}}
        # Not support to edit view name
        # if you want to edit oids, please delete old view, then add a new view with the same name
        options = dict(SNMPApi.default_options)
        options.update(kwargs)
        json_input = self.build_json_view(**options)
        return self.fw.api_post(self.url_view, msg, data=json_input)

    def snmp_view_delete(self, msg=False, **kwargs):
        options = dict(SNMPApi.default_options)
        options.update(kwargs)
        json_input = self.build_json_view(**options)
        return self.fw.api_delete(self.url_view, msg, data=json_input)

    ### ------------------------ User: add, edit & delete
    def find_user(self, name):
        json_get = self.fw.api_get(self.url_user)
        if not json_get.get('snmp') or not json_get['snmp'].get('user'):
            logger.error('No snmp user found.')
            return -1, {}
        for user in enumerate(json_get['snmp']['user']):
            location = user[0]
            if json_get['snmp']['user'][location].get('name') == name:
                break
        else:
            logger.error('Not found the specific user.')
            return -1, {}
        return location, json_get

    def build_json_user(self, edit_json={}, **kwargs):
        # kwargs, dict, user parameters
        # example: {'user_name': 'UserTest', 'user_new_name': 'UserEdit', 'user_security': 'authentication_and_privacy', 'user_auth_method': 'sha1', 'user_auth_key': '12345678', 'user_encrypt_method': 'des', 'user_priv_key': 'abcdefgh', 'user_group': 'Group'}
        logger.info(f"kwargs to build user base json: {kwargs}")
        json_input = copy.deepcopy(self.init_user_json_new)
        path = edit_json if edit_json else json_input['snmp']['user'][0]
        # config name and new_name
        path['name'] = kwargs['user_new_name'] if 'user_new_name' in kwargs else kwargs['user_name']
        # config security
        if 'user_security' in kwargs:
            path['security_level'] = {kwargs['user_security']: True} if kwargs['user_security'] else {}
            if 'authentication_and_privacy' not in path['security_level'] and 'encryption' in path:
                path.pop('encryption')
                if not path['security_level']:
                    path.pop('authentication')
        # config auth
        if path['security_level'] and 'user_auth_key' in kwargs:
            if 'user_auth_method' in kwargs:
                path['authentication'] = {kwargs['user_auth_method']: kwargs['user_auth_key']}
            else:
                for auth in ['md5', 'sha1']:
                    if auth in path['authentication']:
                        path['authentication'][auth] = kwargs['user_auth_key']
        # config encrypt
        if 'authentication_and_privacy' in path['security_level'] and 'user_priv_key' in kwargs:
            if 'user_encrypt_method' in kwargs:
                path['encryption'] = {kwargs['user_encrypt_method']: kwargs['user_priv_key']}
            else:
                for encrypt in ['aes', 'des']:
                    if encrypt in path['encryption']:
                        path['encryption'][encrypt] = kwargs['user_priv_key']
        # config user group
        if 'user_group' in kwargs:
            path['group'] = kwargs['user_group']
        json_input['snmp']['user'][0] = path
        logger.info("SNMP user json obtained: ")
        logger.info(json_input)
        return json_input

    def snmp_user_add(self, msg=False, **kwargs):
        # kwargs: refer to kwargs comment in build_json_user()
        options = dict(SNMPApi.default_options)
        options.update(kwargs)
        json_input = self.build_json_user(**options)
        return self.fw.api_post(self.url_user, msg, data=json_input)

    def snmp_user_edit(self, msg=False, **kwargs):
        # kwargs: refer to kwargs comment in build_json_user()
        if 'user_name' not in kwargs:
            logger.error("ERROR: Please input a valid 'user_name' to edit!")
            return False
        location, json_get = self.find_user(name=kwargs['user_name'])
        if not json_get:
            return False
        path = json_get['snmp']['user'][location]
        json_input = self.build_json_user(edit_json=path, **kwargs)
        return self.fw.api_put(self.url_user + '/name/' + kwargs['user_name'], msg, data=json_input)

    def snmp_user_delete(self, msg=False, name=""):
        if not name:
            logger.error("ERROR: Please input valid name to delete!")
            return False
        location, json_get = self.find_user(name=name)
        if not json_get:
            return False
        group = json_get['snmp']['user'][location].get('group')
        json_input = self.build_json_user(**{'user_name': name, 'user_group': group})
        return self.fw.api_delete(self.url_user, msg, data=json_input)

    # ------------------------ Access: add, edit & delete
    def find_access(self, name):
        json_get = self.fw.api_get(self.url_access)
        if not json_get.get('snmp') or not json_get['snmp'].get('access'):
            logger.error('No snmp access found.')
            return -1, {}
        for access in enumerate(json_get['snmp']['access']):
            location = access[0]
            if json_get['snmp']['access'][location]['name'] == name:
                break
        else:
            logger.error('Not found the specific access.')
            return -1, {}
        return location, json_get

    def build_json_access(self, edit_json={}, **kwargs):
        # kwargs, dict, access parameters
        # example: {'access_name': 'AccessTest', 'access_new_name': 'AccessEdit', 'access_security': '', 'access_view': 'root', 'access_group': 'Group'}
        logger.info(f"kwargs to build access json: {kwargs}")
        json_input = copy.deepcopy(self.init_access_json)
        path = edit_json if edit_json else json_input['snmp']['access'][0]
        # config access name and edit new name
        path['name'] = kwargs['access_new_name'] if 'access_new_name' in kwargs else kwargs['access_name']
        # config access security level
        if 'access_security' in kwargs:
            path['security_level'] = {kwargs['access_security']: True} if kwargs['access_security'] else {}
        # config access view
        if 'access_view' in kwargs:
            path['read_view'] = kwargs['access_view']
        # config access group
        if 'access_group' in kwargs:
            path['master_group'] = kwargs['access_group']
        json_input['snmp']['access'][0] = path
        logger.info("SNMP access json obtained: ")
        logger.info(json_input)
        return json_input

    def snmp_access_add(self, msg=False, **kwargs):
        # kwargs: refer to kwargs comment in build_json_access()
        options = dict(SNMPApi.default_options)
        options.update(kwargs)
        json_input = self.build_json_access(**options)
        return self.fw.api_post(self.url_access, msg, data=json_input)

    def snmp_access_edit(self, msg=False, **kwargs):
        # kwargs: refer to kwargs comment in build_json_access()
        if 'access_name' not in kwargs:
            logger.error("ERROR: Please input a valid 'access_name' to edit!")
            return False
        location, json_get = self.find_access(name=kwargs['access_name'])
        if not json_get:
            return False
        path = json_get['snmp']['access'][location]
        json_input = self.build_json_access(edit_json=path, **kwargs)
        return self.fw.api_put(self.url_access + '/name/' + kwargs['access_name'], msg, data=json_input)

    def snmp_access_delete(self, msg=False, name=""):
        if not name:
            logger.error("ERROR: Please input valid name to delete!")
            return False
        location, json_get = self.find_access(name=name)
        if not json_get:
            return False
        path = json_get['snmp']['access'][location]
        json_input = self.build_json_access(edit_json=path, **{'access_name': name, 'access_security': {}})
        return self.fw.api_delete(self.url_access, msg, data=json_input)

# -------------------- rewritten by jxia #
# on page -> SNMP
    def show_snmp(self):
        # result = {"snmp":{"enable":true,"system_name":"automation","system_contact":"test","system_location":"Shanghai","asset_number":"12345678","get_community_name":"public","trap_community_name":"public_trap","host_1":"","host_2":"","host_3":"","host_4":"","snmp3":{"mandatory":true,"engine_id":"80002225032CB8ED6D7FE0","increase_subsystem_priority":false}}}
        url = self.url + '/base'
        return self.fw.api_get(url)

    def show_engineid(self):
        output = self.show_snmp()
        logger.info(output)
        engine_id = output["snmp"]["snmp3"]["engine_id"]
        return engine_id

    def enable_snmp(self):
        url = self.url + '/base'
        enable_json = {
            "snmp": {
                "enable": True
                }
        }
        rc = self.fw.api_put(url, msg=False, data=enable_json)
        return rc

    def disable_snmp(self):
        url = self.url + '/base'
        disable_json = {"snmp":{"enable":False}}
        return self.fw.api_put(url, msg=False, data=disable_json)

    def configure_snmp(self, msg=False, **kwargs):
        # kwargs = config_json
        # config_json = {
        #   "snmp":{
        #     "enable":True,
        #     "system_name":"111",
        #     "system_contact":"222",
        #     "system_location":"333",
        #     "asset_number":"12345678",
        #     "get_community_name":"public",
        #     "trap_community_name":"",
        #     "host_1":"",
        #     "host_2":"",
        #     "host_3":"",
        #     "host_4":"",
        #     "snmp3":{
        #       "mandatory":True,
        #       "engine_id":"80002225032CB8ED6D7FE0",
        #       "increase_subsystem_priority":True
        #     }
        #   }
        # }
        url = self.url + '/base'
        input_json = copy.deepcopy(kwargs)
        return self.fw.api_put(url, msg, data=input_json)

# on page -> View
    def show_snmp_view(self):
        url = self.url + '/views'
        return self.fw.api_get(url)

    def config_view(self, msg=False, **kwargs):
        # json = {"snmp":{"view":[{"name":"test2","oid":"12345"}]}}
        # if you want to modify oid or name... modify your input kwargs, do not use api_put on this page
        url = self.url + '/views'
        input_json = copy.deepcopy(kwargs)
        return self.fw.api_post(url, msg, data=input_json)

    def delete_view(self, msg=False, **kwargs):
        # input kwargs make sure be your input_json in self.config_view()
        url = self.url + '/views'
        del_json = copy.deepcopy(kwargs)
        return self.fw.api_delete(url, msg, data=del_json)

# on page -> User/Group
    # Group
    def show_snmp_group(self):
        url = self.url + '/groups'
        return self.fw.api_get(url)

    def add_snmp_group(self, msg=False, name=''):
        #json = {"snmp":{"group":[{"name":"group1"}]}}
        # add_snmp_group(name='group1')
        url = self.url + '/groups'
        init_json = {'snmp': {}}
        if name:
            init_json['snmp'] = {'group': [{'name': name}]}
        else:
            logger.info("Please input group name!")
            return False
        return self.fw.api_post(url, msg, data=init_json)

    def delete_snmp_group(self, msg=False, name=''):
        # delete_snmp_group(name='group1')
        url = self.url + '/groups'
        init_json = {'snmp': {}}
        if name:
            init_json['snmp'] = {'group': [{'name': name}]}
        else:
            logger.info("Please input group name!")
            return False
        return self.fw.api_delete(url, msg, data=init_json)

    def edit_snmp_group(self, msg=False, name=''):
        # input a new group name
        url = self.url + '/groups'
        init_json = {'snmp': {}}
        if name:
            init_json['snmp'] = {'group': [{'name': name}]}
        else:
            logger.info("Please input group name!")
            return False
        return self.fw.api_put(url, msg, data=init_json)

    # User
    def show_snmp_user(self):
        url = self.url + '/users'
        return self.fw.api_get(url)

    def add_snmp_user(self, msg=False, **kwargs):
        url = self.url + '/users'
        input_json = copy.deepcopy(kwargs)
        return self.fw.api_post(url, msg, data=input_json)

    def delete_snmp_user(self, msg=False, **kwargs):
        # user_json = {"snmp": {"user": [
        #     {"name": "test1", "authentication":
        #         {"md5": "12345678"},
        #      "security_level":
        #          {"authentication_only": True},
        #      "group": "group1"}]}}
        url = self.url + '/users'
        del_json = {"snmp": {"user": [{"name": kwargs["snmp"]["user"][0]["name"], "security_level":{}, "group": kwargs["snmp"]["user"][0]["group"]}]}}
        logger.info(del_json)
        return self.fw.api_delete(url, msg, data=del_json)

# on page -> Access
    def show_snmp_access(self):
        url = self.url + '/accesses'
        return self.fw.api_get(url)

    def delete_access(self, msg=False, **kwargs):
        # access_json = {"snmp": {"access": [
        #     {"name": "Access1",
        #      "read_view": "root",
        #      "master_group": "group1",
        #      "security_level":
        #          {"authentication_only": True}}]}}
        url = self.url + '/accesses'
        #del_json = {"snmp": {"access": [{"name": kwargs["snmp"]["access"][0]["name"], "read_view": kwargs["snmp"]["access"][0]["read_view"], "master_group": kwargs["snmp"]["access"][0]["master_group"], "security_level":{}}]}}
        return self.fw.api_delete(url, msg, data=kwargs)

    def add_access(self, msg=False, **kwargs):
        url = self.url + '/accesses'
        input_json = copy.deepcopy(kwargs)
        return self.fw.api_post(url, msg, input_json)

    def edit_access(self, msg=False, **kwargs):
        # make sure access is existed
        url = self.url + '/accesses'
        input_json = copy.deepcopy(kwargs)
        return self.fw.api_put(url, msg, input_json)

# ------------------------ old version----------------------------------
    def edit_snmp(self, msg=False, **kwargs):
        url = self.url + '/base'
        init_json = self.show_snmp()
        if not init_json['snmp']:
            init_json = copy.deepcopy(self.init_snmp_json)
        init_json['snmp'].update(kwargs)
        return self.fw.api_put(url, msg, data=init_json)

    def edit_snmp_user(self, msg=False, **kwargs):
        url = self.url + '/users'
        init_json = self.show_snmp_user()
        if not init_json['snmp']:
            logger.error('No snmp user found.')
            return False
        if 'name' not in kwargs.keys():
            logger.error('Please specify an user name')
            return False
        found = 0
        for i in range(0, len(init_json['snmp']['user'])):
            if init_json['snmp']['user'][i]['name'] == kwargs['name']:
                init_json['snmp']['user'][i].update(kwargs)
                if 'security_level' in kwargs.keys():
                    if not kwargs['security_level']:
                        if 'authentication' in init_json['snmp']['user'][i].keys():
                            init_json['snmp']['user'][i].pop('authentication')
                        if 'encryption' in init_json['snmp']['user'][i].keys():
                            init_json['snmp']['user'][i].pop('encryption')
                    elif 'authentication_only' in kwargs['security_level'].keys():
                        if 'encryption' in init_json['snmp']['user'][i].keys():
                            init_json['snmp']['user'][i].pop('encryption')
                found = 1
                break
        if not found:
            logger.error('Not found the user.')
            return False
        return self.fw.api_put(url, msg, data=init_json)

    def add_snmp_view(self, msg=False, **kwargs):
        url = self.url + '/views'
        init_json = { 'snmp': { 'view': kwargs } }
        return self.fw.api_post(url, msg, data=init_json)

    def delete_snmp_view(self, msg=False, **kwargs):
        url = self.url + '/views'
        init_json = { 'snmp': { 'view': [kwargs] } }
        return self.fw.api_delete(url, msg, data=init_json)

    def add_snmp_access(self, msg=False, **kwargs):
        url = self.url + '/accesses'
        init_json = {'snmp': {}}
        if kwargs:
            init_json['snmp'] = { 'access': kwargs }
        return self.fw.api_post(url, msg, data=init_json)

    def edit_snmp_access(self, msg=False, **kwargs):
        url = self.url + '/accesses'
        init_json = self.show_snmp_access()
        if not init_json['snmp']:
            logger.error('No snmp access found.')
            return False
        if 'name' not in kwargs.keys():
            logger.error('Please specify an access name')
            return False
        found = 0
        for i in range(0, len(init_json['snmp']['access'])):
            if init_json['snmp']['access'][i]['name'] == kwargs['name']:
                init_json['snmp']['access'][i].update(kwargs)
                found = 1
                break
        if not found:
            logger.error('Not found the access.')
            return False
        return self.fw.api_put(url, msg, data=init_json)

    def delete_snmp_access(self, name, msg=False):
        url = self.url + '/accesses'
        init_json = { 'snmp': { 'access': [{ 'name': str(name) }] } }
        return self.fw.api_delete(url, msg, data=init_json)


class SettingApi:
    '''SettingSpi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/firmware'
        self.url_bk = 'api/sonicos/'
        self.init_firmware_json = {
            "firmware": {
                "auto": {
                    "update": True,
                    "download": False
                },
                "diagnostics": False
            }
        }
        self.initial_local_bk_json = {
            "local_backup": {
                "create": None,
                "comment": None,
            }
        }
        self.initial_local_bk_gold_json = {
            "local_backup": {
                "gold": False,
                "name": None,   ### backup name
            }
        }

    def create_local_backups(self, msg=False, **kwargs):
        if 'name' in kwargs.keys() and kwargs['name']:
            lc_bk = self.url_bk + 'local/backups/name/' + kwargs['name']
        else:
            lc_bk = self.url_bk + 'local/backups'

        json_input = self.build_json_local_bk(**kwargs)
        local_bk_resp = self.fw.api_post(lc_bk, msg, data=json_input)
        return local_bk_resp

    def build_json_local_bk(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_local_bk_json)
            json_input['local_backup']['create'] = kwargs['create']
            json_input['local_backup']['comment'] = kwargs['comment']
        except KeyError:
            logger.error('Error: In creating JSON for local backup object')
        return json_input

    def show_firmware_and_settings(self):
        url = self.url_bk + 'dynamic-file/getFwExpList.json?type=1'
        return self.fw.api_get(url)
    
    def show_firmware_update_status(self):
        url = 'api/sonicos/reporting/firmware-update'
        return self.fw.api_get(url)
    
    def show_firmware(self):
        url = 'api/sonicos/firmware/base'
        return self.fw.api_get(url)

    def delete_local_backups(self, name, msg=False):
        lc_bk = self.url_bk + 'local/backups/name/' + name
        return self.fw.api_delete(lc_bk, msg)
        
    def delete_local_backups_new(self, name, msg=False):
        lc_bk = self.url_bk + 'local-backups/version/' + name
        return self.fw.api_delete(lc_bk, msg)

    def download_local_backups(self, name, msg=False):
        lc_bk = self.url_bk + 'export/local-backup-firmware/version/' + name
        return self.fw.api_get(lc_bk, msg)

    def local_bk_gold(self, msg=False, **kwargs):
        json_input = copy.deepcopy(self.initial_local_bk_gold_json)
        try:
            json_input['local_backup']['gold'] = kwargs['gold']
            json_input['local_backup']['name'] = kwargs['name']
        except KeyError:
            logger.error('Error: In creating JSON for local backup object')
        lc_bk = self.url_bk + 'local-backup-gold'
        return self.fw.api_put(lc_bk, msg, data=json_input)

    def show_local_backup_boot_file(self, bk_name):
        lc_bk = self.url_bk + 'local-backup-boot/name/' + bk_name
        return self.fw.api_get(lc_bk)

    def boot_local_backup(self, bk_name):
        lc_bk = self.url_bk + 'local-backup-boot/name/' + bk_name
        return self.fw.api_post(lc_bk)

    def edit_bk_comment(self, msg=False, **kwargs):
        url = self.url_bk + 'local-backup-comment'
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        edit_bk_comment_resp = self.fw.api_put(url, msg, data=json_input)
        return edit_bk_comment_resp

    def show_firmware(self):
        url = self.url + '/base'
        return self.fw.api_get(url)

    def edit_firmware(self, msg=False, **kwargs):
        url = self.url + '/base'
        init_json = self.show_firmware()
        init_json['firmware'].update(kwargs)
        return self.fw.api_put(url, msg, init_json)

    def backup_firmware(self, msg=False):
        url = self.url + '/backup'
        return self.fw.api_post(url, msg)

    def export_setting(self, server: str, user: str, password: str, msg=False):
        ftpurl = 'ftp:%2f%2f' + user + ':' + password + '@' + server + '/'
        url = 'api/sonicos/export/current-config/cli/ftp/' + ftpurl
        return self.fw.api_post(url, msg)
        
    def export_setting_exp(self, filepath='/tmp/test.exp'):
        url = 'api/sonicos/export/current-config/exp'
        exp = self.fw.api_get(url, log_switch=False)
        with open(filepath, 'w+') as f:
            f.write(str(exp))
        logger.info('the exp file {} has been exported.'.format(filepath))
        return True

    def export_cur_firmware(self, server: str, user: str, password: str, msg=False):
        ftpurl = 'ftp:%2f%2f' + user + ':' + password + '@' + server + '/'
        url = 'api/sonicos/export/firmware/current/ftp/' + ftpurl
        return self.fw.api_post(url, msg)
        
    def import_setting_exp(self,filepath, max_time=180):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/import/exp'
        self.fw.api_login()
        curl_command = ['curl', '-k', '-i', '-H', "'Content-Type: multipart/form-data' ", 'POST',
             url, '-F', 'importFile=@'+filepath, '--max-time', f'{max_time}']
        logger.info('--------curl command:')
        logger.info(curl_command)
        try:
            resp = subprocess.Popen(curl_command, stdout=subprocess.PIPE).communicate()[0]
            resp = resp.decode('ASCII')

            if not re.search('HTTP/1.1 100 Continue', resp, re.I):
                return False
        except Exception as e:
            logger.info("Firewall may start rebooting after import setting file")
            logger.info(e)

        time.sleep(10)

        result = is_Firewall_up(self.fw.ip, ssh=False)
        if result:
            logger.info('Firewall boots up after exp imported.')
        else:
            logger.info('Error during boot up.')
        return result

    def import_setting_exp_by_message(self,filepath):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/import/exp'
        self.fw.api_login()
        curl_command = ['curl', '-k', '-i', '-H', "'Content-Type: multipart/form-data' ", 'POST',
             url, '-F', 'importFile=@'+filepath, '--max-time', '120']
        logger.info('--------curl command:')
        logger.info(curl_command)
        try:
            resp = subprocess.Popen(curl_command, stdout=subprocess.PIPE).communicate()[0]
            resp = resp.decode('ASCII')
            logger.info(resp)
            return resp
        except Exception as e:
            logger.info("Firewall may start rebooting after import setting file")
            logger.info(e)
            return e

    def upload_firmware(self, filepath):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/import/firmware'
        self.fw.api_login()
        curl_command = ['curl', '-k', '-i', '-u', self.fw.user+':'+self.fw.new_password,
                        '-H', "'Accept: application/json'", '-H', "'Content-Type: multipart/form-data'",
                        '-F', 'firmware=@'+filepath, '-X', 'POST', url, '--max-time', '330']
        logger.info('--------curl command:')
        logger.info(curl_command)
        resp = subprocess.Popen(curl_command, stdout=subprocess.PIPE).communicate()[0]
        resp = resp.decode('ASCII')

        logger.info(resp)
        if not re.search('Firmware uploaded successfully', resp, re.I):
            return False
        logger.info('Upload firmware successfully.')
        return True

    def upload_firmware_by_message(self, filepath):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/import/firmware'
        self.fw.api_login()
        curl_command = ['curl', '-k', '-i', '-u', self.fw.user + ':' + self.fw.new_password,
                        '-H', "'Accept: application/json'", '-H', "'Content-Type: multipart/form-data'",
                        '-F', 'firmware=@' + filepath, '-X', 'POST', url, '--max-time', '330']
        logger.info('--------curl command:')
        logger.info(curl_command)
        resp = subprocess.Popen(curl_command, stdout=subprocess.PIPE).communicate()[0]
        time.sleep(200)
        resp = resp.decode('ASCII')
        return resp

    def export_backup_firmware(self, server: str, user: str, password: str, msg=False):
        ftpurl = 'ftp:%2f%2f' + user + ':' + password + '@' + server + '/'
        url = 'api/sonicos/export/firmware/system-backup/ftp/'
        return self.fw.api_post(url, msg)

    def export_upload_firmware(self, server: str, user: str, password: str, msg=False):
        ftpurl = 'ftp:%2f%2f' + user + ':' + password + '@' + server + '/'
        url = 'api/sonicos/export/firmware/uploaded/ftp/'
        return self.fw.api_post(url, msg)

    def boot_fw(self, mode=None, reg=True, msg=False):
        if not mode:
            logger.warning('Please specify mode to: 1, 2, 3, 4')
            return False
        if mode == 1: 
            url = 'api/sonicos/boot/current'
            ssh_flag = False
        elif mode == 2: 
            url = 'api/sonicos/boot/current/factory-default'
            ssh_flag = True
        elif mode ==3: 
            url = 'api/sonicos/boot/uploaded'
            ssh_flag = False
        elif mode == 4:
            url = 'api/sonicos/boot/uploaded/factory-default'
            ssh_flag = True
        else:
            logger.warning('Please specify mode to: 1, 2, 3, 4')
            return False
        self.fw.api_post(url, msg)
        
        result = is_Firewall_up(self.fw.ip, ssh=ssh_flag)
        # if ssh_flag:
        #     cmd = 'python3 ' + os.environ['PYTHON_COMMON_HOME'] + '/config/add_security_rule.py'
        #     rc =subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE,stderr = subprocess.STDOUT).communicate()[0].decode('ASCII')
        #     logger.info(rc)            
        if result:
            logger.info('Firewall boots up.')
        else:
            logger.info('Error during boot up.')
        return result

    def enable_ndpp(self, msg=False):
        url = 'api/sonicos/ndpp'
        json_input = {"ndpp": True}
        return self.fw.api_put(url, msg, json_input)

    def disable_ndpp(self, msg=False):
        url = 'api/sonicos/ndpp'
        json_input = {"ndpp": False}
        return self.fw.api_put(url, msg, json_input)
    
    def show_tsr_reports_ftp_base(self):
        url = self.url_bk + 'ftp/base'
        resp = self.fw.api_get(url)
        return resp

    def edit_tsr_reports_ftp_base(self, msg=False, **kwargs):
        url = self.url_bk + 'ftp/base'
        input_json = self.show_tsr_reports_ftp_base()
        if not input_json:
            logger.error('Not found the base info')
            return (False, {}) if msg else False
        else:
            input_json['ftp'].update(kwargs)
        return self.fw.api_put(url, msg, input_json)

    def show_fips_base(self):
        url = self.url_bk + 'fips'
        resp = self.fw.api_get(url)
        return resp

    def show_ndpp_base(self):
        url = self.url_bk + 'ndpp'
        resp = self.fw.api_get(url)
        return resp

    def show_firmware_auto_update(self):
        url = self.url_bk + 'firmware/base'
        resp = self.fw.api_get(url)
        return resp

    def edit_firmware_auto_update(self, msg=False, **kwargs):
        url = self.url_bk + 'firmware/base'
        input_json = self.show_firmware_auto_update()
        if not input_json:
            logger.error('Not found the base info')
            return (False, {}) if msg else False
        else:
            input_json['firmware']['auto'].update(kwargs)
        return self.fw.api_put(url, msg, input_json)

    def delete_uploaded_firmware(self, msg=False):
        lc_bk = self.url_bk + 'upload-firmware'
        return self.fw.api_delete(lc_bk, msg)


class TimeApi:
    '''TimeApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/time'
        self.init_time_json = {
            'time': {
                'daylight_savings': True,
                'international_format': False,
                'ntp_update_interval': 60,
                'only_custom_ntp': False,
                'time_zone': 'pacific-time',
                'universal': False,
                'use_ntp': True
            }
        }

    def show_time(self):
        url = self.url + '/base'
        return self.fw.api_get(url)

    def edit_time(self, msg=False, **kwargs):
        url = self.url + '/base'
        init_json = self.show_time()
        init_json['time'].update(kwargs)
        if 'use_ntp' in kwargs.keys() and kwargs['use_ntp']:
            if 'date' in init_json['time'].keys():
                init_json['time'].pop('date')
            if 'time' in init_json['time'].keys():
                init_json['time'].pop('time')
        return self.fw.api_put(url, msg, init_json)
        
    def set_time(self, msg=False, **kwargs):
        url = self.url + '/base'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def show_ntp_server(self):
        url = self.url + '/ntp-servers'
        return self.fw.api_get(url)

    def add_ntp_server(self, msg=False, **kwargs):
        url = self.url + '/ntp-servers'
        init_json = { 'time': { 'ntp_server': [{}]} }
        init_json['time']['ntp_server'][0] = copy.deepcopy(kwargs)
        return self.fw.api_post(url, msg, data=init_json)

    def edit_ntp_server(self, msg=False, **kwargs):
        url = self.url + '/ntp-servers'
        if 'name' not in kwargs.keys():
            logger.error('Please specify an ntp-server name')
            return False
        init_json = self.show_ntp_server()
        if not init_json.get('time'):
            logger.error('Not found any ntp-servers.')
            return False
        found = 0
        for i in range(0, len(init_json['time']['ntp_server'])):
            if init_json['time']['ntp_server'][i]['name'] == kwargs['name']:
                init_json['time']['ntp_server'][i].update(kwargs)
                if 'no_auth' in kwargs.keys() and kwargs['no_auth']:
                    if 'md5' in init_json['time']['ntp_server'][i]:
                        init_json['time']['ntp_server'][i].pop('md5')
                found = 1
                break
        if not found:
            logger.error('Not found the ntp-server.')
            return False
        return self.fw.api_put(url, msg, data=init_json)

    def delete_ntp_server(self, name, msg=False):
        url = self.url + '/ntp-servers'
        init_json = { 'time': { 'ntp_server': [{ 'name': str(name) }] } }
        return self.fw.api_delete(url, msg, data=init_json)


class ScheduleApi:
    '''ScheduleApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/schedules'

    def show_schedules(self):
        return self.fw.api_get(self.url)

    def get_schedule(self, name):
        url = self.url + '/name/' + str(name)
        return self.fw.api_get(url)

    def add_schedule(self, msg=False, **kwargs):
        init_json = { "scheduler":{"schedule": [{}] }}
        init_json['scheduler']['schedule'][0].update(kwargs)
        return self.fw.api_post(self.url, msg, data=init_json)

    def edit_schedule(self, msg=False, **kwargs):
    # # # edit the whole schedule by name
        if 'name' not in kwargs.keys():
            logger.error('Please specify a schedule name.')
            return False
        url = self.url + '/name/' + str(kwargs['name'])
        init_json = self.get_schedule(str(kwargs['name']))
        if not init_json:
            logger.error('Not found the schedule.')
            return False
        init_json['scheduler']['schedule'][0].update(kwargs)
        return self.fw.api_put(url, msg, data=init_json)

    def delete_schedule(self, name: str, msg=False):
    # # # delete the whole schedule by name
        url = self.url + '/name/' + str(name)
        init_json = self.get_schedule(name)
        if not init_json:
            logger.error('Not found the schedule.')
            return False
        return self.fw.api_delete(url, msg)

    def edit_schedules(self, msg=False, **kwargs):
    # # # edit sub schedules under same schedule name
        if 'name' not in kwargs.keys():
            logger.error('Please specify a schedule name.')
            return False
        init_json = self.get_schedule(str(kwargs['name']))
        if not init_json:
            logger.error('Not found the schedule.')
            return False
        init_json['schedule'].update(kwargs)
        return self.fw.api_put(self.url, msg, data=init_json)

    def delete_schedules(self, msg=False, **kwargs):
    # # # delete sub schedules under same name
        if 'name' not in kwargs.keys():
            logger.error('Please specify a schedule name.')
            return False
        init_json = self.get_schedule(str(kwargs['name']))
        if not init_json:
            logger.error('Not found the schedule.')
            return False
        init_json['schedule'] = kwargs
        return self.fw.api_delete(self.url, msg, data=init_json)

    def get_from_uuid(self, uuid: str, msg=False):
        url = self.url + '/uuid/' + uuid
        return self.fw.api_get(url)

    def edit_from_uuid(self, msg=False, **kwargs):
        if 'uuid' not in kwargs.keys():
            logger.error('Please specify a schedule uuid.')
            return False
        url = self.url + '/uuid/' + str(kwargs['uuid'])
        init_json = self.get_from_uuid(str(kwargs['uuid']))
        if not init_json:
            logger.error('Not found the schedule.')
            return False
        init_json['schedule'].update(kwargs)
        return self.fw.api_put(url, msg, data=init_json)

    def delete_from_uuid(self, uuid: str, msg=False):
        url = self.url + '/uuid/' + uuid
        return self.fw.api_delete(url, msg)


class CertificateApi:
    '''CertificateApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/certificates'

    def show_certs(self):
        url = 'api/sonicos/reporting/certificates'
        return self.fw.api_get(url)

    def show_imported_certs(self):
        url = 'api/sonicos/reporting/certificates/imported'
        return self.fw.api_get(url)

    def show_builtin_certs(self):
        url = 'api/sonicos/reporting/certificates/build-in/with-expired'
        return self.fw.api_get(url)

    def show_cert(self, name: str):
        urlname = encode_url(name)
        url = 'api/sonicos/reporting/certificates/name/' + urlname
        return self.fw.api_get(url)

    def export_cert_keypair_ftp(self, ftpsvr, ftpusr, ftppwd, cname, cpwd, msg=False):
        cname = encode_url(cname)
        furl = encode_url('ftp://' + ftpusr + ':' + ftppwd + '@' + ftpsvr)
        url = self.url + '/export/cert-key-pair-ftp/name/' + cname + \
              '/password/' + cpwd + '/url/' + furl + '/'
        return self.fw.api_post(url, msg)

    def export_cert_keypair_scp(self, scpsvr, scpusr, scppwd, cname, cpwd, msg=False):
        cname = encode_url(cname)
        surl = encode_url('scp://' + scpusr + '@' + scpsvr)
        url = self.url + '/export/cert-key-pair-scp/name/' + cname + \
              '/password/' + cpwd + '/url/' + surl + '/'
        return self.fw.api_post(url, msg)

    def import_cert_keypair_ftp(self, ftpsvr, ftpusr, ftppwd, cname, cpwd, msg=False):
        cname = encode_url(cname)
        furl = encode_url('ftp://' + ftpusr + ':' + ftppwd + '@' + ftpsvr)
        url = self.url + '/import/cert-key-pair-ftp/name/' + cname + \
              '/password/' + cpwd + '/url/' + furl + '/'
        return self.fw.api_post(url, msg)

    def import_cert_keypair_scp(self, scpsvr, scpusr, scppwd, cname, cpwd, msg=False):
        cname = encode_url(cname)
        surl = encode_url('scp://' + scpusr + '@' + scpsvr)
        url = self.url + '/import/cert-key-pair-scp/name/' + cname + \
              '/password/' + cpwd + '/url/' + surl + '/'
        return self.fw.api_post(url, msg)

    def no_enrollment(self):
        url = self.url + '/enrollment'
        return self.fw.api_delete(url, msg=False)

    def export_req_ftp(self, ftpsvr, ftpusr, ftppwd, reqname, msg=False):
        reqname = encode_url(reqname)
        furl = encode_url('ftp://' + ftpusr + ':' + ftppwd + '@' + ftpsvr)
        url = self.url + '/export/signing-request-ftp/name/' + reqname + '/url/' + furl + '/'
        return self.fw.api_post(url, msg)

    def export_req_scp(self, scpsvr, scpusr, scppwd, reqname, msg=False):
        reqname = encode_url(reqname)
        surl = encode_url('scp://' + scpusr + '@' + scpsvr)
        url = self.url + '/export/signing-request-scp/name/' + reqname + '/url/' + surl + '/'
        return self.fw.api_post(url, msg)

    def generate_req(self, msg=False, nologin=False,**kwargs):
        url = self.url + '/generate-signing-request'
        json_input = copy.deepcopy(kwargs)
        return self.fw.api_post(url, msg, data=json_input,nologin=nologin)

    def export_req(self, filename, filepath, msg=False,nologin=False):
        url = 'api/sonicos/export/certificates/signing-request/name/' + filename
        req = self.fw.api_get(url, msg,nologin)
        req = str(req)
        os.system('rm -rf {}*'.format(filename))
        with open(filepath, 'w+') as f:
            f.write(req)
        logger.info('the req cert file {} has been exported to {}.'.format(filename,filepath))
        return True
        
    def export_csr(self, name, password, filepath='/tmp/csr.txt'):
        # create file to save download text
        os.system('touch {}'.format(filepath))
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/export/certificates/cert-key-pair/name/' + name + '/password/' + password
        self.fw.api_login()
        cmd = 'curl -k -i -H "Content-Type: application/json" -H "Accept: application/json" -X GET {} >> {}'.format(url, filepath)
        logger.info(cmd)
        os.system(cmd)
        resp = ''.join(os.popen("grep -a '200' /tmp/csr.txt "))
        os.system("rm -f /tmp/csr.txt")
        return resp

    def import_req_cert(self,req_cert, signed_cert, msg=False,nologin=False):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/import/certificates/signed-cert/name/' + req_cert
        if not nologin:
            self.fw.api_login()
        curl_cmd = "curl -k  --location --request PUT '" + url + "' --header 'Content-Type: application/json' --header 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' --data-binary '@" + signed_cert + "' --max-time 60"
        resp = os.popen(curl_cmd).read()
        if msg:
            return resp
        logger.info(curl_cmd)
        if re.search('\"success\":true', resp, re.I):
            return True
        else:
            logger.info(resp)
            return False

    def delete_local_cert(self, filename, msg=False):
        url = 'api/sonicos/certificates/name/' + filename
        return self.fw.api_delete(url, msg)

    def import_ca_ftp(self, ftpsvr, ftpusr, ftppwd, file, msg=False):
        furl = encode_url('ftp://' + ftpusr + ':' + ftppwd + '@' + ftpsvr) + file
        url = self.url + '/import/ca-cert/ftp/' + furl
        return self.fw.api_post(url, msg)

    def import_ca_scp(self, scpsvr, scpusr, scppwd, file, msg=False):
        surl = encode_url('scp://' + scpusr + '@' + scpsvr) + file
        url = self.url + '/import/ca-cert/scp/' + surl
        return self.fw.api_post(url, msg)

    def import_ca_cert(self, file, msg=False):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/import/certificates/ca-cert'
        self.fw.api_login()
        curl_cmd = "curl -k  --location --request PUT '" + url + "' --header 'Content-Type: application/json' --header 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' --data-binary '@" + file + "' --max-time 60"
        resp = os.popen(curl_cmd).read()
        if msg:
            return resp
        logger.info(curl_cmd)
        if re.search('\"success\":true', resp, re.I):
            return True
        else:
            logger.info(resp)
            return False

    def import_ca_cert_directly(self, name,file, msg=False):
        name = name.replace(' ','%20')
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/import/certificates/crl-directly/ca-name/'+name

        self.fw.api_login()
        curl_cmd = "curl -k  --location --request PUT '" + url + "' --header 'Content-Type: application/json' --header 'Authorization: Basic YWRtaW46cGFzc3dvcmQ=' --data-binary '@" + file + "' --max-time 60"
        resp = os.popen(curl_cmd).read()
        if msg:
            return resp
        logger.info(curl_cmd)
        if re.search('\"success\":true', resp, re.I):
            return True
        else:
            logger.info(resp)
            return False

    def delete_ca_cert(self,ca_hash):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/certificates/ca/' + ca_hash
        self.fw.api_login()
        curl_cmd = 'curl -k -i -H "Content-Type: application/json" -H "Accept: application/json" -X DELETE ' + url
        resp = os.popen(curl_cmd).read()
        logger.info(curl_cmd)
        logger.info("111111")
        logger.info(resp)
        if re.search('\"success\":true', resp, re.I):
            return True
        else:
            logger.info(resp)
            return False

    def import_signedca_ftp(self, ftpsvr, ftpusr, ftppwd, cname, file, msg=False):
        cname = encode_url(cname)
        furl = encode_url('ftp://' + ftpusr + ':' + ftppwd + '@' + ftpsvr) + file
        url = self.url + '/import/signed-cert-ftp/name/' + cname + '/url/' + furl
        return self.fw.api_post(url, msg)

    def import_signedca_scp(self, scpsvr, scpusr, scppwd, cname, file, msg=False):
        cname = encode_url(cname)
        surl = encode_url('scp://' + scpusr + '@' + scpsvr) + file
        url = self.url + '/import/signed-cert-scp/name/' + cname + '/url/' + surl
        return self.fw.api_post(url, msg)

    def delete_cert(self, cname, msg=False):
        cname = encode_url(cname)
        url = self.url + '/name/' + cname
        return self.fw.api_delete(url, msg)

    def import_crl(self, cname, msg=False):
        cname = encode_url(cname)
        url = self.url + '/import/crl/ca-name/' + cname
        return self.fw.api_post(url, msg)

    def import_crl_invalca(self, cname, msg=False):
        cname = encode_url(cname)
        url = self.url + '/import/crl/ca-name/' + cname + '/invalidate-certificates'
        return self.fw.api_post(url, msg)

    def import_crl_disinvalca(self, cname, msg=False):
        cname = encode_url(cname)
        url = self.url + '/import/crl/ca-name/' + cname + '/disable-invalidate-certificates'
        return self.fw.api_post(url, msg)

    def import_crl_urlper(self, cname, crlurl, invalidate_cert='disable-invalidate-certificates',msg=False):
        crlurl = encode_http_url(crlurl)  # update by Jlian
        cname = encode_http_url(cname)  # update by JLian
        url = self.url + '/import/crl-periodically/ca-name/' + cname + '/url/' + crlurl + '/' +invalidate_cert
        return self.fw.api_post(url, msg)

#    def import_crl_urlper(self, cname, crlurl, msg=False):
#        crlurl = encode_url(crlurl)
#        cname = encode_url(cname)
#        url = self.url + '/import/crl-periodically/ca-name/' + cname + '/url/' + crlurl
#        return self.fw.api_post(url, msg)

    def import_crl_urlper_invalca(self, cname, crlurl, msg=False):
        crlurl = encode_url(crlurl)
        cname = encode_url(cname)
        url = self.url + '/import/crl-periodically/ca-name/' + cname + '/url/' + crlurl + \
              '/invalidate-certificates'
        return self.fw.api_post(url, msg)

    def import_crl_urlper_disinvalca(self, cname, crlurl, msg=False):
        crlurl = encode_url(crlurl)
        cname = encode_url(cname)
        url = self.url + '/import/crl-periodically/ca-name/' + cname + '/url/' + crlurl + \
              '/disable-invalidate-certificates'
        return self.fw.api_post(url, msg)

    def import_crl_ftp(self, ftpsvr, ftpusr, ftppwd, cname, file, msg=False):
        cname = encode_url(cname)
        furl = encode_url('ftp://' + ftpusr + ':' + ftppwd + '@' + ftpsvr) + file
        url = self.url + '/import/crl-directly-ftp/ca-name/' + cname + '/url/' + furl
        return self.fw.api_post(url, msg)

    def import_crl_scp(self, scpsvr, scpusr, scppwd, cname, file, msg=False):
        cname = encode_url(cname)
        surl = encode_url('scp://' + scpusr + '@' + scpsvr) + file
        url = self.url + '/import/crl-directly-scp/ca-name/' + cname + '/url/' + surl
        return self.fw.api_post(url, msg)

    def import_crl_ftp_invalca(self, ftpsvr, ftpusr, ftppwd, cname, file, msg=False):
        cname = encode_url(cname)
        furl = encode_url('ftp://' + ftpusr + ':' + ftppwd + '@' + ftpsvr) + file
        url = self.url + '/import/crl-directly-ftp/ca-name/' + cname + '/url/' + furl + \
              '/invalidate-certificates'
        return self.fw.api_post(url, msg)

    def import_crl_scp_invalca(self, scpsvr, scpusr, scppwd, cname, file, msg=False):
        cname = encode_url(cname)
        surl = encode_url('scp://' + scpusr + '@' + scpsvr) + file
        url = self.url + '/import/crl-directly-scp/ca-name/' + cname + '/url/' + surl + \
              '/invalidate-certificates'
        return self.fw.api_post(url, msg)

    def import_crl_ftp_disinvalca(self, ftpsvr, ftpusr, ftppwd, cname, file, msg=False):
        cname = encode_url(cname)
        furl = encode_url('ftp://' + ftpusr + ':' + ftppwd + '@' + ftpsvr) + file
        url = self.url + '/import/crl-directly-ftp/ca-name/' + cname + '/url/' + furl + \
              '/disable-invalidate-certificates'
        return self.fw.api_post(url, msg)

    def import_crl_scp_disinvalca(self, scpsvr, scpusr, scppwd, cname, file, msg=False):
        cname = encode_url(cname)
        surl = encode_url('scp://' + scpusr + '@' + scpsvr) + file
        url = self.url + '/import/crl-directly-scp/ca-name/' + cname + '/url/' + surl + \
              'disable-/invalidate-certificates'
        return self.fw.api_post(url, msg)

    def scep(self, msg=False, **kwargs):
        url = self.url + '/scep'
        init_json = { 'certificates': { 'scep': {} } }
        init_json['certificates'] = { 'scep': [kwargs] }
        return self.fw.api_post(url, msg, data=init_json)
      #"signing_request": "string",
      #"ca_url": "string",
      #"challenge_password": "string",
      #"request_count": 0,
      #"polling_interval": 0,
      #"max_polling_time": 0,
      #"scep": true

    def import_cert_local(self, cert_path, name, password, msg=False):
        url = 'api/sonicos/import/certificates/cert-key-pair/'
        url_put = url + 'name' + '/' + name + '/' + 'password' + '/' + password
        #url = 'api/sonicos/import/certificates/cert-key-pair/name/vsftpd/password/password'
        logger.info(cert_path)
        return self.fw.api_put(url_put, msg, data=cert_path)

    def export_cert_local(self, name, password, msg=False):
        url = ' https://192.168.168.168/api/sonicos/export/certificates/cert-key-pair/'
        url_put = url + 'name' + '/' + name + '/' + 'password' + '/' + password
        cert_path = '/tmp/' + name + '.pfx'
        self.fw.api_login()
        cmd = 'curl -k -i -H "Content-Type: application/json" -H "Accept: application/json" \
            -X GET {} >> {}'.format(url_put, cert_path)
        os.system('rm -rf {}'.format(cert_path))
        logger.info(cmd)
        os.system(cmd)
        resp = ''.join(os.popen("grep -a '200' {}".format(cert_path)))
        return resp

    def import_ca_crl_local(self, cert_path, name, msg=False):
        url = 'api/sonicos/import/certificates/crl-directly/'
        url_put = url + 'ca-name' + '/' + name + '/' + 'disable-invalidate-certificates'
        logger.info(cert_path)
        return self.fw.api_put(url_put, msg, data=cert_path)

class DiagnosticApi:
    '''DiagnosticApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.init_tsr_json = {
            'tech_support_report': {
                'options': {
                    'arp_cache': False,
                    'atp_cache': False,
                    'debug_info': True,
                    'dhcp_bindings': False,
                    'dns_proxy_cache': False,
                    'extra_routing': False,
                    'geo_ip_cache': False,
                    'ike_info': False,
                    'ip_stack_info': False,
                    'ipv6': {
                        'dhcp': False,
                        'ndp': False
                    },
                    'secure_backup': {
                        'interval': 1440
                    },
                    'send_raw_flow_data': False,
                    'sonicpointn': {
                        'diagnostics': False
                    },
                    'users': {
                        'current': True,
                        'detail': True,
                        'inactive': True
                    },
                    'vpn_keys': False
                }
            }
        }

    def show_icmp_conf(self):
        url = 'api/sonicos/icmp'
        return self.fw.api_get(url)

    def conf_icmp(self, msg=False, **kwargs):
        url = 'api/sonicos/icmp'
        init_json = self.show_icmp_conf()
        init_json['icmp'].update(kwargs)
        return self.fw.api_put(url, msg, data=init_json)

    def get_icmp_statistics(self):
        url = 'api/sonicos/reporting/icmp'
        return self.fw.api_get(url)

    def delete_icmp_statistics(self):
        url = 'api/sonicos/reporting/icmp'
        return self.fw.api_delete(url, msg=False)

    def show_tsr_conf(self):
        url = 'api/sonicos/tech-support-report/options'
        return self.fw.api_get(url)

    def conf_tsr(self, msg=False, **kwargs):
        url = 'api/sonicos/tech-support-report/options'
        init_json = self.show_tsr_conf()
        init_json['tech_support_report']['options'].update(kwargs)
        return self.fw.api_put(url, msg, data=init_json)

    def send_tsr(self):
        url = 'api/sonicos/tech-support-report/send'
        return self.fw.api_post(url, msg=False)

    def export_tsr(self, server: str, user: str, password: str, msg=False):
        ftpurl = 'ftp:%2f%2f' + user + ':' + password + '@' + server + '/'
        url = 'api/sonicos/export/tech-support-report/ftp/' + ftpurl
        return self.fw.api_post(url, msg)

    def get_tsr(self, server=None):
        if not server:
            rc = re.search(r'inet addr:(\d*.\d*.\d*.\d*)', subprocess.Popen('ifconfig', stdout=subprocess.PIPE).communicate()[0], re.I)
            if rc:
                server = re.group(1)
        self.export_tsr(server=server, user='root', password='password')
    
    # add timeout parms to make sure x86 fw download tsr
    def download_tsr(self, filepath='/tmp/techSupport', timeout=60):
        url = 'api/sonicos/export/tech-support-report'
        tsr = self.fw.api_get(url, log_switch=False, timeout=timeout)
        with open(filepath, 'w+') as f:
            f.write(str(tsr))
        logger.info('the tsr file {} has been exported.'.format(filepath))
        
    def get_tsr_part(self, func, lab1=None, lab2=None):
        self.download_tsr()
        tsr_content = os.popen('cat /tmp/techSupport').read()
        start = "#" + func + " : " + lab1 + "_START"
        end   = "#" + func + " : " + lab1 + "_END"        
        pattern1 = start + '\n(.*)\n' + end
        lab1_match = re.search(r''+ pattern1 +'', tsr_content, re.I|re.S|re.M) 
        if lab1_match:
            tsr_part1 = lab1_match.group(1)
            if lab2:
                pattern2 = '--' + lab2 + '--\n(.*)(\n+)--'
                lab2_match = re.search(r''+ pattern2 +'', tsr_part1, re.I|re.S|re.M) 
                if lab2_match:
                    return lab2_match.group(1)
                else:
                    logger.error('Fail to get tsr.')
            else:
                return tsr_part1
        else:
            logger.error('Fail to get tsr.')
        return False

    def get_tsr_part_with_pattern(self, pattern):
        # pattern example: 'start str(.*?)end str'
        if not pattern:
            logger.error('Pattern must be provided.')
            return False 
        try:
            self.download_tsr()
            tsr_content = os.popen('cat /tmp/techSupport').read()
            match = re.search(pattern, tsr_content, re.I | re.S | re.M)
            if match:
                content = match.group(1).strip()
                logger.debug(f'Successfully extracted TSR content matching pattern')
                return content
            else:
                logger.error(f'Failed to find content matching pattern')
                return False
        except Exception as e:
            logger.error(f'Error getting TSR content: {str(e)}')
            return False

    def get_tsr_part2(self, func):
        self.download_tsr()
        tsr_content = os.popen('cat /tmp/techSupport').read()
        start = "#" + func +  "_START"
        end = "#" + func +  "_END"
        pattern1 = start + '\n(.*)\n' + end
        lab1_match = re.search(r'' + pattern1 + '', tsr_content, re.I | re.S | re.M)
        if lab1_match:
            tsr_part1 = lab1_match.group(1)
            return tsr_part1
        else:
            logger.error('Fail to get tsr.')
        return False

    # add by JLian
    def get_tsr_route_policy_part(self, func):
        self.download_tsr()
        tsr_content = os.popen('cat /tmp/techSupport').read()
        start = f"======={func}======="
        end = "=======Network : IPv6 Routing======="
        pattern1 = start + '\n(.*)\n' + end
        lab1_match = re.search(r'' + pattern1 + '', tsr_content, re.I | re.S | re.M)
        if lab1_match:
            tsr_part1 = lab1_match.group(1)
            return tsr_part1
        else:
            logger.error('Fail to get tsr.')
        return False
    
    # add by JLian
    def get_tsr_dynamic_routing_protocol_setting(self, dynamic_pro):    #dynamic_pro = OSPF,OSPFv3,RIP,RIPing,BGP
        self.download_tsr()
        tsr_content = os.popen('cat /tmp/techSupport').read()
        net_list = tsr_content.split('\n\n\n')
        for net in net_list:
            if f'Advanced Routing: {dynamic_pro} Settings' in net:
                return net
        return False

    # add by JLian
    def get_tsr_accessrule_part(self):
        self.download_tsr()
        tsr_content = os.popen('cat /tmp/techSupport').read()
        start = "#Firewall : Access Rules_START"
        end = "#Firewall : Security Policy Table_END"
        pattern1 = start + '\n(.*)\n' + end
        lab1_match = re.search(r'' + pattern1 + '', tsr_content, re.I | re.S | re.M)
        if lab1_match:
            tsr_part1 = lab1_match.group(1)
            return tsr_part1
        else:
            logger.error('Fail to get tsr.')
        return False
        
    def get_tsr_interface_part(self, lab1=None, lab2=None):
        self.download_tsr()
        tsr_content = os.popen('cat /tmp/techSupport').read()
        start = 'Interface Name' + ' '*33 + " : " + lab1 
        if lab2:
            end = 'Interface Name' + ' ' * 33 + " : " + lab2
        else:
            end = '-'*65


        pattern1 = start + '(.*)' + end
        print(pattern1)
        lab1_match = re.search(r''+ pattern1 + '', tsr_content, re.I|re.S|re.M) 
        print((lab1_match))
        if lab1_match:
            tsr_part1 = lab1_match.group(1)
           
            return tsr_part1
        else:
            logger.error('Fail to get tsr.')
        return False
    
    def diag_dns_name_lookup(self, cmd, msg=0):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/direct/cli'
        self.fw.api_login()
        command = "curl -k -i --basic -u admin:password -H 'Accept: text/plain' \
           -H 'Content-Type: text/plain' --data ' " + cmd + "' -X POST " + url + " --max-time 180";
        resp = os.popen(command).read()
        return resp

    def get_check_network_setting(self):
        url = 'api/sonicos/dynamic-file/getChkNetSettings.json'
        return self.fw.api_get(url)
       
    def connect_mysonicwall(self):
        url = 'api/sonicos/diag/check-network-settings-action/host/www.mysonicwall.com/version/0/type/4/itemGrpIndex/3/itemIndex/0'
        resp = self.fw.api_post_no_need_pending(url)
        return resp
    
    def connect_license_manager(self):
        url = 'api/sonicos/diag/check-network-settings-action/host/lm2.sonicwall.com/version/0/type/4/itemGrpIndex/4/itemIndex/0'
        resp = self.fw.api_post_no_need_pending(url)
        return resp

    def connect_default_gateway(self, ip):
        url = 'api/sonicos/diag/check-network-settings-action/host/{}/version/0/type/0/itemGrpIndex/0/itemIndex/0'.format(ip)
        # url = 'api/sonicos/diag/check-network-settings-action/host/13.11.0.1/version/0/type/0/itemGrpIndex/0/itemIndex/0'
        logger.info(url)
        resp = self.fw.api_post_no_need_pending(url)
        return resp

    def connect_dns1_server(self,ip):
        url = 'api/sonicos/diag/check-network-settings-action/host/{}/version/0/type/1/itemGrpIndex/1/itemIndex/0'.format(ip)
        logger.info(url)
        resp = self.fw.api_post_no_need_pending(url)
        return resp

    def connect_server_by_type(self, host, server_type):
        servers_info = {
            'gw': (0, 0, 0),
            'dns1': (1, 1, 0),
            'dns2': (1, 1, 1),
            'dns3': (1, 1, 2),
            'ntp1': (2, 2, 0),
            'ntp2': (2, 2, 1),
            'msw': (4, 3, 0),
            'lm': (4, 4, 0),
            'cfs': (6, 5, 0),
        }
        if not servers_info.get(server_type):
            logger.error(f'Unsupport server type in this API method = {server_type}')
            return {}
        test_type, gp_index, it_index = servers_info.get(server_type)
        url = f'api/sonicos/diag/check-network-settings-action/host/{host}/version/0/type/{test_type}/itemGrpIndex/{gp_index}/itemIndex/{it_index}'
        logger.info(f'API url for testing server connection = {url}')
        resp = self.fw.api_post_no_need_pending(url, sleep_time=0, loop=1)
        return resp

   # update by JLian
    def diag_find_network_path(self, host, msg=True):
        url = 'api/sonicos/diag/network-path-action/' + host
        return self.fw.api_post(url, msg)

    def get_find_network_path_Result(self):
        url = 'api/sonicos/dynamic-file/getFindNetPathResult.json'
        return self.fw.api_get(url)

    def diag_traceroute(self, host, msg=True):
        url = 'api/sonicos/diag/traceroute-action/' + host
        return self.fw.api_post(url, msg)

    def real_time_lookup(self,ip,domain,dnsServer,msg=True):
        url = f'api/sonicos/diag/rbl-lookup-action/ip/{ip}/domain/{domain}/dns-server/{dnsServer}'
        resp = self.fw.api_post(url,msg)
        return resp

    def get_RBL_lookup_result(self):
        url = 'api/sonicos/dynamic-file/getRBLLookupResult.json'
        resp = self.fw.api_get(url)
        return resp

    def get_TraceRoute_Result(self, timeout=60):
        url = 'api/sonicos/dynamic-file/getTraceRouteResult.json'
        return self.fw.api_get(url, timeout=timeout)

    def diag_ping(self, dn, msg=True):
        url = 'api/sonicos/diag/ping-action/' + dn
        return self.fw.api_post(url, msg)

    def get_Ping_Result(self):
        url = 'api/sonicos/dynamic-file/getPingResult.json'
        return self.fw.api_get(url)

    def get_name_lookup_Result(self):
        url = 'api/sonicos/dynamic-file/getNameLookupResult.json'
        return self.fw.api_get(url)

    def diag_dns_lookup_name_by_api(self, msg=True, **kwargs):
        base_url = 'api/sonicos/diag/nslookup-action/'
        options = {
            'version': 'ipv4',
            'type': '',
            'domain_name': '',
            'ipv4-dns1': '10.190.202.200',
            'ipv6-dns1': '::',
        }
        options.update(kwargs)
        print(options)

        if options['type'] == 'customized':
            if options['ipv6-dns1'] != '::':
                options['ipv4-dns1'] = '0.0.0.0'
            url = base_url + kwargs['domain_name'] + '/' + options['version'] \
                + '/' + options['type'] + '/ipv4-dns1/' + \
                options['ipv4-dns1'] + \
                '/ipv4-dns2/0.0.0.0/ipv4-dns3/0.0.0.0' + '/ipv6-dns1/' + \
                options['ipv6-dns1'] + '/ipv6-dns2/::/ipv6-dns3/::'

        elif options['type'] == 'system':
            url = base_url + kwargs['domain_name'] + '/' + options['version']
        return self.fw.api_post(url, msg)
        
    def reverse_lookup_action(self, host='', msg=False):
        url = f'api/sonicos/diag/reverse-lookup-action/{host}'
        if not host:
            logger.info('the host can not be empty.')
            return False if not msg else (False, dict)
        return self.fw.api_post(url, msg)

    def get_rev_name_lookup_result(self):
        url = 'api/sonicos/dynamic-file/getRevNameLookupResult.json'
        return self.fw.api_get(url)


    def lookup_url_rating(self, domain):
        url = f'api/sonicos/diag/cfs-lookup-action/{domain}'
        resp = self.fw.api_post_no_need_pending(url)
        return resp
    
    def get_url_rating_result(self):
        url = f'api/sonicos/dynamic-file/getCFSUrlRatingResult.json'
        resp = self.fw.api_get(url)
        return resp

class PacketmonitorApi:
    '''PacketmonitorApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/packet-monitor'
        self.connection_ipv6_url = 'api/sonicos/dynamic-file/getACMFilter.json?ipv6=1'
        self.connection_ipv4_url = 'api/sonicos/dynamic-file/getACMFilter.json?ipv6=0'
        self.init_pack_json = {
            'packet_monitor': {
                'bytes_to_capture': 1520,
                'display_filter': {
                    'bidirectional': True,
                    'destination_ips': '',
                    'destination_ports': '',
                    'ether_types': '',
                    'interfaces': '',
                    'ip_types': '',
                    'source_ips': '',
                    'source_ports': '',
                    'status': {
                        'consumed': True,
                        'dropped': True,
                        'forwarded': True,
                        'generated': True
                    }
                },
                'exclude': {
                    'encrypted_gms': False,
                    'internal_traffic': {
                        'ha': True,
                        'sonicpoint': True
                    },
                    'management': {
                        'http': True,
                        'snmp': False,
                        'ssh': False
                    },
                    'syslog': {
                        'gms_server': False,
                        'syslog_servers': False
                    }
                },
                'ftp': {
                    'automatic': False,
                    'directory': 'captures',
                    'html': True,
                    'login': 'admin',
                    'password': '4,ce85ab016a6b890f4d12fed356fcbb34864ec47a5b2fe7185a10121f114d951f',
                    'pcapng': True,
                    'server': '0.0.0.0'
                },
                'mirror': {
                    'forward_interface': '',
                    'interface': '',
                    'ip': '0.0.0.0',
                    'max_rate': 100,
                    'only_ip_packets': False,
                    'receive_from_ip': '0.0.0.0',
                    'to_capture_buffer': False
                },
                'monitor_filter': {
                    'based_on_firewall_rule': False,
                    'bidirectional': True,
                    'destination_ips': '',
                    'destination_ports': '',
                    'ether_types': '',
                    'firewall_generated': False,
                    'interfaces': '',
                    'intermediate': {
                        'intermediate_packets': False
                    },
                    'ip_types': '',
                    'source_ips': '',
                    'source_ports': '',
                    'status': {
                        'consumed': False,
                        'dropped': False,
                        'forwarded': False
                    }
                },
                'wrap_buffer': False
            }
        }

    def show_packmon_setting(self):
        url = self.url + '/base'
        return self.fw.api_get(url)

    def conf_packmon(self, msg=False, **kwargs):
        url = self.url + '/base'
        init_json = self.show_packmon_setting()
        init_json['packet_monitor'].update(kwargs)
        return self.fw.api_put(url, msg, data=init_json)

    def config_packetmoni(self, msg=False, **kwargs):
        url = self.url + '/base'
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        conf_packmon_resp = self.fw.api_put(url, msg, data=json_input)
        return conf_packmon_resp
    
    def show_pack_statistics(self):
        url = 'api/sonicos/reporting/packet-monitor'
        return self.fw.api_get(url)

    def clear_packets(self):
        url = self.url + '/capture'
        return self.fw.api_post(url, msg=False)

    def packets_to_ftp(self):
    # # # Need config FTP server in conf_packmon
        url = self.url + '/log-to-ftp'
        return self.fw.api_post(url, msg=False)

    def monitor_all(self):
        url = self.url + '/monitor/all'
        return self.fw.api_post(url, msg=False)

    def monitor_default(self):
        url = self.url + '/monitor/default'
        return self.fw.api_post(url, msg=False)

    def start_capture(self):
        url = self.url + '/start/capture'
        return self.fw.api_post(url, msg=False)

    def stop_capture(self):
        url = self.url + '/stop/capture'
        return self.fw.api_post(url, msg=False)

    def start_mirror(self):
        url = self.url + '/start/mirror'
        return self.fw.api_post(url, msg=False)

    def stop_mirror(self):
        url = self.url + '/stop/mirror'
        return self.fw.api_post(url, msg=False)

    def export_captured_packets_text_file(self, filepath = '/tmp/packetcaptute', format='text'):
        url = 'api/sonicos/export/captured-packets/' + format
        packet = self.fw.api_get(url, log_switch=False)
        with open(filepath,'w+') as f:
            f.write(str(packet))
        logger.info('the tsr file {} has been exported.'.format(filepath))

    def export_captured_packets(self, format='text'):
        url = 'api/sonicos/export/captured-packets/' + format
        return self.fw.api_get(url, log_switch=False)

    def export_captured_packets_pcapng(self, filepath = '/tmp/packet-c.pcapng'):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/export/captured-packets/pcapng'
        self.fw.api_login()
        curl_command = ['curl', '-k', '-H', "'Content-type: application/json' ", '-H', "'Accept: application/json' ",'-X','GET',
             url,  '-o', filepath]
        logger.info('--------curl command:')
        logger.info(curl_command)
        resp = subprocess.Popen(curl_command, stdout=subprocess.PIPE).communicate()[0]
        logger.info("the pcapng file has been export " + filepath)
        
    def export_captured_packets_libpcap(self, filepath = '/tmp/packet-c.pcap'):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/export/captured-packets/libpcap'
        self.fw.api_login()
        curl_command = ['curl', '-k', '-H', "'Content-type: application/json' ", '-H', "'Accept: application/json' ",'-X','GET',
             url,  '-o', filepath]
        logger.info('--------curl command:')
        logger.info(curl_command)
        resp = subprocess.Popen(curl_command, stdout=subprocess.PIPE).communicate()[0]
        logger.info("the pcap file has been export " + filepath)

    def connections(self):
        url = 'api/sonicos/dynamic-file/getCacheFlowList.json'
        return self.fw.api_get(url, log_switch=False)
        
    def get_connections_list(self):
        url = "api/sonicos/dynamic-file/getCacheFlowList.json?fulljson=1"
        return self.fw.api_get(url, log_switch=False)

    def flush_connections_all(self,version = 'ipv4'):
        if version == 'ipv6':
            self.fw.api_get(self.connection_ipv6_url, log_switch=False)
        elif version == 'ipv4':
            self.fw.api_get(self.connection_ipv4_url, log_switch=False)
        url = 'api/sonicos/diag/advanced/firewall-connections'
        return self.fw.api_delete(url)
    
    def get_ipv6_connections_list(self):
        url = 'api/sonicos/dynamic-file/getACMFilter.json?ipv6=1'
        self.fw.api_get(url, log_switch=False)
        res = self.get_connections_list()
        return res

    ## not support 701
    def export_connections_list(self,version='ipv4',format='csv',filepath='/tmp/connection_list.csv'):
        url = 'https://' + self.fw.ip + '/' +'api/sonicos/dynamic-file/'
        if format == 'csv':
            file_url = url + 'connectionReport_1600_0.csv'
        elif format == 'json':
            file_url = url + 'connectionReport_1600_0.wri'
        
        curl_command = ['curl', '-k', '-H', "'Content-type: application/json' ", '-H', "'Accept: application/json' ",
                        '-X', 'GET',
                        file_url, '-o', filepath]
        logger.info('--------curl command:')
        logger.info(curl_command)
        self.fw.api_login()
        if version == 'ipv6':
            self.fw.api_get(self.connection_ipv6_url, log_switch=False)
        elif version == 'ipv4':
            self.fw.api_get(self.connection_ipv4_url, log_switch=False)
        resp = subprocess.Popen(curl_command, stdout=subprocess.PIPE).communicate()[0]
        logger.info("the pcap file has been export " + filepath)
        


    def get_connections_filter(self, **kwargs):
        # url = 'api/sonicos/dynamic-file/getACMFilter.json?cfIIPEdit=-1.-1.-1.-1\32&cfRIPEdit=-1.-1.-1.-1\32&cfRPortEdit=-1&cfProtoGroup=-1&curFlowType=-1&iIfSelect=-1&rIfSelect=1610612993&cfGroupValue=0'
        url = 'api/sonicos/dynamic-file/getACMFilter.json?'
        if 'srcIp'  in kwargs.keys():
            srcip_url = 'cfIIPEdit=' + kwargs['srcIp'] + '\32&'
        else:
            srcip_url = 'cfIIPEdit=-1.-1.-1.-1\32&'
        if 'dstIp' in kwargs.keys():
            dstip_url = 'cfRIPEdit=' + kwargs['dstIp'] + '\32&'
        else:
            dstip_url = 'cfRIPEdit=-1.-1.-1.-1\32&'
        if 'dstPort' in kwargs.keys():
            dstport_url = 'cfRPortEdit=' + kwargs['dstPort'] + '&'
        else:
            dstport_url = 'cfRPortEdit=-1&'
        if 'proto' in kwargs.keys():
            if kwargs['proto'].lower() == 'udp':
                proto_url = 'cfProtoGroup=' + '17' + '&'
            elif  kwargs['proto'].lower() == 'icmp':
                proto_url = 'cfProtoGroup=' + '1' + '&'
            elif  kwargs['proto'].lower() == 'igmp':
                proto_url = 'cfProtoGroup=' + '2' + '&'
            elif  kwargs['proto'].lower() == 'tcp':
                proto_url = 'cfProtoGroup=' + '6' + '&'
            elif  kwargs['proto'].lower() == 'gre':
                proto_url = 'cfProtoGroup=' + '47' + '&'
            elif  kwargs['proto'].lower() == 'esp':
                proto_url = 'cfProtoGroup=' + '50' + '&'
            elif  kwargs['proto'].lower() == 'ah':
                proto_url = 'cfProtoGroup=' + '51' + '&'
            elif  kwargs['proto'].lower() == 'icmpv6':
                proto_url = 'cfProtoGroup=' + '58' + '&'
            elif  kwargs['proto'].lower() == 'eigrp':
                proto_url = 'cfProtoGroup=' + '88' + '&'
            elif  kwargs['proto'].lower() == 'ospf':
                proto_url = 'cfProtoGroup=' + '89' + '&'
            elif  kwargs['proto'].lower() == 'pimsm':
                proto_url = 'cfProtoGroup=' + '103' + '&'
            elif  kwargs['proto'].lower() == 'l2tp':
                proto_url = 'cfProtoGroup=' + '115' + '&'
        else:
            proto_url = 'cfProtoGroup=-1&'
        if 'flowType' in kwargs.keys():
            #This number is in the order of the drop down list
            if  kwargs['flowType'].lower() == 'generic':
                flowtype_url = 'curFlowType=' + '0' + '&'
            elif  kwargs['flowType'].lower() == 'dhcp_bootp':
                flowtype_url = 'curFlowType=' + '1' + '&'
            elif  kwargs['flowType'].lower() == 'dns':
                flowtype_url = 'curFlowType=' + '2' + '&'
            elif kwargs['flowType'].lower() == 'http'  :
                flowtype_url = 'curFlowType=' + '9' + '&'
            elif kwargs['flowType'].lower() == 'http_mngm' :
                flowtype_url = 'curFlowType=' + '10' + '&'
            elif kwargs['flowType'].lower() == 'https' :
                flowtype_url = 'curFlowType=' + '11' + '&'
        else:
            flowtype_url = 'curFlowType=-1&'
        if 'srcIf' in kwargs.keys():
            if isinstance(kwargs['srcIf'],str):
                if 'x' in kwargs['srcIf'].lower():
                    id = kwargs['srcIf'][-1]
                elif 'u0' == kwargs['srcIf'].lower():
                    id = '10'
                if 'x0' == kwargs['srcIf'].lower():
                    id = 'undefined'
            else:
                try:
                    if kwargs['srcIf']['type'] == 'TI' and 'num_id' in kwargs['srcIf'].keys():
                        num = '0x60000{}01'.format(kwargs['srcIf']['num_id'])
                        id = str(int(num,16))
                except KeyError:
                    logger.error('Error: Interface type is TI ,the keys of type and num_id is must')
            srcif_url = 'iIfSelect=' + id + '&'
        else:
            srcif_url = 'iIfSelect=-1&'
        if 'dstIf' in kwargs.keys():
            if isinstance(kwargs['dstIf'],str):
                if 'x' in kwargs['dstIf'].lower():
                    id = kwargs['dstIf'][-1]
                elif 'u0' == kwargs['dstIf'].lower():
                    id = '10'
                if 'x0' == kwargs['dstIf'].lower():
                    id = 'undefined'
            else:
                try:
                    if kwargs['dstIf']['type'] == 'TI' and 'num_id' in kwargs['dstIf'].keys():
                        num = '0x60000{}01'.format(kwargs['dstIf']['num_id'])
                        id = str(int(num,16))
                except KeyError:
                    logger.error('Error: Interface type is TI ,the keys of type and num_id is must')
            dstif_url = 'rIfSelect=' + id + '&'
        else:
            dstif_url = 'rIfSelect=-1&'
        if 'group' in kwargs.keys():
            grp_url = ''
        else:
            grp_url = 'cfGroupValue=0'
        filter_url = url + srcip_url + dstip_url + dstport_url + proto_url + flowtype_url + srcif_url + dstif_url + grp_url
        self.fw.api_get(filter_url, log_switch=False)
        res = self.get_connections_list()
        return res
        
    def get_packet_capture(self):
        url = "api/sonicos/dynamic-file/getPktCapture.json"
        return self.fw.api_get(url, log_switch=False)

    def show_packet_statistics(self):
        url = "api/sonicos/dynamic-file/getPktCaptureStatus.json"
        return self.fw.api_get(url, log_switch=False)

    def get_packet_policy(self, policy_id):
        url = "api/sonicos/dynamic-file/getPolicy.json?policy_id={}&type=1".format(policy_id)
        return self.fw.api_get(url, log_switch=False)

         
class RestartApi:
    '''RestartApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/restart'

    def restart_now(self):
        url = self.url
        (rc, output) = self.fw.api_post(url, msg=True)
        if not rc:
            logger.error(output)
        time.sleep(30)
        if is_Firewall_up(self.fw.ip, ssh=False):
            logger.info('Firewall boots up')
            return rc
        logger.error('Firewall boots up failed.')
        return False

    def restart_at(self, time: str, msg=False):
        url = self.url + '/at/'
        pattern = re.compile(r'\W+')
        out = pattern.findall(time)
        time_new = ''
        if not out:
            if len(time) == 14:
                time_list = (time[0:4], time[4:6], time[6:8], time[8:10], time[10:12], time[12:14])
                connect = ':'
                time_new = connect.join(time_list)
            else:
                logger.error('Wrong time format.')
                return False
        else:
            time_new = pattern.sub(':', time)
        logger.info('Friewall will restart at ' + time_new)
        url = url + time_new
        return self.fw.api_post(url, msg)

    def restart_in(self, count: int, mode: str, msg=False):
        url = self.url + '/in/' + str(count) + '/' + mode.lower()
        logger.info('Firewall will restart in ' + str(count) + mode.lower())
        return self.fw.api_post(url, msg)
        

class DiagnosticPingApi:
    '''DiagnosticPing'''
    def __init__(self, fw):
        self.fw = fw

    def diag_ping(self, cmd, msg=0, count=1):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/direct/cli'
        self.fw.api_login()
        command = "curl -k -i --basic -u admin:password -H 'Accept: text/plain' \
           -H 'Content-Type: text/plain' --data ' " + cmd + "' -X POST " + url + " --max-time 60";
        logger.info(command)
        resp = os.popen(command).read()
        logger.info(resp)
        if msg == 1:
            return resp
        if re.search('is alive', resp, re.I):
            return True
        else:
            return False
            

class CloudBackupApi:
    '''CloudBackupApi Class'''

    def __init__(self, fw):
        self.fw = fw

    def conf_packmon(self, msg=False, **kwargs):
        url = self.url + '/base'
        init_json = self.show_packmon_setting()
        init_json['packet_monitor'].update(kwargs)
        return self.fw.api_put(url, msg, data=init_json)

    def notification_center_status(self):
        url = 'api/sonicos/dynamic-file/getStatsData.json?restype=4&datatype=2'
        return self.fw.api_get(url)

    def retain_cloud_bk(self, msg=False, **kwargs):
        url = 'api/sonicos/cloud-backup-retain'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def boot_cloud_firmware(self, name, msg=False):
        if not name:
            logger.info("Error:fw name is empty...")
            return False
        url =  'api/sonicos/cloud-backup-boot/name/' + name
        resp = self.fw.api_post(url, msg)
        return resp

    def download_cloud_back(self, name, filepath='/tmp/test.exp', msg=False):
        if not name:
            logger.info("Error:fw name is empty...")
            return False
        url =  'api/sonicos/export/cloud-backup/name/' + name
        resp = self.fw.api_get(url, msg)
        with open(filepath, 'w+') as f:
            f.write(str(resp))
        logger.info('the exp file {} has been exported.'.format(filepath))
        return True

    def gold_master_cloud_bk(self, msg=False, **kwargs):
        url = 'api/sonicos/cloud-backup-gold'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def enable_cloud_backup(self, msg=False, **kwargs):
        url = 'api/sonicos/administration/global'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp
  
    def get_exp_list(self, type = 2):
        '''
           local: type=1, cloud: type =2
        '''
        url = 'api/sonicos/dynamic-file/getFwExpList.json?type=' + str(type)
        return self.fw.api_get(url)

    def add_cloud_backup(self, msg=False, **kwargs):
        url = 'api/sonicos/cloud-backup'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def delete_all_cloud_backups_by_version(self, version, msg=False):
        if not version:
            logger.info("Error:version is empty...")
            return False
        url = 'api/sonicos/cloud-backups/version/' + version
        resp = self.fw.api_delete(url, msg)
        return resp

    def delete_clould_bk_by_name(self, name, msg=False):
        if not name:
            logger.info("Error:name is empty...")
            return False
        url = 'api/sonicos/cloud-backup/name/' + name
        resp = self.fw.api_delete(url, msg)
        return resp

class OneTouchConfigApi:
    '''DiagnosticApi Class'''
    def __init__(self, fw):
        self.fw = fw

    def set_DPI_stateful_fw_security(self,msg=False):
        url = 'api/sonicos/diag/advanced/dpi-stateful-firewall-security'
        return self.fw.api_post(url, msg,check_online='tcp')


    def set_stateful_fw_security(self,msg=False):
        url = 'api/sonicos/diag/advanced/stateful-firewall-security'
        return self.fw.api_post(url, msg, check_online='tcp')
        
        
class PacketReplayApi:
    '''PackeyReplayApi Class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/packet-replay'

    def crafting_udp_packet(self, msg=False, **kwargs):
        url = self.url + '/packet-crafting-udp/action-val'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def crafting_packet_buffer(self, msg=False, **kwargs):
        url = self.url + '/packet-crafting-buffer/action-val'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(url, msg, data=json_input)

    def clear_packets(self, msg=False):
        url = self.url + '/clear-packets'
        resp = self.fw.api_post(url, msg)
        return resp 

    def export_replayed_packets(self, mode=''):
        if mode == "":
            logger.error("Need specify export mode:text,libpcap,app-data,html or pcapng")
            return False
        if mode not in ['text', 'libcap', 'app-data', 'html', 'pcapng']:
            logger.error("export mode false, mode should be text,libpcap,app-data,html or pcapng")
        url = 'api/sonicos/export/replayed-packets/' + mode
        return self.fw.api_get(url) 

    def import_packets_file(self, filepath, msg=False):
        url = 'https://' + self.fw.ip + '/' + 'api/sonicos/import/packet-replay'
        self.fw.api_login()
        curl_cmd = 'curl -k -i -H "Content-Type: multipart/form-data" -X POST ' + '-F filename=@' + filepath + ' --max-time 50 '+ url 
        logger.info('--------curl command:')
        logger.info(curl_cmd)
        resp = os.popen(curl_cmd).read()
        if msg:
            return resp
        logger.info(curl_cmd)
        if re.search('\"success\":\s*true', resp, re.I):
            return True
        else:
            logger.info(resp)
            return False

    def replay_packets_from_file(self, msg=False, **kwargs):
        url = self.url + '/replay/action-val'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def delete_uploaded_file(self, msg=False):
        url = self.url + '/delete/packet-replay-file'
        resp = self.fw.api_post(url, msg)


class FipsApi:
    """FipsApi Class"""

    def __init__(self, fw):
        self.fw = fw
        self.geturl = 'api/sonicos/dynamic-file/getFipsModeSettings.json'

    def get_fips_warning(self):
        return self.fw.api_get(self.geturl)
        
        
class NetworkAccessControlApi:
    """Network Access Control Api Class"""

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/network-access-control/clearpass/base'
        self.admin_url = 'api/sonicos/network-access-control/clearpass/generate-json-web-token/user-name/admin'
        self.gwt_url = 'api/sonicos/dynamic-file/getClearpassJwtStatus.json'
        self.session_url = 'api/sonicos/threat-session'
        self.config_session_url = 'api/sonicos/threat-session/source-ip/'
        self.servers_url = 'api/sonicos/network-access-control/clearpass/servers/'
        self.server_name_url = 'api/sonicos/network-access-control/clearpass/servers/name/'
        self.active_tokens_url = 'api/sonicos/reporting/network-access-control/clearpass/json-web-tokens'
        self.query_url = 'api/sonicos/network-access-control/clearpass/query-now'
        self.query_status_url = 'api/sonicos/dynamic-file/getClearpassQueryStatus.json'

        self.initial_clearpass_json = {
            "network_access_control": {
                "clearpass": {
                    "enable": True,
                    "json_web_token_aging": 30,
                    "user_role_interval": 1
                }
            }
        }
        self.initial_server_json = {
            "network_access_control": {
                "clearpass": {
                    "server": [
                        {
                            "client_id": "88",
                            "name": "37.37.37.37",
                            "password": "password",
                            "port": 443,
                            "user_name": "user_01"
                        }
                    ]
                }
            }
        }

    def edit_clearpass_settings(self, msg=False, **kwargs):
        # kwargs = {
        #     "enable": True,
        #     "json_web_token_aging": 30,
        #     "user_role_interval": 1
        # }
        json_input = self.initial_clearpass_json
        if 'enable' in kwargs.keys():
            json_input['network_access_control']['clearpass']['enable'] = kwargs['enable']
        if 'json_web_token_aging' in kwargs.keys():
            json_input['network_access_control']['clearpass']['json_web_token_aging'] = kwargs['json_web_token_aging']
        if 'user_role_interval' in kwargs.keys():
            json_input['network_access_control']['clearpass']['user_role_interval'] = kwargs['user_role_interval']

        logger.info(f'edit_clearpass_settings put url: {self.base_url}')
        logger.info(json_input)
        return self.fw.api_put(self.base_url, msg, data=json_input)

    def generate_admin_jwt(self, msg=False):
        # not need post data
        logger.info(f'generate_jwt post url: {self.base_url}')
        return self.fw.api_post(self.admin_url, msg)

    def get_clearpass_base_settings(self):
        logger.info(f'get_clearpass_base_settings get url: {self.base_url}')
        return self.fw.api_get(self.base_url)

    def get_json_web_tokens(self):
        logger.info(f'get_json_web_tokens get url: {self.gwt_url}')
        return self.fw.api_get(self.gwt_url)

    def get_active_tokens(self):
        logger.info(f'get_active_tokens get url: {self.active_tokens_url}')
        return self.fw.api_get(self.active_tokens_url)

    def get_threat_session(self):
        logger.info(f'get_threat_session get url: {self.session_url}')
        return self.fw.api_get(self.session_url)

    def get_session_source_ip(self, ip=''):
        logger.info(f'get_session_source_ip get url: {self.config_session_url}{ip}')
        return self.fw.api_get(self.config_session_url+ip)

    def del_session_source_ip(self, ip='', msg=False):
        logger.info(f'del_session_source_ip del url: {self.config_session_url}{ip}')
        return self.fw.api_delete(self.config_session_url+ip, msg)

    def add_clearpass_server(self, msg=True, **kwargs):
        # kwargs = {
        #     "client_id": "88",
        #     "name": "37.37.37.37",
        #     "password": "password",
        #     "port": 443,
        #     "user_name": "user_01"
        # }
        json_input = self.initial_server_json
        if 'name' in kwargs.keys():
            json_input['network_access_control']['clearpass']['server'][0]['name'] = kwargs['name']
        if 'password' in kwargs.keys():
            json_input['network_access_control']['clearpass']['server'][0]['password'] = kwargs['password']
        if 'port' in kwargs.keys():
            json_input['network_access_control']['clearpass']['server'][0]['port'] = kwargs['port']
        if 'user_name' in kwargs.keys():
            json_input['network_access_control']['clearpass']['server'][0]['user_name'] = kwargs['user_name']
        if 'client_id' in kwargs.keys():
            json_input['network_access_control']['clearpass']['server'][0]['client_id'] = kwargs['client_id']

        logger.info(f'add_clearpass_server post url: {self.servers_url}')
        logger.info(json_input)
        return self.fw.api_post(self.servers_url, msg, data=json_input)

    def get_clearpass_servers(self):
        logger.info(f'get_clearpass_servers get url: {self.servers_url}')
        return self.fw.api_get(self.servers_url)

    def get_clearpass_server(self, name=''):
        logger.info(f'get_clearpass_server get url: {self.server_name_url}{name}')
        return self.fw.api_get(self.server_name_url + name)

    def del_clearpass_server(self, name='', msg=False):
        logger.info(f'del_clearpass_server del url: {self.server_name_url}{name}')
        return self.fw.api_delete(self.server_name_url + name, msg)

    def send_query_now(self, msg=False):
        # not need post data
        logger.info(f'send_query_now post url: {self.query_url}')
        return self.fw.api_post(self.query_url, msg)

    def get_query_status(self):
        logger.info(f'get_query_status get url: {self.query_status_url}')
        return self.fw.api_get(self.query_status_url)


class StorageApi:
    '''Storage Class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/sysfile/storage'
        self.inital_storage_json = {
            "sysfile": {
                "storage_dev": 1,
                "logs_on_storage": True
            }
        }

    def configure_storage(self, logs_on_storage=True, storage_dev=1, msg=False):  # 1:primary,2:secondary
        json_input = copy.deepcopy(self.inital_storage_json)
        json_input['sysfile']['logs_on_storage'] = logs_on_storage
        json_input['sysfile']['storage_dev'] = storage_dev
        logger.info(f'configure storage post url: {self.url}')
        logger.info(json_input)
        return self.fw.api_put(self.url, msg, data=json_input)

