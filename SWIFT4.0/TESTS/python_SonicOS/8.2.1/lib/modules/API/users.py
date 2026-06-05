import copy
import json
import re
import traceback
import collections
from collections import OrderedDict
import urllib3
import requests
from pprint import pprint
from runner.settings import logger
from modules.API.users import UserStatusApi
from modules.API.users import UsersettingApi
from modules.API.users import RadiusApi
from modules.API.users import LdapApi
from modules.API.users import SSOApi
from modules.API.users import UserLocalApi
from modules.API.users import UserGuestApi
from modules.API.users import UserLoginApi
from modules.API.users import TacacsApi
from modules.API.users import SAMLApi


class SAMLApi(SAMLApi):
    '''SAMLApi Class'''


class TacacsApi(TacacsApi):
    '''TacacsApi Class'''

class UserStatusApi(UserStatusApi):
    '''UserStatusApi Class'''


class UsersettingApi(UsersettingApi):
    default_user_session_options = {
        'service': {},
        'originating_externally': "",
        'other_unidentified': "",
        'ssoFailUserName': 'Unknown (SSO failed)',
        'bypassSsoUserName': 'Unknown (SSO bypassed)',
        'show_user_status_window': True,
        'disconnected_user_detect': True,
        'period_in_seconds': 120,
        'open_in_same_window': False,
    }
    '''UsersettingApi Class'''
    def __init__(self, fw):
        super().__init__(fw)
        self.fw = fw
        self.url1 = 'api/sonicos/user/authentication/base'
        self.url2 = 'api/sonicos/user/authentication/methods'
        self.bypass = 'api/sonicos/user/authentication/rule-auth-bypass-http-urls'
        self.initial_user_methods_json = {
            "user": {
                "auth": {
                    "auth_method": "locals",
                    "sso_method": {
                        "sso_agent": False,
                        "terminal_services_agent": False,
                        "radius_accounting": False,
                        "third_party_api": False,
                        "capture_client": False,
                        "browser_ntlm": {}
                    }
                }
            }
        }
        self.initial_user_session_json = {
            "user": {
                "auth": {
                    "inactivity_timeout": 15,
                    "prevent_inactivity_logout": {
                        "service": {}
                    },
                    "log_user_name": {
                        "originating_externally": "",
                        "other_unidentified": "",
                        "sso_fail": "Unknown (SSO failed)",
                        "bypass_sso": "Unknown (SSO bypassed)"
                    },
                    "user_connections_logout": {
                        "inactivity": {
                            "authentication": {
                                "keep_alive": True
                            },
                            "other": {
                                "keep_alive": True
                            }
                        },
                        "reported": {
                            "authentication": {
                                "terminate": {
                                    "now": True
                                }
                            },
                            "other": {
                                "terminate": {
                                    "after": 15
                                }
                            }
                        }
                    },
                    "inactive_user": {
                        "login": True,
                        "timeout": True
                    },
                    "age_out": 60,
                    "show_user_status_window": True,
                    "disconnected_user_detect": True,
                    "status_window_heartbeat": {
                        "period": 120,
                        "timeout": 10
                    },
                    "open_in_same_window": False,
                    "web_login_session_limit": 30
                }
            }
        }    

    def user_session(self, msg=False, **kwargs):
        self.options = dict(UsersettingApi.default_user_session_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_user_session_json)
            logger.info("\n\nInitial Json is :\n")
            pprint(json_input)
            if ('inactivity_time_in_minutes' in kwargs.keys() and kwargs['inactivity_time_in_minutes']):
                json_input['user']['auth']['inactivity_timeout'] = kwargs['inactivity_time_in_minutes']
            if 'service' in kwargs.keys():
                if 'group' in kwargs['service']:
                    json_input['user']['auth']['prevent_inactivity_logout']['service']['group'] = {}
                    json_input['user']['auth']['prevent_inactivity_logout']['service']['group']['serviceGroupName'] = kwargs['service'][1]
                elif 'name' in kwargs['service']:
                    json_input['user']['auth']['prevent_inactivity_logout']['service']['name'] = kwargs['service'][1]
                else:
                    logger.error('Please specify service type')
            json_input['user']['auth']['log_user_name']['originating_externally'] = kwargs['originating_externally']
            json_input['user']['auth']['log_user_name']['other_unidentified'] = kwargs['other_unidentified']
            if 'ssoFailUserName' in kwargs.keys():
                if kwargs['ssoFailUserName']:
                    json_input['user']['auth']['log_user_name']['sso_fail'] = kwargs['ssoFailUserName']
                else:
                    del json_input['user']['auth']['log_user_name']['sso_fail']
            if 'bypassSsoUserName' in kwargs.keys():
                if kwargs['bypassSsoUserName']:
                    json_input['user']['auth']['log_user_name']['bypass_sso'] = kwargs['bypassSsoUserName']
                else:
                    del json_input['user']['auth']['log_user_name']['bypass_sso']
            if ('inactivity_authentication' in kwargs.keys() and kwargs['inactivity_authentication']):
                if 'terminate_now' in kwargs['inactivity_authentication']:
                    del json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['keep_alive']
                    json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['terminate'] = {}
                    json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['terminate']['now'] = True
                elif 'terminate_after' in kwargs['inactivity_authentication'][0]:
                    del json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['keep_alive']
                    json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['terminate'] = {}
                    json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['terminate']['after'] = 15
                    json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['terminate']['after'] = kwargs['inactivity_authentication'][1]
                else:
                    logger.error('Please verify the style for connections requiring user authentication on logout due to inactivity')
            if ('inactivity_other' in kwargs.keys() and kwargs['inactivity_other']):
                if 'terminate_now' in kwargs['inactivity_other']:
                    del json_input['user']['auth']['user_connections_logout']['inactivity']['other']['keep_alive']
                    json_input['user']['auth']['user_connections_logout']['inactivity']['other']['terminate'] = {}
                    json_input['user']['auth']['user_connections_logout']['inactivity']['other']['terminate']['now'] = True
                elif 'terminate_after' in kwargs['inactivity_other'][0]:
                    del json_input['user']['auth']['user_connections_logout']['inactivity']['other']['keep_alive']
                    json_input['user']['auth']['user_connections_logout']['inactivity']['other']['terminate'] = {}
                    json_input['user']['auth']['user_connections_logout']['inactivity']['other']['terminate']['after'] = 15
                    json_input['user']['auth']['user_connections_logout']['inactivity']['other']['terminate']['after'] = kwargs['inactivity_other'][1]
                else:
                    logger.error('Please verify the style for other connections on logout due to inactivity')
            if ('reported_authentication' in kwargs.keys() and kwargs['reported_authentication']):
                if 'keep_alive' in kwargs['reported_authentication']:
                    del json_input['user']['auth']['user_connections_logout']['reported']['authentication']['terminate']
                    json_input['user']['auth']['user_connections_logout']['reported']['authentication']['keep_alive'] = True
                elif 'terminate_after' in kwargs['reported_authentication'][0]:
                    del json_input['user']['auth']['user_connections_logout']['reported']['authentication']['terminate']['now']
                    json_input['user']['auth']['user_connections_logout']['reported']['authentication']['terminate']['after'] = 15
                    json_input['user']['auth']['user_connections_logout']['reported']['authentication']['terminate']['after'] = kwargs['reported_authentication'][1]
                else:
                    logger.error('Please verify the style for connections requiring user authentication on active/reported logout')
            if ('reported_other' in kwargs.keys() and kwargs['reported_other']):
                if 'keep_alive' in kwargs['reported_other']:
                    del json_input['user']['auth']['user_connections_logout']['reported']['other']['terminate']
                    json_input['user']['auth']['user_connections_logout']['reported']['other']['keep_alive'] = True
                elif 'terminate_now' in kwargs['reported_other']:
                    del json_input['user']['auth']['user_connections_logout']['reported']['other']['terminate']['after']
                    json_input['user']['auth']['user_connections_logout']['reported']['other']['terminate']['now'] = True
                elif 'terminateMinute' in kwargs.keys():
                    json_input['user']['auth']['user_connections_logout']['reported']['other']['terminate'] \
                        ['after'] = kwargs['terminateMinute']
                else:
                    logger.error('Please verify the style for other connections on active/reported logout')
            if 'inactive_user' in kwargs.keys():
                for key1 in kwargs['inactive_user']:
                    json_input['user']['auth']['inactive_user'][key1] = kwargs['inactive_user'][key1]
            if ('age_out_time_in_minutes' in kwargs.keys() and kwargs['age_out_time_in_minutes']):
                json_input['user']['auth']['age_out'] = kwargs['age_out_time_in_minutes']
            if 'show_user_status_window' in kwargs.keys():
                if (isinstance(kwargs['show_user_status_window'], bool) and kwargs['show_user_status_window'] is True):
                    json_input['user']['auth']['show_user_status_window'] = True
                    json_input['user']['auth']['status_window_heartbeat']['period'] = kwargs['period_in_seconds']
                    if 'disconnected_user_detect' in kwargs.keys():
                        if (isinstance(kwargs['disconnected_user_detect'], bool) and kwargs['disconnected_user_detect'] is True):
                            json_input['user']['auth']['disconnected_user_detect'] = True
                            if ('heartbeat_time_in_minutes' in kwargs.keys() and kwargs['heartbeat_time_in_minutes']):
                                json_input['user']['auth']['status_window_heartbeat']['timeout'] = kwargs['heartbeat_time_in_minutes']
                            else:
                                pass
                        else:
                            json_input['user']['auth']['disconnected_user_detect'] = False
                            del json_input['user']['auth']['status_window_heartbeat']['timeout']
                    json_input['user']['auth']['open_in_same_window'] = kwargs['open_in_same_window']
                    if 'web_login_session_limit' in kwargs.keys():
                        if kwargs['web_login_session_limit']:
                            json_input['user']['auth']['web_login_session_limit'] = kwargs['web_login_session_limit']
                        else:
                            del json_input['user']['auth']['web_login_session_limit']
                else:
                    json_input['user']['auth']['show_user_status_window'] = False
                    del json_input['user']['auth']['open_in_same_window']
                    del json_input['user']['auth']['disconnected_user_detect']
                    del json_input['user']['auth']['status_window_heartbeat']
                    
        
        except KeyError:
            logger.info("Error in creating JSON for user_session setting")
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        user_auth_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return user_auth_resp


