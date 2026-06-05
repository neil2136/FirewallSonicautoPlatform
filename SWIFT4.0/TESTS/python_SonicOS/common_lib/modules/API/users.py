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
import os


class UserStatusApi:
    '''UserStatusApi class'''

    default_management_options = {
        'inactive_users': False,
        'unauthenticated_users': False,
        }

    def __init__(self, fw):
        self.fw = fw
        self.url1 = 'api/sonicos/user/status/active'
        # self.url1 = 'api/sonicos/user/status/all'
        self.user_session = 'api/sonicos/user/sessions'
        self.url2 = 'api/sonicos/user/management'
        # self.url3 = 'api/sonicos/user/logged-in'
        # self.url4 = 'api/sonicos/user/name/{NAME}'
        # self.url5 = 'api/sonicos/user/at/{IP}'
        self.url6 = 'api/sonicos/user/status/inactive'
        self.url_session = 'api/sonicos/user/session/name/'
        self.url_session_inactive = 'api/sonicos/user/session/inactive/at/'
        self.url_session_active = 'api/sonicos/user/session/at/'
        self.url_unlock_user_ip = 'api/sonicos/user/lock/at/'
        self.url_unlock_user_name = 'api/sonicos/user/lock/name/'
        self.url_user_lockedout = 'api/sonicos/user/status/account-locked-out'
        self.url_unauth_users = 'api/sonicos/user/status/unauthenticated'
        
        self.initial_user_management_json = {
            "user": {
                "management": {
                    "include": {
                        "inactive_users": False,
                        "unauthenticated_users": False
                    }
                }
            }
        }

    def show_user_status(self,nologin=False):
        output = self.fw.api_get(self.url1,nologin = nologin)
        return output
        
    def show_user_status_inactive(self):
        output = self.fw.api_get(self.url6)
        return output
        
    def logout_user_ip(self,ip,msg=False,):
        if not ip:
            return False
        url = self.url_session_active + ip
        output = self.fw.api_delete(url,msg)
        return output
        
    def logout_user_session(self,msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_delete(self.user_session, msg, data=json_input)
        return repu_resp
        
    def show_user_status_by_name(self,name):
        url = 'api/sonicos/user/status/name/'+ name
        output = self.fw.api_get(url)
        return output

    def show_local_users_quota(self):
        url = 'api/sonicos/reporting/local/user/quota/users'
        output = self.fw.api_get(url)
        return output
        
    def user_logout_by_admin(self, name=None):
        if name:
            url = self.url_session + name
        else:
            logger.error("Pls enter user's name")
        output = self.fw.api_delete(url)
        return output
        
    def user_logout_by_active_user(self, ip=None):
        if ip:
            url = self.url_session_active + ip
        else:
            logger.error("Pls enter user's name")
        output = self.fw.api_delete(url)
        return output

    def user_logout_by_inactive_user(self, ip=None):
        if ip:
            url = self.url_session_inactive + ip
        else:
            logger.error("Pls enter user's name")
        output = self.fw.api_delete(url)
        return output

    def show_local_users_quota_by_name(self, name):
        url = 'api/sonicos/reporting/local/user/quota/users/name/' + name
        output = self.fw.api_get(url)
        return output

    def show_local_users_quota_by_domain(self, name, domainname):
        url = 'api/sonicos/reporting/local/user/quota/users/name/' + name + '/domain/' + domainname
        output = self.fw.api_get(url)
        return output
    
    def show_user_management(self):
        output = self.fw.api_get(self.url2)
        return output
        
    def user_management(self, msg=False, **kwargs):
        self.options = dict(UserStatusApi.default_management_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_user_management_json)
            pprint(json_input)
            json_input['user']['management']['include']['inactive_users'] = kwargs['inactive_users']
            json_input['user']['management']['include']['unauthenticated_users'] = kwargs['unauthenticated_users']
        except KeyError:
            logger.info("Error in creating JSON for user status setting")
        pprint(json_input)

        user_management_resp = self.fw.api_put(self.url2, msg, data=json_input)
        return user_management_resp
        
    def user_send_message(self,msg=False,nologin=False,**kwargs):
        url ='api/sonicos/send-message'
        json_input = copy.deepcopy(kwargs)
        return self.fw.api_post(url, msg,nologin=nologin, data=json_input)
    
    def unlock_user_ip(self, ip):
        url = self.url_unlock_user_ip + ip
        return self.fw.api_delete(url)
    
    def unlock_user_name(self, username):
        url = self.url_unlock_user_name + username
        return self.fw.api_delete(url)

    def get_locked_out_account(self):
        output = self.fw.api_get(self.url_user_lockedout)
        return output

    def get_unauthenticated_users(self):
        output = self.fw.api_get(self.url_unauth_users)
        return output
        
class UsersettingApi:
    '''UsersettingApi class'''
    
    default_authen_options = {
        "display_login_info": False,
        'case_sensitive_names': True,
        'login_uniqueness': False,
        'relogin_after_password_change': False,
        'method': 'local',
        'email_format': 'plain_text',
        'format': 'characters',
        'min': 10,
        'max': 10
    }
    default_auth_method_options = {
        'auth_method': 'local',
        'sso_agent': False,
        'terminal_services_agent': False,
        'radius_accounting': False,
        'third_party_api': False,
        'capture_client': False,
        'browser_ntlm': {}
    }

    default_weblogin_options = {
        'time_in_minutes': 1,
        'http_redirect_after_login': True,
        'browser_redirect_via': 'interface_ip',
    }
    default_user_session_options = {
        'service': {},
        'originating_externally': '',
        'other_unidentified': '',
        'sso_fail': 'Unknown (SSO failed)',
        'bypass_sso': 'Unknown (SSO bypassed)',
        'show_user_status_window': True,
        'disconnected_user_detect': True,
        'period_in_seconds': 120,
        'open_in_same_window': False,
    }
    default_customization_options = {
        'width': 460,
        'height': 310,
        'scroll_bars': True,
        # 'content': {},
        'trusted': True,
        'wan': False,
        'public': True,
        'wireless': False,
        'vpn': False,
        'preempt': {},
        'authentication': {},
        'logged_out': {},
        'full': {},
        'disallowed': {},
        'lockout': {},
        'status': {},
        'guest_status': {},
        'access_barred': {},
        'access_down': {},
        'access_unavailable': {},
        'redirect': {},
        'sso_failure': {},
        'password_update': {},
        'message': {}
    }

    def __init__(self, fw):
        self.fw = fw
        self.url1 = 'api/sonicos/user/authentication/base'
        self.url2 = 'api/sonicos/user/authentication/methods'
        self.bypass = 'api/sonicos/user/authentication/rule-auth-bypass-http-urls'
        
        self.initial_user_auth_json = {
            "user": {
                 "auth": {
                     "method": {
                        #"local": True
                     },
                     "case_sensitive_names": True,
                     "login_uniqueness": False,
                     "relogin_after_password_change": False,
                     "one_time_password": {
                         "email_format": {
                             "plain_text": True
                         },
                         "format": {
                            "characters": True
                         },
                         "length": {
                             "min": 10,
                             "max": 10
                         }
                     }
                 }
            }
        }
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
        self.initial_weblogin_json = {
            "user": {
                "auth": {
                    "auth_page_timeout": {
                        "time_in_minutes": 1
                    },
                    "browser_redirect_via": {
                        "interface_ip": True
                    },
                    "http_redirect_after_login": True,
                }
            }
        }
        self.initial_bypass_json = {
            "user": {
                "auth": {
                    "rule_auth_bypass_http_url": {
                        "url": ""
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
                        "originating_externally": {},
                        "other_unidentified": {},
                        "sso_fail": {
                            "ssoFailUserName": "Unknown (SSO failed)"
                        },
                        "bypass_sso": {
                            "bypassSsoUserName": "Unknown (SSO bypassed)"
                       }
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
                            "other":{"terminate":{"after":5}}
                        }
                    },
                    "inactive_user": {
                        "login": True,
                        "timeout": True
                    },
                    "age_out":60,
                    "show_user_status_window": True,
                    "disconnected_user_detect": True,
                    "status_window_heartbeat": {
                        "period": {
                            "period_in_seconds": 120
                        },
                        "timeout": 10
                    },
                    "open_in_same_window": False,
                    "web_login_session_limit": 30
                }
            }
        }
        self.initial_customization_json = {
            "user": {
                "auth": {
                    "policy_banner_before_login": False,
                    "policy_banner": {
                         "content": {}
                    },
                    "acceptable_use_policy": {
                        "window_size": {
                            "width": 460,
                            "height": 310
                        },
                        "scroll_bars": True,
                        # "content": {},
                        "aup_on_zones": {
                            "trusted": True,
                            "wan": False,
                            "public": True,
                            "wireless": False,
                            "vpn": False
                        }
                    },
                    "customize_login_page": {
                        "preempt": {},
                        "authentication": {},
                        "logged_out": {},
                        "full": {},
                        "disallowed": {},
                        "lockout": {},
                        "status": {},
                        "guest_status": {},
                        "access_barred": {},
                        "access_down": {},
                        "access_unavailable": {},
                        "redirect": {},
                        "sso_failure": {},
                        "password_update": {},
                        "message": {}
                    }
                }
            }
        }

    def show_user_setting(self):
        output = self.fw.api_get(self.url1)
        return output

    def show_user_auth(self):
        output = self.fw.api_get(self.url2)
        return output

    def user_authentication(self, msg=False, **kwargs):
        self.options = dict(UsersettingApi.default_authen_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_user_auth_json)
            logger.info("\n\nInitial Json is :\n")
            pprint(json_input)
            json_input['user']['auth']['display_login_info'] = kwargs['display_login_info']
            json_input['user']['auth']['method'] = kwargs['method']
            json_input['user']['auth']['one_time_password']['format'][kwargs['format']] = True
            json_input['user']['auth']['one_time_password']['email_format'][kwargs['email_format']] = True
            json_input['user']['auth']['case_sensitive_names'] = kwargs['case_sensitive_names']
            json_input['user']['auth']['login_uniqueness'] = kwargs['login_uniqueness']
            json_input['user']['auth']['relogin_after_password_change'] = kwargs['relogin_after_password_change']
            json_input['user']['auth']['one_time_password']['length']['min'] = kwargs['Onetimepasswordlengthmin']
            json_input['user']['auth']['one_time_password']['length']['max'] = kwargs['Onetimepasswordlengthmax']
        except KeyError:
            logger.info("Error in creating JSON for user_auth setting")
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        user_auth_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return user_auth_resp

    def user_method_authentication(self, msg=False, **kwargs):
        self.options = dict(UsersettingApi.default_auth_method_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_user_methods_json)
            logger.info("\n\nInitial Json is :\n")
            pprint(json_input)
            json_input['user']['auth']['auth_method'] = kwargs['auth_method']
            json_input['user']['auth']['sso_method']['sso_agent'] = kwargs['sso_agent']
            json_input['user']['auth']['sso_method']['terminal_services_agent'] = kwargs['terminal_services_agent']
            json_input['user']['auth']['sso_method']['radius_accounting'] = kwargs['radius_accounting']
            json_input['user']['auth']['sso_method']['third_party_api'] = kwargs['third_party_api']
            json_input['user']['auth']['sso_method']['capture_client'] = kwargs['capture_client']


        except KeyError:
            logger.info("Error in creating JSON for user_auth method setting")
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        user_auth_resp = self.fw.api_put(self.url2, msg, data=json_input)
        return user_auth_resp

    def web_login(self, msg=False, **kwargs):
        self.options = dict(UsersettingApi.default_weblogin_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_weblogin_json)
            logger.info("\n\nInitial Json is :\n")
            pprint(json_input)
            json_input['user']['auth']['browser_redirect_via'][kwargs['browser_redirect_via']] = True
            json_input['user']['auth']['auth_page_timeout']['time_in_minutes'] = kwargs['time_in_minutes']
            json_input['user']['auth']['http_redirect_after_login'] = kwargs['http_redirect_after_login']
        
        except KeyError:
            logger.info("Error in creating JSON for weblogin setting")
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        user_auth_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return user_auth_resp
    
    ########################API is ready, but not merge to related version######################      
    # def bypass(self, msg=False, **kwargs):
        # if ('add' or 'edit' in kwargs.keys()):
            # json_input = copy.deepcopy(self.initial_bypass_json)
            # if ('url' in kwargs.keys() and kwargs['url']):
                # json_input['user']['auth']['rule_auth_bypass_http_url']['url'] = kwargs['url']
        # else:
            # logger.info("Error in creating JSON for bypass setting")
            
        # pprint(json_input)

        # user_auth_resp = self.fw.api_put(self.url, msg, data=json_input)
        # return user_auth_resp

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
            if 'originating_externally' in kwargs.keys():
                json_input['user']['auth']['log_user_name']['originating_externally'] = kwargs['originating_externally']
            if 'other_unidentified' in kwargs.keys():
                json_input['user']['auth']['log_user_name']['other_unidentified'] = kwargs['other_unidentified']
            if 'sso_fail' in kwargs.keys():
                if kwargs['sso_fail']:
                    json_input['user']['auth']['log_user_name']['sso_fail'] = kwargs['sso_fail']
                else:
                    del json_input['user']['auth']['log_user_name']['sso_fail']
            if 'bypass_sso' in kwargs.keys():
                if kwargs['bypass_sso']:
                    json_input['user']['auth']['log_user_name']['bypass_sso'] = kwargs['bypass_sso']
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
                    json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['terminate']['after'] = {}
                    json_input['user']['auth']['user_connections_logout']['inactivity']['authentication']['terminate']['after'] \
                         = kwargs['inactivity_authentication'][1]
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
                    json_input['user']['auth']['user_connections_logout']['inactivity']['other']['terminate']['after'] = {}
                    json_input['user']['auth']['user_connections_logout']['inactivity']['other']['terminate'] \
                        ['after']['terminateMinute'] = kwargs['inactivity_other'][1]
                else:
                    logger.error('Please verify the style for other connections on logout due to inactivity')
            if ('reported_authentication' in kwargs.keys() and kwargs['reported_authentication']):
                if 'keep_alive' in kwargs['reported_authentication']:
                    del json_input['user']['auth']['user_connections_logout']['reported']['authentication']['terminate']
                    json_input['user']['auth']['user_connections_logout']['reported']['authentication']['keep_alive'] = True
                elif 'terminate_after' in kwargs['reported_authentication'][0]:
                    del json_input['user']['auth']['user_connections_logout']['reported']['authentication']['terminate']['now']
                    json_input['user']['auth']['user_connections_logout']['reported']['authentication']['terminate']['after'] = {}
                    json_input['user']['auth']['user_connections_logout']['reported']['authentication'] \
                        ['terminate']['after'] = kwargs['reported_authentication'][1]
                else:
                    logger.error('Please verify the style for connections requiring user authentication on active/reported logout')
            if ('reported_other' in kwargs.keys() and kwargs['reported_other']):
                if 'keep_alive' in kwargs['reported_other']:
                    del json_input['user']['auth']['user_connections_logout']['reported']['other']['terminate']
                    json_input['user']['auth']['user_connections_logout']['reported']['other']['keep_alive'] = True
                elif 'terminate_now' in kwargs['reported_other']:
                    del json_input['user']['auth']['user_connections_logout']['reported']['other']['terminate']['after']
                    json_input['user']['auth']['user_connections_logout']['reported']['other']['terminate'] \
                        ['now'] = True
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
                            json_input['user']['auth']['web_login_session_limit']  \
                                = kwargs['web_login_session_limit']
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
        
    def customization(self, msg=False, **kwargs):
        self.options = dict(UsersettingApi.default_customization_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_customization_json)
            logger.info("\n\nInitial Json is :\n")
            pprint(json_input)
            if 'policy_banner_before_login' in kwargs.keys():
                json_input['user']['auth']['policy_banner_before_login'] = kwargs['policy_banner_before_login']
            if ('pocontent' in kwargs.keys() and kwargs['pocontent']):
                json_input['user']['auth']['policy_banner']['content']['text'] = kwargs['pocontent']
            json_input['user']['auth']['acceptable_use_policy']['window_size']['width'] = kwargs['window_size_width']
            json_input['user']['auth']['acceptable_use_policy']['window_size']['height'] = kwargs['window_size_height']
            # width/height:400~1280
            json_input['user']['auth']['acceptable_use_policy']['scroll_bars'] = kwargs['scroll_bars']
            # json_input['user']['auth']['acceptable_use_policy']['content']['text'] = kwargs['content']
            if 'zonetype' in kwargs.keys():
                for key1 in kwargs['zonetype']:
                    json_input['user']['auth']['acceptable_use_policy']['aup_on_zones'][key1] = kwargs['zonetype'][key1]
            if 'loginpage' in kwargs.keys():
                for key1 in kwargs['loginpage']:
                    json_input['user']['auth']['customize_login_page'][key1]['text'] = kwargs['loginpage'][key1]
        except KeyError:
            logger.info("Error in creating JSON for add_customization setting")
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        user_auth_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return user_auth_resp
    def user_settings_base(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return repu_resp
        
    def add_bypass(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.bypass, msg, data=json_input)
        return repu_resp
    
    def get_bypass(self, msg=False, **kwargs):
        repu_resp = self.fw.api_get(self.bypass)
        return repu_resp
        
    def delete_bypass(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_delete(self.bypass, msg, data=json_input)
        return repu_resp

class TacacsApi:
    test_tacacs_server_json = {
        "user": {
            "tacacs": {
                "test": {
                    "name": "192.168.168.85"
                }
            }
        }
    }
    test_tacacs_accounting_json = {
        "user": {
            "tacacs": {
                "accounting":{
                    "test": {
                        "name": "192.168.168.85"
                    }
                }
            }
        }
    }
    default_user_tacacs_options = {
        'local_users_only': False,
        'default_user_group': {},
        'timeout': 5,
        'Retries': 3,
        'ldap': True
    }
    default_tacacs_server_options = {}
    default_tacacs_accounting_options = {}
    default_tacacs_accounting_base = {
        'timeout': 30,
        'retries': 3,
        'single_connect': True,
        'packet_encrypted': True,
        'watchdog_messages': 5,
        'web_login': False,
        'remote_client': False,
        'guest': False,
        'sso_authenticated': False,
        'sso_users_identified_via_radius_accounting': False,
        'domain_users': False
    }
    def __init__(self, fw):
        self.fw = fw
        self.url1 = 'api/sonicos/user/tacacs/servers'
        self.url2 = 'api/sonicos/user/tacacs/test'
        self.url3 = 'api/sonicos/user/tacacs/servers/name/'
        self.url4 = 'api/sonicos/user/tacacs/accounting/servers'
        self.url5 = 'api/sonicos/user/tacacs/accounting/base'
        self.url6 = 'api/sonicos/user/tacacs/accounting/servers/name/'
        self.url7 = 'api/sonicos/user/tacacs/accounting/test'
        self.url8 = 'api/sonicos/user/tacacs/base'

        self.initial_tacacs_servers_json = {
            "user": {
                "tacacs": {
                    # "server": [
                    #     {
                    #         "host": "",
                    #         "port": {
                    #             "port_num": ""
                    #         },
                    #         "shared_secret": {
                    #             "secret": ""
                    #         },
                    #         "send_through_vpn_tunnel": False,
                    #         "user_name_format": {
                    #             "user_name": True
                    #         },
                    #         "enable": True
                    #     },
                    #     {
                    #         "host": "",
                    #         "port": {
                    #             "port_num": ""
                    #         },
                    #         "shared_secret": {
                    #             "secret": ""
                    #         },
                    #         "send_through_vpn_tunnel": False,
                    #         "user_name_format": {
                    #             "user_name": True
                    #         },
                    #         "enable": True
                    #     },
                    # ]
                }
            }
        }
        self.initial_user_tacacs_json = {
            "user": {
                "tacacs": {
                    "local_users_only": False,
                    "default_user_group": {},
                    "timeout": {
                        "seconds": 5
                    },
                    "retries": {
                        "number": 3
                    },
                    "user_group_mechanism": {
                        "local_only": True
                    }
                }
            }
        }
        self.initial_tacacs_account_json = {
            'user': {
                'tacacs': {
                    'accounting': {
                        'server': [
                            {
                                # 'enable': True,
                                # 'host': '123.123.123.123',
                                # 'port': 1813,
                                # 'shared_secret': 'very_secret',
                                # 'user_name_format': {'down_level_logon': True}
                            },
                            {
                                # 'enable': True,
                                # 'host': '123.123.123.123',
                                # 'port': 1813,
                                # 'shared_secret': 'very_secret',
                                # 'user_name_format': {'down_level_logon': True}
                            }
                        ]
                    }
                }
            }
        }
        self.initial_user_acc_base_json = {
            "user": {
                "tacacs": {
                    "accounting": {
                        "timeout": 0,
                        "retries": 0,
                        "single_connect": False,
                        "packet_encrypted": False,
                        "watchdog_messages": 0,
                        "data": {
                            "web_login": False,
                            "remote_client": False,
                            "guest": False,
                            "sso_authenticated": False,
                            "sso_users_identified_via_radius_accounting": False
                        },
                        "include": {
                            "domain_users": False
                        }
                    }
                }
            }
        }

    def add_tacacs_server(self, msg=False, **kwargs):
        logger.info("\nAdd tacacs server\n")
        self.options = dict(TacacsApi.default_tacacs_server_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_tacacsserver(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        logger.info(json_input)
        tacacs_server_resp = self.fw.api_post(self.url1, msg, data=json_input)
        return tacacs_server_resp
    def build_json_tacacsserver(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_tacacs_servers_json)
        logger.info("\n\nInitial Json is :\n")
        logger.info(json_input)
        json_input['user']['tacacs']['server'] = []
        json_input1 = self.sub_dict(**kwargs)
        json_input['user']['tacacs']['server'].append(json_input1)
        return json_input
    def sub_dict(self, **kwargs):
        json_input = {}
        json_input['host'] = ''
        if ('host' in kwargs.keys() and kwargs['host']):
            json_input['host'] = kwargs['host']
        if 'enable' in kwargs.keys():
            json_input['enable'] = kwargs['enable']
        if ('port_num' in kwargs.keys() and kwargs['port_num']):
            json_input['port'] = {}
            json_input['port'] = kwargs['port_num']
        if ('secret' in kwargs.keys() and kwargs['secret']):
            json_input['shared_secret'] = {}
            json_input['shared_secret']= kwargs['secret']
        if 'send_through_vpn_tunnel' in kwargs.keys():
            json_input['through_vpn'] = kwargs['send_through_vpn_tunnel']
        return json_input

    def test_tacacs_server(self, msg=False, payload=test_tacacs_server_json):
        json_input = copy.deepcopy(payload)
        repu_resp = self.fw.api_post(self.url2, msg, data=json_input)
        return repu_resp

    def show_tacacs_server(self):
        output = self.fw.api_get(self.url1)
        return output

    def del_tacacs_server(self, tacacsserver_name):
        url = self.url1 + '/name/' + tacacsserver_name
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def show_tacacs_server_name(self, tacacsserver_name):
        url = self.url3 + tacacsserver_name
        logger.info(url)
        output = self.fw.api_get(url)
        return output

    def edit_tacacs_server(self, name=None, msg=False, **kwargs):
        logger.info("\nEdit Tacacs server\n")

        options = {**TacacsApi.default_tacacs_server_options, **kwargs}
        json_input = self.build_json_tacacsserver(**options)
        logger.info("\n\nUpdate Json is :\n")
        logger.info(json_input)
        if name:
            url = f'{self.url1}/name/{name}'
        else:
            url = self.url1
        # API call with the built JSON data
        tacacs_server_resp = self.fw.api_put(url, msg, data=json_input)
        return tacacs_server_resp

    def show_tacacs_accounts_base(self):
        output = self.fw.api_get(self.url5)
        return output

    def show_tacacs_account_name(self, tacacsaccount_name):
        url = self.url6 + tacacsaccount_name
        logger.info(url)
        output = self.fw.api_get(url)
        return output

    def show_tacacs_accounts(self):
        output = self.fw.api_get(self.url4)
        return output

    def del_tacacs_account(self, tacacsaccount_name):
        url = self.url6 + tacacsaccount_name
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def show_tacacs_base_settings(self):
        output = self.fw.api_get(self.url8)
        return output

    def user_tacacs_base_settings(self, msg=False, **kwargs):
        self.options = dict(TacacsApi.default_user_tacacs_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_user_tacacs_json)
            logger.info("\n\nInitial Json is :\n")
            logger.info(json_input)
            json_input['user']['tacacs']['local_users_only'] = kwargs['local_users_only']
            json_input['user']['tacacs']['default_user_group']['group_name'] = kwargs['group_name']
            json_input['user']['tacacs']['timeout']['seconds'] = kwargs['timeout']
            json_input['user']['tacacs']['retries']['number'] = kwargs['retries']
            json_input['user']['tacacs']['user_group_mechanism']['local_only'] = kwargs['local_only']
        except KeyError:
            logger.error("Error: in creating JSON for user radius")
        if ('mechanism_ldap' in kwargs.keys() and kwargs['mechanism_ldap']):
            del json_input['user']['tacacs']['user_group_mechanism']['radius_attribute']
            json_input['user']['tacacs']['user_group_mechanism']['ldap'] = True
        if ('mechanism_local_only' in kwargs.keys() and kwargs['mechanism_local_only']):
            del json_input['user']['tacacs']['user_group_mechanism']['radius_attribute']
            json_input['user']['tacacs']['user_group_mechanism']['local_only'] = True

        logger.info("\n\nUpdate Json is :\n")
        logger.info(json_input)

        user_tacacs_resp = self.fw.api_put(self.url8, msg, data=json_input)
        return user_tacacs_resp

    def add_tacacs_account(self, msg=False, **kwargs):
        json_input = self.build_json_tacacs_account(**kwargs)
        logger.info(f"Payload for adding tacacs accounting server = {json_input}")
        resp = self.fw.api_post(self.url4, msg, data=json_input)
        return resp

    def build_json_tacacs_account(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_tacacs_account_json)
        logger.info("\n\nInitial Json is :\n")
        logger.info(json_input)
        json_input['user']['tacacs']['accounting']['server'] = []
        json_input1 = self.sub_dict(**kwargs)
        json_input['user']['tacacs']['accounting']['server'].append(json_input1)
        return json_input

    def edit_tacacs_accounting(self,name=None,msg=False, **kwargs):
        logger.info("\nEdit Tacacs accounting\n")
        self.options = dict(TacacsApi.default_tacacs_accounting_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_tacacs_account(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        logger.info(json_input)
        if name:
            url = self.url4 + '/name/' + name
            tacacs_server_resp = self.fw.api_put(url, msg, data=json_input)
            return tacacs_server_resp
        else:
            tacacs_server_resp = self.fw.api_put(self.url4, msg, data=json_input)
        return tacacs_server_resp

    def test_tacacs_accounting(self, msg=False, payload=test_tacacs_accounting_json):
        json_input = copy.deepcopy(payload)
        repu_resp = self.fw.api_post(self.url7, msg, data=json_input)
        return repu_resp
    
    def user_tacacs_acc_base(self, msg=False, **kwargs):
        self.options = copy.deepcopy(TacacsApi.default_tacacs_accounting_base)
        self.options.update(kwargs)

        try:
            # Create a deep copy of the initial JSON to avoid modifying the original
            json_input = copy.deepcopy(self.initial_user_acc_base_json)
            logger.info("\n\nInitial Json is :\n")
            logger.info(json_input)

            # Update JSON based on the passed options
            json_input['user']['tacacs']['accounting']['timeout'] = self.options['timeout']
            json_input['user']['tacacs']['accounting']['retries'] = self.options['retries']
            json_input['user']['tacacs']['accounting']['single_connect'] = self.options['single_connect']
            json_input['user']['tacacs']['accounting']['packet_encrypted'] = self.options['packet_encrypted']
            json_input['user']['tacacs']['accounting']['watchdog_messages'] = self.options['watchdog_messages']

            json_input['user']['tacacs']['accounting']['data']['web_login'] = self.options['web_login']
            json_input['user']['tacacs']['accounting']['data']['remote_client'] = self.options['remote_client']
            json_input['user']['tacacs']['accounting']['data']['guest'] = self.options['guest']
            json_input['user']['tacacs']['accounting']['data']['sso_authenticated'] = self.options['sso_authenticated']
            json_input['user']['tacacs']['accounting']['data']['sso_users_identified_via_radius_accounting'] = self.options['sso_users_identified_via_radius_accounting']

            json_input['user']['tacacs']['accounting']['include']['domain_users'] = self.options['domain_users']

        except KeyError as e:
            logger.error(f"Error: Missing key {str(e)} in updating JSON")
            return None

        logger.info("\n\nUpdated Json is :\n")
        logger.info(json_input)
        # Make the API PUT call with the updated JSON
        user_tacacs_resp = self.fw.api_put(self.url5, msg, data=json_input)
        return user_tacacs_resp        

class RadiusApi:
    '''RadiusApi class'''

    default_user_radius_options = {
        'local_users_only': False,
        'default_user_group': {},
        'timeout': 5,
        'Retries': 3,
        'radius_attribute': 'vendor-specific'
    }

    default_radius_server_options = {}

    default_radius_account_options = {}
    test_radius_server_json = {
        "user": {
            "radius": {
                "test": {
                    "name": "192.168.168.85"
                }
            }
        }
    }

    def __init__(self, fw):
        self.fw = fw
        self.url1 = 'api/sonicos/user/radius/base'
        self.url2 = 'api/sonicos/user/radius/servers'
        self.url3 = 'api/sonicos/reporting/radius'
        self.url4 = 'api/sonicos/user/radius/accounting/servers'
        self.url5 = 'api/sonicos/user/radius/servers'
        self.url6 = 'api/sonicos/user/radius/accounting/servers'
        self.url7 = 'api/sonicos/user/radius/servers/name/'
        self.url8= 'api/sonicos/user/radius/test'
        self.url9= 'api/sonicos/user/radius/accounting/base'
        self.url10= 'api/sonicos/user/radius/accounting/test'

        self.initial_user_radius_json = {
            "user": {
                "radius": {
                    "local_users_only": False,
                    "default_user_group": {},
                    "timeout": {
                        "seconds": 5
                    },
                    "retries": {
                        "number": 3
                    },
                    "user_group_mechanism": {
                        "radius_attribute": "vendor-specific"
                    }
                }
            }
        }
        self.initial_radius_servers_json = {
            "user": {
                "radius": {
                    "server": [
                        {
                            "host": "",
                            "enable": True,
                            "port": 1,
                            # "partition": "",
                            "shared_secret": "",
                            "send_through_vpn_tunnel": True,
                            "user_name_format": {
                                "name_dot_domain": True
                            }
                        }
                    ]
                }
            }
        }
        self.initial_radius_accounts_json = {
            "user": {
                "radius": {
                    "accounting": {
                        "server": [
                            {
                                "host": "",
                                "enable": True,
                                "port": 1,
                                # "partition": "",
                                "shared_secret": "",
                                "send_through_vpn_tunnel": True,
                                "user_name_format": {
                                    #"name_dot_domain": True
                                }
                            }
                        ]
                    }
                }
            }
        }

    def test_radius_server(self, msg=False, payload=test_radius_server_json):
        json_input = copy.deepcopy(payload)
        repu_resp = self.fw.api_post(self.url8, msg, data=json_input)
        return repu_resp


    def show_user_radius_settings(self):
        output = self.fw.api_get(self.url1)
        return output
        
    def show_radius_server(self):
        output = self.fw.api_get(self.url2)
        return output
        
    def show_radius_account(self):
        output = self.fw.api_get(self.url4)
        return output 
        
    def show_radius_reporting_statistic(self):
        output = self.fw.api_get(self.url3)
        return output

    def del_radius_reporting_statistic(self):
        output = self.fw.api_delete(self.url3)
        return output

    def user_radius_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)

        self.options = dict(RadiusApi.default_user_radius_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_user_radius_json)
            logger.info("\n\nInitial Json is :\n")
            pprint(json_input)
            json_input['user']['radius']['local_users_only'] = kwargs['local_users_only']
            json_input['user']['radius']['default_user_group']['group_name'] = kwargs['group_name']
            json_input['user']['radius']['timeout']['seconds'] = kwargs['timeout']
            json_input['user']['radius']['retries']['number'] = kwargs['retries']
            json_input['user']['radius']['user_group_mechanism']['radius_attribute'] = kwargs['radius_attribute']
        except KeyError:
            logger.error("Error: in creating JSON for user radius")
        if ('mechanism_ldap' in kwargs.keys() and kwargs['mechanism_ldap']):
            del json_input['user']['radius']['user_group_mechanism']['radius_attribute']
            json_input['user']['radius']['user_group_mechanism']['ldap'] = True
        if ('mechanism_local_only' in kwargs.keys() and kwargs['mechanism_local_only']):
            del json_input['user']['radius']['user_group_mechanism']['radius_attribute']
            json_input['user']['radius']['user_group_mechanism']['local_only'] = True
                
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        user_radius_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return user_radius_resp

    def add_radius_server(self, msg=False, **kwargs):
        logger.info("\nAdd radius server\n")
        self.options = dict(RadiusApi.default_radius_server_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_radiusserver(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        radius_server_resp = self.fw.api_post(self.url2, msg, data=json_input)
        return radius_server_resp

    def edit_radius_server(self, msg=False, **kwargs):
        logger.info("\nEdit radius server\n")
        self.options = dict(RadiusApi.default_radius_server_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_radiusserver(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        radius_server_resp = self.fw.api_put(self.url2, msg, data=json_input)
        return radius_server_resp

    def edit_user_radius_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        output = self.fw.api_put(self.url1, msg, data=json_input)
        return output

    def build_json_radiusserver(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_radius_servers_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['radius']['server'] = []
        json_input1 = self.sub_dict(**kwargs)
        json_input['user']['radius']['server'].append(json_input1)

        return json_input
        
    def sub_dict(self, **kwargs):
        json_input = {}
        json_input['host'] = ''
        if ('host' in kwargs.keys() and kwargs['host']):
            json_input['host'] = kwargs['host']
        if 'enable' in kwargs.keys():
            json_input['enable'] = kwargs['enable']
        if ('port_num' in kwargs.keys() and kwargs['port_num']):
            json_input['port'] = {}
            json_input['port'] = kwargs['port_num']
        if ('secret' in kwargs.keys() and kwargs['secret']):
            json_input['shared_secret'] = {}
            json_input['shared_secret'] = kwargs['secret']
        if 'send_through_vpn_tunnel' in kwargs.keys():
            json_input['send_through_vpn_tunnel'] = kwargs['send_through_vpn_tunnel']
        if ('user_name_format' in kwargs.keys() and kwargs['user_name_format']):
            json_input['user_name_format'] = {}
            json_input['user_name_format'][kwargs['user_name_format']] = True
        return json_input

    def del_radius_server(self, radiusserver_name):
        url = str(self.url5) + '/' + "name" + '/' + radiusserver_name
        logger.info(url)
        output = self.fw.api_delete(url)
        return output


########### Radius_account functions are temporarily unavailable, dts#221377###############      
        
    def show_radius_account_reporting(self):
        output = self.fw.api_get(self.url3)
        return output

    def add_radius_account(self, msg=False, **kwargs):
        logger.info("\nAdd radius account\n")
        self.options = dict(RadiusApi.default_radius_account_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_radiusaccount(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        radius_account_resp = self.fw.api_post(self.url4, msg, data=json_input)
        return radius_account_resp

    def edit_radius_account(self, msg=False, **kwargs):
        logger.info("\nEdit radius account\n")
        self.options = dict(RadiusApi.default_radius_account_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_radiusaccount(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        radius_account_resp = self.fw.api_put(self.url4, msg, data=json_input)
        return radius_account_resp

    def build_json_radiusaccount(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_radius_accounts_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['radius']['accounting']['server'] = []   
        json_input1 = self.sub_dict1(**kwargs)
        json_input['user']['radius']['accounting']['server'].append(json_input1)
        
        return json_input

    def sub_dict1(self, **kwargs):
        json_input = {}
        json_input['host'] = ''
        if ('host' in kwargs.keys() and kwargs['host']):
            json_input['host'] = kwargs['host']
        if 'enable' in kwargs.keys():
            json_input['enable'] = kwargs['enable']
        if ('port' in kwargs.keys() and kwargs['port']):
            json_input['port'] = kwargs['port']
        if ('secret' in kwargs.keys() and kwargs['secret']):
            json_input['shared_secret'] = kwargs['secret']
        if ('user_name_format' in kwargs.keys() and kwargs['user_name_format']):
            json_input['user_name_format'] = {}
            json_input['user_name_format'][kwargs['user_name_format']] = True

        return json_input
    
    def edit_user_radius_accounting(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        output = self.fw.api_put(self.url9, msg, data=json_input)
        return output

    def get_user_radius_accounting(self, msg=False):
        output = self.fw.api_get(self.url9, msg)
        return output

    def show_radius_account_by_name(self, name):
        url = self.url4 + '/name/' + name
        output = self.fw.api_get(url)
        return output
        
    def del_radius_account(self, radiusaccount_name):
        url = str(self.url6) + '/' + "name" + '/' + radiusaccount_name
        logger.info(url)
        output = self.fw.api_delete(url)
        return output
    
    def test_radius_accounting_server(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url10, msg, data=json_input)
        return repu_resp


class LdapApi:
    '''LdapApi class'''

    default_ldap_setting_options = {
        'version': 3,
        'require_valid_certificate': True,
        'local_tls_certificate': {},
        'allow_referrals': True,
        'user_authentication': False,
        'auto_configuration': True,
        'domain_search': True,
        'other_search': True,
        'local_users_only': False,
        'group_name': '',
        'mirror_user_groups': {},
        'enableradiustoldaprelay': False,
        'trusted_zones': False,
        'wan_zone': True,
        'public_zones': False,
        'wireless_zones': False,
        'vpn_zone': True,
        'vpn': "",
        'vpn_client': {},
        'l2tp': {},
        'internet': {}
    }
    default_ldap_server_options = {}

    def __init__(self, fw):
        self.fw = fw
        self.url1 = 'api/sonicos/user/ldap/base'
        self.url2 = 'api/sonicos/user/ldap/servers'
        self.url3 = 'api/sonicos/reporting/ldap-statistic/global'
        # self.url4 = 'api/sonicos/reporting/ldap-statistic/server'    # error api url
        self.url4 = 'api/sonicos/reporting/ldap-statistic/servers'
        self.url5 = 'api/sonicos/user/ldap/server'
        self.url6 = 'api/sonicos/user/ldap/test/normal'
        self.url7 = 'api/sonicos/user/ldap/mirror-user-groups/refresh'
        self.url8 = 'api/sonicos/user/ldap/exclude-trees'
        self.url9 = 'api/sonicos/user/ldap/test/basic-search'
        self.url10 = 'api/sonicos/user/ldap/test/advanced-search'
        self.url11 = 'api/sonicos/user/ldap/server/auto-config-trees'
        self.url12 = 'api/sonicos/user/tacacs/base'
        self.url13 = 'api/sonicos/user/tacacs/servers'
        self.url14 = 'api/sonicos/user/tacacs/accounting/servers'


        self.initial_ldap_setting_json = {
            "user": {
                "ldap": {
                    "protocol_version": 3,
                    "require_valid_certificate": True,
                    "local_tls_certificate": "",
                    "allow_referrals": True,
                    "allow_references": {
                        "user_authentication": False,
                        "auto_configuration": True,
                        "domain_search": True,
                        "other_search": True
                    },
                    "local_users_only": False,
                    "default_user_group": "",
                    "mirror_user_groups": {
                        # "all": True,
                        # "refresh": {
                        #     "period": {
                        #         "minutes": 5
                        #     }
                        # }
                    },
                    "relay": {
                        "enable": False,
                        "clients_connect": {
                            "trusted_zones": False,
                            "wan_zone": True,
                            "public_zones": True,
                            "wireless_zones": True,
                            "vpn_zone": True
                        },
                        "shared_secret": "",
                        "legacy_user_group": {
                            "vpn": "",
                            "vpn_client": "",
                            "l2tp": "",
                            "internet": ""
                        }
                    }
                }
            }
        }
        self.initial_ldap_server_json = {
            "user": {
                "ldap": {
                    # "server": [
                    #     {
                    #         "host": "1.1.1.1",
                    #         "enable": True,
                    #         "role": {
                    #             "primary": True
                    #         },
                    #         "port": {
                    #             "port_num": 389
                    #         },
                    #         "timeout": {
                    #             "server": {
                    #                 "seconds": 10
                    #             },
                    #             "operation": {
                    #                 "minutes": 5
                    #             }
                    #         },
                    #         "use_tls": True,
                    #         "send_start_tls_request": False,
                    #         "schema": "microsoft-active-directory",
                    #         "user_class": "user",
                    #         "user_attribute": {
                    #             "logon_name": "sAMAccountName",
                    #             "qualified_logon_name": "userPrincipalName",
                    #             "group_membership": "memberOf",
                    #             "additional_group_id": "primaryGroupID",
                    #             "framed_ip_address": "msRADIUSFramedIPAddress"
                    #         },
                    #         "user_group_class": "group",
                    #         "user_group_attribute": {
                    #             "member": {
                    #                 "type": "distinguished-name",
                    #                 "name": "member"
                    #             },
                    #             "additional_group_match": "primaryGroupToken"
                    #         },
                    #         "directory": {
                    #             "primary_domain": "mydomain.com",
                    #             "users_tree": [
                    #                 {
                    #                     "name": "mydomain.com/Users"
                    #                 }
                    #             ],
                    #             "user_groups_tree": [
                    #                 {
                    #                     "name": "mydomain.com/Users"
                    #                 }
                    #             ]
                    #         },
                    #         "bind": {
                    #             "anonymous": True
                    #         },
                    #         "bind_password": "",
                    #         "referred_bind_with_account": "local"
                    #     },
                    #
                    # ]
                }
            }
        }

        self.initial_tacacs_server_json = {
            'user': {
                'tacacs': {
                    'server': [
                        {
                            # 'enable': True,
                            # 'host': '123.123.123.123',
                            # 'port': 49,
                            # 'shared_secret': 'very_secret',
                            # 'through_vpn': False
                        }
                    ]
                }
            }
        }

        self.initial_tacacs_account_json = {
            'user': {
                'tacacs': {
                    'accounting': {
                        'server': [
                            {
                                # 'enable': True,
                                # 'host': '123.123.123.123',
                                # 'port': 1813,
                                # 'shared_secret': 'very_secret',
                                # 'user_name_format': {'down_level_logon': True}
                            }
                        ]
                    }
                }
            }
        }


    def show_ldap_setting(self):
        output = self.fw.api_get(self.url1)
        return output

    def show_ldap_servers(self):
        output = self.fw.api_get(self.url2)
        return output

    def show_ldap_server_by_name(self, name):
        url = self.url2 + '/name/' + name
        output = self.fw.api_get(url)
        return output

    def show_ldap_reporting_statistic(self):
        output = self.fw.api_get(self.url3)
        return output

    def del_ldap_reporting_statistic(self, msg=False):
        ldap_reporting = self.fw.api_delete(self.url3, msg)
        return ldap_reporting

    def show_ldap_server_reporting_statistic(self, ldapserverip):
        url = str(self.url4) + '/' + ldapserverip
        output = self.fw.api_get(url)
        return output

    def del_ldap_server_reporting_statistic(self, ldapserverip):
        url = str(self.url4) + '/' + ldapserverip
        output = self.fw.api_delete(url)
        return output

    def ldap_setting(self, msg=False, **kwargs):
        self.options = dict(LdapApi.default_ldap_setting_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:

            json_input = copy.deepcopy(self.initial_ldap_setting_json)
            logger.info("\n\nInitial json file is:\n")
            pprint(json_input)
            if ('version' in kwargs.keys() and kwargs['version']):
                json_input['user']['ldap']['protocol_version'] = kwargs['version']
            if ('require_valid_certificate' in kwargs.keys() and kwargs['require_valid_certificate']):
                json_input['user']['ldap']['require_valid_certificate'] = kwargs['require_valid_certificate']
            if ('local_tls_certificate' in kwargs.keys() and kwargs['local_tls_certificate']):
                json_input['user']['ldap']['local_tls_certificate'] = kwargs['local_tls_certificate']

            if ('user_authentication' in kwargs.keys() and kwargs['user_authentication']):
                json_input['user']['ldap']['allow_references']['user_authentication'] = kwargs['user_authentication']
            if ('auto_configuration' in kwargs.keys() and kwargs['auto_configuration']):
                json_input['user']['ldap']['allow_references']['auto_configuration'] = kwargs['auto_configuration']

            if ('domain_search' in kwargs.keys() and kwargs['domain_search']):
                json_input['user']['ldap']['allow_references']['domain_search'] = kwargs['domain_search']
            if ('other_search' in kwargs.keys() and kwargs['other_search']):
                json_input['user']['ldap']['allow_references']['other_search'] = kwargs['other_search']

            if ('local_users_only' in kwargs.keys() and kwargs['local_users_only']):
                json_input['user']['ldap']['local_users_only'] = kwargs['local_users_only']
            if ('group_name' in kwargs.keys() and kwargs['group_name']):
                json_input['user']['ldap']['default_user_group'] = kwargs['group_name']

            if ('mirror_user_groups' in kwargs.keys() and kwargs['mirror_user_groups']):
                json_input['user']['ldap']['mirror_user_groups']['have_members'] = True
                json_input['user']['ldap']['mirror_user_groups']['all'] = True
                if ('refresh' in kwargs.keys() and kwargs['refresh']):
                    # if 'now' in kwargs['refresh']:
                    # json_input['user']['ldap']['mirror_user_groups']['refresh']['now'] = True
                    # elif ('period' in kwargs['refresh'] and 'minutes' in kwargs.keys() and kwargs['minutes']):
                    if ('period' in kwargs.keys()):
                        # json_input['user']['ldap']['mirror_user_groups']['refresh'] = {}
                        json_input['user']['ldap']['mirror_user_groups']['refresh']['period'] = kwargs['period']
                        # json_input['user']['ldap']['mirror_user_groups']['refresh']['period']['minutes'] = kwargs['minutes']
                    else:
                        logger.error('Please specify when to refresh mirror user groups')
            # if ('vpnGroupName' in kwargs.keys() and kwargs['vpnGroupName']):
            #      json_input['user']['ldap']['relay']['legacy_user_group']['vpn']['vpnGroupName'] = kwargs['vpnGroupName']
            if ('vpn' in kwargs.keys()):
                json_input['user']['ldap']['relay']['legacy_user_group']['vpn'] = kwargs['vpn']

            # if ('vpnClientGroupName' in kwargs.keys() and kwargs['vpnClientGroupName']):
            # json_input['user']['ldap']['relay']['legacy_user_group']['vpn_client']['vpnClientGroupName'] = kwargs[
            #  'vpnClientGroupName']
            if ('vpn_client' in kwargs.keys() and kwargs['vpn_client']):
                json_input['user']['ldap']['relay']['legacy_user_group']['vpn_client'] = kwargs['vpn_client']

            # if ('l2tpGroupName' in kwargs.keys() and kwargs['l2tpGroupName']):
            #   json_input['user']['ldap']['relay']['legacy_user_group']['l2tp']['l2tpGroupName'] = kwargs['l2tpGroupName']
            if ('l2tp' in kwargs.keys() and kwargs['l2tp']):
                json_input['user']['ldap']['relay']['legacy_user_group']['l2tp'] = kwargs['l2tp']

            # if ('internetAccessGroupName' in kwargs.keys() and kwargs['internetAccessGroupName']):

            # json_input['user']['ldap']['relay']['legacy_user_group']['internet']['internetAccessGroupName'] = kwargs[
            # 'internetAccessGroupName']
            if ('internet' in kwargs.keys() and kwargs['internet']):
                json_input['user']['ldap']['relay']['legacy_user_group']['internet'] = kwargs['internet']

            if ('public_zones' in kwargs.keys() and kwargs['public_zones']):
                json_input['user']['ldap']['relay']['clients_connect']['public_zones'] = kwargs['public_zones']
            if ('trusted_zones' in kwargs.keys() and kwargs['trusted_zones']):
                json_input['user']['ldap']['relay']['clients_connect']['trusted_zones'] = kwargs['trusted_zones']
            if ('vpn_zone' in kwargs.keys() and kwargs['vpn_zone']):
                json_input['user']['ldap']['relay']['clients_connect']['vpn_zone'] = kwargs['vpn_zone']
            if ('wan_zone' in kwargs.keys() and kwargs['wan_zone']):
                json_input['user']['ldap']['relay']['clients_connect']['wan_zone'] = kwargs['wan_zone']
            if ('wireless_zones' in kwargs.keys() and kwargs['wireless_zones']):
                json_input['user']['ldap']['relay']['clients_connect']['wireless_zones'] = kwargs['wireless_zones']
            if ('enable_relay' in kwargs.keys() and kwargs['enable_relay']):
                json_input['user']['ldap']['relay']['enable'] = kwargs['enable_relay']
            if ('shared_secret' in kwargs.keys() and kwargs['shared_secret']):
                json_input['user']['ldap']['relay']['shared_secret'] = kwargs['shared_secret']

        except KeyError:
            logger.info("Error: In creating JSON for Ldap settings")

        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        ldap_setting_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return ldap_setting_resp

    def config_ldap_setting(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return repu_resp
    
    def ldap_setting_new(self, msg=False, **kwargs):
        self.options = dict(LdapApi.default_ldap_setting_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:

            json_input = copy.deepcopy(self.initial_ldap_setting_json)
            logger.info("\n\nInitial json file is:\n")
            pprint(json_input)
            if ('version' in kwargs.keys() and kwargs['version']):
                json_input['user']['ldap']['protocol_version'] = kwargs['version']
            if 'require_valid_certificate' in kwargs.keys():
                json_input['user']['ldap']['require_valid_certificate'] = kwargs['require_valid_certificate']
            if ('local_tls_certificate' in kwargs.keys() and kwargs['local_tls_certificate']):
                json_input['user']['ldap']['local_tls_certificate'] = kwargs['local_tls_certificate']

            if ('user_authentication' in kwargs.keys() and kwargs['user_authentication']):
                json_input['user']['ldap']['allow_references']['user_authentication'] = kwargs['user_authentication']
            if ('auto_configuration' in kwargs.keys() and kwargs['auto_configuration']):
                json_input['user']['ldap']['allow_references']['auto_configuration'] = kwargs['auto_configuration']

            if ('domain_search' in kwargs.keys() and kwargs['domain_search']):
                json_input['user']['ldap']['allow_references']['domain_search'] = kwargs['domain_search']
            if ('other_search' in kwargs.keys() and kwargs['other_search']):
                json_input['user']['ldap']['allow_references']['other_search'] = kwargs['other_search']

            if ('local_users_only' in kwargs.keys() and kwargs['local_users_only']):
                json_input['user']['ldap']['local_users_only'] = kwargs['local_users_only']
            if ('group_name' in kwargs.keys() and kwargs['group_name']):
                json_input['user']['ldap']['default_user_group'] = kwargs['group_name']

            if ('mirror_user_groups' in kwargs.keys() and kwargs['mirror_user_groups']):
                json_input['user']['ldap']['mirror_user_groups']['have_members'] = True
                json_input['user']['ldap']['mirror_user_groups']['all'] = True
                if ('refresh' in kwargs.keys() and kwargs['refresh']):
                    if ('period' in kwargs.keys()):
                        json_input['user']['ldap']['mirror_user_groups']['refresh']['period'] = kwargs['period']
                    else:
                        logger.error('Please specify when to refresh mirror user groups')
            if ('vpn_client' in kwargs.keys() and kwargs['vpn_client']):
                json_input['user']['ldap']['relay']['legacy_user_group']['vpn_client'] = kwargs['vpn_client']
            if ('l2tp' in kwargs.keys() and kwargs['l2tp']):
                json_input['user']['ldap']['relay']['legacy_user_group']['l2tp'] = kwargs['l2tp']
            if ('internet' in kwargs.keys() and kwargs['internet']):
                json_input['user']['ldap']['relay']['legacy_user_group']['internet'] = kwargs['internet']

            if ('public_zones' in kwargs.keys() and kwargs['public_zones']):
                json_input['user']['ldap']['relay']['clients_connect']['public_zones'] = kwargs['public_zones']
            if ('trusted_zones' in kwargs.keys() and kwargs['trusted_zones']):
                json_input['user']['ldap']['relay']['clients_connect']['trusted_zones'] = kwargs['trusted_zones']
            if ('vpn_zone' in kwargs.keys() and kwargs['vpn_zone']):
                json_input['user']['ldap']['relay']['clients_connect']['vpn_zone'] = kwargs['vpn_zone']
            if ('wan_zone' in kwargs.keys() and kwargs['wan_zone']):
                json_input['user']['ldap']['relay']['clients_connect']['wan_zone'] = kwargs['wan_zone']
            if ('wireless_zones' in kwargs.keys() and kwargs['wireless_zones']):
                json_input['user']['ldap']['relay']['clients_connect']['wireless_zones'] = kwargs['wireless_zones']
            if ('enable_relay' in kwargs.keys() and kwargs['enable_relay']):
                json_input['user']['ldap']['relay']['enable'] = kwargs['enable_relay']
            if ('shared_secret' in kwargs.keys() and kwargs['shared_secret']):
                json_input['user']['ldap']['relay']['shared_secret'] = kwargs['shared_secret']

        except KeyError:
            logger.info("Error: In creating JSON for Ldap settings")

        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        ldap_setting_resp = self.fw.api_put(self.url1, msg, data=json_input)
        return ldap_setting_resp
        
    def exclude_sub_trees(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url8, msg, data=json_input)
        return repu_resp 
    
    def delete_exclude_sub_trees(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_delete(self.url8, msg, data=json_input)
        return repu_resp 

    def add_ldap_server(self, msg=False, **kwargs):
        self.options = dict(LdapApi.default_ldap_server_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_ldapserver(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        ldap_server_resp = self.fw.api_post(self.url2, msg, data=json_input)
        return ldap_server_resp
        
    def add_ldap_server_new(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url2, msg, data=json_input)
        return repu_resp

    def edit_ldap_server(self, msg=False, **kwargs):
        self.options = dict(LdapApi.default_ldap_server_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_ldapserver(**kwargs)
        logger.info("\n\nUpdate Json is :\n")
        logger.info(json_input)
        url = str(self.url2) + '/name/' + kwargs['host']  # modified url and ldap_server_resp in edit_ldap_sever
        ldap_server_resp = self.fw.api_put(url, msg, data=json_input)
        return ldap_server_resp
        
    def test_ldap_server(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url6, msg, data=json_input)
        return repu_resp

    def test_ldap_server_basic_search(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url9, msg, data=json_input)
        return resp

    def test_ldap_server_advance_search(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url10, msg, data=json_input)
        return resp

    def auto_configure_trees(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.url11, msg, data=json_input)
        return resp
    
    def refresh_from_ldap(self, msg=False):
        resp = self.fw.api_post(self.url7, msg)
        return resp

    def build_json_ldapserver(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_ldap_server_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['ldap']['server'] = []
        json_input1 = self.sub_dict_server1(**kwargs)
        json_input['user']['ldap']['server'].append(json_input1)
        return json_input

    def sub_dict_server1(self, **kwargs):
        json_input = {}
        if ('role' in kwargs.keys() and kwargs['role']):
            json_input['role'] = {}
            if kwargs['role'] == 'primary':
                json_input['role']['primary'] = True
            elif kwargs['role'] == 'secondary':
                json_input['role']['secondary'] = True
            # elif kwargs['role1'] == 'backup':
                # json_input['role']['backup'] = True
            json_role = self.different_role(**kwargs)
            json_input.update(json_role)

        return json_input

    def different_role(self, **kwargs):
        json_input = {}
        if ('host' in kwargs.keys() and kwargs['host']):
            json_input['host'] = kwargs['host']
        if ('timeout' in kwargs.keys() and kwargs['timeout'] == True):
            json_input['timeout'] = {}
            if ('servertimeout' in kwargs.keys() and kwargs['servertimeout']):
                json_input['timeout']['server'] = {}
                json_input['timeout']['server'] = kwargs['servertimeout']
            if ('overalloperationtimeout' in kwargs.keys() and kwargs['overalloperationtimeout']):
                json_input['timeout']['operation'] = {}
                json_input['timeout']['operation'] = kwargs['overalloperationtimeout']
        if 'enable' in kwargs.keys():
            if (isinstance(kwargs['enable'], bool) and kwargs['enable'] is True):
                json_input['enable'] = True
            else:
                json_input['enable'] = False
        if ('port_num' in kwargs.keys() and kwargs['port_num']):
            json_input['port'] = {}
            json_input['port'] = kwargs['port_num']
        if ('partition' in kwargs.keys() and kwargs['partition']):
            json_input['partition'] = {}
            json_input['partition'] = kwargs['partition']
        if 'use_tls' in kwargs.keys():
            if (isinstance(kwargs['use_tls'], bool) and kwargs['use_tls']):
                json_input['use_tls'] = True
                if 'send_start_tls_request' in kwargs.keys():
                    if (isinstance(kwargs['send_start_tls_request'], bool) and kwargs[
                        'send_start_tls_request']):
                        json_input['send_start_tls_request'] = True
                    else:
                        json_input['send_start_tls_request'] = False
            else:
                json_input['use_tls'] = False
        if ('bind' in kwargs.keys() and kwargs['bind']):
            if kwargs['bind'] == 'anonymous':
                json_input['bind'] = {}
                json_input['bind']['anonymous'] = True
                json_input['referred_bind_with_account'] = kwargs['referred_bind_with_account']
            if kwargs['bind'] == 'acct':
                json_input['bind'] = {}
                json_input['bind']['acct'] = {}
                if ('anonymousname' in kwargs.keys() and kwargs['anonymousname']):
                    json_input['bind']['acct']['name'] = kwargs['anonymousname']
                if ('location' in kwargs.keys() and kwargs['location']):
                    json_input['bind']['acct']['location'] = kwargs['location']
                if ('bind_password' in kwargs.keys() and kwargs['bind_password']):
                    json_input['bind_password'] = kwargs['bind_password']
                else:
                    pass
                json_input['referred_bind_with_account'] = kwargs['referred_bind_with_account']
            if kwargs['bind'] == 'distinguished_name':
                json_input['bind'] = {}
                if ('distinguished_name' in kwargs.keys() and kwargs['distinguished_name']):
                    json_input['bind']['distinguished_name'] = kwargs['distinguished_name']
                if ('bind_password' in kwargs.keys() and kwargs['bind_password']):
                    json_input['bind_password'] = kwargs['bind_password']
                json_input['referred_bind_with_account'] = kwargs['referred_bind_with_account']
        if ('directory' in kwargs.keys() and kwargs['directory'] == True):
            json_input['directory'] = {}
            if ('primary_domain' in kwargs.keys() and kwargs['primary_domain']):
                json_input['directory']['primary_domain'] = kwargs['primary_domain']
            if 'users_tree' in kwargs.keys():
                json_input['directory']['users_tree'] = []
                for key in kwargs['users_tree']:
                    json_input['directory']['users_tree'].append({'name': key})
            if 'user_groups_tree' in kwargs.keys():
                json_input['directory']['user_groups_tree'] = []
                for key in kwargs['user_groups_tree']:
                    json_input['directory']['user_groups_tree'].append({'name': key})
        if ('schema' in kwargs.keys() and kwargs['schema']):
            if kwargs['schema'] == 'microsoft-active-directory':
                json_input['schema'] = 'microsoft-active-directory'
                if ('qualified_logon_name' in kwargs.keys() and kwargs['qualified_logon_name']):
                    json_input['user_attribute'] = {}
                    json_input['user_attribute']['qualified_logon_name'] = kwargs['qualified_logon_name']
                else:
                    pass
            elif kwargs['schema'] == 'inet-org-person':
                json_input['schema'] = 'inet-org-person'
                json_input['user_attribute'] = {}
                if ('additional_group_id' in kwargs.keys() and kwargs['additional_group_id']):
                    json_input['user_attribute']['additional_group_id'] = kwargs['additional_group_id']
                if ('framed_ip_address' in kwargs.keys() and kwargs['framed_ip_address']):
                    json_input['user_attribute']['framed_ip_address'] = kwargs['framed_ip_address']
                if ('additional_group_match' in kwargs.keys() and kwargs['additional_group_match']):
                    json_input['user_group_attribute'] = {}
                    json_input['user_group_attribute']['additional_group_match'] = kwargs['additional_group_match']
            elif kwargs['schema'] == 'network-information-service':
                json_input['schema'] = 'network-information-service'
                json_input['user_attribute'] = {}
                if ('additional_group_id' in kwargs.keys() and kwargs['additional_group_id']):
                    json_input['user_attribute']['additional_group_id'] = kwargs['additional_group_id']
                if ('framed_ip_address' in kwargs.keys() and kwargs['framed_ip_address']):
                    json_input['user_attribute']['framed_ip_address'] = kwargs['framed_ip_address']
                if ('qualified_logon_name' in kwargs.keys() and kwargs['framed_ip_address']):
                    json_input['user_attribute']['qualified_logon_name'] = kwargs['qualified_logon_name']
            elif kwargs['schema'] == 'samba-smb':
                json_input['schema'] = 'samba-smb'
                json_input['user_attribute'] = {}
                json_input['user_class'] = 'sambaSAMAccount'
                json_input['user_attribute']['logon_name'] = 'uid'
                json_input['user_attribute']['additional_group_id'] = 'sambaPrimaryGroupSID'
                if ('qualified_logon_name' in kwargs.keys() and kwargs['framed_ip_address']):
                    json_input['user_attribute']['qualified_logon_name'] = kwargs['qualified_logon_name']
                if ('framed_ip_address' in kwargs.keys() and kwargs['framed_ip_address']):
                    json_input['user_attribute']['framed_ip_address'] = kwargs['framed_ip_address']
            elif kwargs['schema'] == 'custom':
                json_input['schema'] = 'custom'
                json_input['user_attribute'] = {}
                json_input['user_group_attribute'] = {}
                json_input['user_group_attribute']['member'] = {}
                if ('user_class' in kwargs.keys() and kwargs['user_class']):
                    json_input['user_class'] = kwargs['user_class']
                if ('user_group_class' in kwargs.keys() and kwargs['user_group_class']):
                    json_input['user_group_class'] = kwargs['user_group_class']
                if ('additional_group_id' in kwargs.keys() and kwargs['additional_group_id']):
                    json_input['user_attribute']['additional_group_id'] = kwargs['additional_group_id']
                if ('framed_ip_address' in kwargs.keys() and kwargs['framed_ip_address']):
                    json_input['user_attribute']['framed_ip_address'] = kwargs['framed_ip_address']
                if ('qualified_logon_name' in kwargs.keys() and kwargs['framed_ip_address']):
                    json_input['user_attribute']['qualified_logon_name'] = kwargs['qualified_logon_name']
                if ('logon_name' in kwargs.keys() and kwargs['logon_name']):
                    json_input['user_attribute']['logon_name'] = kwargs['logon_name']
                if ('group_membership' in kwargs.keys() and kwargs['group_membership']):
                    json_input['user_attribute']['group_membership'] = kwargs['group_membership']
                if ('membertype' in kwargs.keys() and kwargs['membertype']):
                    json_input['user_group_attribute']['member']['type'] = kwargs['membertype']
                if ('membername' in kwargs.keys() and kwargs['membername']):
                    json_input['user_group_attribute']['member']['name'] = kwargs['membername']
                if ('additional_group_match' in kwargs.keys() and kwargs['additional_group_match']):
                    json_input['user_group_attribute']['additional_group_match'] = kwargs['additional_group_match']
            # One DTS on schema NovelleDirectory, DTS#221580
            # elif kwargs['schema'] == 'NovelleDirectory':
                # json_input['schema'] = 'NovelleDirectory'
            else:
                pass

        return json_input

    def del_ldap_server(self, name):
        url = self.url2 + '/name/' + name
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def show_tacacs_base_settings(self):
        output = self.fw.api_get(self.url12)
        return output

    def show_tacacs_servers(self):
        output = self.fw.api_get(self.url13)
        return output

    def show_tacacs_accounts(self):
        output = self.fw.api_get(self.url14)
        return output

    def add_tacacs_server(self, msg=False, **kwargs):
        json_input = self.build_json_tacacs_server(**kwargs)
        logger.info(f"Payload for adding tacacs server = {json_input}")
        resp = self.fw.api_post(self.url13, msg, data=json_input)
        return resp

    def add_tacacs_account(self, msg=False, **kwargs):
        json_input = self.build_json_tacacs_account(**kwargs)
        logger.info(f"Payload for adding tacacs accounting server = {json_input}")
        resp = self.fw.api_post(self.url14, msg, data=json_input)
        return resp

    def build_json_tacacs_server(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_tacacs_server_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['tacacs']['server'] = []
        json_input['user']['tacacs']['server'].append(kwargs)
        return json_input

    def build_json_tacacs_account(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_tacacs_account_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['tacacs']['accounting']['server'] = []
        json_input['user']['tacacs']['accounting']['server'].append(kwargs)
        return json_input


class AuthPartitionsApi:
    '''AuthPartitionsApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/user/partitioning/partitions'
        self.url_policies = 'api/sonicos/user/partitioning/policies'
        self.raw_url = 'api/sonicos/raw'
        self.headers = OrderedDict([('Accept', 'application/json'),
                                    ('Content-Type', 'application/json'),
                                    ('Accept-Encoding', 'application/json'),
                                    ('X-SNWL-API-Scope', 'extended'),
                                    ('charset', 'UTF-8')])

        self.initial_json = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [
                            ]
                        }
                    ]
                }
            }
        }

    def enable_disable_auth_partition(self, enable):
        if enable:
            data = {
                "stream": "csrfToken=0E59231D864BEFC9B8675B2DA0082446&cgiaction=none&refresh_page: authPartitionsView.html?changePosted=yes&auditPath=Users+%2F+Partitions&authPartitionsEnable=1"}
        else:
            data = {
                "stream": "csrfToken=0E59231D864BEFC9B8675B2DA0082446&cgiaction=none&refresh_page: authPartitionsView.html?changePosted=yes&auditPath=Users+%2F+Partitions&authPartitionsEnable=0"}
        repu_resp = self.fw.api_post(self.raw_url, data=data, headers=self.headers)
        return repu_resp

    def add_auth_partition(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url, msg, data=json_input)
        return repu_resp

    def show_auth_partitions(self):
        output = self.fw.api_get(self.url)
        return output

    def edit_auth_partition(self, msg=False, name=None, **kwargs):
        if not name:
            logger.info('Please specify agent name')
            return False
        url = self.url + '/name/' + name
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(url, msg, data=json_input)
        return repu_resp

    def del_auth_partition(self, name):
        url = self.url + '/name/' + name
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def add_auth_partition_policies(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url_policies, msg, data=json_input)
        return repu_resp

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
        self.edit_sso_name = 'api/sonicos/user/sso/agents/name/'
        self.sso_base = 'api/sonicos/user/sso/base'
        self.url2 = 'api/sonicos/user/sso/agents'
        self.url3 = 'api/sonicos/user/sso/terminal-services-agents'
        self.edit_tsa_name = 'api/sonicos/user/sso/terminal-services-agents/name/'
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
        self.edit_rac = 'api/sonicos/user/sso/radius-accounting-clients/name/'
        self.url14 = 'api/sonicos/user/sso/third-party-api/clients'
        self.url15 = 'api/sonicos/user/sso/third-party-api/clients/name'

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
        
        self.initial_sso_third_party_json = {
            "user": {
                "sso": {
                "third_party_api": {
                    "client": [
                    {
                        "host": "None",
                        "enable": True,
                        "authentication_type": "shared-secret",
                        "shared_secret": "None",
                        "security_level": {
                        "high": "allow-all"
                        },
                        "replay_prevention": False,
                        "origin_restriction": {},
                        "persistent_connections": False
                    }
                    ]
                }
                }
            }
          }
        
    def show_sso_settings(self):
        output = self.fw.api_get(self.url1)
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
        
    def del_sso_agent(self,msg=False, name=None):
        if not name:
            logger.info('Please specify agent name')
            return False
        url_del = self.edit_sso_name + name
        output = self.fw.api_delete(url_del)
        return output
        
    def edit_sso_agent(self,msg=False, name=None, **kwargs):
        if not name:
            logger.info('Please specify agent name')
            return False
        url_edit = self.edit_sso_name + name
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(url_edit, msg, data=json_input)
        return repu_resp

    def edit_sso_agent_name_port(self,msg=False, name=None, port=None, **kwargs):
        if not name:
            logger.info('Please specify agent name')
            return False
        if not port:
            logger.info('Please specify agent port number')
            return False
        url_edit = self.edit_sso_name + name + '/port/' + port
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(url_edit, msg, data=json_input)
        return repu_resp
        
    def show_sso_accounting_client(self):
        output = self.fw.api_get(self.url4)
        return output
        
    def edit_sso_accounting(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(self.url4, msg, data=json_input)
        return repu_resp
        
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
    
    def add_enforce_on_zone_json(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url9, msg, data=json_input)
        return repu_resp

    def del_enforce_on_zone(self, delete_zone):
        url = str(self.url9) + '/' + delete_zone
        logger.info(url)
        output = self.fw.api_delete(url)
        return output
        
    def config_sso_base_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(self.sso_base, msg, data=json_input)
        return repu_resp

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
            json_input['shared_key'] = {}
            json_input['shared_key']['number'] = kwargs['number']
        if ('timeout' in kwargs.keys() and kwargs['timeout']):
            json_input['timeout'] = kwargs['timeout']
        if ('retries' in kwargs.keys() and kwargs['retries']):
            json_input['retries'] = kwargs['retries']
        if ('max_requests' in kwargs.keys() and kwargs['max_requests']):
            json_input['max_requests'] = kwargs['max_requests']
        if ('shared_key' in kwargs.keys() and kwargs['shared_key']):
            json_input['shared_key'] = kwargs['shared_key']

        return json_input

    # def del_sso_agent(self, del_sso_agent):
    #     url = str(self.url11) + '/' + del_sso_agent
    #     logger.info(url)
    #     output = self.fw.api_delete(url)
    #     return output

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

    def edit_terminal_services_agent(self, msg=False, name=None, **kwargs):
        if not name:
            logger.info('Please specify terminal service agent name')
            return False
        url_name = self.edit_tsa_name + name
        json_input = copy.deepcopy(kwargs)
        response = self.fw.api_put(url_name, msg, data=json_input)
        return response

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
        if ('shared_key' in kwargs.keys() and kwargs['shared_key']):
            json_input['shared_key'] = kwargs['shared_key']
        return json_input
        
    def edit_terminal_services_agent_by_host(self, msg=False, host=None,port=None,**kwargs ):
        if not host:
            logger.info('Pls specify the agent host.')
            return False
        url = self.url3 + '/name/' + host + '/port/' +  port
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(url, msg, data=json_input)
        return repu_resp   
    
    def edit_terminal_services_agent_json(self, msg=False,**kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(self.url3, msg, data=json_input)
        return repu_resp

    def get_terminal_services_agent(self, msg=False):
        repu_resp = self.fw.api_get(self.url3)
        return repu_resp  

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

    def edit_radius_accounting_client(self, msg=False, name=None, **kwargs):
        if not name:
            logger.info('Please specify radius accounting client name')
            return False
        url_name = self.edit_rac + name
        json_input = copy.deepcopy(kwargs)
        response = self.fw.api_put(url_name, msg, data=json_input)
        return response

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

    def del_sso_radius_accounting_client(self, name):
        if not name:
            logger.info('Pls specify the accounting name.')
            return False
        url = self.url4 + '/name/' + name 
        logger.info(url)
        output = self.fw.api_delete(url)
        return output   

    def add_sso_radius_accounting_client(self, msg=False,**kwargs ):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url4, msg, data=json_input)
        return repu_resp
        
    def edit_sso_radius_accounting_client(self, msg=False, name=None,**kwargs ):
        if not name:
            logger.info('Pls specify the accounting name.')
            return False
        url = self.url4 + '/name/' + name 
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(url, msg, data=json_input)
        return repu_resp
    
    def build_sso_third_party_api_settings(self, **kwargs):
       
        json_input = copy.deepcopy(self.initial_sso_third_party_json)
        logger.info("\n\nInitial json file is:\n")
        pprint(json_input)
        try:
            
            json_input['user']['sso']['third_party_api']['client'][0]['host'] = kwargs['host']
            json_input['user']['sso']['third_party_api']['client'][0]['enable'] = kwargs['enable']
            json_input['user']['sso']['third_party_api']['client'][0]['authentication_type'] = kwargs['authentication_type']
            json_input['user']['sso']['third_party_api']['client'][0]['shared_secret'] = kwargs['shared_secret']
            json_input['user']['sso']['third_party_api']['client'][0]['security_level'] = kwargs['security_level']
            json_input['user']['sso']['third_party_api']['client'][0]['replay_prevention'] = kwargs['replay_prevention']
            json_input['user']['sso']['third_party_api']['client'][0]['origin_restriction'] = kwargs['origin_restriction']
            json_input['user']['sso']['third_party_api']['client'][0]['persistent_connections'] = kwargs['persistent_connections']
            
        except KeyError:
            logger.error('Error: In creating JSON for app rule object')
        return json_input    
    
    def create_sso_third_party_client(self,msg=False, **kwargs):
        json_input = self.build_sso_third_party_api_settings(**kwargs)
        add_client = self.fw.api_post(self.url14, msg, data=json_input)
        return add_client
    
    def edit_sso_third_party_client(self,msg=False, **kwargs):
        json_input = self.build_sso_third_party_api_settings(**kwargs)
        edit_client = self.fw.api_put(self.url14, msg, data=json_input)
        return edit_client
    
    def delete_sso_third_party_client(self,name):
        url = self.url15 + '/' + name
        delete_client = self.fw.api_delete(url)
        return delete_client
    
    def get_sso_third_party_client(self):
        get_client = self.fw.api_get(self.url14)
        return get_client
    
    
class SAMLApi:
    '''SAML APi class, author by cyuan'''

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/user/saml'
        self.init_identity_provider_json = {
            'user': {
                'saml': {
                    "identity_provider": [{
                        "authentication_url": "",
                        "group_name_attribute": "",
                        "logout_url": "",
                        "name": "",
                        "server_id": "",
                        "trusted_certificate": "",
                        "user_name_attribute": ""
                    }]
                }
            }
        }
        self.init_service_provider_json = {
            "user": {
                "saml": {
                    "service_provider": [{
                        "name": "",
                        "type": "",
                        # "address_object": "",
                        # "domain_name": "",
                        "service": {}
                    }]
                }
            }
        }
        self.init_profile_json = {
            "user": {
                "saml": {
                    "profile": [{
                        "name": "",
                        "identity_provider": "",
                        "service_provider": "",
                        "single_sign_off": False,
                        "sslvpn": False,
                        "use_certificate_sign_sp_request": False,
                        "management": False
                    }]
                }
            }
        }

    def add_saml_identify_provider(self, msg=False, **kwargs):
        '''
        :param kwargs:
        idp = {
            "authentication_url": "test.com",
            "group_name_attribute": "sonicauto",
            "logout_url": "test.com",
            'name': "idp",
            'server_id': "11",
            'trusted_certificate': "OneLogin Account  (0482EEBEB71556A11F5D8252B9F5F754A21AF08F)",
            'user_name_attribute': "sonicauto"
        }
        '''
        url = self.base_url + '/identity-providers'
        input_json = copy.deepcopy(self.init_identity_provider_json)
        try:
            input_json['user']['saml']["identity_provider"][0].update(kwargs)
            return self.fw.api_post(url, msg, data=input_json)
        except Exception as e:
            logger.error('error in creating input saml identify proivder json\n', repr(e))
            return False

    def add_saml_service_provider(self, msg=False, **kwargs):
        '''
        :param kwargs:
        svc_provider = {
            'address_object': "X1 IP",
            'name': "sp_tc25",
            'service': {'https': True},
            'type': "ip"
        }
        '''
        url = self.base_url + '/service-providers'
        input_json = copy.deepcopy(self.init_service_provider_json)
        try:
            input_json['user']['saml']['service_provider'][0].update(kwargs)
            return self.fw.api_post(url, msg, data=input_json)
        except Exception as e:
            logger.error('error in creating saml service provider json: \n', repr(e))
            return False

    def add_saml_profile(self, msg=False, **kwargs):
        '''
        :param kwargs:
        profile = {
            'name': 'profile',
            "identity_provider": 'idp',
            "service_provider": 'sp',
        }
        '''
        url = self.base_url + '/profiles'
        input_json = copy.deepcopy(self.init_profile_json)
        try:
            input_json['user']['saml']['profile'][0].update(kwargs)
            return self.fw.api_post(url, msg, data=input_json)
        except Exception as e:
            logger.error('error in creating saml service provider json: \n', repr(e))
            return False

    def get_saml_identity_providers(self):
        url = self.base_url + '/identity-providers'
        return self.fw.api_get(url)

    def get_saml_service_providers(self):
        url = self.base_url + '/service-providers'
        return self.fw.api_get(url)

    def get_saml_profiles(self):
        url = self.base_url + '/profiles'
        return self.fw.api_get(url)

    def edit_saml_identify_provider_by_name(self, idp_name, msg=False, **kwargs):
        '''
        :param kwargs:
        idp_edit = {
            'name': 'idp_tc24_edit'
        }
        '''
        url = self.base_url + '/identity-providers/name/' + idp_name
        input_json = copy.deepcopy(self.init_identity_provider_json)
        resp = self.get_saml_identity_providers()
        try:
            for idp in resp["user"]['saml']['identity_provider']:
                if idp.get("name") == idp_name:
                    input_json['user']['saml']["identity_provider"][0].update(idp)
                    input_json['user']['saml']["identity_provider"][0].update(kwargs)
                    return self.fw.api_put(url, msg, data=input_json)
            else:
                logger.error(f'not find the <{idp_name}> idp!!!')
        except Exception as e:
            logger.error(repr(e))
        return False

    def edit_saml_service_provider_by_name(self, svc_name, msg=False, **kwargs):
        '''
        :param kwargs:
        sp = {
            'name': 'sp_tc37_edit',
        }
        '''
        url = self.base_url + '/service-providers/name/' + svc_name
        input_json = copy.deepcopy(self.init_service_provider_json)
        resp = self.get_saml_service_providers()
        try:
            for service in resp["user"]['saml']["service_provider"]:
                if service.get("name") == svc_name:
                    input_json["user"]['saml']["service_provider"][0].update(service)
                    input_json["user"]['saml']["service_provider"][0].update(**kwargs)
                    return self.fw.api_put(url, msg, data=input_json)
            else:
                logger.error(f'not find the <{svc_name}> service provider!!')
        except Exception as e:
            logger.error(repr(e))
        return False

    def edit_saml_profile_by_name(self, profile_name='', msg=False, **kwargs):
        '''
        :param kwargs:
        profile = {
            'name': 'profile_tc42_edit'
        }
        '''
        url = self.base_url + '/profiles/name/' + profile_name
        input_json = copy.deepcopy(self.init_profile_json)
        resp = self.get_saml_profiles()
        try:
            for profile in resp["user"]['saml']["profile"]:
                if profile.get("name") == profile_name:
                    input_json["user"]['saml']["profile"][0].update(profile)
                    input_json["user"]['saml']["profile"][0].update(kwargs)
                    return self.fw.api_put(url, msg, data=input_json)
            else:
                logger.error(f'not find the <{profile_name}> saml profile!!')
        except Exception as e:
            logger.error(repr(e))
        return False

    def delete_saml_profile_by_name(self, profile_name, msg=False):
        url = self.base_url + '/profiles/name/' + profile_name
        return self.fw.api_delete(url, msg)

    def delete_saml_service_provider_by_name(self, name, msg=False):
        url = self.base_url + '/service-providers/name/' + name
        return self.fw.api_delete(url, msg)

    def delete_saml_identity_provider_by_name(self, name, msg=False):
        url = self.base_url + '/identity-providers/name/' + name
        return self.fw.api_delete(url, msg)

    def delete_all_saml_identity_providers(self, msg=False):
        url = self.base_url + '/identity-providers'
        idp_json = {"user": {'saml': {"identity_provider": []}}}
        resp = self.get_saml_identity_providers()
        if not resp:
            logger.info('no identity provider profile!!!')
            return True
        try:
            for idp in resp["user"]['saml']["identity_provider"]:
                idp_json["user"]['saml']["identity_provider"].append({"name": idp.get("name")})
            return self.fw.api_delete(url, msg, data=idp_json)
        except Exception as e:
            logger.error(repr(e))
            return False

    def delete_all_saml_service_provider(self, msg=False):
        url = self.base_url + '/service-providers'
        service_json = {"user": {'saml': {"service_provider": []}}}
        resp = self.get_saml_service_providers()
        if not resp:
            logger.info('no service provider profile!!!')
            return True
        try:
            if resp['user']['saml'] is {}:
                logger.info('==========>no service providers, no need to delete')
                return False
            for service in resp["user"]['saml']["service_provider"]:
                service_json["user"]['saml']["service_provider"].append({"name": service.get("name")})
            return self.fw.api_delete(url, msg, data=service_json)
        except Exception as e:
            logger.error(repr(e))
            return False

    def delete_all_saml_profiles(self, msg=False):
        url = self.base_url + '/profiles'
        profile_json = {"user": {'saml': {"profile": []}}}
        resp = self.get_saml_profiles()
        try:
            if resp["user"]['saml'] is {}:
                logger.info('no saml profile!!')
                return True
            for profile in resp["user"]['saml']["profile"]:
                profile_json["user"]['saml']["profile"].append({"name": profile.get("name")})
            return self.fw.api_delete(url, msg, data=profile_json)
        except Exception as e:
            logger.error(repr(e))
            return False

    def export_saml_profile_by_name(self, name, export_path='/tmp/saml_profile.xml'):
        '''
        :param name: exported saml profile name
        :param export_path: exported saml profile xml file path
        '''
        url = 'api/sonicos/export/saml/profile/' + name
        resp = self.fw.api_get(url)
        with open(export_path, 'w') as f:
            f.write(resp)
        logger.info(f'export saml profile <{name}> success, the download path is {export_path}')
        return os.path.exists(export_path)
    

class UserLocalApi:
    '''UserLocalApi class'''

    default_sso_setting_options = {
        'apply_password_constraints': True,
        'prune_on_expiry': True
    }

    default_local_user_options = {}

    default_local_group_options = {}

    def __init__(self, fw):
        self.fw = fw

        self.url1 = 'api/sonicos/user/local/user'
        self.url2 = 'api/sonicos/user/local/users'
        self.url3 = 'api/sonicos/user/local/group'
        self.url4 = 'api/sonicos/user/local/groups'
        self.url5 = 'api/sonicos/user/local/base'
        self.url_member_of = 'api/sonicos/user/local/users/name/'
        self.url_uuid = 'api/sonicos/user/local/users/uuid/'
        self.logout_url = 'api/sonicos/user/logout/users'
        self.local_base = 'api/sonicos/user/local/base'
        self.url_unbind = 'api/sonicos/user/local/unbind-totp-key'

        self.initial_local_settings_json = {
            "user": {
                "local": {
                    "apply_password_constraints": True,
                    "prune_on_expiry": True
                }
            }
        }

        self.initial_local_user_json = {
            "user": {
                "local": {
                     # "user": [
                     #     {
                     #         "name": "test123",
                     #         "comment": {
                     #             "comment_string": "mycomment"
                     #         },
                     #         "password": {
                     #             "pwd": ""
                     #         },
                     #         "force_password_change": False,
                     #         "one_time_password": {
                     #             "otp": True
                     #         },
                     #         "email_address": {
                     #             "email": "admin@test.local"
                     #         },
                     #         "vpn_client_access": {
                     #             "group": "LAN Subnets"
                     #         },
                     #         "quota_cycle": {
                     #             "day": True
                     #         },
                     #         "session_lifetime": {
                     #             "lifetime": 30,
                     #             "minutes": True
                     #         },
                     #         "limit": {
                     #             "receive": {
                     #                 "valInMB": 20
                     #             },
                     #             "transmit": {
                     #                  "valInMB": 20
                     #             }
                     #         },
                     #         "member_of": [
                     #             {
                     #
                     #                 "name": "SonicWALL Administrators"
                     #             }
                     #
                     #         ]
                     #     }
                     # ]
                }
            }
        }

        self.initial_user_member_of_json = {
            "user": {
                "local": {
                    # "user": [
                        # {
                            # "name": "",
                            # "password": {
                                # "pwd": ""
                            # },
                            # "member_of": [
                            #     {
                            #
                            #         "name": "SonicWALL Administrators"
                            #     },
                            #     {
                            #
                            #         "name": "Guest Services"
                            #     }
                            # ]
                        # }
                    # ]
                }
            }
        }

        self.initial_user_vpn_client_access_json = {
            "user": {
                "local": {
                    # "user": [
                        # {
                            # "name": "",
                            # "password": {
                                # "pwd": ""
                            # },
                            # "vpn_client_access": [
                                # {
                                #     "group": "Guest Authentication Server 2"
                                # },
                                # {
                                #     "group": "All Rogue Devices"
                                # },
                                # {
                                #     "group": "All Rogue Access Points"
                                # },
                                # {
                                #     "group": "DMZ Interface IPv6 Addresses"
                                # },
                                # {
                                #     "group": "LAN Interface IPv6 Addresses"
                                # },
                                # {
                                #     "group": "LAN Interface IP"
                                # }
                            # ]
                        # }
                    # ]
                }
            }
        }

        self.initial_user_bookmark_json = {
            "user": {
                "local": {
                    # "user": [
                        # {
                            # "name": "",
                            # "password": {
                                # "pwd": ""
                            # },
                            # "bookmark": [
                            #     {
                            #         "name": "test",
                            #         "host": "test",
                            #         "service": {
                            #             "rdp": {
                            #                 "redirect_clipboard": True,
                            #                 "redirect_audio": False,
                            #                 "auto_reconnection": True,
                            #                 "desktop_background": False,
                            #                 "window_drag": False,
                            #                 "animation": False,
                            #                 "screen_size": "full-screen",
                            #                 "colors": "16bit",
                            #                 "application_path": "",
                            #                 "start_in_folder": "/C/",
                            #                 "automatic_login": {
                            #                     "ssl_vpn": True
                            #                 },
                            #                 "display_on_mobile": True
                            #             }
                            #         }
                            #     }
                            # ]
                        # }
                    # ]
                }
            }
        }

        self.initial_local_group_json = {
            "user": {
                "local": {
                    # "group": [
                    #     {
                    #         "name": "test1",
                    #         "domain": {
                    #             "name": "any"
                    #         },
                    #         "comment": {
                    #             "comment_string": "sssss"
                    #         },
                    #         "memberships_by_ldap_location": {},
                    #         "one_time_password": {
                    #             "otp": True
                    #         }
                    #     },
                    #     {
                    #         "name": "test2",
                    #         "comment": {
                    #             "comment_string": "dddd"
                    #         },
                    #         "memberships_by_ldap_location": {},
                    #         "one_time_password": {
                    #             "otp": True
                    #         }
                    #     },
                    #     {
                    #         "name": "test3",
                    #         "comment": {
                    #             "comment_string": "wwwwww"
                    #         },
                    #         "memberships_by_ldap_location": {
                    #             "under_or_at": True
                    #         },
                    #         "ldap_location": {
                    #             "ldapLocation": "wwwwwwwww"
                    #         },
                    #         "one_time_password": {
                    #             "totp": True
                    #         }
                    #     },
                    #     {
                    #         "name": "test4",
                    #         "comment": {
                    #             "comment_string": "aaa"
                    #         },
                    #         "memberships_by_ldap_location": {},
                    #         "one_time_password": {}
                    #     },
                    #     {
                    #         "name": "test5",
                    #         "comment": {},
                    #         "memberships_by_ldap_location": {
                    #             "at": True
                    #         },
                    #         "ldap_location": {
                    #             "ldapLocation": "aaaaaaaaa"
                    #         },
                    #         "one_time_password": {}
                    #     }
                    # ]
                }
            }
        }

        self.initial_group_member_of_json = {
            "user": {
                "local": {
                    # "group": [
                    #     {
                    #         "name": "aaa",
                    #         "member": [
                    #             {
                    #                 "name": "Guest Services"
                    #             },
                    #             {
                    #                 "name": "SonicWALL Read-Only Admins"
                    #             },
                    #             {
                    #                 "name": "SonicWALL Administrators"
                    #             },
                    #             {
                    #                 "name": "55666"
                    #             }
                    #         ]
                    #     }
                    # ]
                }
            }
        }

        self.initial_group_vpn_client_access_json = {
            "user": {
                "local": {
                    # "group": [
                    #     {
                    #         "name": "Everyone",
                    #         "vpn_client_access": [
                    #             {
                    #                 "name": "X2 IPv6 Link-Local Address"
                    #             },
                    #             {
                    #                 "group": "Social Login Pass Group"
                    #             },
                    #             {
                    #                 "group": "All U1 Management IP"
                    #             },
                    #             {
                    #                 "group": "All U0 Management IP"
                    #             },
                    #             {
                    #                 "group": "All MGMT Management IP"
                    #             },
                    #             {
                    #                 "group": "All X7 Management IP"
                    #             },
                    #             {
                    #                 "group": "All X6 Management IP"
                    #             }
                    #         ]
                    #     }
                    # ]
                }
            }
        }

    def show_local_users(self):
        output = self.fw.api_get(self.url2)
        return output

    def show_local_user_by_name(self, name):
        url = self.url2 + '/name/' + name
        output = self.fw.api_get(url)
        return output

    def import_local_usr_from_ldap(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url2, msg, data=json_input)
        return repu_resp

    def show_local_groups(self):
        output = self.fw.api_get(self.url4)
        return output

    def show_local_group_by_name(self, name):
        url = self.url4 + '/name/' + name
        output = self.fw.api_get(url)
        return output
    
    def show_local_users_by_domain_name(self, username, domainname):
        url = str(self.url2) + '/name/' + username + '/domain/' + domainname
        logger.info(url)
        output = self.fw.api_get(url)
        return output
        
    def show_local_settings(self):
        output = self.fw.api_get(self.url5)
        return output

    def show_local_user_by_uuid(self, uuid):
        url = self.url2 + '/uuid/' + uuid          # addded show_local_user_by_uuid def
        output = self.fw.api_get(url)
        return output

    def show_local_group_by_uuid(self, uuid):
        url = self.url4 + '/uuid/' + uuid          # addded show_local_group_by_uuid def
        output = self.fw.api_get(url)
        return output

    def show_local_group_by_domain_name(self, groupname, domainname):
        url = str(self.url4) + '/name/' + groupname + '/domain/' + domainname
        logger.info(url)
        output = self.fw.api_get(url)
        return output
    
    def add_local_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url4, msg, data=json_input)
        return resp

    def logout_all_users(self ):
        output = self.fw.api_delete(self.logout_url)
        return output

    def get_local_user_uuid(self, username):
        resp = self.show_local_user_by_name(username)  # added get_local_user_uuid def
        uuid = resp['user']['local']['user'][0]['uuid']
        return uuid
        
    def config_user_local_base(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_put(self.local_base, msg, data=json_input)
        return repu_resp

    def get_local_group_uuid(self, groupname):
        resp = self.show_local_group_by_name(groupname)  # added get_local_group_uuid def
        uuid = resp['user']['local']['group'][0]['uuid']
        return uuid

    def delete_local_user_uuid(self,username):
        uuid = self.get_local_user_uuid(username) 
        url = 'api/sonicos/user/local/users/uuid/' + uuid 
        local_user = self.fw.api_delete(url)
        return local_user
    
    def edit_local_user_using_name(self, name, msg=False,**kwargs):
        json_input = copy.deepcopy(kwargs)
        url = self.url2 + '/name/' + name
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def local_settings(self, msg=False, **kwargs):
        self.options = dict(UserLocalApi.default_sso_setting_options)
        self.options.update(kwargs)
        kwargs = self.options
        try:
            json_input = copy.deepcopy(self.initial_local_settings_json)
            logger.info("\n\nInitial Json is :\n")
            pprint(json_input)
            json_input['user']['local']['apply_password_constraints'] = kwargs['apply_password_constraints']
            json_input['user']['local']['prune_on_expiry'] = kwargs['prune_on_expiry']
        except KeyError:
            logger.info("Error in creating JSON for user/group local settings")

        logger.info("\n\nUpdate Json is :\n")
        pprint(json_input)

        user_auth_resp = self.fw.api_put(self.url5, msg, data=json_input)
        return user_auth_resp


    def local_user(self, msg=False, **kwargs):
        self.options = dict(UserLocalApi.default_local_user_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_local_user(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd local user\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_post(self.url2, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'edit':
                logger.info("\n\nEdit local user\n")
                logger.info("\n\nUpdate Json is :\n")
                logger.info(json_input)
                if ('oldusername' in kwargs.keys() and kwargs['oldusername'] and
                         'domain' in kwargs.keys() and kwargs['domain']):
                    url = str(self.url2) + '/name/' + kwargs['oldusername'] + '/domain/' + kwargs['domain']
                    logger.info(url)
                    local_user = self.fw.api_put(url, msg, data=json_input)
                    return local_user
                else:
                    url = str(self.url2) + '/name/' + kwargs['username']
                    # url = str(self.url1) + '/name/' + kwargs['oldusername']
                    # logger.info(url)
                    # local_user = self.fw.api_put(url, msg, data=json_input)
                    # return local_user
                    local_user = self.fw.api_put(url, msg, data=json_input)
                    #local_user = self.fw.api_put(self.url2, msg, data=json_input)
                    return local_user
            else:
                pass

    def edit_local_user_by_uuid(self, uuid, **kwargs):
        self.options = dict(UserLocalApi.default_local_user_options)      #added edit_local_user_by_uuid def
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_local_user(**kwargs)
        url = self.url2 + '/uuid/' + uuid
        local_user = self.fw.api_put(url, data=json_input)
        return local_user

    def edit_local_user_by_name(self, name, **kwargs):
        self.options = dict(UserLocalApi.default_local_user_options)      #added edit_local_user_by_name def
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_local_user(**kwargs)
        url = self.url2 + '/name/' + name
        local_user = self.fw.api_put(url, data=json_input)
        return local_user
    
    def unbind_totp_key_with_name(self, name, msg=False):
        url = self.url_unbind + '/' + name
        return self.fw.api_post(url, msg)
    
    def unbind_totp_key_with_domain_name(self, name, domain, msg=False):
        url = self.url_unbind + '/' + name + '/' + 'domain' + '/' + domain
        return self.fw.api_post(url, msg)
    
    def build_local_user(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_local_user_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['local']['user'] = []
        json_input1 = self.sub_local_user_dict(**kwargs)
        json_input['user']['local']['user'].append(json_input1)

        return json_input

    def sub_local_user_dict(self, **kwargs):
        json_input = {}
        if ('username' in kwargs.keys() and kwargs['username']):
            json_input['name'] = kwargs['username']
        else:
            logger.error('User name must be specified')
        if ('userpassword' in kwargs.keys() and kwargs['userpassword']):
            json_input['password'] = kwargs['userpassword']
        else:
            logger.error('User password must be specified')
        if 'force_password_change' in kwargs.keys():
            json_input['force_password_change'] = kwargs['force_password_change']
        if 'domain' in kwargs.keys():
            if kwargs['domain']:
                json_input['domain'] = {}
                json_input['domain'] = kwargs['domain']  # domain type is any or kwargs['domain'], such as mydomain.com
            else:
                json_input['domain'] = {}
        if 'one_time_password' in kwargs.keys():
            json_input['one_time_password'] = {}
            if kwargs['one_time_password'] == 'totp':
                json_input['one_time_password']['totp'] = True   # one_time_password method is totp
            if kwargs['one_time_password'] == 'otp':
                json_input['one_time_password']['otp'] = True   # one_time_password method is otp
        if 'email_address' in kwargs.keys():
            if kwargs['email_address']:
                json_input['email_address'] = kwargs['email_address']
            else:      # kwargs['email_address'] == False, leave the field blank
                json_input['email_address'] = {}
        if 'account_lifetime' in kwargs.keys():
            if kwargs['account_lifetime']:   # kwargs['account_lifetime'] == True
                json_input['account_lifetime'] = {}
                # if ('accountlifetime' in kwargs.keys() and kwargs['accountlifetime']):
                #     json_input['account_lifetime']['lifetime'] = kwargs['accountlifetime']
                # else:
                #     logger.error('Lifetime must be specified')
                if ('lifetype' in kwargs.keys() and kwargs['lifetype']):    # life type is hours/minutes/days
                    json_input['account_lifetime'][kwargs['lifetype']] = kwargs['accountlifetime']
                else:
                    logger.error('Life type must be specified')
                if 'prune_on_expiry' in kwargs.keys():
                    json_input['prune_on_expiry'] = kwargs['prune_on_expiry']
            else:   # kwargs['account_lifetime'] == False
                json_input['account_lifetime'] = {}
        if 'comment' in kwargs.keys():
            if kwargs['comment']:
                json_input['comment'] = {}
                json_input['comment']['comment_string'] = kwargs['comment']
            else:           # kwargs['comment'] == False
                json_input['comment'] = {}
        if 'member_of' in kwargs.keys():
            json_input['member_of'] = []
            for key in kwargs['member_of']:
                json_input['member_of'].append({'name': key})
        if 'vpn_client_access' in kwargs.keys():
            json_input['vpn_client_access'] = []
            for key in kwargs['vpn_client_access']:
                if 'vpn_client_name' in kwargs.keys() and kwargs['vpn_client_name']:
                    json_input['vpn_client_access'].append({'name': key})
                else:
                    json_input['vpn_client_access'].append({'group': key})
        if 'guest_login_uniqueness' in kwargs.keys():
            json_input['guest_login_uniqueness'] = kwargs['guest_login_uniqueness']
            if 'guest_idle_timeout' in kwargs.keys():
                if kwargs['guest_idle_timeout']:   # kwargs['guest_idle_timeout'] == True
                    json_input['guest_idle_timeout'] = {}

                if ('timeout_type' in kwargs.keys() and kwargs['timeout_type']):    # timeout_type is hours/minutes/days
                    json_input['guest_idle_timeout'][kwargs['timeout_type']] = kwargs['guestidletimeout']
                else:
                    logger.error('timeout_type  must be specified')

        if 'quota_cycle' in kwargs.keys():
            if kwargs['quota_cycle']:
                json_input['quota_cycle'] = {}  # kwargs['quota_cycle'] is day/week/month
                json_input['quota_cycle'][kwargs['quota_cycle']] = True
            else:  # kwargs['quota_cycle'] is False/quota_cycle==no cycle
                json_input['quota_cycle'] = {}
        if 'session_lifetime' in kwargs.keys():
            if kwargs['session_lifetime']:  # kwargs['session_lifetime'] == True
                json_input['session_lifetime'] = {}
                if ('sessionlifetime' in kwargs.keys() and kwargs['sessionlifetime']):
                    json_input['session_lifetime'][kwargs['sessionlifetimetype']] = kwargs['sessionlifetime']
                else:
                    logger.error('Session_lifetime type must be specified')
            else:
                json_input['session_lifetime'] = {}
        if ('userquotalimit' in kwargs.keys() and kwargs['userquotalimit']):  # kwargs['userquotalimit'] == True
            json_input['limit'] = {}
            if 'receivelimit' in kwargs.keys():
                if kwargs['receivelimit']:
                    json_input['limit']['receive'] = kwargs['receivelimit']
                else:
                    json_input['limit']['receive'] = 0
            if 'transmit' in kwargs.keys():
                if kwargs['transmit']:
                    json_input['limit']['transmit'] = kwargs['transmit']
                else:
                    json_input['limit']['transmit'] = 0
        return json_input
    

    def delete_local_user_no_domain(self, username):
        url = str(self.url2) + '/name/' + username
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def delete_local_user_with_domain(self, username, domainname):
        url = str(self.url2) + '/name/' + username + '/domain/' + domainname
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def user_member_of(self, msg=False, domain = None, **kwargs):
        self.options = dict(UserLocalApi.default_local_user_options)
        self.options.update(kwargs)
        kwargs = self.options
        if domain:
            url_member = str(self.url_member_of) + kwargs['username'] + '/domain/' + domain
        else:
            url_member = str(self.url_member_of) + kwargs['username']
        logger.info(url_member)
        # url_no_domain = str(self.url1) + '/name/' + kwargs['oldusername']
        # url_with_domain = str(self.url2) + '/name/' + kwargs['oldusername'] + '/domain/' + kwargs['domain']
        json_input = self.build_user_member_of(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd user_member_of group\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_put(url_member, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'delete':
                logger.info("\n\nDelete user_member_of group\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_delete(url_member, msg, data=json_input)
                return local_user
            else:
                pass

    def build_user_member_of(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_user_member_of_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['local']['user'] = []
        json_input1 = self.sub_user_member(**kwargs)
        json_input['user']['local']['user'].append(json_input1)

        return json_input

    def sub_user_member(self, **kwargs):
        json_input = {}
        if ('username' in kwargs.keys() and kwargs['username']):
            json_input['name'] = kwargs['username']
        else:
            logger.error('User name must be specified')
        if ('userpassword' in kwargs.keys() and kwargs['userpassword']):
            # json_input['password'] = {}
            # json_input['password']['pwd'] = kwargs['userpassword']
            json_input['password'] = kwargs['userpassword']
        else:
            logger.error('User password must be specified')
        # member:SonicWALL Administrators/Content Filtering Bypass/Limited Administrators
        # /SSLVPN Services/SonicWALL Read-Only Admins/Guest Services/
        if 'member_of' in kwargs.keys():
            json_input['member_of'] = []
            for key in kwargs['member_of']:
                json_input['member_of'].append({'name': key})
        if 'vpn_client_access' in kwargs.keys():
            json_input['vpn_client_access'] = []
            for key in kwargs['vpn_client_access']:
                json_input['vpn_client_access'].append({'group': key})
        if "email_address" in kwargs.keys():
            json_input["email_address"] = kwargs["email_address"]

        
        return json_input

    def user_vpn_client_access(self, msg=False, **kwargs):
        self.options = dict(UserLocalApi.default_local_user_options)
        self.options.update(kwargs)
        kwargs = self.options
        # url_no_domain = str(self.url1) + '/' + 'name' + '/' + username
        # url_with_domain = str(self.url2) + '/' + 'name' + '/' + username + '/' + 'domain' + '/' + domainname
        json_input = self.build_user_vpn_client_access(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd user_vpn_client_access\n")
                logger.info("\n\nUpdate Json is :\n")
                logger.info(json_input)
                if 'domain' in kwargs.keys():
                    url = self.url2 + '/name/' + kwargs['username'] + '/domain/' + kwargs['domain']
                else:
                    url = self.url2 + '/name/' + kwargs['username']
                local_user = self.fw.api_put(url, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'delete':
                logger.info("\n\nDelete user_vpn_client_access\n")
                logger.info("\n\nUpdate Json is :\n")
                logger.info(json_input)
                local_user = self.fw.api_delete(self.url2, msg, data=json_input)
                return local_user
            else:
                pass

    def add_user_vpn_client_access(self, msg=False, **kwargs):
        self.options = dict(UserLocalApi.default_local_user_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_user_vpn_client_access(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd user_vpn_client_access\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_put(self.url2, msg, data=json_input)
                return local_user
            else:
                pass

    def build_user_vpn_client_access(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_user_vpn_client_access_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['local']['user'] = []
        json_input1 = self.sub_user_vpn_client_access(**kwargs)
        json_input['user']['local']['user'].append(json_input1)

        return json_input

    def sub_user_vpn_client_access(self, **kwargs):
        json_input = {}
        if ('username' in kwargs.keys() and kwargs['username']):
            json_input['name'] = kwargs['username']
        else:
            logger.error('User name must be specified')
        if ('userpassword' in kwargs.keys() and kwargs['userpassword']):
            json_input['password'] = {}
            json_input['password']= kwargs['userpassword']
        else:
            logger.error('User password must be specified')
        if 'vpn_client_access' in kwargs.keys():
            json_input['vpn_client_access'] = []
            for key in kwargs['vpn_client_access']:
                json_input['vpn_client_access'].append({'group': key})

        return json_input

    def user_bookmark(self, msg=False, **kwargs):
        self.options = dict(UserLocalApi.default_local_user_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_user_bookmark(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd user_bookmark\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_put(self.url2, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'edit':
                logger.info("\n\nEdit user_bookmark\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_put(self.url2, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'delete':
                logger.info("\n\nDelete user_bookmark\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_delete(self.url2, msg, data=json_input)
                return local_user
            else:
                pass

    def build_user_bookmark(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_user_bookmark_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['local']['user'] = []
        if ('username' in kwargs.keys() and kwargs['username']):
            json_input['user']['local']['user'].append({'name': kwargs['username']})
        else:
            logger.error('User name must be specified')
        if ('userpassword' in kwargs.keys() and kwargs['userpassword']):
            json_input['user']['local']['user'].append({'password': {'pwd': kwargs['userpassword']}})
        else:
            logger.error('User password must be specified')
        json_input1 = self.sub_bookmark(**kwargs)
        json_input['user']['local']['user'].append({'bookmark': [json_input1]})

        return json_input

    def sub_bookmark(self, **kwargs):
        json_input = {}
        if ('bookmarkname' in kwargs.keys() and kwargs['bookmarkname']):
            json_input['name'] = kwargs['bookmarkname']
        else:
            logger.error('Bookmark name must be specified')
        if ('bookmarkhost' in kwargs.keys() and kwargs['bookmarkhost']):
            json_input['host'] = kwargs['bookmarkhost']
        else:
            logger.error('Bookmark host must be specified')
        if 'service' in kwargs.keys():
            json_input['service'] = {}
            if kwargs['service'] == 'rdp':
                json_input['service']['rdp'] = {}
                if ('screen_size' in kwargs.keys() and kwargs['screen_size']):
                    # screen_size:640X480/800X600/1024X768/1280X1024/full-screen
                    json_input['service']['rdp']['screen_size'] = kwargs['screen_size']
                if ('colors' in kwargs.keys() and kwargs['colors']):
                    # colors:256/15bit/16bit/24bit/32bit
                    json_input['service']['rdp']['colors'] = kwargs['colors']
                if ('application_path' in kwargs.keys() and kwargs['application_path']):
                    json_input['service']['rdp']['application_path'] = kwargs['application_path']
                if ('start_in_folder' in kwargs.keys() and kwargs['start_in_folder']):
                    json_input['service']['rdp']['start_in_folder'] = kwargs['start_in_folder']
                if 'windows_advanced_options' in kwargs.keys():
                #options: redirect_clipboard/redirect_audio/auto_reconnection/desktop_background/window_drag/animation
                    for key in kwargs['windows_advanced_options']:
                        json_input['service']['rdp'][key] = kwargs['windows_advanced_options'][key]
                if ('automatic_login' in kwargs.keys() and kwargs['automatic_login']):
                    if kwargs['automatic_login'] == 'ssl_vpn':
                        json_input['service']['rdp']['automatic_login'] = {}
                        json_input['service']['rdp']['automatic_login']['ssl_vpn'] = True
                    elif kwargs['automatic_login'] == 'custom':
                        json_input['service']['rdp']['automatic_login'] = {}
                        json_input['service']['rdp']['automatic_login']['custom'] = {}
                        if ('usecustomcredentialsname' in kwargs.keys() and kwargs['usecustomcredentialsname']):
                            json_input['service']['rdp']['automatic_login']['custom']['name'] = kwargs['usecustomcredentialsname']
                        if ('usecustomcredentialspass' in kwargs.keys() and kwargs['usecustomcredentialspass']):
                            json_input['service']['rdp']['automatic_login']['custom']['password'] = kwargs[
                                'usecustomcredentialspass']
                        if ('usecustomcredentialsdomain' in kwargs.keys() and kwargs['usecustomcredentialsdomain']):
                            json_input['service']['rdp']['automatic_login']['custom']['domain'] = kwargs[
                                'usecustomcredentialsdomain']
                    else:
                        pass
                if 'display_on_mobile' in kwargs.keys():
                    json_input['service']['rdp']['display_on_mobile'] = kwargs['display_on_mobile']
            elif kwargs['service'] == 'sshv2':
                json_input['service']['sshv2'] = {}
                if 'automatic_accept_host_key' in kwargs.keys():
                    json_input['service']['sshv2']['automatic_accept_host_key'] = kwargs['automatic_accept_host_key']
                if 'display_on_mobile' in kwargs.keys():
                    json_input['service']['sshv2']['display_on_mobile'] = kwargs['display_on_mobile']
            elif kwargs['service'] == 'telnet':
                json_input['service']['telnet'] = {}
                if 'display_on_mobile' in kwargs.keys():
                    json_input['service']['telnet']['display_on_mobile'] = kwargs['display_on_mobile']
            elif kwargs['service'] == 'vnc':
                json_input['service']['vnc'] = {}
                if 'display_on_mobile' in kwargs.keys():
                    json_input['service']['vnc']['display_on_mobile'] = kwargs['display_on_mobile']
                if 'view_only' in kwargs.keys():
                    json_input['service']['vnc']['view_only'] = kwargs['view_only']
                if 'share_desktop' in kwargs.keys():
                    json_input['service']['vnc']['share_desktop'] = kwargs['share_desktop']
            else:
                json_input['service']['telnet'] = {}
                if 'display_on_mobile' in kwargs.keys():
                    json_input['service']['telnet']['display_on_mobile'] = kwargs['display_on_mobile']

        return json_input

    def local_group(self, msg=False, **kwargs):
        self.options = dict(UserLocalApi.default_local_group_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_local_group(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd local group\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                if 'domainname' in kwargs.keys():
                    url = self.url4 + '/name/' + kwargs['groupname'] + '/domain/' + kwargs['domainname']
                else:
                    url = self.url4
                local_group = self.fw.api_post(url, msg, data=json_input)
                return local_group
            elif kwargs['action'] == 'edit':
                logger.info("\n\nEdit local group\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                if 'domainname' in kwargs.keys():
                    url = self.url4 + '/name/' + kwargs['groupname'] + '/domain/' + kwargs['domainname']
                else:
                    url = self.url4
                local_group = self.fw.api_put(url, msg, data=json_input)
                return local_group
            else:
                pass

    def build_local_group(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_local_group_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['local']['group'] = []
        json_input1 = self.sub_local_group_dict(**kwargs)
        json_input['user']['local']['group'].append(json_input1)

        return json_input

    def sub_local_group_dict(self, **kwargs):
        json_input = {}
        json_input['name'] = ''
        json_input['comment'] = ''
        # json_input['comment']['comment_string'] = ''
        json_input['one_time_password'] = {}
        if 'grouptype' in kwargs.keys():
            if kwargs['grouptype'] == 'domaingroup':
                json_input['domain'] = {}
                json_input['domain']['name']= ''
                # if ('domainname' in kwargs.keys() and kwargs['domainname']):
                #     json_input['domain']['name'] = kwargs['domainname']
                    # kwargs['domainname'] == 'any' or like mydomain.com
                if kwargs['domainname'] == 'any':
                    json_input['domain'] = kwargs['domainname']
                else:
                    json_input['domain']['name'] = kwargs['domainname']
                if ('groupname' in kwargs.keys() and kwargs['groupname']):
                    json_input['name'] = kwargs['groupname']
                if ('comment' in kwargs.keys() and kwargs['comment']):
                    json_input['comment'] = kwargs['comment']
                if ('one_time_password' in kwargs.keys() and kwargs['one_time_password']):
                    json_input['one_time_password'][kwargs['one_time_password']] = True  # one_time_password method is otp/totp
                if 'read_only_restriction' in kwargs.keys() :
                    json_input['read_only_restriction'] = kwargs['read_only_restriction']
                if 'member' in kwargs.keys() :
                    json_input['member'] = kwargs['member']
            elif kwargs['grouptype'] == 'locally_only':
                if ('groupname' in kwargs.keys() and kwargs['groupname']):
                    json_input['name'] = kwargs['groupname']
                if ('comment' in kwargs.keys() and kwargs['comment']):
                    json_input['comment']= kwargs['comment']
                if ('one_time_password' in kwargs.keys() and kwargs['one_time_password']):
                    json_input['one_time_password'][kwargs['one_time_password']] = True  # one_time_password method is otp/totp
            elif kwargs['grouptype'] == 'LDAP_directory':
                json_input['ldap_location'] = {}
                json_input['ldap_location']['ldapLocation'] = ''
                json_input['memberships_by_ldap_location'] = {}
                if ('groupname' in kwargs.keys() and kwargs['groupname']):
                    json_input['name'] = kwargs['groupname']
                if ('comment' in kwargs.keys() and kwargs['comment']):
                    json_input['comment'] = kwargs['comment']
                if ('one_time_password' in kwargs.keys() and kwargs['one_time_password']):
                    json_input['one_time_password'][kwargs['one_time_password']] = True  # one_time_password method is otp/totp
                if ('ldap_location' in kwargs.keys() and kwargs['ldap_location']):
                    json_input['ldap_location']['ldapLocation'] = kwargs['ldap_location']
                if ('memberships_by_ldap_location' in kwargs.keys() and kwargs['memberships_by_ldap_location']):
                    json_input['memberships_by_ldap_location'][kwargs['memberships_by_ldap_location']] = True
                    # kwargs['memberships_by_ldap_location'] = 'at' or 'under_or_at'
            else:
                logger.error('Group type must be specified')

        if 'quota_cycle' in kwargs.keys():
            if kwargs['quota_cycle']:
                json_input['quota_cycle'] = {}  # kwargs['quota_cycle'] is day/week/month
                json_input['quota_cycle'][kwargs['quota_cycle']] = True
            else:  # kwargs['quota_cycle'] is False/quota_cycle==no cycle
                json_input['quota_cycle'] = {}
        if 'session_lifetime' in kwargs.keys():
            if kwargs['session_lifetime']:  # kwargs['session_lifetime'] == True
                json_input['session_lifetime'] = {}
                if ('sessionlifetime' in kwargs.keys() and kwargs['sessionlifetime']):
                    json_input['session_lifetime'][kwargs['sessionlifetimetype']] = kwargs['sessionlifetime']
                else:
                    logger.error('Session_lifetime type must be specified')
            else:
                json_input['session_lifetime'] = {}
        if ('userquotalimit' in kwargs.keys() and kwargs['userquotalimit']):  # kwargs['userquotalimit'] == True
            json_input['limit'] = {}
            if 'receivelimit' in kwargs.keys():
                if kwargs['receivelimit']:
                    json_input['limit']['receive'] = kwargs['receivelimit']
                else:
                    json_input['limit']['receive'] = 0
            if 'transmit' in kwargs.keys():
                if kwargs['transmit']:
                    json_input['limit']['transmit'] = kwargs['transmit']
                else:
                    json_input['limit']['transmit'] = 0

        return json_input

    # Group Administration part: no related json and code of this part

    def group_administration_tab(self, **kwargs):
        json_input = self.show_local_group_by_name(kwargs['groupname'])
        # set value of 'to_management_on_login' to True/False
        if 'to_management_on_login' in kwargs.keys():
            json_input['user']['local']['group'][0]['to_management_on_login'] = kwargs['to_management_on_login']
        if 'domain' in kwargs.keys():
            url = self.url4 + '/name/' + kwargs['groupname'] + '/domain/' + kwargs['domain']
        else:
            url = self.url4
        local_group = self.fw.api_put(url, data=json_input)
        return local_group


    def delete_local_group_no_domain(self, groupname):
        url = str(self.url4) + '/' + 'name' + '/' + groupname
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def delete_local_group_with_domain(self, groupname, domainname):
        url = str(self.url4) + '/' + 'name/' + groupname + '/domain/' + domainname
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def group_member_of(self, msg=False, name = '' ,**kwargs):
        self.options = dict(UserLocalApi.default_local_group_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_group_member_of(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                if 'domain' in kwargs.keys():
                    url = self.url4 + '/name/' + kwargs['groupname'] + '/domain/' + kwargs['domain']
                else:
                    url = self.url4
                    if name:
                        url = self.url4 + '/name/' + name
                logger.info("\n\nAdd  group member \n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_group = self.fw.api_put(url, msg, data=json_input)
                return local_group
            elif kwargs['action'] == 'delete':
                logger.info("\n\nDelete group member\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_group = self.fw.api_delete(self.url4, msg, data=json_input)
                return local_group
            else:
                pass

    def build_group_member_of(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_group_member_of_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['local']['group'] = []
        json_input1 = self.sub_group_member(**kwargs)
        json_input['user']['local']['group'].append(json_input1)

        return json_input

    def sub_group_member(self, **kwargs):
        json_input = {}
        if ('groupname' in kwargs.keys() and kwargs['groupname']):
            json_input['name'] = kwargs['groupname']
        else:
            logger.error('Group name must be specified')
        # member:SSLVPN Services/Guest Services/SonicWALL Read-Only Admins
        # /SonicWALL Administrators/"Limited Administrators/Content Filtering Bypass
        if 'member_of' in kwargs.keys():
            json_input['member'] = []
            for key in kwargs['member_of']:
                json_input['member'].append({'name': key})

        return json_input

    # delete one or more members from a group
    def delete_members_from_group(self, **kwargs):
        group_json = self.show_local_group_by_name(kwargs['groupname'])
        member_list = group_json['user']['local']['group'][0]['member']
        index = []
        for i, mem in enumerate(member_list):
            if mem['name'] in kwargs['members']:
                index.append(i)
        index.reverse()
        for i in index:
            group_json['user']['local']['group'][0]['member'].pop(i)
        if 'domain' in kwargs.keys():
            url = self.url4 + '/name/' + kwargs['groupname'] + '/domain/' + kwargs['domain']
        else:
            url = self.url4 + '/name/' + kwargs['groupname']
        local_group = self.fw.api_put(url, data=group_json)
        return local_group

    def group_vpn_client_access(self, msg=False, **kwargs):
        self.options = dict(UserLocalApi.default_local_group_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_group_vpn_client_access(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd group_vpn_client_access\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_put(self.url4, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'delete':
                logger.info("\n\nDelete group_vpn_client_access\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_delete(self.url4, msg, data=json_input)
                return local_user
            else:
                pass

    def build_group_vpn_client_access(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_group_vpn_client_access_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['local']['group'] = []
        json_input1 = self.sub_group_vpn_client_access(**kwargs)
        json_input['user']['local']['group'].append(json_input1)

        return json_input

    def sub_group_vpn_client_access(self, **kwargs):
        json_input = {}
        if ('groupname' in kwargs.keys() and kwargs['groupname']):
            json_input['name'] = kwargs['groupname']
        else:
            logger.error('Group name must be specified')
        if 'vpn_client_access' in kwargs.keys():
            json_input['vpn_client_access'] = []
            # for key in kwargs['vpn_client_access']:
            #     json_input['vpn_client_access'].append({'group': key})
            for obj in kwargs['vpn_client_access']:
                json_input['vpn_client_access'].append(obj)

        return json_input

    def group_bookmark(self, msg=False, **kwargs):
        self.options = dict(UserLocalApi.default_local_group_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_group_bookmark(**kwargs)
        if 'action' in kwargs.keys():
            # if kwargs['action'] == 'add':
            #     logger.info("\n\nAdd group_bookmark\n")
            #     logger.info("\n\nUpdate Json is :\n")
            #     pprint(json_input)
            #     local_group = self.fw.api_put(self.url4, msg, data=json_input)
            #     return local_group
            if kwargs['action'] == 'edit':
                logger.info("\n\nEdit group_bookmark\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_put(self.url4, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'delete':
                logger.info("\n\nDelete group_bookmark\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_group = self.fw.api_delete(self.url4, msg, data=json_input)
                return local_group
            else:
                pass

    def build_group_bookmark(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_user_bookmark_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['local']['group'] = []
        if ('groupname' in kwargs.keys() and kwargs['groupname']):
            json_input['user']['local']['group'].append({'name': kwargs['groupname']})
        else:
            logger.error('Group name must be specified')
        json_input1 = self.sub_bookmark(**kwargs)
        json_input['user']['local']['group'][0]['bookmark'] = [json_input1] 

        return json_input   
    
        
    def config_local_group_by_name(self, groupname, domainname, msg=False, **kwargs):
        if groupname:
            json_input = copy.deepcopy(kwargs)
            url = str(self.url4) + '/name/' + groupname + '/domain/' + domainname
            logger.info(url)
            resp = self.fw.api_put(url, msg, data=json_input)
            return resp
        else:
            logger.error("Pls enter group's name")
            return False



class UserGuestApi:
    '''UserGuestApi class'''

    default_user_guest_settings_options = {}

    default_user_guest_profile_options = {}

    def __init__(self, fw):
        self.fw = fw
        self.url1 = 'api/sonicos/user/guest/base'
        self.url2 = 'api/sonicos/user/guest/profiles'
        self.url3 = 'api/sonicos/user/guest/profile'
        self.url4 = 'api/sonicos/user/guest/user'
        self.url5 = 'api/sonicos/user/guest/users'
        self.url6 = 'api/sonicos/reporting/user/guest/statistics'
        self.url7 = 'api/sonicos/export/user/guest-accounts'
        self.get_guest_user_status = 'api/sonicos/reporting/user/guest/status'
        self.autogenerate = 'api/sonicos/user/guest/generate'

        self.initial_user_guest_settings_json = {}

        self.initial_user_guest_profile_json = {
            "user": {
                "guest": {
                    # "profile": [
                    #     {
                    #         "name": "guest",
                    #         "generate": {
                    #             "name": True,
                    #             "password": True
                    #         },
                    #         "name_prefix": {
                    #             "prefix": "guest"
                    #         },
                    #         "comment": {
                    #             "commentString": "ffsgfgafffff"
                    #         },
                    #         "enable": True,
                    #         "activate_on_login": True,
                    #         "login_uniqueness": True,
                    #         "prune_on_expiry": True,
                    #         "account_lifetime": {
                    #             "lifetime": 7,
                    #             "days": True
                    #         },
                    #         "quota_cycle": {
                    #             "day": True
                    #         },
                    #         "session_lifetime": {
                    #             "lifetime": 1,
                    #             "hours": True
                    #         },
                    #         "idle_timeout": {
                    #             "idle_time": 10,
                    #             "minutes": True
                    #         },
                    #         "limit": {
                    #             "receive": {
                    #                 "valInMB": 30
                    #             },
                    #             "transmit": {
                    #                 "valInMB": 50
                    #             }
                    #         }
                    #     }
                    # ]
                }
            }
        }

        self.initial_user_guest_account_json = {
            "user": {
                "guest": {
                    # "user": [
                    #     {
                    #         "name": "test",
                    #         "comment": {
                    #             "commentString": "test111"
                    #         },
                    #         "password": {
                    #             "pwd": ""
                    #         },
                    #         "enable": True,
                    #         "activate_on_login": True,
                    #         "login_uniqueness": True,
                    #         "prune_on_expiry": True,
                    #         "account_lifetime": {
                    #             "lifetime": 7,
                    #             "days": True
                    #         },
                    #         "quota_cycle": {
                    #             "day": True
                    #         },
                    #         "session_lifetime": {
                    #             "lifetime": 1,
                    #             "hours": True
                    #         },
                    #         "idle_timeout": {
                    #             "idle_time": 10,
                    #             "minutes": True
                    #         },
                    #         "limit": {
                    #             "receive": {},
                    #             "transmit": {}
                    #         }
                    #     }
                    # ]
                }
            }
        }


    def get_guest_user_status(self):
        output = self.fw.api_get(self.get_guest_user_status)
        return output

    def guest_user_autogenerate(self, msg = False, i = 3):
        json_input = {
              "user": {
                "guest": {
                  "generate": {
                    "num": i,
                    "name_prefix": "Guest",
                    "comment": "Autogenerated guest user",
                    "enable": True,
                    "activate_on_login": True,
                    "login_uniqueness": True,
                    "prune_on_expiry": True,
                  }
                }
              }
            }
        guest_user = self.fw.api_post(self.autogenerate, msg, data=json_input)
        return guest_user

    def show_user_guest_settings(self):
        output = self.fw.api_get(self.url1)
        return output

    def show_user_guest_profile(self):
        output = self.fw.api_get(self.url2)
        return output

    def show_user_guest_profile_by_name(self, name):  # added show_user_guest_profile_by_name
        url = self.url2 + '/name/' + name
        output = self.fw.api_get(url)
        return output

    def show_user_guest_account(self):
        output = self.fw.api_get(self.url5)
        return output

    def show_user_guest_session(self):  # added user guest session
        output = self.fw.api_get(self.url6)
        return output

    def show_user_guest_account_by_name(self, name):  # added show_user_guest_account_by_name
        url = self.url5 + '/name/' + name
        output = self.fw.api_get(url)
        return output

    def get_user_guest_account_uuid(self, username):
        resp = self.show_user_guest_account_by_name(username)  # added get_user_guest_account_uuid
        uuid = resp['user']['guest']['user'][0]['uuid']
        return uuid

    def show_user_guest_account_by_uuid(self, uuid):
        url = self.url5 + '/uuid/' + uuid  # addded show_user_guest_account_by_uuid
        output = self.fw.api_get(url)
        return output

    def show_user_guest_account(self):
        output = self.fw.api_get(self.url5)
        return output

    def user_guest_profile(self, msg=False, **kwargs):
        self.options = dict(UserGuestApi.default_user_guest_profile_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_user_guest_profile(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd user guest profile\n")
                logger.info("\n\nUpdate Json is :\n")
                logger.info(json_input)
                local_user = self.fw.api_post(self.url2, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'edit':
                logger.info("\n\nEdit user guest profile\n")
                logger.info("\n\nUpdate Json is :\n")
                logger.info(json_input)
                url = str(self.url2) + '/name/' + kwargs['profilename']
                local_user = self.fw.api_put(url, msg, data=json_input)
                return local_user
            else:
                pass

    def build_user_guest_profile(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_user_guest_profile_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['guest']['profile'] = []
        json_input1 = self.sub_user_guest_profile(**kwargs)
        json_input['user']['guest']['profile'].append(json_input1)

        return json_input

    def sub_user_guest_profile(self, **kwargs):
        json_input = {}
        json_input['name'] = ''
        if ('profilename' in kwargs.keys() and kwargs['profilename']):
            json_input['name'] = kwargs['profilename']
        if ('name_prefix' in kwargs.keys() and kwargs['name_prefix']):
            json_input['name_prefix'] = {}
            json_input['name_prefix']['prefix'] = kwargs['name_prefix']
        if ('generate' in kwargs.keys() and kwargs['generate']):  # kwargs['generate'] == True
            json_input['generate'] = {}
            if 'generatename' in kwargs.keys():
                json_input['generate']['name'] = kwargs['generatename']
            if 'generatepassword' in kwargs.keys():
                json_input['generate']['password'] = kwargs['generatepassword']
        if 'enable_account' in kwargs.keys():
            json_input['enable'] = kwargs['enable_account']
        json_input1 = self.sub_user_guest(**kwargs)
        json_input.update(json_input1)

        return json_input

    def sub_user_guest(self, **kwargs):
        json_input = {}
        if ('comment' in kwargs.keys() and kwargs['comment']):
            # json_input['comment'] = {}
            # json_input['comment']['commentString'] = kwargs['comment']
            json_input['comment'] = kwargs['comment']
        if 'login_uniqueness' in kwargs.keys():
            json_input['login_uniqueness'] = kwargs['login_uniqueness']
        if 'prune_on_expiry' in kwargs.keys():
            json_input['prune_on_expiry'] = kwargs['prune_on_expiry']
        if 'activate_on_login' in kwargs.keys():
            json_input['activate_on_login'] = kwargs['activate_on_login']
        if 'account_lifetime' in kwargs.keys():
            json_input['account_lifetime'] = {}
            if ('acco_lifetime' in kwargs.keys() and kwargs['acco_lifetime']):
                json_input['account_lifetime'] = {}
            if ('acco_lifetype' in kwargs.keys() and kwargs['acco_lifetype']):
                # acco_lifetype:minutes/hours/days
                type = kwargs.get('acco_lifetype', 'days')
                json_input['account_lifetime'][type] = kwargs['acco_lifetime']
        if ('idle_timeout' in kwargs.keys() and kwargs['idle_timeout']):
            json_input['idle_timeout'] = {}
            if ('idle_time' in kwargs.keys() and kwargs['idle_time']):
                json_input['idle_timeout'] = {}
                # json_input['idle_timeout']['idle_time'] = kwargs['idle_time']
            if ('idle_type' in kwargs.keys() and kwargs['idle_type']):
                # idle_type:minutes/hours/days
                type = kwargs.get('idle_type', 'days')
                json_input['idle_timeout'][type] = kwargs['idle_time']
        if 'quota_cycle' in kwargs.keys():
            if kwargs['quota_cycle']:
                json_input['quota_cycle'] = {}
                json_input['quota_cycle'][kwargs['quota_cycle']] = True
                # quota_cycle: day/week/month
            else:
                json_input['quota_cycle'] = {}
        if 'session_lifetime' in kwargs.keys():
            json_input['session_lifetime'] = {}
            if ('sess_lifetime' in kwargs.keys() and kwargs['sess_lifetime']):
                json_input['session_lifetime'] = {}
            if ('sess_lifetype' in kwargs.keys() and kwargs['sess_lifetype']):
                # sess_lifetype:minutes/hours/days
                type = kwargs.get('sess_lifetype', 'days')
                json_input['session_lifetime'][type] = kwargs['sess_lifetime']
        if 'limit' in kwargs.keys():
            json_input['limit'] = {}
            if ('limit_receive' in kwargs.keys() and kwargs['limit_receive']):
                json_input['limit']['receive'] = {}
                json_input['limit']['receive'] = kwargs['limit_receive']
            if ('limit_transmit' in kwargs.keys() and kwargs['limit_transmit']):
                json_input['limit']['transmit'] = {}
                json_input['limit']['transmit'] = kwargs['limit_transmit']

        return json_input

    def del_user_guest_profile(self, profilename):
        url = str(self.url2) + '/name/' + profilename
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def configure_user_guest_account_json(self, **kwargs):

        json_input = copy.deepcopy(kwargs)
        put_response = self.fw.api_put(self.url5, data=json_input)
        return put_response

    def export_guest_account(self):
        res = self.fw.api_get(self.url7)
        return res

    def user_guest_account(self, msg=False, **kwargs):
        self.options = dict(UserGuestApi.default_user_guest_profile_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_user_guest_account(**kwargs)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                logger.info("\n\nAdd user guest account\n")
                logger.info("\n\nUpdate Json is :\n")
                pprint(json_input)
                local_user = self.fw.api_post(self.url5, msg, data=json_input)
                return local_user
            elif kwargs['action'] == 'edit':
                logger.info("\n\nEdit user guest account\n")
                logger.info("\n\nUpdate Json is :\n")
                logger.info(json_input)
                url = str(self.url5) + '/name/' + kwargs['accountname']
                local_user = self.fw.api_put(url, msg, data=json_input)
                return local_user
            else:
                pass

    def build_user_guest_account(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_user_guest_account_json)
        logger.info("\n\nInitial Json is :\n")
        pprint(json_input)
        json_input['user']['guest']['user'] = []
        json_input1 = self.sub_user_guest_account(**kwargs)
        json_input['user']['guest']['user'].append(json_input1)

        return json_input

    def sub_user_guest_account(self, **kwargs):
        json_input = {}
        json_input['name'] = ''
        if ('accountname' in kwargs.keys() and kwargs['accountname']):
            json_input['name'] = kwargs['accountname']
        if ('password' in kwargs.keys() and kwargs['password']):
            # json_input['password'] = {}
            json_input['password'] = kwargs['password']
        if 'enable_guest_service_privilege' in kwargs.keys():
            json_input['enable'] = kwargs['enable_guest_service_privilege']
        json_input1 = self.sub_user_guest(**kwargs)
        json_input.update(json_input1)

        return json_input

    def edit_guest_user_account_by_uuid(self, uuid, **kwargs):
        self.options = dict(
            UserGuestApi.default_user_guest_profile_options)  # added edit_guest_user_account_by_uuid def
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_user_guest_account(**kwargs)
        url = self.url5 + '/uuid/' + uuid
        guest_user = self.fw.api_put(url, data=json_input)
        return guest_user

    def del_user_guest_account(self, accountname):
        url = str(self.url5) + '/name/' + accountname
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def get_user_guest_status(self, ip=None):
        url = 'api/sonicos/reporting/user/guest/status'
        if ip:
            url = url + '/ip/' + str(ip)
        output = self.fw.api_get(url)
        return output

    def logout_all_guest_user(self):
        url = 'api/sonicos/user/logout/guests'
        logger.info(url)
        output = self.fw.api_delete(url)
        return output

    def add_guest_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.url2, msg, data=json_input)
        return resp
    
    def add_guest_account(self, msg=False, **kwargs):
        '''
        Kwargs format example:
        guest_user = {
          "name": "c",
          "comment": "Auto-Generated",
          "password": "c",
          "enable": true,
          "login_uniqueness": true,
          "prune_on_expiry": true,
          "activate_on_login": false,
          "account_lifetime": {
            "minutes": 1
          },
          "idle_timeout": {
            "minutes": 1
          },
          "quota_cycle": {},
          "session_lifetime": {
            "minutes": 1
          },
          "limit": {
            "receive": 0,
            "transmit": 0
          }
        }
        '''
        json_input = copy.deepcopy(self.initial_user_guest_account_json)
        json_input['user']['guest']['user'] = []
        json_input['user']['guest']['user'].append(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.url5, msg, data=json_input)
        return resp

    def get_guest_status(self,ip=None):
        url = 'api/sonicos/dynamic-file/getGuestUserStatus.json'
        if ip:
            url = url + '/ip/' + str(ip)
        output = self.fw.api_get(url)
        return output


class UserLoginApi:
    '''
    UserLoginApi class
    use for local user login, written by Neil Zhang
    '''
    urllib3.disable_warnings()

    def __init__(self, headers, ip, username, password):
        # if headers is None:
        self.headers = OrderedDict([('Accept', 'application/json'),
                                    ('Content-Type', 'application/json'),
                                    ('Accept-Encoding', 'application/json'),
                                    ('charset', 'UTF-8')])
        self.ip = ip
        self.username = username
        self.password = password
        self.fwurl = 'https://' + self.ip + '/'
        self.loginapi = self.fwurl + 'api/sonicos/auth'
        self.startmgmtapi = self.fwurl + 'api/sonicos/start-management'
        self.configmodeapi = self.fwurl + 'api/sonicos/config-mode'
        self.pendingapi = self.fwurl + 'api/sonicos/config/pending'
        self.guestuserapi = self.fwurl + 'api/sonicos/user/guest/users'
        self.localuserapi = self.fwurl + 'user/local/users'
        self.nonconfigapi = self.fwurl + 'api/sonicos/non-config-mode'

        self.initial_user_guest_account_json = {
            "user": {
                "guest": {
                    "user": [
                        {
                            "name": "None",
                            "password": "None",
                            "bearer_token": "None"

                        }]}}}

    def local_user_login(self):
        payload = {'override': False, 'snwl': True}
        payload = json.dumps(payload)
        urllib3.disable_warnings()
        resp = requests.post(self.loginapi, auth=(self.username, self.password), data=payload, headers=self.headers,
                             verify=False)
        response = resp.content.decode('utf-8')
        logger.info("Login response after decode:\r\n{}".format(response))
        try:
            login_response = json.loads(response)
            logger.debug(login_response)
            if login_response['status']['success']:
                logger.info('Successfully login sonincos')
                for token in login_response['status']['info']:
                    if token['bearer_token']:
                        bearer_token = login_response['status']['info'][0]['bearer_token']
                        # post managment button in start managment page
                        self.headers = OrderedDict([('Accept', 'application/json'),
                                                    ('Content-Type', 'application/json'),
                                                    ('Accept-Encoding', 'application/json'),
                                                    ('charset', 'UTF-8'),
                                                    ('Authorization', 'Bearer ' + bearer_token)])
                        startmgmtresponse = requests.post(self.startmgmtapi, headers=self.headers, data={},
                                                          verify=False)
                        if startmgmtresponse.status_code == 200:
                            logger.info('Successfully post start managment.')
                        else:
                            logger.error('Post start managment failed. response json: ' + startmgmtresponse.json())
                            return False, False
                        # post config mode from start managment page to index page
                        configmoderesponse = requests.post(self.configmodeapi, headers=self.headers, data={},
                                                           verify=False)
                        status_code = configmoderesponse.status_code
                        resp = configmoderesponse.content.decode('utf-8')
                        return_msg = json.loads(resp)
                        logger.info(return_msg)
                        return_value = return_msg['status']['success']
                        if configmoderesponse.status_code == 200:
                            logger.info('Successfully post config mode in start managment page.')
                        elif configmoderesponse.status_code != 200 and return_msg['status']['info'][0][
                            'config_mode'] == 'No' or return_msg['status']['info'][0][
                            'message'] == 'Cannot change to config mode':
                            logger.info('non config mode, re-login')
                            resp = requests.post(self.nonconfigapi, headers=self.headers, verify=False)
                            status_code = resp.status_code
                            resp1 = resp.content.decode('utf-8')
                            return_msg = json.loads(resp1)
                            logger.info(return_msg)
                            return_value = return_msg['status']['success']
                        else:
                            logger.error('Post config mode failed. response json: ' + configmoderesponse.json())
                            return False, False
                        return True, bearer_token
                    else:
                        logger.error('Get the bearer_token failed !')
                        return False, False
            else:
                logger.info("Login error\nResponse is " + login_response['status'])
                return "Login error\nResponse is " + login_response['status'], False
        except:
            logger.error('Limit user Login failed !')
            return False, False
        
    def add_guest_user_account(self, **kwargs):
        # Check limit user configurable
        self.headers = OrderedDict([('Accept', 'application/json'),
                                    ('Content-Type', 'application/json'),
                                    ('Accept-Encoding', 'application/json'),
                                    ('charset', 'UTF-8'),
                                    ('Authorization', 'Bearer ' + kwargs['bearer_token'])])
        del kwargs['bearer_token']
        guestresponse = requests.post(self.guestuserapi, headers=self.headers, data=json.dumps(kwargs), verify=False)
        logger.info(guestresponse.status_code)
        # post pending to submit guest user configure
        pendingresponse = requests.post(self.pendingapi, headers=self.headers, data={}, verify=False)
        result = True if pendingresponse.status_code == 200 else False
        logger.info(result)
        return result

    def add_local_user_account(self, **kwargs):
        # Check limit user no configurable
        self.headers = OrderedDict([('Accept', 'application/json'),
                                    ('Content-Type', 'application/json'),
                                    ('Accept-Encoding', 'application/json'),
                                    ('charset', 'UTF-8'),
                                    ('Authorization', 'Bearer ' + kwargs['bearer_token'])])
        del kwargs['bearer_token']
        try:

            localresponse = requests.post(self.localuserapi, headers=self.headers, data=json.dumps(kwargs),
                                          verify=False)
            logger.info(localresponse.status_code)
            # post pending to submit guest user configure
            pendingresponse = requests.post(self.pendingapi, headers=self.headers, data={}, verify=False)
            result = True if pendingresponse.status_code == 200 else False
            logger.info(result)
            return result
        except:
            return False

    def logout_guest_user(self, **kwargs):  # Added Logout method
        self.headers = OrderedDict([('Accept', 'application/json'),
                                    ('Content-Type', 'application/json'),
                                    ('Accept-Encoding', 'application/json'),
                                    ('charset', 'UTF-8'),
                                    ('Authorization', 'Bearer ' + kwargs['bearer_token'])])
        del kwargs['bearer_token']
        resp = requests.delete(self.loginapi, headers=self.headers, verify=False)
        logger.info("Logout response:")
        logger.info(resp)
        status_code = resp.status_code
        logger.info(status_code)
        response = resp.content.decode('utf-8')
        logout_response = json.loads(response)
        logger.info(logout_response)
        if not logout_response['status']['success']:
            logger.error("Response is " + logout_response['status']['info'][0]['message'])
            return "Logout error\nResponse is " + logout_response['status']['info'][0]['message']
        else:
            logger.info('Successfully logout sonincos')
            return True

    def guest_user_login(self):
        payload = {'override': False, 'snwl': True}
        payload = json.dumps(payload)
        urllib3.disable_warnings()
        resp = requests.post(self.loginapi, auth=(self.username, self.password), data=payload, headers=self.headers,
                             verify=False)
        response = resp.content.decode('utf-8')
        logger.info("Login response after decode:\r\n{}".format(response))
        try:
            login_response = json.loads(response)
            logger.debug(login_response)
            if login_response['status']['success']:
                logger.info('Successfully login sonincos')
                for token in login_response['status']['info']:
                    if token['bearer_token']:
                        bearer_token = login_response['status']['info'][0]['bearer_token']
                        return True, bearer_token
                    else:
                        logger.error('Get the bearer_token failed !')
                        return False, False
            else:
                logger.info("Login error\nResponse is " + login_response['status'])
                return "Login error\nResponse is " + login_response['status'], False
        except:
            logger.error('Limit user Login failed !')
            return False, False