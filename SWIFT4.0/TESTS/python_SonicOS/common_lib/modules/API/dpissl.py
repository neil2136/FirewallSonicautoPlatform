import copy
import re
import json
from collections import OrderedDict
#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)
from runner.settings import logger

class ServerSslApi:
    """ServerSslApi class"""
    default_options = {
        'enable': False,
        'application_firewall': False,
        'intrusion_prevention': False,
        'gateway_anti_virus': False,
        'gateway_anti_spyware': False,
        'include_address': True,
        'include_address_type': 'all',
        'include_user': True,
        'include_user_type': 'all',
        'exclude_address': None,
        'exclude_address_type': None,
        'exclude_user': None,
        'exclude_user_type': None,
        'ssl_server': 'X0 IP',
        'ssl_server_type': 'name',
        'certificate': 'ca1',
        'cleartext': False,
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/dpi-ssl/server'
        self.initial_general_settings_json = {
            "dpi_ssl": {
                "server": {
                    "enable": False,
                    "intrusion_prevention": False,
                    "gateway": {
                        "anti_virus": False,
                        "anti_spyware": False
                    },
                    "application_firewall": False,
                    "exclude": {
                        "address": {},
                        "user": {}
                    },
                    "include": {
                        "address": {
                            "all": True
                        },
                        "user": {
                            "all": True
                        }
                    }
                }
            }
        }

        self.initial_add_server_json = {
            "dpi_ssl": {
                "server": {
                    "ssl_server": [
                        {
                            "name": "X0 IP",
                            "certificate": "ca1",
                        }
                    ]
                }
            }
        }

    def config_general_settings(self, msg=False, **kwargs):
        url = self.url + '/base'
        self.options = dict(ServerSslApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_general_settings(**kwargs)
        sslserver_resp = self.fw.api_put(url, msg, data=json_input)
        return sslserver_resp

    def build_json_general_settings(self, **kwargs):
        json_input = {}
        logger.info(kwargs)

        try:
            json_input = copy.deepcopy(self.initial_general_settings_json)
            json_input['dpi_ssl']['server']['enable'] = kwargs['enable']
            json_input['dpi_ssl']['server']['intrusion_prevention'] = kwargs['intrusion_prevention']
            json_input['dpi_ssl']['server']['application_firewall'] = kwargs['application_firewall']
            json_input['dpi_ssl']['server']['gateway']['anti_virus'] = kwargs['gateway_anti_virus']
            json_input['dpi_ssl']['server']['gateway']['anti_spyware'] = kwargs['gateway_anti_spyware']

            address_type_list = ['group', 'all', 'name']
            user_type_list = ['name', 'all', 'guest','guests','administrator', 'group']

            if 'include_address' in kwargs.keys() and 'include_address_type' in kwargs.keys():
                if kwargs['include_address_type'] in address_type_list: 
                    if kwargs['include_address_type'] != 'all':
                        json_input['dpi_ssl']['server']['include']['address'][kwargs['include_address_type']] \
                            = kwargs['include_address']
                        del json_input['dpi_ssl']['server']['include']['address']['all']
                    else:
                        pass
                else:
                    logger.error('dpissl server include_address_type error')
                    return False
            elif 'include_address' not in kwargs.keys() and 'include_address_type' in kwargs.keys():
                logger.error('Please specify dpissl server include_address.')
            elif 'include_address' in kwargs.keys() and 'include_address_type' not in kwargs.keys():
                logger.error('Please specify dpissl server include_address_type.')
            else:
                logger.info('Include address type is all,include address is True by default')

            if 'include_user' in kwargs.keys() and 'include_user_type' in kwargs.keys():
                if kwargs['include_user_type'] in user_type_list:
                    if kwargs['include_user_type'] != 'all':
                        json_input['dpi_ssl']['server']['include']['user'][kwargs['include_user_type']] \
                            = kwargs['include_user']
                        del json_input['dpi_ssl']['server']['include']['user']['all']
                    else:
                        pass
                else:
                    logger.error('include_user_type error')
                    return False
            elif 'include_user' not in kwargs.keys() and 'include_user_type' in kwargs.keys():
                logger.error('Please specify include_user.')
            elif 'include_user' in kwargs.keys() and 'include_user_type'not in kwargs.keys():
                logger.error('Please specify include_user_type.')
            else:
                logger.info('include_user_type is all,include_user value is True by default')

            if 'exclude_address_type' in kwargs.keys() and 'exclude_address_type' in kwargs.keys():
                if kwargs['exclude_address_type'] in address_type_list:
                    json_input['dpi_ssl']['server']['exclude']['address'][kwargs['exclude_address_type']] \
                        = kwargs['exclude_address']
                else:
                    if kwargs['exclude_address_type'] is None:
                        json_input['dpi_ssl']['server']['exclude']['address'] = {}
                    else:
                        logger.error('exclude_address_type error')
                        return False
            elif 'exclude_address_type' not in kwargs.keys() and 'exclude_address' in kwargs.keys():
                logger.error('Please specify exclude_address_type.')
            elif 'exclude_address_type' in kwargs.keys() and 'exclude_address' not in kwargs.keys():
                logger.error('Please specify exclude_address.')
            else:
                logger.info('exclude_address_type is None,exclude_address is None by default')

            if 'exclude_user' in kwargs.keys() and 'exclude_user_type' in kwargs.keys():
                if kwargs['exclude_user_type'] in user_type_list:
                    json_input['dpi_ssl']['server']['exclude']['user'][kwargs['exclude_user_type']] \
                        = kwargs['exclude_user']
                else:
                    if kwargs['exclude_user_type'] is None:
                        json_input['dpi_ssl']['server']['exclude']['user'] = {}
                    else:
                        logger.error('exclude_user_type error')
                        return False
            elif 'exclude_user' not in kwargs.keys() and 'exclude_user_type' in kwargs.keys():
                logger.error('Please specify exclude_user.')
            elif 'exclude_user' in kwargs.keys() and 'exclude_user_type' not in kwargs.keys():
                logger.error('Please specify exclude_user_type.')
            else:
                logger.info('exclude_user_type is None,exclude_user is None by default')

        except KeyError:
            logger.error("Error: in creating JSON for dpissl server")
        logger.info(json_input)
        return json_input

    def add_sslserver(self, msg=False, **kwargs):
        self.options = dict(ServerSslApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_add_server(**kwargs)
        url = self.url + '/ssl-servers'
        logger.info(url)
        sslserver_resp = self.fw.api_post(url, msg, data=json_input)
        return sslserver_resp

    def del_sslserver(self, msg=False, **kwargs):
        self.options = dict(ServerSslApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_add_server(**kwargs)
        url = self.url + '/ssl-servers'
        sslserver_resp = self.fw.api_delete(url, msg, data=json_input)
        return sslserver_resp

    def edit_sslserver(self, msg=False, **kwargs):
        self.options = dict(ServerSslApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_edit_server(**kwargs)
        sslserver_resp = self.fw.api_put(self.url, msg, data=json_input)
        return sslserver_resp

    def build_json_add_server(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        server_type_list = ['name','group']

        try:
            json_input = copy.deepcopy(self.initial_add_server_json)
            if 'ssl_server' in kwargs.keys() and 'ssl_server_type' in kwargs.keys():
                if kwargs['ssl_server_type'] in server_type_list:
                    json_input['dpi_ssl']['server']['ssl_server'][0]['certificate'] = kwargs['certificate']
                    json_input['dpi_ssl']['server']['ssl_server'][0][kwargs['ssl_server_type']] = kwargs['ssl_server']
                    json_input['dpi_ssl']['server']['ssl_server'][0]['cleartext'] = kwargs['cleartext']

                    if json_input['dpi_ssl']['server']['ssl_server'][0]['cleartext'] is False:
                        del json_input['dpi_ssl']['server']['ssl_server'][0]['cleartext']
                    else:
                        logger.info('ssl server cleartext value is true...')
                else:
                    logger.error('ssl_server_type error')
                    return False
            elif 'ssl_server' not in kwargs.keys() and 'ssl_server_type' in kwargs.keys():
                logger.error('ssl_server must be specified.')
            elif 'ssl_server' in kwargs.keys() and 'ssl_server_type' not in kwargs.keys():
                logger.error('ssl_server_type must be specified')
            else:
                logger.info('ssl_server_type is name and ssl_server is X0 IP by default')

        except KeyError:
            logger.error("Error: in creating JSON for dpissl server")
        logger.info(json_input)
        return json_input

    def build_json_edit_server(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        server_type_list = ['name', 'group']
        try:
            json_input = copy.deepcopy(self.initial_add_server_json)
# currently only support edit checkbox cleartext status on our DUT
#            if 'ssl_server_new' in kwargs.keys() and 'ssl_server_type_new' in kwargs.keys():
#                if kwargs['ssl_server_type_new'] in server_type_list:
#                    json_input['dpi_ssl']['server']['ssl_server'][0][kwargs['ssl_server_type_new']] = kwargs['ssl_server_new']
#                else:
#                    logger.error('ssl_server_type error')
#                    return False
#            elif 'ssl_server' not in kwargs.keys() and 'ssl_server_type' in kwargs.keys():
#                logger.error('ssl_server must be specified.')
#            elif 'ssl_server' in kwargs.keys() and 'ssl_server_type' not in kwargs.keys():
#                logger.error('ssl_server_type must be specified')
#            else:
#                logger.info('ssl_server_type is name and ssl_server is X0 IP by default')
#                       
#            if 'certificate_new' in kwargs.keys():
#                json_input['dpi_ssl']['server']['ssl_server'][0]['certificate'] = kwargs['certificate_new']
#
            if 'cleartext_new' in kwargs.keys():
                json_input['dpi_ssl']['server']['ssl_server'][0]['cleartext'] = kwargs['cleartext_new']

            if json_input['dpi_ssl']['server']['ssl_server'][0]['cleartext'] is False:
                del json_input['dpi_ssl']['server']['ssl_server'][0]['cleartext']
            else:
                logger.info('ssl server cleartext value is true...')

        except KeyError:
            logger.error("Error: in creating JSON for dpissl server")
        logger.info(json_input)
        return json_input

    def del_all_servers(self, msg=False):
        server_details = self.get_sslserver_config()
        sslserver_resp = self.fw.api_delete(self.url, msg, data=server_details)
        return sslserver_resp

    def get_sslserver_config(self, msg=False, ip='192.168.168.168'):
        server_url_base = self.url + '/base'
        response = self.fw.api_get(server_url_base)
        return response
         
    def get_ssl_servers_config(self, msg=False, ip='192.168.168.168'):
        server_url_base = self.url + '/ssl-servers'
        response = self.fw.api_get(server_url_base)
        return response

    def config_sslserver(self, msg=False, **kwargs):
        url = 'api/sonicos/dpi-ssl/server/ssl-servers'
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        response = self.fw.api_post(url, msg, data=json_input)
        return response

class ClientSslApi:
    """ClientSslApi class"""
    default_options = {
        'enable': False,
        'application_firewall': False,
        'intrusion_prevention': False,
        'gateway_anti_virus': False,
        'gateway_anti_spyware': False,
        'content_filter': False,
        'authenticate_server_for_decrypted_connections': False,
        'expired_ca': False,
        'deployment_server_domains': False,
        'bypass_decryption': True,
        'audit_built_in_exclusion': False,
        'authenticate_server': False,
        'open_failed_connections': True,
        'cert': "2048-bit",
        'exclude_type':None,
        'exclude_address_type': None,
        'exclude_address': None,
        'exclude_service_type': None,
        'exclude_service': None,
        'exclude_user_type': None,
        'exclude_user': None,
        'cfs_category_unavailable': False,
        'include_address_type': 'all',
        'include_address': True,
        'include_service_type': 'all',
        'include_service': True,
        'include_user_type': 'all',
        'include_user': True,
        'common_name': "test1",
        'common_name_action': "skip_content_filter_exclusion",
        'selected':'include',
        
    }

    def __init__(self, fw):
        self.fw = fw
        self.url_raw = 'api/sonicos/raw'
        self.url = 'api/sonicos/dpi-ssl/client'
        self.url_category = 'api/sonicos/dpi-ssl/client/cfs-categories'
        self.get_common_name_list = 'api/sonicos/dynamic-file/getConnFailureList.json'
        self.url_common = 'api/sonicos/dpi-ssl/client/common-names'
        self.headers = OrderedDict([('Accept', 'application/json'),
                        ('Content-Type', 'application/json'),
                        ('Accept-Encoding', 'application/json'),
                        ('X-SNWL-API-Scope', 'extended'),
                        ('charset', 'UTF-8')])
        self.initial_general_settings_json = {
            "dpi_ssl": {
                "client": {
                    "enable": False,
                    "intrusion_prevention": False,
                    "gateway": {
                        "anti_virus": False,
                        "anti_spyware": False
                    },
                    "application_firewall": False,
                    "content_filter": False,
                    "authenticate_server_for_decrypted_connections": False,
                    "deployment_server_domains": False,
                    "bypass_decryption": True,
                    "audit_built_in_exclusion": False,
                    "authenticate_server": False,
                    "open_failed_connections": True,
                }
            }
            
        }

        self.initial_certificate_json = {
            "dpi_ssl": {
                "client": {
                    "resigning_authority": {                
                        "default": "2048-bit"
                    }
                }
            }
        }

        self.initial_objects_json = {
            "dpi_ssl": {
                "client": {
                    "exclude": {
                        "address": {},
                        "service": {},
                        "user": {},
                        "cfs_category_unavailable": False
                    },
                    "include": {
                        "address": {
                            "all": True
                        },
                        "service": {
                            "all": True
                        },
                        "user": {
                            "all": True
                        }
                    }
                }
            }
        }

        self.initial_common_name_json = {
            "dpi_ssl": {
                "client": {
                    "common_name":[
                        {
                            "cName": "",
                            "action":{"exclude":{}}
                        }
                    ]
                }
            }
        }

        self.initial_cfs_category_based_exclusion_inclusion = {
            "dpi_ssl": {
                "client": {
                    "cfs_categories":{
                        "exclude": True,
                        "include": True,
                        "category":[]
                    },
                    "exclude": {
                        "cfs_category_unavailable": False
                    }
                }
            }
        }
    
        self.categories = {
            "dpi_ssl": {
                "client": {
                    "cfs_categories": {
                        "category": [
                            {
                                "category": "1. Violence"
                            },
                            {
                                "category": "2. Intimate Apparel/Swimsuit"
                            },
                            {
                                "category": "3. Nudism"
                            },
                            {
                                "category": "4. Pornography"
                            },
                            {
                                "category": "5. Weapons"
                            },
                            {
                                "category": "6. Adult/Mature Content"
                            },
                            {
                                "category": "7. Cult/Occult"
                            },
                            {
                                "category": "8. Drugs/Illegal Drugs"
                            },
                            {
                                "category": "9. Illegal Skills/Questionable Skills"
                            },
                            {
                                "category": "10. Sex Education"
                            },
                            {
                                "category": "11. Gambling"
                            },
                            {
                                "category": "12. Alcohol/Tobacco"
                            },
                            {
                                "category": "13. Chat/Instant Messaging (IM)"
                            },
                            {
                                "category": "14. Arts/Entertainment"
                            },
                            {
                                "category": "15. Business and Economy"
                            },
                            {
                                "category": "16. Abortion/Advocacy Groups"
                            },
                            {
                                "category": "17. Education"
                            },
                            {
                                "category": "18. Training and Tools"
                            },
                            {
                                "category": "19. Cultural Institutions"
                            },
                            {
                                "category": "20. Online Banking"
                            },
                            {
                                "category": "21. Online Brokerage and Trading"
                            },
                            {
                                "category": "22. Games"
                            },
                            {
                                "category": "23. Government"
                            },
                            {
                                "category": "24. Military"
                            },
                            {
                                "category": "25. Political/Advocacy Groups"
                            },
                            {
                                "category": "26. Health"
                            },
                            {
                                "category": "27. Information Technology/Computers"
                            },
                            {
                                "category": "28. Hacking"
                            },
                            {
                                "category": "29. Search Engines and Portals"
                            },
                            {
                                "category": "30. E-Mail"
                            },
                            {
                                "category": "31. Web Communications"
                            },
                            {
                                "category": "32. Job Search"
                            },
                            {
                                "category": "33. News and Media"
                            },
                            {
                                "category": "34. Personals and Dating"
                            },
                            {
                                "category": "35. Usenet News Groups"
                            },
                            {
                                "category": "36. Reference"
                            },
                            {
                                "category": "37. Religion"
                            },
                            {
                                "category": "38. Shopping"
                            },
                            {
                                "category": "39. Internet Auctions"
                            },
                            {
                                "category": "40. Real Estate"
                            },
                            {
                                "category": "41. Society and Lifestyle"
                            },
                            {
                                "category": "43. Restaurants and Dining"
                            },
                            {
                                "category": "44. Sports"
                            },
                            {
                                "category": "45. Travel"
                            },
                            {
                                "category": "46. Vehicles"
                            },
                            {
                                "category": "47. Humor/Jokes"
                            },
                            {
                                "category": "48. Multimedia"
                            },
                            {
                                "category": "49. Freeware/Software Downloads"
                            },
                            {
                                "category": "50. Pay to Surf Sites"
                            },
                            {
                                "category": "52. Keyloggers and Monitoring"
                            },
                            {
                                "category": "53. Kid Friendly"
                            },
                            {
                                "category": "54. Advertisement"
                            },
                            {
                                "category": "55. Web Hosting"
                            },
                            {
                                "category": "56. Other"
                            },
                            {
                                "category": "57. Internet Watch Foundation CAIC"
                            },
                            {
                                "category": "58. Social Networking"
                            },
                            {
                                "category": "59. Malware"
                            },
                            {
                                "category": "60. Radicalization and Extremism"
                            },
                            {
                                "category": "61. Hate and Racism"
                            },
                            {
                                "category": "62. Questionable"
                            },
                            {
                                "category": "63. Proxy Avoidance and Anonymizers"
                            },
                            {
                                "category": "64. Not Rated"
                            },
                            {
                                "category": "65. Spyware and Adware"
                            },
                            {
                                "category": "66. Legal"
                            },
                            {
                                "category": "67. Hunting and Fishing"
                            },
                            {
                                "category": "68. Online Greeting Cards"
                            },
                            {
                                "category": "69. Recreation and Hobbies"
                            },
                            {
                                "category": "70. Home and Garden"
                            },
                            {
                                "category": "71. Fashion and Beauty"
                            },
                            {
                                "category": "72. Personal Sites and Blogs"
                            },
                            {
                                "category": "73. Local Information"
                            },
                            {
                                "category": "74. Translation"
                            },
                            {
                                "category": "75. Music"
                            },
                            {
                                "category": "76. Computer and Internet Security"
                            },
                            {
                                "category": "77. Online Personal Storage"
                            },
                            {
                                "category": "78. Content Delivery Networks"
                            },
                            {
                                "category": "79. Image and Video Search"
                            },
                            {
                                "category": "80. Dynamic Content"
                            },
                            {
                                "category": "81. P2P"
                            },
                            {
                                "category": "82. Open HTTP Proxies"
                            },
                            {
                                "category": "83. Marijuana"
                            },
                            {
                                "category": "84. Cheating"
                            },
                            {
                                "category": "85. Gross"
                            },
                            {
                                "category": "86. Phishing and Other Frauds"
                            },
                            {
                                "category": "87. Bot Nets"
                            },
                            {
                                "category": "88. SPAM URLs"
                            },
                            {
                                "category": "91. Parked Domains"
                            },
                            {
                                "category": "92. Dead Sites"
                            },
                            {
                                "category": "93. Private IP Addresses"
                            }
                        ]
                    }
                }
            }
        }



    def show_dpissl_client(self):
        url_base = str(self.url) + '/base'
        dpissl_resp = self.fw.api_get(url_base)
        return dpissl_resp  

    def clear_connection_list(self, msg=False, **kwargs):
        json_input = {"stream": ''}
        json_input['stream'] = kwargs['stream'] 
        res = self.fw.api_post(self.url_raw, msg, data=json_input, headers=self.headers)
        return res  

    def show_connection_failure_list(self):
        dpissl_resp = self.fw.api_get(self.get_common_name_list)
        return dpissl_resp    


    def config_general_settings(self, msg=False, **kwargs):
        self.options = dict(ClientSslApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options

        json_input = self.build_json_general_settings(**kwargs)
        url_base = str(self.url) + '/base'
        sslserver_resp = self.fw.api_put(url_base, msg, data=json_input)
        return sslserver_resp 

    def build_json_general_settings(self, **kwargs):
        json_input = {}
        logger.info(kwargs)

        try:
            json_input = copy.deepcopy(self.initial_general_settings_json)
            json_input['dpi_ssl']['client']['enable'] = kwargs['enable']
            json_input['dpi_ssl']['client']['intrusion_prevention'] = kwargs['intrusion_prevention']
            json_input['dpi_ssl']['client']['application_firewall'] = kwargs['application_firewall']
            json_input['dpi_ssl']['client']['gateway']['anti_virus'] = kwargs['gateway_anti_virus']
            json_input['dpi_ssl']['client']['gateway']['anti_spyware'] = kwargs['gateway_anti_spyware']
            json_input['dpi_ssl']['client']['content_filter'] = kwargs['content_filter']
            json_input['dpi_ssl']['client']['deployment_server_domains'] = kwargs['deployment_server_domains']
            json_input['dpi_ssl']['client']['bypass_decryption'] = kwargs['bypass_decryption']
            json_input['dpi_ssl']['client']['audit_built_in_exclusion'] = kwargs['audit_built_in_exclusion']
            json_input['dpi_ssl']['client']['authenticate_server'] = kwargs['authenticate_server']
            json_input['dpi_ssl']['client']['open_failed_connections'] = kwargs['open_failed_connections']

            if kwargs['authenticate_server_for_decrypted_connections'] is True and "expired_ca" in kwargs.keys():
                json_input['dpi_ssl']['client']['authenticate_server_for_decrypted_connections'] \
                    = kwargs['authenticate_server_for_decrypted_connections']
                json_input['dpi_ssl']['client']['expired_ca'] = kwargs['expired_ca']
            elif kwargs['authenticate_server_for_decrypted_connections'] is True and "expired_ca" not in kwargs.keys():
                logger.error("when authenticate_server_for_decrypted_connections is True,expired_ca should be specified") 
            elif kwargs['authenticate_server_for_decrypted_connections'] is False and "expired_ca" not in kwargs.keys():
                json_input['dpi_ssl']['client']['authenticate_server_for_decrypted_connections'] \
                    = kwargs['authenticate_server_for_decrypted_connections']
            else:  
                logger.error("when authenticate_server_for_decrypted_connections is False,expired_ca shouldn't be specified") 
                
            logger.info(json_input)

        except KeyError:
            logger.error("Error: in creating JSON for dpissl server")
        logger.info(json_input)
        return json_input


    def config_cert(self, msg=False, **kwargs):
        self.options = dict(ClientSslApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options

        default_cert_list = ['2048-bit','none-2048-bit']

        json_input = {}
        json_input = copy.deepcopy(self.initial_certificate_json)
        if kwargs['certificate'] in default_cert_list: 
            json_input['dpi_ssl']['client']["resigning_authority"]['default'] = kwargs['certificate']
        else:
            json_input['dpi_ssl']['client']["resigning_authority"]['certificate'] = kwargs['certificate']
            del json_input['dpi_ssl']['client']["resigning_authority"]['default']
        url_base = str(self.url) + '/base'
        sslserver_resp = self.fw.api_put(url_base, msg, data=json_input)
        return sslserver_resp

    def config_objects(self, msg=False, **kwargs):
        self.options = dict(ClientSslApi.default_options)
        self.options.update(kwargs) 
        kwargs = self.options
        json_input = self.build_json_objects(**kwargs)
        url = self.url + '/base'
        sslclient_resp = self.fw.api_put(url, msg, data=json_input)
        return sslclient_resp

    def build_json_objects(self, **kwargs):
        json_input = {}
        logger.info(kwargs)

        try:
            json_input = copy.deepcopy(self.initial_objects_json)

            address_type_list = ['group', 'all', 'name']
            user_type_list = ['name', 'guest', 'all', 'guests', 'administrator', 'group']
            service_type_list = ['group', 'all', 'name']

            if 'include_address' in kwargs.keys() and 'include_address_type' in kwargs.keys():
                if kwargs['include_address_type'] in address_type_list: 
                    if kwargs['include_address_type'] != 'all':
                        json_input['dpi_ssl']['client']['include']['address'][kwargs['include_address_type']] \
                            = kwargs['include_address']
                        del json_input['dpi_ssl']['client']['include']['address']['all']
                    else:
                        pass
                else:
                    logger.error('dpissl client include address type error')
                    return False
            elif 'include_address' not in kwargs.keys() and 'include_address_type' in kwargs.keys():
                logger.error('Please specify dpissl client include_address.')
            elif 'include_address' in kwargs.keys() and 'include_address_type' not in kwargs.keys():
                logger.error('Please specify dpissl client include_address_type.')
            else:
                logger.info('include_address_type is all,include_address is True by default')

            if 'include_user' in kwargs.keys() and 'include_user_type' in kwargs.keys():
                if kwargs['include_user_type'] in user_type_list:
                    if kwargs['include_user_type'] != 'all':
                        json_input['dpi_ssl']['client']['include']['user'][kwargs['include_user_type']] \
                            = kwargs['include_user']
                        del json_input['dpi_ssl']['client']['include']['user']['all']
                    else:
                        pass
                else:
                    logger.error('include_user_type error')
                    return False
            elif 'include_user' not in kwargs.keys() and 'include_user_type' in kwargs.keys():
                logger.error('Please specify include_user.')
            elif 'include_user' in kwargs.keys() and 'include_user_type'not in kwargs.keys():
                logger.error('Please specify include_user_type.')
            else:
                logger.info('include_user_type is all,include_user is True by default')

            if 'include_service' in kwargs.keys() and 'include_service_type' in kwargs.keys():
                if kwargs['include_service_type'] in service_type_list:
                    if kwargs['include_service_type'] != 'all':
                        json_input['dpi_ssl']['client']['include']['service'][kwargs['include_service_type']] \
                            = kwargs['include_service']
                        del json_input['dpi_ssl']['client']['include']['service']['all']
                    else:
                        pass
                else:
                    logger.error('include service type error')
                    return False
            elif 'include_service' not in kwargs.keys() and 'include_service_type' in kwargs.keys():
                logger.error('Please specify include_service.')
            elif 'include_service' in kwargs.keys() and 'include_service_type'not in kwargs.keys():
                logger.error('Please specify include_service_type.')
            else:
                logger.info('include_service_type is all,include_service is True by default')

            if 'exclude_address' in kwargs.keys() and 'exclude_address_type' in kwargs.keys():
                if kwargs['exclude_address_type'] in address_type_list:
                    json_input['dpi_ssl']['client']['exclude']['address'][kwargs['exclude_address_type']] \
                        = kwargs['exclude_address']
                else:
                    if kwargs['exclude_address_type'] is None:
                        json_input['dpi_ssl']['client']['exclude']['address'] = {}
                    else:
                        logger.error('exclude_address_type error')
                        return False
            elif 'exclude_address_type' not in kwargs.keys() and 'exclude_address' in kwargs.keys():
                logger.error('Please specify exclude_address_type.')
            elif 'exclude_address_type' in kwargs.keys() and 'exclude_address' not in kwargs.keys():
                logger.error('Please specify exclude_address.')
            else:
                logger.info('exclude_address is None,exclude_address_type is None by default')

            if 'exclude_user' in kwargs.keys() and 'exclude_user_type' in kwargs.keys():
                if kwargs['exclude_user_type'] in user_type_list:
                    json_input['dpi_ssl']['client']['exclude']['user'][kwargs['exclude_user_type']] \
                        = kwargs['exclude_user']
                else:
                    if kwargs['exclude_user_type'] is None:
                        json_input['dpi_ssl']['client']['exclude']['user'] = {}
                    else:
                        logger.error('exclude_user_type error')
                        return False
            elif 'exclude_user' not in kwargs.keys() and 'exclude_user_type' in kwargs.keys():
                logger.error('Please specify exclude_user.')
            elif 'exclude_user' in kwargs.keys() and 'exclude_user_type' not in kwargs.keys():
                logger.error('Please specify exclude_user_type.')
            else:
                logger.info('exclude_user_type is None,exclude_user is None by default')

            if 'exclude_service' in kwargs.keys() and 'exclude_service_type' in kwargs.keys():
                if kwargs['exclude_service_type'] in service_type_list:
                    json_input['dpi_ssl']['client']['exclude']['service'][kwargs['exclude_service_type']] \
                        = kwargs['exclude_service']
                else:
                    if kwargs['exclude_service_type'] is None:
                        json_input['dpi_ssl']['client']['exclude']['service'] = {}
                    else:
                        logger.error('exclude_service_type error')
                        return False
            elif 'exclude_service' not in kwargs.keys() and 'exclude_service_type' in kwargs.keys():
                logger.error('Please specify exclude_service.')
            elif 'exclude_service' in kwargs.keys() and 'exclude_service_type' not in kwargs.keys():
                logger.error('Please specify exclude_service_type.')
            else:
                logger.info('exclude_service_type is None,exclude_service is None by default')

            json_input['dpi_ssl']['client']['exclude']['cfs_category_unavailable'] = kwargs['cfs_category_unavailable']
        
        except KeyError:
            logger.error("Error: in creating JSON for dpissl client objects")
        logger.info(json_input)
        return json_input

    def add_common_name(self, msg=False, **kwargs):
        self.options = dict(ClientSslApi.default_options)
        self.options.update(kwargs) 
        kwargs = self.options
        json_input = self.build_json_add_common_name(**kwargs)
        sslclient_resp = self.fw.api_post(self.url_common, msg, data=json_input)
        return sslclient_resp

    def delete_common_name(self, msg=False, **kwargs):
        self.options = dict(ClientSslApi.default_options)
        self.options.update(kwargs) 
        kwargs = self.options
        json_input = self.build_json_add_common_name(**kwargs)
        sslclient_resp = self.fw.api_delete(self.url_common, msg, data=json_input)
        return sslclient_resp

#########################################currently not support on our dut 
#    def edit_common_name(self, msg=False, **kwargs):
#        self.options = dict(ClientSslApi.default_options)
#        self.options.update(kwargs) 
#        kwargs = self.options
#        json_input = self.build_json_edit_common_name(**kwargs)
#        sslclient_resp = self.fw.api_put(self.url, msg, data=json_input)
#        return sslclient_resp
#
#    def build_json_edit_common_name(self, **kwargs):
#        json_input = {}
#        logger.info(kwargs)
#
#        try:
#            json_input = copy.deepcopy(self.initial_common_name_json)
#            action_type_list = ['skip_content_filter_exclusion','skip_authentication','exclude']
#            exclude_list = ['disable_authenticate_server','authenticate_server']
#            if 'common_name_action_new' in kwargs.keys(): 
#                if kwargs['common_name_action_new'] in action_type_list: 
#                    if kwargs['common_name_action_new'] is not 'exclude':
#                        json_input['dpi_ssl']['client']['common_name'][0]['cName'] = kwargs['common_name']
#                        json_input['dpi_ssl']['client']['common_name'][0]['action'][kwargs['common_name_action_new']] = True
#                        del json_input['dpi_ssl']['client']['common_name'][0]['action']['exclude']
#                    else:
#                        if 'exclude_type_new' in kwargs.keys() and kwargs['exclude_type_new'] in exclude_list:
#                            json_input['dpi_ssl']['client']['common_name'][0]['cName'] = kwargs['common_name']
#                            json_input['dpi_ssl']['client']['common_name'][0]['action'][kwargs['common_name_action_new']][kwargs['exclude_type_new']] = True
#                        else:
#                            logger.error('when new common name action is exclude,please specify exclude type also')
#                else:
#                    logger.error('dpissl client new common name action is incorrect')
#                    return False
#            else:
#                logger.error('common_name should be specified when try to edit common name entry')
#
#        except KeyError:
#            logger.error("Error: in creating JSON for dpissl client edit common name")
#        logger.info(json_input)
#        return json_input
#########################################################################
    def build_json_add_common_name(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_common_name_json)

            action_type_list = ['skip_content_filter_exclusion','skip_authentication','exclude']
            exclude_list = ['disable_authenticate_server','authenticate_server']
            if 'common_name' in kwargs.keys(): 
                if kwargs['common_name_action'] in action_type_list: 
                    if kwargs['common_name_action'] is not 'exclude':
                        json_input['dpi_ssl']['client']['common_name'][0]['cName'] = kwargs['common_name']
                        json_input['dpi_ssl']['client']['common_name'][0]['action'][kwargs['common_name_action']] = True
                        del json_input['dpi_ssl']['client']['common_name'][0]['action']['exclude']
                    else:
                        if 'exclude_type' in kwargs.keys() and kwargs['exclude_type'] in exclude_list:
                            json_input['dpi_ssl']['client']['common_name'][0]['cName'] = kwargs['common_name']
                            json_input['dpi_ssl']['client']['common_name'][0]['action'][kwargs['common_name_action']][kwargs['exclude_type']] = True
                        else:
                            logger.error('when common name action is exclude,please specify exclude type also')
                else:
                    logger.error('dpissl client common name action is incorrect')
                    return False
            elif 'common_name' not in kwargs.keys() and 'common_name_action' in kwargs.keys():
                logger.error('Please specify common_name.')
            elif 'common_name' in kwargs.keys() and 'common_name_action' not in kwargs.keys():
                logger.error('Please specify common_name_action.')
            else:
                logger.info('common_name is test1 and common_name_action is skip_content_filter_exclusion by default')

        except KeyError:
            logger.error("Error: in creating JSON for dpissl client common name")
        logger.info(json_input)
        return json_input

    def get_sslclient_config(self, msg=False, ip='192.168.168.168'):
        client_url_base = self.url + '/base'
        response = self.fw.api_get(client_url_base)
        return response

    def del_all_common_names(self, msg=False):
        client_details = self.get_sslclient_config()
        sslclient_resp = self.fw.api_delete(self.url, msg, data=client_details)
        return sslclient_resp

    def select_all_cfs_categories(self, msg=False):
        json_input = self.categories
        logger.info(json_input)
        sslclient_resp = self.fw.api_post(self.url_category, msg, data=json_input)
        return sslclient_resp

    def config_category_based_exclusion_inclusion_exclude_include(self, msg=False, **kwargs):
        logger.info('=============')
        logger.info(kwargs)
        json_input = self.build_json_cfs_category(**kwargs)
        logger.info(json_input)
        sslclient_resp = self.fw.api_put(self.url+'/base', msg, data=json_input)
        return sslclient_resp
    
    def delete_some_cfs_categories(self, msg=False, **kwargs):
        all_categories = {"dpi_ssl":{"client":{"cfs_categories":{"category":[{"category":"all"}]}}}}
        self.fw.api_delete(self.url_category, msg, data=all_categories)
        input_json = self.categories
        categories = input_json['dpi_ssl']['client']['cfs_categories']['category']
        for i in range(len(kwargs['category'])): 
            categories = [item for item in categories if item['category'] != kwargs['category'][i]]
        input_json['dpi_ssl']['client']['cfs_categories']['category'] = categories
        resp = self.fw.api_post(self.url_category, msg, data=input_json)
        return resp
    
    def cfs_category_based_exclusion_inclusion(self, msg=False, **kwargs):
        self.options = dict(ClientSslApi.default_options)
        self.options.update(kwargs) 
        kwargs = self.options
        json_input = self.build_json_cfs_category(**kwargs)
        logger.info(json_input)
        sslclient_resp = self.fw.api_post(self.url_category, msg, data=json_input)
        return sslclient_resp

    def build_json_cfs_category(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_cfs_category_based_exclusion_inclusion)
            if 'selected' in kwargs.keys():
                if kwargs['selected'] is 'include':
                    json_input['dpi_ssl']['client']['cfs_categories'][kwargs['selected']] = True
                    del json_input['dpi_ssl']['client']['cfs_categories']['exclude']
                elif kwargs['selected'] is 'exclude':   
                    json_input['dpi_ssl']['client']['cfs_categories'][kwargs['selected']] = True
                    del json_input['dpi_ssl']['client']['cfs_categories']['include']
                else:
                    logger.error("cfs_category_based_exclusion_inclusion selected value error") 
            else:
                logger.info('Please specify selected value')

            if 'category' in kwargs.keys():
                if kwargs['category'] is ['all']:
                    json_input['dpi_ssl']['client']['cfs_categories']['category'].append({'category':'all'})
                else:
                    for c in kwargs['category']:
                        json_input['dpi_ssl']['client']['cfs_categories']['category'].append({"category": c})
            else:
                logger.info("When category is empty,no option is selected")
                del json_input['dpi_ssl']['client']['cfs_categories']['category']

        except KeyError:
            logger.info(json_input)
            logger.error("Error: in creating JSON for dpissl client common name")
        logger.info(json_input)
        return json_input
        
    def add_dpissl_client_category(self, name):
        dpissl_client_category = {
             "dpi_ssl": {
                 "client": {
                     "cfs_categories": {
                         "category": [
                             {
                                 "category": name   # "1. Violence/Hate/Racism"
                             }
                         ]
                     }
                 }
             }
        }
        response = self.fw.api_post(self.url_category, data=dpissl_client_category)
        return response

    def get_dpissl_client_category(self):
        response = self.fw.api_get(self.url_category)
        return response
    
    def add_dpissl_cfs_category(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        post_response = self.fw.api_post(self.url_category, msg, data=json_input)
        return post_response

    def get_common_name(self):
        common_url = 'api/sonicos/dynamic-file/getDPISSLCNArray.json'
        response = self.fw.api_get(common_url)
        return response

    def config_cfs_category_based_exclusion_inclusion(self, msg=False, **kwargs):
        self.options = dict(ClientSslApi.default_options)
        self.options.update(kwargs) 
        kwargs = self.options
        json_input = self.build_json_cfs_category(**kwargs)
        logger.info(json_input)
        sslclient_resp = self.fw.api_delete(self.url_category, msg, data=json_input)
        return sslclient_resp
    
    def delete_dpissl_cfs_category(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        post_response = self.fw.api_delete(self.url_category, msg, data=json_input)
        return post_response

    def get_status(self):
        url = 'api/sonicos/dynamic-file/getDPISSLStatus.json'
        response = self.fw.api_get(url)
        return response