class RadiusApi(RadiusApi):
    '''RadiusApi Class'''


class LdapApi(LdapApi):
    '''LdapApi Class'''


class UserLocalApi(UserLocalApi):
    '''UserLocalApi Class'''


class UserGuestApi(UserGuestApi):
    '''UserGuestApi Class'''

        
class UserLoginApi(UserLoginApi):
    '''UserLoginApi Class'''
    
    
class SSOApi:
    '''SSOApi class'''

    default_sso_setting_options = {
        'EnableSSOagentauthentication': False,
        'terminal_services_agent': False,
        'enablessobyradiusaccounting': False,
        'next_agent_on_no_name': False,
        'block_traffic': True,
        'local_users_only': False,
        'non_domain_limited_access': False,
        'probe': {},
        'user_group_mechanism': 'ldap',
        'pollrate': 5,
        'pollsame_agent': False,
        'holdtime_after_failure': 1,
        'holdtime_after_no_user': 1,
        'dummy_user': {},
        'tsa_services_bypass': True,
        'radius_accountingport': 1813
    }

    default_sso = {}
    # sso_bypass/sso_agent/terminal_services_agent/sso_radius_accounting_client
    # /sso_enforce_on_zone/windows_service_user_name

    def __init__(self, fw):
        self.fw = fw
        self.url1 = 'api/sonicos/user/sso/settings'
        self.url2 = 'api/sonicos/user/sso/agents'
        self.sso_base = 'api/sonicos/user/sso/base'
        self.edit_sso_name = 'api/sonicos/user/sso/agents/name/'
        self.url3 = 'api/sonicos/user/sso/terminal-services-agents'
        self.url4 = 'api/sonicos/user/sso/radius-accounting-clients'
        self.url5 = 'api/sonicos/reporting/sso-statistic/global'
        self.url6 = 'api/sonicos/reporting/sso-statistic/terminal-services-agent'
        self.url7 = 'api/sonicos/reporting/sso-statistic/radius-accounting-client'
        self.url8 = 'api/sonicos/reporting/sso-status'
        self.url9 = 'api/sonicos/user/sso/enforce-on-zone'
        self.url10 = 'api/sonicos/user/sso/windows-service-user-name'
        self.url11 = 'api/sonicos/user/sso/agent'
        self.url12 = 'api/sonicos/user/sso/terminal-services-agent'
        self.url13 = 'api/sonicos/user/sso/radius-accounting-client'
        self.sso_test = 'api/sonicos/user/sso/test'
        self.edit_rac = 'api/sonicos/user/sso/radius-accounting-clients/name/'
        self.edit_tsa_name = 'api/sonicos/user/sso/terminal-services-agents/name/'

        self.initial_sso_settings_json = {
            "user": {
                "sso": {
                    "method": {
                        "sso_agent": False,
                        "terminal_services_agent": False,
                        "radius_accounting": False
                    },
                    "next_agent_on_no_name": False,
                    "block_traffic": True,
                    "local_users_only": False,
                    "non_domain_limited_access": False,
                    "probe": {
                        # "netapi": {
                            # "over_tcp": true
                        # },
                        # "timeout": 10,
                        # "test_mode": true
                    },
                    "user_group_mechanism": {
                        "ldap": True
                    },
                    "hold_time": {
                        "after_failure": {
                            "minutes": 1
                        },
                        "after_no_user": {
                            "minutes": 1
                        }
                    },
                    "tsa_services_bypass": True,
                    'dummy_user': {},
                    "poll": {
                        "rate": {
                            "minutes": 5
                        },
                        "same_agent": False
                    },
                    "radius_accounting": {
                        "port": 1813
                    }
                }
            }
        }

        self.sso_enforce_on_zone_json = {
            "user": {
                "sso": {
                    # "enforce_on_zone": [
                        # {
                            # "zone_name": "LAN"
                        # },
                        # {
                            # "zone_name": "DMZ"
                        # },
                        # {
                            # "zone_name": "VPN"
                        # },
                        # {
                            # "zone_name": "MGMT"
                        # },
                        # {
                            # "zone_name": "WLAN"
                        # }
                    # ]
                }
            }
        }

        self.initial_sso_bypass_json = {
            "user": {
                "sso": {
                    # "security_service_bypass": [
                    #     {
                    #         "service": {
                    #             "built_in": "VOIP"
                    #         },
                    #         "type": "trigger-sso"
                    #     },
                    # ]
                }
            }
        }

        self.initial_sso_agents_json = {
            "user": {
                "sso": {
                    # "agent": [
                    #     {
                    #         "host": "10.10.10.11",
                    #         "port": 2258,
                    #         "timeout": 11,
                    #         "retries": 5,
                    #         "max_requests": 31,
                    #         "enable": True,
                    #         "shared_key": {
                    #             "number": ""
                    #         }
                    #     }
                    # ]
                }
            }
        }
        self.initial_terminal_services_agent_json = {
            "user": {
                 "sso": {
                     # "terminal_services_agent": [
                     #     {
                     #         "host": "10.10.10.11",
                     #         "port": 2259,
                     #         "enable": True,
                     #         "shared_key": {
                     #             "number": ""
                     #        }
                     #     }
                     # ]
                 }
            }
        }

        self.initial_sso_radius_accounting_client_json = {
            "user": {
                "sso": {
                    # "radius_accounting_client": [
                    #     {
                    #         "host": "10.10.10.10",
                    #         "shared_secret": {
                    #             "secret": ""
                    #         },
                    #         "user_name_format": {
                    #             "canonical": True
                    #         },
                    #         "missing_domain": {
                    #             "local_user": True
                    #         },
                    #         "log_user_out": 11,
                    #         "server": [
                    #             {
                    #                 "serverId": 1,
                    #                 "name": "10.10.10.101",
                    #                 "port": 51813,
                    #                 "shared_secret": ""
                    #             },
                    #             {
                    #                 "serverId": 2,
                    #                 "name": "10.10.10.102",
                    #                 "port": 1813,
                    #                 "shared_secret": ""
                    #             },
                    #             {
                    #                 "serverId": 3,
                    #                 "name": "0.0.0.0",
                    #                 "port": 1813,
                    #                 "shared_secret": ""
                    #             },
                    #             {
                    #                 "serverId": 4,
                    #                 "name": "0.0.0.0",
                    #                 "port": 1813,
                    #                 "shared_secret": ""
                    #             }
                    #         ],
                    #         "proxy_forward": {
                    #             "timeout": 11,
                    #             "retries": 4,
                    #             "type": {
                    #                 "forward_to_all": True
                    #             }
                    #         }
                    #     }
                    # ]
                }
            }
        }

    def show_sso_settings(self):
        output = self.fw.api_get(self.url1)
        return output

    def show_sso_base(self):
        output = self.fw.api_get(self.sso_base)
        return output

    def config_sso_base_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(self.sso_base, msg, data=json_input)
        return repu_resp

    def show_sso_agent_test(self):
        output = self.fw.api_get(self.sso_test)
        return output

    def show_sso_agents(self):
        output = self.fw.api_get(self.url2)
        return output
        
    def show_sso_statistic(self):
        output = self.fw.api_get(self.url5)
        return output

    def show_sso_reporting_status(self):
        output = self.fw.api_get(self.url8)
        return output
        
    def sso_settings(self, msg=False, **kwargs):
        self.options = dict(SSOApi.default_sso_setting_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = copy.deepcopy(self.initial_sso_settings_json)
        logger.info("\n\nInitial json file is:\n")
        pprint(json_input)
        try:
            json_input['user']['sso']['method']['sso_agent'] = kwargs['EnableSSOagentauthentication']
            json_input['user']['sso']['method']['terminal_services_agent'] = kwargs['terminal_services_agent']
            json_input['user']['sso']['method']['radius_accounting'] = kwargs['enablessobyradiusaccounting']
            json_input['user']['sso']['next_agent_on_no_name'] = kwargs['next_agent_on_no_name']
            json_input['user']['sso']['local_users_only'] = kwargs['local_users_only']
            json_input['user']['sso']['non_domain_limited_access'] = kwargs['non_domain_limited_access']
            json_input['user']['sso']['user_group_mechanism'][kwargs['user_group_mechanism']] = True
            json_input['user']['sso']['poll']['rate']['minutes'] = kwargs['poll_rate']
            json_input['user']['sso']['poll']['same_agent'] = kwargs['poll_same_agent']
            json_input['user']['sso']['hold_time']['after_failure']['minutes'] = kwargs['holdtime_after_failure']
            json_input['user']['sso']['hold_time']['after_no_user']['minutes'] = kwargs['holdtime_after_no_user']
            json_input['user']['sso']['tsa_services_bypass'] = kwargs['tsa_services_bypass']
            json_input['user']['sso']['radius_accounting']['port'] = kwargs['radius_accounting_port']
        except KeyError:
            logger.info("Error: In creating JSON for SSO settings")
        if 'block_traffic' in kwargs.keys():
            if kwargs['block_traffic'] == True:
                json_input['user']['sso']['block_traffic'] = True
            else:
                json_input['user']['sso']['block_traffic'] = False
                if 'including_for_access_rules' in kwargs.keys():
                    json_input['user']['sso']['including_for_access_rules'] = {}
                    json_input['user']['sso']['including_for_access_rules'][kwargs['including_for_access_rules']] = True
                else:
                    pass
        if ('dummy_user_name' in kwargs.keys() and kwargs['dummy_user_name']):
            json_input['user']['sso']['dummy_user']['name'] = {}
            json_input['user']['sso']['dummy_user']['name']['userName'] = kwargs['dummy_user_name']
            if ('dummy_user_timeout' in kwargs.keys() and kwargs['dummy_user_timeout']):
                json_input['user']['sso']['dummy_user']['timeout'] = {}
                json_input['user']['sso']['dummy_user']['timeout']['inactiveTimeValue'] = kwargs['dummy_user_timeout']
            else:
                logger.error('Dummy_user_timeout must be specified')
        if ('probeusersfor' in kwargs.keys() and kwargs['probeusersfor']):
            if kwargs['probeusersfor'] == 'wmi':
                json_input['user']['sso']['probe']['wmi'] = True
            else:
                json_input['user']['sso']['probe']['netapi'] = {}
                json_input['user']['sso']['probe']['netapi'][kwargs['probeusersfor']] = True
            if ('probetimeout' in kwargs.keys() and kwargs['probetimeout']):
                json_input['user']['sso']['probe']['timeout'] = kwargs['probetimeout']
            if 'probetest_mode' in kwargs.keys():
                json_input['user']['sso']['probe']['test_mode'] = kwargs['probetest_mode']

        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        sso_setting_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return sso_setting_resp

    def add_enforce_on_zone(self, msg=False, **kwargs):
        self.options = dict(SSOApi.default_sso)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = copy.deepcopy(self.sso_enforce_on_zone_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        if 'enforce_on_zone' in kwargs.keys():
            json_input['user']['sso']['enforce_on_zone'] = []
            for key in kwargs['enforce_on_zone']:
                json_input['user']['sso']['enforce_on_zone'].append({'zone_name': key})
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        enforce_on_zone = self.fw.api_put(self.url1, msg, data=json_input)
        return enforce_on_zone

    def del_enforce_on_zone(self, delete_zone):
        url = str(self.url9) + '/' + delete_zone
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def edit_sso_agent(self,msg=False, name=None, port=None ,**kwargs):
        if not name or not port:
            logger.info('Please specify agent name or agent port')
            return False
        url_edit = self.edit_sso_name + name + '/port/' + str(port)
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(url_edit, msg, data=json_input)
        return repu_resp

    def del_sso_agent(self,msg=False, name=None, port=None):
        if not name or not port:
            logger.info('Please specify agent name or agent port')
            return False
        url_del = self.edit_sso_name + name + '/port/' + str(port)
        output = self.fw.api_delete(url_del)
        return output
   
    def test_sso_agent(self,ip,port = 2258):
        sso_test = {
            "user":{
                "sso":{
                    "test":{
                        "agent":{
                            "name_or_ip_addr":ip,
                            "port": 2258
                            }
                        }
                        }
                    }
            }
        resp = self.fw.api_post(self.sso_test, msg=True, data=sso_test)
        return resp
    
    def add_windows_service_user_name(self, msg=False, **kwargs):
    # windows_service on SSO--SSO Agents---General Setting---User names used by Windows services
        self.options = dict(SSOApi.default_sso)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = copy.deepcopy(self.sso_enforce_on_zone_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        if 'windows_service_user_name' in kwargs.keys():
            json_input['user']['sso']['windows_service_user_name'] = []
            for key in kwargs['windows_service_user_name']:
                json_input['user']['sso']['windows_service_user_name'].append({'name': key})
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        enforce_on_zone = self.fw.api_post(self.url1, msg, data=json_input)
        return enforce_on_zone

    def del_windows_service_user_name(self, delete_windows_service):
        url = str(self.url10) + '/' + delete_windows_service
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def sso_bypass(self, msg=False, **kwargs):
        self.options = dict(SSOApi.default_sso)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_sso_bypass(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd sso bypass service\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                sso_bypass = self.fw.api_post(self.url1, msg, data=json_input)
                return sso_bypass
            elif kwargs['action'] == 'delete':
                logger.info("\n\nEdit sso bypass service\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                sso_bypass = self.fw.api_delete(self.url1, msg, data=json_input)
                return sso_bypass
            else:
                pass

    def build_sso_bypass(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_sso_bypass_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        if 'security_service_bypass' in kwargs.keys():
            json_input['user']['sso']['security_service_bypass'] = []
            for key in kwargs['security_service_bypass']:
                json_input['user']['sso']['security_service_bypass'].append(kwargs['security_service_bypass'][key])

        return json_input

    def sso_agent(self, msg=False, **kwargs):
        self.options = dict(SSOApi.default_sso)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_ssoagent(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd sso agent\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                sso_agents_resp = self.fw.api_post(self.url2, msg, data=json_input)
                return sso_agents_resp
            elif kwargs['action'] == 'edit':
                logger.info("\n\nEdit sso agent\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                sso_agents_resp = self.fw.api_put(self.url2, msg, data=json_input)
                return sso_agents_resp
            else:
                pass

    def edit_sso_agent_name_port(self,msg=False, name=None, port=None, **kwargs):
        if not name:
            logger.info('Please specify agent name')
            return False
        if not port:
            logger.info('Please specify agent port number')
            return False
        url_edit = self.edit_sso_name + name + '/port/' + port
        print(url_edit)
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(url_edit, msg, data=json_input)
        return repu_resp

    def build_json_ssoagent(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_sso_agents_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['sso']['agent'] = []
        json_input1 = self.sub_dict(**kwargs)
        json_input['user']['sso']['agent'].append(json_input1)

        return json_input

    def sub_dict(self, **kwargs):
        json_input = {}
        if ('host' in kwargs.keys() and kwargs['host']):
            json_input['host'] = kwargs['host']
        if 'enable' in kwargs.keys():
            json_input['enable'] = kwargs['enable']
        if ('port' in kwargs.keys() and kwargs['port']):
            json_input['port'] = kwargs['port']
        if ('number' in kwargs.keys() and kwargs['number']):
            json_input['shared_key'] = kwargs['shared_key']
        if ('timeout' in kwargs.keys() and kwargs['timeout']):
            json_input['timeout'] = kwargs['timeout']
        if ('retries' in kwargs.keys() and kwargs['retries']):
            json_input['retries'] = kwargs['retries']
        if ('max_requests' in kwargs.keys() and kwargs['max_requests']):
            json_input['max_requests'] = kwargs['max_requests']
        if ('shared_key' in kwargs.keys() and kwargs['shared_key']):
            json_input['shared_key'] = kwargs['shared_key']

        return json_input

    def terminal_services_agent(self, msg=False, **kwargs):
        self.options = dict(SSOApi.default_sso)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_tsa(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd terminal services agent\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                tsr_resp = self.fw.api_post(self.url3, msg, data=json_input)
                return tsr_resp
            elif kwargs['action'] == 'edit':
                logger.info("\n\nEdit terminal services agent\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                tsr_resp = self.fw.api_put(self.url3, msg, data=json_input)
                return tsr_resp


    def build_json_tsa(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_terminal_services_agent_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['sso']['terminal_services_agent'] = []
        json_input1 = self.sub_terminal_services_agent(**kwargs)
        json_input['user']['sso']['terminal_services_agent'].append(json_input1)

        return json_input

    def sub_terminal_services_agent(self, **kwargs):
        json_input = {}
        if ('host' in kwargs.keys() and kwargs['host']):
            json_input['host'] = kwargs['host']
        if 'enable' in kwargs.keys():
            json_input['enable'] = kwargs['enable']
        if ('port' in kwargs.keys() and kwargs['port']):
            json_input['port'] = kwargs['port']
        if ('number' in kwargs.keys() and kwargs['number']):
            json_input['shared_key'] = {}
            json_input['shared_key']['number'] = kwargs['number']

        return json_input
        
    def del_terminal_services_agent(self, del_tsa):
        url = str(self.url12) + '/' + del_tsa
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def sso_radius_accounting_client(self, msg=False, **kwargs):
        self.options = dict(SSOApi.default_sso)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_srac(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd sso radius accounting client\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                srac_resp = self.fw.api_post(self.url4, msg, data=json_input)
                return srac_resp
            elif kwargs['action'] == 'edit':
                logger.info("\n\nEdit sso radius accounting client\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                srac_resp = self.fw.api_put(self.url4, msg, data=json_input)
                return srac_resp

    def build_json_srac(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_sso_radius_accounting_client_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['sso']['radius_accounting_client'] = []
        json_input1 = self.sub_sso_radius_accounting_client(**kwargs)
        json_input['user']['sso']['radius_accounting_client'].append(json_input1)

        return json_input

    def sub_sso_radius_accounting_client(self, **kwargs):
        json_input = {}
        if ('host' in kwargs.keys() and kwargs['host']):
            json_input['host'] = kwargs['host']
        if 'user_name_format' in kwargs.keys():
            if (kwargs['user_name_format'] == 'user_name' or kwargs['user_name_format'] == 'sonicwall_aventail'):
                json_input['user_name_format'] = {}
                json_input['user_name_format'][kwargs['user_name_format']] = True
            # kwargs['user_name_format'] == 'down_level_logon' or kwargs['user_name_format'] == 'canonical'
                 # or kwargs['user_name_format'] == 'user_principle'
            else:
                json_input['user_name_format'] = {}
                json_input['user_name_format'][kwargs['user_name_format']] = True
                if 'missing_domain' in kwargs.keys():
                    json_input['missing_domain'] = {}
                    json_input['missing_domain'][kwargs['missing_domain']] = True
                else:
                    pass
        if ('secret' in kwargs.keys() and kwargs['secret']):
            json_input['shared_secret'] = kwargs['secret']
            # json_input['shared_secret'] = {}
            # json_input['shared_secret']['secret'] = kwargs['secret']
        if ('log_user_out' in kwargs.keys() and kwargs['log_user_out']):
            json_input['log_user_out'] = kwargs['log_user_out']
        if ('proxy_forward' in kwargs.keys() and kwargs['proxy_forward'] == True):
            json_input['proxy_forward'] = {}
            if ('proxyforward_timeout' in kwargs.keys() and kwargs['proxyforward_timeout']):
                json_input['proxy_forward']['timeout'] = kwargs['proxyforward_timeout']
            if ('proxyforward_retries' in kwargs.keys() and kwargs['proxyforward_retries']):
                json_input['proxy_forward']['retries'] = kwargs['proxyforward_retries']
            if 'server' in kwargs.keys():
                json_input['server'] = []
                for key in kwargs['server']:
                    json_input['server'].append(kwargs['server'][key])
                if ('proxyforward_type' in kwargs.keys() and kwargs['proxyforward_type']):
                    json_input['proxy_forward']['type'] = {}
                    json_input['proxy_forward']['type'][kwargs['proxyforward_type']] = True

        return json_input

    def del_sso_radius_accounting_client(self, del_srac):
        url = str(self.url13) + '/' + del_srac
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def edit_terminal_services_agent_name_port(self, msg=False, name=None, port=None, **kwargs):
        if not name:
            logger.info('Please specify terminal service agent name')
            return False
        if not port:
            logger.info('Please specify terminal service agent port')
            return False
        url_name = self.edit_tsa_name + name + '/port/' + port
        json_input = copy.deepcopy(kwargs)
        response = self.fw.api_put(url_name, msg, data=json_input)
        return response
    
    def get_terminal_services_agent_by_host(self, msg=False, host=None,port=None):
        if not host:
            logger.info('Pls specify the agent host.')
            return False
        url = self.url3 + '/name/' + host + '/port/' +  port
        repu_resp = self.fw.api_get(url, msg)
        return repu_resp
    
    def del_terminal_services_agent_by_host(self, msg=False, host=None,port=None):
        if not host:
            logger.info('Pls specify the agent host.')
            return False
        url = self.url3 + '/name/' + host + '/port/' +  port
        repu_resp = self.fw.api_delete(url, msg)
        return repu_resp

    def edit_radius_accounting_client(self, msg=False, name=None, **kwargs):
        if not name:
            logger.info('Please specify radius accounting client name')
            return False
        url_name = self.edit_rac + name
        json_input = copy.deepcopy(kwargs)
        response = self.fw.api_put(url_name, msg, data=json_input)
        return response