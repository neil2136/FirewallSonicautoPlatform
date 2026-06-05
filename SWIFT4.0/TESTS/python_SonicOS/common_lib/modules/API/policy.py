import copy
import sys

from runner.settings import logger


class SecurityPolicyApi:
    '''SecurityPolicyApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_v4 = 'api/sonicos/security-policies/ipv4/'
        self.url_v6 = 'api/sonicos/security-policies/ipv6/'

    def add_security_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['security_policies'][0].keys():
            url = self.url_v6
        else:
            url = self.url_v4
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def get_security_policy(self, version = 'v4'):
        if version == 'v4':
            url = self.url_v4
        else:
            url = self.url_v6
        resp = self.fw.api_get(url)
        return resp

    def get_security_policy_by_uuid(self, uuid, version = 'v4'):
        if version == 'v4':
            url = self.url_v4
        else:
            url = self.url_v6
        url_tmp = url + 'uuid/' + uuid
        resp = self.fw.api_get(url_tmp)
        return resp

    def get_security_policy_uuid(self, name ,version = 'ipv4'):
        if version == 'ipv4':
            url = self.url_v4
        else:
            url = self.url_v6
        resp = self.fw.api_get(url)
        for security_policy in resp['security_policies']:
            if security_policy[version]['name'] == name:
                uuid = security_policy[version]['uuid']
        return uuid
        
    def is_security_policy_exists(self,**kwd):
        url1 = 'api/sonicos/security-policies/ipv4/'
        version = "ipv4"
        if "version" in kwd.keys():
            if kwd["version"] == "ipv6":
                url1 =  'api/sonicos/security-policies/ipv6/'
                version = "ipv6"
            kwd.remove("version")
        access_rules = self.fw.api_get(url1)
        logger.info('---***'*20)
        logger.info(access_rules)
        kwd_len = len(kwd)
        rc = False
        for access_rule in access_rules['security_policies']:
            flag = 0
            for key in kwd.keys():
                if access_rule[version][key] != kwd[key]:
                    logger.info('The key is')
                    break
                elif access_rule[version][key] == kwd[key]:
                    flag += 1
            if flag == kwd_len:
                logger.info("The access rule is exited")
                logger.info(access_rule)
                logger.info('--**--'*20)
                rc = True
                break  
        return rc

    def edit_security_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['security_policies'][0].keys():
            url = self.url_v6
        else:
            url = self.url_v4
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp
        
    def edit_security_policy_by_uuid(self, uuid, msg=False, version = 'v4', **kwargs):
        json_input = copy.deepcopy(kwargs)
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        url_tmp = url + 'uuid/' + uuid
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def del_security_policy(self, name,version ='v4'):
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        for policy in policies['security_policies']:
            print(policy)
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                url_tmp = url + 'uuid/' + uuid
                resp = self.fw.api_delete(url_tmp)
        return resp

    '''
    return:
    {'uuid': '00000000-0000-0019-0700-004010292f2d', 'id': 1, 'from': 'LAN', 'to': 'WAN', 'priority': 2, 'source': 'any', 
    'destination': 'any', 'sourceport': 'any', 'service': 'any', 'action': 'service action',
     'enable': 'enable', 'rxbytes': 0, 'rxpackets': 0, 'txbytes': 0, 'txpackets': 0, 
     'usage': 17, 'time_last_hit': 1591164780, 'time_created': 1591097303, 'time_updated': 1591097303, 'iptype': 'IPv4'}
    '''
    def get_security_policy_statistics(self, name,version ='v4'):
        if version == 'v4':
            url1 = self.url_v4
            url2 = 'api/sonicos/reporting/security-policies/ipv4'
            version = 'ipv4'
        else:
            url1 = self.url_v6
            url2 = 'api/sonicos/reporting/security-policies/ipv6'
            version = 'ipv6'
        policies = self.fw.api_get(url1)
        statistics = self.fw.api_get(url2)
        uuid = ''
        for policy in policies['security_policies']:
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                break
        for stat in statistics:
            if stat['uuid'] == uuid:
                return stat
        else:
            logger.error('error: cannot find {} in security policies '.format(name)) 

    def del_all_ipv4_security_policy(self):
        url = 'api/sonicos/all-security-policies/ipv4'
        resp = self.fw.api_delete(url)
        return resp
    
    def del_all_ipv6_security_policy(self):
        url = 'api/sonicos/security-policies/ipv6'
        resp = self.fw.api_delete(url)
        return resp
            

class CFSSettingApi():
    '''CFSSettingApi'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/content-filter/cfs/base'

    def config_cfs_setting(self,msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp
        
    def get_cfs_setting(self):
        resp = self.fw.api_get(self.url)
        return resp


class GAVSignaturesApi():
    '''GAVSignaturesApi'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/gateway-antivirus/signatures'

    def config_gav_signatures(self, id, msg=False, action = 'enable'):
        if action == 'enable':
            enable = True
        else:
            enable = False
        json_input = {
            "gateway_antivirus":{
                "signature":[
                    {
                        "enable":enable,
                        "id": id
                    }]
            }
        }

        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp
        

class RoutePolicyApi:
    '''RoutePolicyApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_v4 = 'api/sonicos/route-policies/ipv4'   #manual add rule
        self.url_v6 = 'api/sonicos/route-policies/ipv6'
        self.url_v4_auto = 'api/sonicos/reporting/route-policies/ipv4/system' #auto added rule
        self.url_v6_auto = 'api/sonicos/reporting/route-policies/ipv6/system' #auto added rule
        self.url_v4_dynamic = 'api/sonicos/reporting/route-policies/ipv4/dynamic'  # dynamic added rule
        self.url_v6_dynamic = 'api/sonicos/reporting/route-policies/ipv6/dynamic'  # dynamic added rule
        self.url_v4_del = 'api/sonicos/route-policies-ipv4/all'
        self.url_v6_del = 'api/sonicos/route-policies-ipv4/all'
        self.url_getobject = 'api/sonicos/dynamic-file/getObjectList.json?type=134217728'
        self.url_route = 'api/sonicos/routing'
        

    def add_route_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['route_policies'][0].keys():
            url = self.url_v6
        else:
            url = self.url_v4
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def get_route_policy(self, version = 'v4'):
        if version == 'v4':
            url = self.url_v4
        else:
            url = self.url_v6
        resp = self.fw.api_get(url)
        return resp

    def get_auto_route_policy(self, version = 'v4'):
        if version == 'v4':
            url = self.url_v4_auto
        else:
            url = self.url_v6_auto
        resp = self.fw.api_get(url)
        return resp

    def get_dynamic_route_policy(self, version='v4'):
        if version == 'v4':
            url = self.url_v4_dynamic
        else:
            url = self.url_v6_dynamic
        resp = self.fw.api_get(url)
        return resp
        
    def get_route_policy_by_name(self, name, version = 'v4'):
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['route_policies']:
            print(policy)
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                break
        if uuid == None:
            resp = 'Not found designated route policy'
            return resp
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_get(url_tmp)
        return resp

    def del_route_policy_by_uuid(self, uuid, version = 'v4'):
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_delete(url_tmp)
        return resp

    def del_route_policy_by_name(self, name, version = 'v4'):
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['route_policies']:
            logger.info(policy)
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                break
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_delete(url_tmp)
        return resp
    
    def del_all_route_policies(self, version='v4'):
        url = 'api/sonicos/route-policies-sdwan/all'
        res = self.fw.api_delete(url)
        logger.info(f'must delete sdwan first: {res}')
        if version == 'v4':
            url = self.url_v4_del
        else:
            url = self.url_v6_del
        return self.fw.api_delete(url)

    def edit_route_policy_by_uuid(self, uuid, msg=False, version = 'v4', **kwargs):
        json_input = copy.deepcopy(kwargs)
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def edit_route_policy(self, name, version = 'v4', **kwargs):
        json_input = copy.deepcopy(kwargs)
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['route_policies']:
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                break
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_put(url_tmp, data=json_input)
        return resp

    def export_route_policies(self, msg=False):
        url_tmp = 'api/sonicos/export/route-policies'
        resp = self.fw.api_get(url_tmp)
        return resp

    def export_route_policies_address_objects(self):
        url_tmp = 'api/sonicos/export/address-objects'
        resp = self.fw.api_get(url_tmp)
        return resp

    def export_route_policies_service(self):
        url_tmp = 'api/sonicos/export/services'
        resp = self.fw.api_get(url_tmp)
        return resp

    def route_policies_reporting(self, version = 'v4', r_type = 'system'):
        url_tmp = 'api/sonicos/reporting/route-policies/'
        if version == 'v4':
            if r_type == 'system':
                url_tmp = url_tmp + 'ipv4/system'
            else:
                url_tmp = url_tmp + 'ipv4/dynamic'
        else:
            if r_type == 'system':
                url_tmp = url_tmp + 'ipv6/system'
            else:
                url_tmp = url_tmp + 'ipv6/dynamic'
        resp = self.fw.api_get(url_tmp)
        return resp

    def clear_counter_route_policies(self, msg=False):
        url_tmp = 'api/sonicos/raw'
        resp = self.fw.api_post(url_tmp, msg, data=json_input)
        return resp

    def get_route_policy_uuid(self, name, version = 'v4'):
        uuid = None
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['route_policies']:
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                break
        return uuid

    def get_route_policy_status(self,name=None):
        url = 'api/sonicos/dynamic-file/getPolicyStats.json?type=4'
        resp = self.fw.api_get(url)
        resp=resp['entries']
        if name:
            uuid=self.get_route_policy_uuid(name)
            logger.info(uuid)
            for policy in resp.split('|'):
                if policy.split(',')[1] == uuid:
                    resp = policy.split(',')[-1]
                    break
        return resp

    def get_route_policy_stats(self, name=None):
        url = 'api/sonicos/dynamic-file/getPolicyStats.json?type=4'
        resp = self.fw.api_get(url)
        resp = resp['entries']
        if name:
            uuid = self.get_route_policy_uuid(name)
            logger.info(uuid)
            for policy in resp.split('|'):
                if policy.split(',')[1] == uuid:
                    resp = policy.split(',')
                    break
        return resp

    def get_route_pol_list(self):
        logger.info(f'getObjectList get url: {self.url_getobject}')
        objectlist = self.fw.api_get(self.url_getobject)
        if isinstance(objectlist, dict) and "routePolArray" in objectlist.keys():
            return objectlist["routePolArray"]
        else:
            return ''

    def del_all_ipv4_route_policy(self):
        url = 'api/sonicos/route-policies-ipv4/all'
        resp = self.fw.api_delete(url)
        return resp

    def config_route_settings(self,msg=False,metric = 50):
        json_input = {"routing":{
            "ipv6":{
                "default_route_metric":metric
                }
            }}
        resp = self.fw.api_put(self.url_route, msg, data=json_input)
        return resp

    def get_route_settings(self):
        resp = self.fw.api_get(self.url_route)
        return resp

    def get_route_policies_by_uuid(self, uuid, version = 'v4'):
        if version == 'v4':
            url = self.url_v4 + '/uuid/' + uuid
        else:
            url = self.url_v6 + '/uuid/' + uuid
        logger.info("GET from URL: {}".format(url))
        resp = self.fw.api_get(url)
        return resp


class PolicySettingsApi:
    '''PolicySettingsApi class'''
    default_values = {
        'application_based': 'zone',
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/policies-setting/base'
        self.initial_json_base_setting = {
            "policies_setting": {
                "application_based_on": "policy",
                "block_connections": {
                    "application_signatures_unavailable": True,
                    "malware_databases_not_downloaded": True
                },
                "active_application_caching": True,
                "cached_application_bypass": True,
                "application_cache": {
                    "default": {
                        "timeout": 10,
                        "threshold": 100
                    },
                    "global": {
                        "timeout": {
                            "enable": True,
                            "value": 10
                        },
                        "threshold": {
                            "enable": True,
                            "value": 100
                        }
                    }
                }
            }
        }

    def build_json_base_setting(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_base_setting)
        logger.info(json_input)
        try:
        	#App/Match/Malware tab
            if 'application_based' in kwargs.keys():
                json_input['policies_setting']['application_based_on'] = kwargs['application_based']
                if kwargs['application_based'] == 'policy':
                    json_input['policies_setting']['app_custom_malware_mode'] = 'policy'
        except KeyError:
            logger.error('Error: in creating JSON for policy settings')
        return json_input

    def get_policy_settings(self):
        get_response = self.fw.api_get(self.url)
        return get_response

    def configure_policy_settings(self, msg=False, **kwargs):
        self.options = dict(self.default_values)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_base_setting(**kwargs)
        logger.info('The json input build is', json_input)
        response = self.fw.api_put(self.url, msg, data=json_input)
        return response

    def get_dpi_ssl_client_general(self):
        url = 'api/sonicos/dpi-ssl/client/base'
        resp = self.fw.api_get(url)
        return resp

    def config_dpi_ssl_client_general(self, msg=False, **kwargs):
        url = 'api/sonicos/dpi-ssl/client/base'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def get_dpi_ssl_server_general(self):
        url = 'api/sonicos/dpi-ssl/server/base'
        resp = self.fw.api_get(url)
        return resp

    def config_dpi_ssl_server_general(self, msg=False, **kwargs):
        url = 'api/sonicos/policies-setting/base'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def add_ssl_servers(self, msg=False, **kwargs):
        url = 'api/sonicos/dpi-ssl/server/ssl-servers'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp
		
    def config_dpi_ssh_general(self, msg=False, **kwargs):
        url = 'api/sonicos/dpi-ssh'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp
        
    def get_gav_status(self):
        url = 'api/sonicos/reporting/gateway-antivirus'
        resp = self.fw.api_get(url)
        return resp

    def update_gav_signatures(self):
        url = 'api/sonicos/gateway-antivirus/update-signatures'
        resp = self.fw.api_post(url)
        return resp		


class DecryptionPolicyApi:
    '''DecryptionPolicyApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_client = 'api/sonicos/decryption-policies/client'
        self.url_server = 'api/sonicos/decryption-policies/server'
        self.url_ssh = 'api/sonicos/decryption-policies/ssh'
        self.url_statistics = 'api/sonicos/reporting/decryption-policies'    

    def add_decryption_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'client' in kwargs['decryption_policy'].keys():
            url = self.url_client
        elif 'ssh' in kwargs['decryption_policy'].keys():
            url = self.url_ssh
        else:
            url = self.url_server
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def get_decryption_policy(self, version = 'v4',type = 'client'):
        if type == 'client':
            url = self.url_client
        elif type == 'ssh':
            url = self.url_ssh
        else:
            url = self.url_server
        resp = self.fw.api_get(url)
        return resp

    def get_decryption_policy_by_name(self, name, version='v4', type='client'):
        if type == 'client':
            url = self.url_client
        elif type == 'ssh':
            url = self.url_ssh
        else:
            url = self.url_server
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['decryption_policy'][type]:
            if policy['name'] == name:
                uuid = policy['uuid']
                logger.info(uuid)
                break
        if uuid == None:
            resp = 'Not found designated decryption policy'
            return resp
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_get(url_tmp)
        return resp

    def edit_decryption_policy(self, name, msg=False, type = 'client', **kwargs):
        if type == 'client':
            url = self.url_client
        elif type == 'ssh':
            url = self.url_ssh
        else:
            url = self.url_server
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['decryption_policy'][type]:
            logger.info(policy)
            if policy['name'] == name:
                uuid = policy['uuid']
                break
        url_tmp = url + '/uuid/' + uuid
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        json_input['decryption_policy'][type][0]['uuid'] = uuid
        logger.info(json_input)
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def del_decryption_policy(self, name, type = 'client' ):
        if type == 'client':
            url = self.url_client
        elif type == 'ssh':
            url = self.url_ssh
        else:
            url = self.url_server
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['decryption_policy'][type]:
            if policy['name'] == name:
                uuid = policy['uuid']
                logger.info(uuid)
                break
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_delete(url_tmp)
        return resp
    
    def get_decryption_policies_statistics(self, type = 'client'):
        if type == 'client':
            url = self.url_statistics + "/client"
        elif type == 'ssh':
            url = self.url_statistics + "/ssh"
        else:
            url = self.url_statistics + "/server"
        logger.info(url)
        resp = self.fw.api_get(url)
        return resp

    def get_decryption_policy_statistics(self, name, type = 'client'):
        if type == 'client':
            url = self.url_client
        elif type == 'ssh':
            url = self.url_ssh
        else:
            url = self.url_server
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['decryption_policy'][type]:
            logger.info(policy)
            if policy['name'] == name:
                uuid = policy['uuid']
                break
        url_tmp = self.url_statistics + "/" + type + '/uuid/' + uuid
        logger.info(url_tmp)
        resp = self.fw.api_get(url_tmp)
        return resp

    def del_all_client_decryption_policy(self):
        url = 'api/sonicos/all-decryption-policies/client'
        resp = self.fw.api_delete(url)
        return resp
       

class ShadowApi:
    '''ShadowApi'''
    
    def __init__(self, fw): 
        self.fw = fw
        self.url_generate = 'api/sonicos/diag/shadow'
        self.url_export = 'api/sonicos/export/shadow-rule-list'
        self.url_generate_shadow = 'api/sonicos/shadow-rules-list/generate'
        self.url_get_shadow_policy = 'api/sonicos/dynamic-file/getShadowPolicies.json'

    def generate_rule_list(self, type, msg=False):
        type_list = ('access-rules','route-policies','decryption-policies','dos-policies','nat-policies')
        if type:
            if type not in type_list:
                logger.error('type is incorrect for shadow generate rule list.')
                return False
            else:
                url_tmp = self.url_generate + "/" + type
        else:
            logger.error('type shoule be specified for shadow generate rule list.')
            return False
        resp = self.fw.api_post(url_tmp, msg)
        return resp

    def export_rule_list(self, type):
        type_list = ('access-rules','route-policies','decryption-policies','dos-policies','nat-policies')
        if type:
            if type not in type_list:
                logger.error('type is incorrect for shadow export rule list.')
                return False
            else:
                url_tmp = self.url_export + "/" + type
        else:
            logger.error('type shoule be specified for shadow export rule list.')
            return False
        resp = self.fw.api_get(url_tmp)
        return resp
    
    def generate_shadow(self, type, msg=False):
        type_list = ('access-rules','route-policies','decryption-policies','dos-policies','nat-policies')
        if type:
            if type not in type_list:
                logger.error('type is incorrect for shadow generate rule list.')
                return False
            else:
                url_tmp = self.url_generate_shadow + "/" + type
        else:
            logger.error('type shoule be specified for shadow generate rule list.')
            return False
        resp = self.fw.api_post(url_tmp, msg)
        return resp

    def get_shadow_policy_status(self, type, name=None):
        type_dict = {'access-rules': "1", 'nat-policies': "2", 'decryption-policies': "8", 'dos-policies': "16", 'route-policies': "5"}
        if type:
            if type not in type_dict.keys():
                logger.error('type is incorrect for shadow generate rule list.')
                return False
            else:
                url = self.url_get_shadow_policy + "?lookupType=" + type_dict.get(type)
        else:
            logger.error('type shoule be specified for shadow generate rule list.')
            return False

        resp = self.fw.api_get(url)
        return resp
 
		
class DosPolicyApi:
    '''DosPolicyApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/dos-policies'
        self.url1='api/sonicos/dos-action-profiles'

    def get_dos_policies(self):
        resp = self.fw.api_get(self.url)
        return resp

    def get_dos_policy_by_name(self, name):
        policies = self.fw.api_get(self.url)
        uuid = None
        for policy in policies['dos_policies']:
            print(policy)
            if policy['name'] == name:
                uuid = policy['uuid']
                break
        if uuid == None:
            resp = 'Not found designated dos policy'
            return resp
        url_tmp = self.url + '/uuid/' + uuid
        resp = self.fw.api_get(url_tmp)
        return resp

    def add_dos_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def edit_dos_policy_by_uuid(self, uuid, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url_tmp = self.url + '/uuid/' + uuid
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def edit_dos_policy_by_name(self, name, msg=False, **kwargs):
        policies = self.fw.api_get(self.url)
        uuid = None
        for policy in policies['dos_policies']:
            if policy['name'] == name:
                uuid = policy['uuid']
                break
        if uuid == None:
            resp = 'Not found designated dos policy'
            return resp
        url_tmp = self.url + '/uuid/' + uuid
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def del_dos_policy(self, name):
        policies = self.fw.api_get(self.url)
        uuid = None
        for policy in policies['dos_policies']:
            logger.info(policy)
            if policy['name'] == name:
                uuid = policy['uuid']
                break
        url_tmp = self.url + '/uuid/' + uuid
        resp = self.fw.api_delete(url_tmp)
        return resp

    def export_dos_policies(self):
        url_export = 'api/sonicos/export/dos-policies'
        resp = self.fw.api_get(url_export)
        return resp

    def reporting_dos_policies_counter_status(self):
        url_reporting = 'api/sonicos/reporting/dos-policies/counter-status'
        resp = self.fw.api_get(url_reporting)
        return resp

    def reporting_dos_policies_statistics(self):
        url_reporting = 'api/sonicos/reporting/dos-policies/statistics'
        resp = self.fw.api_get(url_reporting)
        return resp

    def reporting_dos_policies_counters(self):
        url_reporting = 'api/sonicos/reporting/dos-policies/counters'
        resp = self.fw.api_get(url_reporting)
        return resp

    def get_dos_action_profile(self):
        resp = self.fw.api_get(self.url1)
        return resp

    def add_dos_action_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.url1, msg, data=json_input)
        return resp

    def edit_dos_action_profile_by_uuid(self, uuid, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url_tmp = self.url1 + '/uuid/' + uuid
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def edit_dos_action_profile_by_name(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url_tmp = self.url1 + '/name/' + name
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def delete_dos_action_profile_by_name(self, name):
        if name:
            url = self.url1 + '/name/'+name
        else:
            logger.error('name should be specified for delete dos action profile.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def del_all_dos_action_profile(self):
        url = 'api/sonicos/all-dos-policies'
        resp = self.fw.api_delete(url)
        return resp

    def get_dos_policy_by_uuid(self, uuid):
        url = self.url + '/uuid/' + uuid
        logger.info("GET from URL: {}".format(url))
        resp = self.fw.api_get(url)
        return resp

    def delete_dos_policy_by_uuid(self, uuid):
        url = self.url + '/uuid/' + uuid
        logger.info("delete URL: {}".format(url))
        resp = self.fw.api_delete(url)
        return resp

    def reporting_dos_policies_statistics_by_uuid(self, uuid):
        url_reporting = 'api/sonicos/reporting/dos-policies/statistics' + '/uuid/' + uuid
        resp = self.fw.api_get(url_reporting)
        return resp

    def delete_dos_policies_statistics_by_uuid(self, uuid):
        url_reporting = 'api/sonicos/reporting/dos-policies/statistics' + '/uuid/' + uuid
        resp = self.fw.api_delete(url_reporting)
        return resp

    def reporting_dos_policies_counters_by_uuid(self, uuid):
        url_reporting = 'api/sonicos/reporting/dos-policies/counters' + '/uuid/' + uuid
        resp = self.fw.api_get(url_reporting)
        return resp


class NatPolicyApi:
    '''NatPolicyApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_v4 = 'api/sonicos/nat-policies/ipv4/'
        self.url_v6 = 'api/sonicos/nat-policies/ipv6/'
        self.url = 'api/sonicos/nat-policies/nat64/'
        self.url_64 = 'api/sonicos/nat-policies/nat64/'
        self.init_nat64_json = {
            "nat_policies": [
                {"nat64": {
                    "comment": "test",
                    "enable": True,
                    "inbound": "any",
                    "name": "",
                    "outbound": "any",
                    "pref64": {
                        # "any": True
                    },
                    "service": {"icmp_udp_tcp": True},
                    "source": {
                        # "any": True
                    },
                    "ticket": {"tag1": "", "tag2": "", "tag3": ""},
                    "translated_destination": {
                        "embedded_ipv4_address": True
                    },
                    "translated_service": {
                        "original": True
                    },
                    "translated_source": {
                        # "any": True
                    }
                    }
                }
            ]
        }

    def build_nat64_json(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.init_nat64_json)
            json_input["nat_policies"][0]["nat64"]['name'] = kwargs['name']
            json_input["nat_policies"][0]["nat64"]['pref64']['name'] = kwargs['pref64']
            json_input["nat_policies"][0]["nat64"]['source'] = kwargs['src']
            json_input["nat_policies"][0]["nat64"]['translated_source']['name'] = kwargs['translated_src']
        except Exception as e:
            logger.error(f'Error: In creating JSON for nat64 rule {e})')
        logger.info("nat64 rule json obtained")
        return json_input    
    
    def add_nat_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        if 'ipv6' in kwargs['nat_policies'][0].keys():
            url = self.url_v6
        else:
            url = self.url_v4
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp
        
    def add_nat64_policy(self, msg=False, **kwargs):
        """
        example: kwargs = {
                    "name": "tc2",
                    "pref64": "Well-Known Pref64",
                    "src": {"any": True},
                    "translated_src": "name": "X1 IP"
                    }
        """
        json_input = self.build_nat64_json(**kwargs)
        resp = self.fw.api_post(self.url_64, msg, data=json_input)
        return resp

    def edit_nat64_policy_by_name(self, name:str, msg=False, **kwargs):
        json_input = {}
        if not name:
            logger.error('param name must be specified!!')
            return False
        policies = self.get_nat64_policy()
        try:
            for policy in policies['nat_policies']:
                if policy["nat64"]["name"] == name:
                    uuid = policy['nat64']['uuid']
                    url = self.url_64+'uuid/'+uuid
                    json_input = {'nat_policies':[policy]}
                    json_input['nat_policies'][0]['nat64'].update(kwargs)
                    logger.info(f'json_input:\n{json_input}')
                    resp = self.fw.api_put(url, msg, data=json_input)
                    return resp
        except Exception as e:
            logger.error(repr(e))
            return False

    def get_nat_policy(self, version = 'v4'):
        if version == 'v4':
            url = self.url_v4
        elif version == 'v64':
            url = self.url_64
        else:
            url = self.url_v6
        resp = self.fw.api_get(url)
        return resp

    def get_nat_policy_by_name(self, name, version='v4'):
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        elif version == 'v64':
            url = self.url_64
            version = 'nat64'
        else:
            url = self.url_v6
            version = 'ipv6'
        resp = self.fw.api_get(url)
        if name:
            for policy in resp['nat_policies']:
                if policy[version]['name'] == name:
                    resp = policy[version]
                    break
        return resp

    def get_nat64_policy(self):
        resp = self.fw.api_get(self.url_64)
        return resp

    def del_nat_policy(self, name, version ='v4'):
        if version == 'nat64':
            url = self.url
            version = 'nat64'
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        if version == 'v6':
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        for policy in policies['nat_policies']:
            print(policy)
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                url_tmp = url + 'uuid/' + uuid
                resp = self.fw.api_delete(url_tmp)
        return resp
    
    def edit_nat_policy_by_uuid(self, uuid, msg=False, version = 'v4', **kwargs):
        json_input = copy.deepcopy(kwargs)
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        url_tmp = url + 'uuid/' + uuid
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp
        
    def edit_nat_policy_by_name(self, name, msg=False, version='v4', **kwargs):
        json_input = copy.deepcopy(kwargs)
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        for policy in policies['nat_policies']:
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                url_tmp = url + 'uuid/' + uuid
                resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def del_all_nat_policy(self):
        url = 'api/sonicos/all-nat-policies'
        resp = self.fw.api_delete(url)
        return resp
    
    def del_nat_policy_by_name(self, name, version='ipv4', msg=False):
        if not name:
            logger.error("param <name> must be specified!!")
            return False
        if version == 'ipv4':
            url = 'api/sonicos/nat-policies/ipv4/'
        else:
            url = 'api/sonicos/nat-policies/ipv6/'
        resp = self.fw.api_get(url)
        for rule in resp['nat_policies']:
            if rule[version]['name'] == name:
                uuid = rule[version]['uuid']
                url_tmp = url + 'uuid/' + uuid
                return self.fw.api_delete(url_tmp, msg)
        logger.error(f'not found the nat rule <{name}>')
        return False

    def get_statistics_by_name(self, name, version='ipv4'):
        if version not in ('ipv4', 'ipv6', 'nat64'):
            logger.error("param 'version' value must be 'ipv4', 'ipv6' or 'nat64'")
            return {}
        if version == 'ipv6':
            url = self.url_v6
        elif version == 'nat64':
            url = self.url_64
        else:
            url = self.url_v4
        policies = self.fw.api_get(url)
        for policy in policies['nat_policies']:
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                url_temp = 'api/sonicos/reporting/nat-policies/'+version
                url_report = url_temp+'/uuid/'+uuid
                resp = self.fw.api_get(url_report)
                return resp
        logger.error(f'not found the <{name}> nat policy')
        return {}

        
class CFSCustomCategoryApi:
    '''CFSCustomCategoryApi class'''
    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/content-filter/cfs/custom-category/base'
        self.url = 'api/sonicos/content-filter/cfs/custom-category/category-entries'

    def get_cfs_custom_category_sattus(self):
        resp = self.fw.api_get(self.base_url)
        return resp

    def config_cfs_custom_category_status(self,  msg=False, status= 'enable'):
        json_input = {
            "content_filter": {
                "cfs": {
                    "custom_category": {
                    }
                }
            }
        }
        if status == 'enable':
            json_input["content_filter"]["cfs"]["custom_category"]["enable"] = True
        else:
            json_input["content_filter"]["cfs"]["custom_category"]["enable"] = False
        resp = self.fw.api_put(self.base_url, msg, data=json_input)
        return resp

    def add_cfs_custom_category(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def get_cfs_custom_category(self, domain=None):
        if domain:
            url = self.url + '/domain/' + domain
        else:
            url = self.url
        resp = self.fw.api_get(url)
        return resp

    def edit_cfs_custom_category_by_domain(self, domain, msg=False, **kwargs):
        if domain:
            url = self.url + '/domain/'+domain
        else:
            logger.error('domain shoule be specified for edit web_category.')
            return False
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def del_cfs_custom_category_by_domain(self,domain):
        if domain:
            url = self.url + '/domain/'+domain
        else:
            logger.error('name shoule be specified for delete cfs_custom_category.')
            return False
        resp = self.fw.api_delete(url)
        return resp        


class AppRulesApi:
    '''AppRulesApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/app-rules/policies'
        self.url_base = 'api/sonicos/app-rules/base/'

    def add_apprule(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        url = self.url
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def config_apprule_setting(self, msg=False, **kwargs):
        setting_json = {
            'app_rules': {
                'enable': 'True',
                'log_redundancy': {}
            }
        }
        if 'enable' in kwargs.keys():
            setting_json['app_rules']['enable'] = kwargs['enable']
        if 'log_redundancy' in kwargs.keys():
            setting_json['app_rules']['log_redundancy'] = kwargs['log_redundancy']
        app_setting_resp = self.fw.api_put(self.url_base, msg, data=setting_json)
        return app_setting_resp

    def delete_apprule_object_byname(self, name):
        url = self.url + '/name/' + name
        appruleobject_resp = self.fw.api_delete(url)
        return appruleobject_resp

    def get_apprule_obj(self):
        url= self.url
        appruleobject_resp = self.fw.api_get(url)
        return appruleobject_resp

    def edit_app_rule(self, name, msg=False, **kwargs):
        url = self.url + '/name/' + name
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        app_setting_resp = self.fw.api_put(url, msg, data=json_input)
        return app_setting_resp

    def get_apprule_settings(self):
        resp = self.fw.api_get(self.url_base)
        return resp

    def get_app_rule(self, name):
        url = self.url + '/name/' + name
        resp = self.fw.api_get(url)
        return resp
