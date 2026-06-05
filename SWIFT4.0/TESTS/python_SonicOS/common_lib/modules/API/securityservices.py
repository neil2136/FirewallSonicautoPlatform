import copy
import json
import sys
from runner.settings import logger

class SecurityServicesSummary:
    default_values = {
        'security': 'performance-optimized',
        'reduce_isdn_antivirus_traffic': False,
        'drop_packets_at_reload': False,
        'http_clientless_notification_timeout': 86400,
        'enable': None

    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/security-services/base'
        self.initial_json_base_setting = {
                'security_services': {
                'security': 'performance-optimized',
                'reduce_isdn_antivirus_traffic': False,
                'drop_packets_at_reload': False,
                'http_clientless_notification_timeout': 86400,
                'proxy_server': {
                    'enable': False,
                    'host': '',
                    'port': 0,
                    'authentication': {
                        'enable': False,
                        'user_name': '',
                        'password': ''
                    }
                }
            }
        }


    def build_json_base_setting(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_base_setting)
        logger.info(json_input)

        try:

            if 'security' in kwargs.keys():
                json_input['security_services']['security'] = kwargs['security']
            if 'reduce_isdn_antivirus_traffic' in kwargs.keys():
                json_input['security_services']['reduce_isdn_antivirus_traffic'] = kwargs['reduce_isdn_antivirus_traffic']
            if 'drop_packets_at_reload' in kwargs.keys():
                json_input['security_services']['drop_packets_at_reload'] = kwargs['drop_packets_at_reload']
            if 'http_clientless_notification_timeout' in kwargs.keys():
                json_input['security_services']['http_clientless_notification_timeout'] = kwargs['http_clientless_notification_timeout']
            json_input['security_services']['proxy_server']['enable'] = kwargs['proxy_enable']
            if (kwargs['proxy_enable'] == True):
                json_input['security_services']['proxy_server']['host'] = kwargs['host']
                json_input['security_services']['proxy_server']['port'] = kwargs['port']
                json_input['security_services']['proxy_server']['authentication']['enable'] = kwargs['enable_auth']
                if (kwargs['enable_auth'] == True):
                    json_input['security_services']['proxy_server']['authentication']['user_name'] = kwargs['user_name']
                    json_input['security_services']['proxy_server']['authentication']['password'] = kwargs['password']
                else:
                    logger.info('Please enable the proxy server')
            else:
                logger.error('Error: While creating base setting')
        except KeyError:
            logger.error('Error: in creating JSON for security services settings')
        return json_input

    def get_security_services_base(self):
        get_response = self.fw.api_get(self.url)
        return get_response

    def configure_services_base(self, msg=False, **kwargs):
        self.options = dict(SecurityServicesSummary.default_values)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_base_setting(**kwargs)
        logger.info('The json input build is', json_input)
        securityservices_base_response = self.fw.api_put(self.url, msg, data=json_input)
        return securityservices_base_response


class ClientEnforcementAPI:
    default_values = {
        'policing': False,
        'interval': 5,
        'low': False,
        'medium': True,
        'high': True,

    }

    def __init__(self, fw):
        self.fw = fw
        self.url = '/api/sonicos/client-enforcement/anti-virus/policy'
        self.initial_json_clientEnforcement = {
            'client_enforcement': {
                'anti_virus': {
                    'policing': False,
                    'force': {
                        'interval': 5,
                        'update': {
                            'low': False,
                            'medium': True,
                            'high': True
                        }
                    }
                }
            }
        }

    def build_json_clientEnforcement(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_clientEnforcement)

        try:

            json_input['client_enforcement']['anti_virus']['policing'] = kwargs['policing']
            json_input['client_enforcement']['anti_virus']['force']['interval'] = kwargs['interval']
            json_input['client_enforcement']['anti_virus']['force']['update']['low'] = kwargs['low']
            json_input['client_enforcement']['anti_virus']['force']['update']['medium'] = kwargs['medium']
            json_input['client_enforcement']['anti_virus']['force']['update']['high'] = kwargs['high']

        except KeyError:
            logger.error('Error: in creating JSON for client-enforcement settings')
        logger.info(json_input)

        return json_input

    def get_clientenforcement(self):
        get_response = self.fw.api_get_response(self.url)
        return get_response

    def edit_clientenforcement_setting(self, msg=False, **kwargs):
        self.options = dict(ClientEnforcementAPI.default_values)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_clientEnforcement(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        clientenforcement_response = self.fw.api_put(self.url, msg, data=json_input)
        return clientenforcement_response


class CFS_Enforcement:
    default_values = {
        'client_enforcement': None,
        'content_filtering': None,
        'grace_period': 5,
        'default_enforcement': None

    }

    def __init__(self, fw):
        self.fw = fw
        self.url = '/api/sonicos/client-enforcement/content-filtering'
        self.initial_json_CFS_Enforcement = {
            'client_enforcement': {
                'content_filtering': {
                    'grace_period': 5,
                    'default_enforcement': 'none'
                }
            }
        }

    def build_json_CFS_Enforcement(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_CFS_Enforcement)
        try:

            json_input['client_enforcement']['content_filtering']['grace_period'] = kwargs['grace_period']
            if 'enforcement_default' in kwargs.keys():
                json_input['client_enforcement']['content_filtering']['grace_period'] = kwargs['enforcement_default']
                if 'enforcement_list_inclusion' in kwargs.keys():
                    json_input['client_enforcement']['content_filtering']['enforcement_list']['inclusion']['group'] = \
                    kwargs['enforcement_list_inclusion']
                if 'enforcement_list_exclusion' in kwargs.keys():
                    json_input['client_enforcement']['content_filtering']['enforcement_list']['exclusion']['group'] = \
                    kwargs['enforcement_list_exclusion']

            elif 'enforcement_client_cf' in kwargs.keys():
                json_input['client_enforcement']['content_filtering']['grace_period'] = kwargs['enforcement_client_cf']
                if 'enforcement_list_inclusion' in kwargs.keys():
                    json_input['client_enforcement']['content_filtering']['enforcement_list']['inclusion']['group'] = \
                    kwargs['enforcement_list_inclusion']
                if 'enforcement_list_exclusion' in kwargs.keys():
                    json_input['client_enforcement']['content_filtering']['enforcement_list']['exclusion']['group'] = \
                    kwargs['enforcement_list_exclusion']


        except KeyError:
            logger.error('Error: in creating JSON for SSLVPN Server settings')
            logger.info(json_input)


        return json_input

    def get_cfs_enforcement(self):
        get_response = self.fw.api_get_response(self.url)
        return get_response

    def configure_cfs_enforcement(self, msg=False, **kwargs):
        self.options = dict(CFS_Enforcement.default_values)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_CFS_Enforcement(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        cfs_enforcement_resp = self.fw.api_post(self.url, msg, data=json_input)
        return cfs_enforcement_resp


class GAV:
    default_values = {
        'enable': False,
        'inbound_inspection': {
            'http': True,
            'ftp': True,
            'imap': True,
            'smtp': True,
            'pop3': True,
            'cifs_netbios': False,
            'tcp_stream': False
        },
        'outbound_inspection': {
            'http': False,
            'ftp': False,
            'smtp': False,
            'tcp_stream': False
        },
        'restrict': {
            'password_protected_zip': {
                'http': False,
                'ftp': False,
                'imap': True,
                'smtp': True,
                'pop3': True,
                'cifs_netbios': False
            },
            'packed_executables': {
                'http': False,
                'ftp': False,
                'imap': True,
                'smtp': True,
                'pop3': True,
                'cifs_netbios': False
            },
            'ms_office_macros': {
                'http': False,
                'ftp': False,
                'imap': True,
                'smtp': True,
                'pop3': True,
                'cifs_netbios': False
            }
        },
        'exclusion_object': {
            'http': {},
            'ftp': {},
            'imap': {},
            'smtp': {},
            'pop3': {},
            'cifs_netbios': {}
        },
        'smtp_responses': True,
        'eicar_detection': False,
        'ftp_rest': True,
        'http_byte_range': True,
        'http_clientless_notification': True,
        'scan_high_compression': False,
        'block_multiple_compress_files': False,
        'detection_only': False,
        'notification_message': 'This request is blocked by the Firewall Gateway Anti-Virus Service.',
        # 'cloud': {}
    }
    default_values_exclusionlist_base = {
        'list': True,
        'address': 'None',
        'name': 'None'
    }

    default_values_exclusionlist_entries = {
        'from': 'None',
        'to': 'None'
    }

    default_gav_cloud = {
        'anti_virus_database': False
    }

    default_cloud_exclusion = {
        'id': ['None']
    }

    def __init__(self, fw):
        self.fw = fw
        self.gav_url = 'api/sonicos/gateway-antivirus/base'
        self.gav_exclusionlist_baseurl = 'api/sonicos/gateway-antivirus/exclusion-list/base'
        self.gav_exclusionlist_entriesurl = 'api/sonicos/gateway-antivirus/exclusion-list/entries'
        self.gav_cloud_url = 'api/sonicos/gateway-antivirus/cloud/base'
        self.cloud_exclusion = 'api/sonicos/gateway-antivirus/cloud/exclusions'
        self.gav_reset = 'api/sonicos/gateway-antivirus/reset-settings'
        self.gav_status = 'api/sonicos/reporting/gateway-antivirus'

        self.initial_json_GAV = {
            'gateway_antivirus': {
                'enable': False,
                'inbound_inspection': {
                    'http': True,
                    'ftp': True,
                    'imap': True,
                    'smtp': True,
                    'pop3': True,
                    'cifs_netbios': False,
                    'tcp_stream': False
                },
                'outbound_inspection': {
                    'http': False,
                    'ftp': False,
                    'smtp': False,
                    'tcp_stream': False
                },
                'restrict': {
                    'password_protected_zip': {
                        'http': False,
                        'ftp': False,
                        'imap': True,
                        'smtp': True,
                        'pop3': True,
                        'cifs_netbios': False
                    },
                    'packed_executables': {
                        'http': False,
                        'ftp': False,
                        'imap': True,
                        'smtp': True,
                        'pop3': True,
                        'cifs_netbios': False
                    },
                    'ms_office_macros': {
                        'http': False,
                        'ftp': False,
                        'imap': True,
                        'smtp': True,
                        'pop3': True,
                        'cifs_netbios': False
                    }
                },
                'exclusion_object': {
                    'http': {},
                    'ftp': {},
                    'imap': {},
                    'smtp': {},
                    'pop3': {},
                    'cifs_netbios': {}
                },
                'smtp_responses': True,
                'eicar_detection': False,
                'ftp_rest': True,
                'http_byte_range': True,
                'http_clientless_notification': True,
                'scan_high_compression': False,
                'block_multiple_compress_files': False,
                'detection_only': False,
                'notification_message': 'This request is blocked by the Firewall Gateway Anti-Virus Service.',
                # 'cloud': {}
            }
        }

        self.initial_json_exclusionlist_base = {
            'gateway_antivirus': {
                'exclusion': {
                    'list': True,
                    'address': 'None',
                    'name': 'None',
                    'group': 'None'

                }
            }
        }
        self.initial_json_exclusionlist_entries = {
            'gateway_antivirus': {
                'exclusion': {
                    'entry': [
                        {
                            'from': 'None',
                            'to': 'None'
                        }
                    ]
                }
            }
        }
        self.initial_gav_cloud = {
            "gateway_antivirus": {
                "cloud": {
                    "anti_virus_database": False
                }
            }
        }

        self.initial_cloud_exclusion = {
            "gateway_antivirus": {

                "cloud": {
                    "exclusion": [
                        {'id': 'None'}

                    ]
                }
            }
        }

        self.initial_signatures = {
            "gateway_antivirus": {
                "signature": [
                    {
                        "enable": False,
                        "id": 'None',
                    }
                ]
            }
        }

    def get_GAV_signatures(self):
        url = 'api/sonicos/gateway-antivirus/signatures'
        resp = self.fw.api_get(url)
        return resp

    def build_json_GAV(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_GAV)
        logger.info(json_input)

        try:
            if 'enable_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['enable'] = kwargs['enable_GAV']
            if 'inbound_http' in kwargs.keys():
                json_input['gateway_antivirus']['inbound_inspection']['http'] = kwargs['inbound_http']
            if 'inbound_ftp' in kwargs.keys():
                json_input['gateway_antivirus']['inbound_inspection']['ftp'] = kwargs['inbound_ftp']
            if 'inbound_imap' in kwargs.keys():
                json_input['gateway_antivirus']['inbound_inspection']['imap'] = kwargs['inbound_imap']
            if 'inbound_smtp' in kwargs.keys():
                json_input['gateway_antivirus']['inbound_inspection']['smtp'] = kwargs['inbound_smtp']
            if 'inbound_pop3' in kwargs.keys():
                json_input['gateway_antivirus']['inbound_inspection']['pop3'] = kwargs['inbound_pop3']
            if 'inbound_cifs_netbios' in kwargs.keys():
                json_input['gateway_antivirus']['inbound_inspection']['cifs_netbios'] = kwargs['inbound_cifs_netbios']
            if 'inbound_tcp_stream' in kwargs.keys():
                json_input['gateway_antivirus']['inbound_inspection']['tcp_stream'] = kwargs['inbound_tcp_stream']
            if 'outbound_http' in kwargs.keys():
                json_input['gateway_antivirus']['outbound_inspection']['http'] = kwargs['outbound_http']
            if 'outbound_ftp' in kwargs.keys():
                json_input['gateway_antivirus']['outbound_inspection']['ftp'] = kwargs['outbound_ftp']
            if 'outbound_smtp' in kwargs.keys():
                json_input['gateway_antivirus']['outbound_inspection']['smtp'] = kwargs['outbound_smtp']
            if 'outbound_tcp_stream' in kwargs.keys():
                json_input['gateway_antivirus']['outbound_inspection']['tcp_stream'] = kwargs['outbound_tcp_stream']
            if 'password_protected_zip_http' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['password_protected_zip']['http'] = kwargs[
                    'password_protected_zip_http']
            if 'password_protected_zip_ftp' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['password_protected_zip']['ftp'] = kwargs[
                    'password_protected_zip_ftp']
            if 'password_protected_zip_imap' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['password_protected_zip']['imap'] = kwargs[
                    'password_protected_zip_imap']
            if 'password_protected_zip_smtp' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['password_protected_zip']['smtp'] = kwargs[
                    'password_protected_zip_smtp']
            if 'password_protected_zip_pop3' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['password_protected_zip']['pop3'] = kwargs[
                    'password_protected_zip_pop3']
            if 'password_protected_zip_cifs_netbios' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['password_protected_zip']['cifs_netbios'] = kwargs[
                    'password_protected_zip_cifs_netbios']
            if 'packed_executables_http' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['packed_executables']['http'] = kwargs[
                    'packed_executables_http']
            if 'packed_executables_ftp' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['packed_executables']['ftp'] = kwargs[
                    'packed_executables_ftp']
            if 'packed_executables_imap' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['packed_executables']['imap'] = kwargs[
                    'packed_executables_imap']
            if 'packed_executables_smtp' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['packed_executables']['smtp'] = kwargs[
                    'packed_executables_smtp']
            if 'packed_executables_pop3' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['packed_executables']['pop3'] = kwargs[
                    'packed_executables_pop3']
            if 'packed_executables_cifs_netbios' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['packed_executables']['cifs_netbios'] = kwargs[
                    'packed_executables_cifs_netbios']
            if 'ms_office_macros_http' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['ms_office_macros']['http'] = kwargs[
                    'ms_office_macros_http']
            if 'ms_office_macros_ftp' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['ms_office_macros']['ftp'] = kwargs['ms_office_macros_ftp']
            if 'ms_office_macros_imap' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['ms_office_macros']['imap'] = kwargs[
                    'ms_office_macros_imap']
            if 'ms_office_macros_smtp' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['ms_office_macros']['smtp'] = kwargs[
                    'ms_office_macros_smtp']
            if 'ms_office_macros_pop3' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['ms_office_macros']['pop3'] = kwargs[
                    'ms_office_macros_pop3']
            if 'ms_office_macros_cifs_netbios' in kwargs.keys():
                json_input['gateway_antivirus']['restrict']['ms_office_macros']['cifs_netbios'] = kwargs[
                    'ms_office_macros_cifs_netbios']
            if 'exclusion_object_http' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion_object']['http'] = kwargs['exclusion_object_http']
            if 'exclusion_object_ftp' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion_object']['ftp'] = kwargs['exclusion_object_ftp']
            if 'exclusion_object_imap' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion_object']['imap'] = kwargs['exclusion_object_imap']
            if 'exclusion_object_smtp' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion_object']['smtp'] = kwargs['exclusion_object_smtp']
            if 'exclusion_object_pop3' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion_object']['pop3'] = kwargs['exclusion_object_pop3']
            if 'exclusion_object_cifs_netbios' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion_object']['cifs_netbios'] = kwargs[
                    'exclusion_object_cifs_netbios']
            if 'smtp_response_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['smtp_responses'] = kwargs['smtp_response_GAV']
            if 'eicar_detection_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['eicar_detection'] = kwargs['eicar_detection_GAV']
            if 'ftp_rest_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['ftp_rest'] = kwargs['ftp_rest_GAV']
            if 'http_byte_range_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['http_byte_range'] = kwargs['http_byte_range_GAV']
            if 'http_clientless_notification_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['http_clientless_notification'] = kwargs[
                    'http_clientless_notification_GAV']
            if 'scan_high_compression_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['scan_high_compression'] = kwargs['scan_high_compression_GAV']
            if 'block_multiple_compress_files_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['block_multiple_compress_files'] = kwargs[
                    'block_multiple_compress_files_GAV']
            if 'detection_only_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['detection_only'] = kwargs['detection_only_GAV']
            if 'notification_message_GAV' in kwargs.keys():
                json_input['gateway_antivirus']['notification_message'] = kwargs['notification_message_GAV']
           

            # json_input['gateway_antivirus']['cloud'] = kwargs['cloud_GAV']
        except KeyError:
            logger.info('Error: in creating JSON for GAV base settings')

        return json_input

    def build_json_GAV_exclusionlist_base(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_exclusionlist_base)
        logger.info(json_input)

        try:
            json_input['gateway_antivirus']['exclusion']['list'] = kwargs['list']
            if 'address' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion']['address'] = kwargs['address']
            if 'group' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion']['group'] = kwargs['group']
                del json_input['gateway_antivirus']['exclusion']['name']
            elif 'name' in kwargs.keys():
                json_input['gateway_antivirus']['exclusion']['name'] = kwargs['name']
                del json_input['gateway_antivirus']['exclusion']['group']
            else:
                raise KeyError
        except KeyError as ke:
            logger.info('Error: in creating JSON for GAV exclusion list settings')

        return json_input

    def build_json_GAV_exclusionlist_entries(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_exclusionlist_entries)
        logger.info(json_input)
        try:
            json_input['gateway_antivirus']['exclusion']['entry'][0]['from'] = kwargs['from']
            json_input['gateway_antivirus']['exclusion']['entry'][0]['to'] = kwargs['to']

        except KeyError as ke:
            logger.info('Error: in creating JSON for GAV exclusion entries')

        return json_input

    def build_json_GAV_cloud(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_gav_cloud)
        logger.info(json_input)
        try:
            json_input['gateway_antivirus']['cloud']['anti_virus_database'] = kwargs['anti_virus_database']

        except KeyError as ke:
            logger.info('Error: in creating JSON for GAV cloud antivirus entries')
        return json_input

    def build_json_cloud_exclusion(self, **kwargs):
        json_input = {}
        id_list = []
        json_input = copy.deepcopy(self.initial_cloud_exclusion)
        logger.info(json_input)
        try:
            if 'id' in kwargs.keys():
                for id_name in kwargs['id']:  # append the ids_list as its in the form of array
                    id_gt = {'id': id_name}
                    id_list.append(id_gt)
                    print(id_list)
                    logger.info('The appended id_list: {}'.format(id_list))
                json_input['gateway_antivirus']['cloud']['exclusion'][0] = id_list
                logger.info(json_input)

        except KeyError as ke:
            logger.info('Error: in creating JSON for GAV cloud antivirus entries id')
        return json_input

    def get_GAV_base(self):
        get_response = self.fw.api_get(self.gav_url)
        return get_response
        
    def update_GAV_signature_database_timestamp(self, msg=False):
        url = 'api/sonicos/gateway-antivirus/update-signatures'
        resp = self.fw.api_post(url, msg)
        return resp

    def update_GAV_signatures(self,**kwargs):
        url = 'api/sonicos/gateway-antivirus/signatures'
        json_input = {}
        json_input = copy.deepcopy(self.initial_signatures)
        logger.info(json_input)
        try:
            if 'id' in kwargs.keys():
                json_input['gateway_antivirus']['signature'][0]['id'] = kwargs['id']
                logger.info(json_input)
        except KeyError as ke:
            logger.info('Error: in creating JSON for GAV cloud antivirus entries id')
        resp = self.fw.api_put(url, json_input, data=json_input)
        return resp

    def get_GAV_status(self):
        get_response = self.fw.api_get(self.gav_status)
        return get_response

    def config_gav(self, msg=False, url=None, **kwargs):
        self.options = dict(GAV.default_values)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_GAV(**kwargs)
        logger.info(json_input)
        GAV_resp = self.fw.api_put(self.gav_url, msg, data=json_input)
        return GAV_resp

    def get_GAV_exclusionlist_base(self):
        get_response = self.fw.api_get(self.gav_exclusionlist_baseurl)
        return get_response

    def config_GAV_exclusionlist_base(self, msg=False, url=None, **kwargs):
        self.options = dict(GAV.default_values_exclusionlist_base)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_GAV_exclusionlist_base(**kwargs)
        logger.info(json_input)
        GAV_resp = self.fw.api_put(self.gav_exclusionlist_baseurl, msg, data=json_input)
        return GAV_resp

    def get_GAV_exclusionlist_entries(self):
        get_response = self.fw.api_get(self.gav_exclusionlist_entriesurl)
        return get_response

    def config_GAV_exclusionlist_entries(self, msg=False, url=None, **kwargs):
        self.options = dict(GAV.default_values_exclusionlist_entries)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_GAV_exclusionlist_entries(**kwargs)
        logger.info(json_input)
        GAV_resp = self.fw.api_put(self.gav_exclusionlist_entriesurl, msg, data=json_input)
        return GAV_resp

    def get_GAV_cloud_base(self):
        get_response = self.fw.api_get(self.gav_cloud_url)
        return get_response

    def config_GAV_cloud_base(self, msg=False, url=None, **kwargs):
        self.options = dict(GAV.default_gav_cloud)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_GAV_cloud(**kwargs)
        logger.info(json_input)
        cloud_resp = self.fw.api_put(self.gav_cloud_url, msg, data=json_input)
        return cloud_resp

    def get_GAV_cloud_exclusion(self):
        get_response = self.fw.api_get(self.cloud_exclusion)
        return get_response

    def config_GAV_cloud_exclusion(self, msg=False, url=None, **kwargs):
        self.options = dict(GAV.default_cloud_exclusion)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cloud_exclusion(**kwargs)
        logger.info("The final json is")
        logger.info(json_input)
        cloud_resp = self.fw.api_post(self.cloud_exclusion, msg, data=json_input)
        return cloud_resp

    def update_GAV_cloud_exclusion(self, msg=False, url=None, **kwargs):
        self.options = dict(GAV.default_cloud_exclusion)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cloud_exclusion(**kwargs)
        logger.info("The final json is")
        logger.info(json_input)
        cloud_resp = self.fw.api_put(self.cloud_exclusion, msg, data=json_input)
        return cloud_resp

    def delete_GAV_cloud_exclusion(self, msg=False, url=None, **kwargs):
        self.options = dict(GAV.default_cloud_exclusion)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cloud_exclusion(**kwargs)
        logger.info(json_input)
        cloud_resp = self.fw.api_delete(self.cloud_exclusion, msg, data=json_input)
        return cloud_resp

    def delete_GAV_exclusionlist_entries(self, msg=False, url=None, **kwargs):
        self.options = dict(GAV.default_values_exclusionlist_entries)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_GAV_exclusionlist_entries(**kwargs)
        logger.info(json_input)
        GAV_resp = self.fw.api_delete(self.gav_exclusionlist_entriesurl, msg, data=json_input)
        return GAV_resp

    def reset_Gav(self):
        reset_resp = self.fw.api_post(self.gav_reset)
        return reset_resp


class AntiSpywareApi:
    '''AntiSpywareApi class'''
	
    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/anti-spyware/base'
        self.exclusion_url = 'api/sonicos/anti-spyware/exclusion-list/base'
        self.exclusion_entry_url = 'api/sonicos/anti-spyware/exclusion-list/entries'
        self.reset_url = 'api/sonicos/anti-spyware/reset'
        self.profile_url = 'api/sonicos/anti-spyware-prevention-profiles'
        self.object_url = 'https://idpapi.global.sonicwall.com/api/spy'
        self.exclusion_url = 'api/sonicos/anti-spyware/exclusion-list/base'
        self.reset_url = 'api/sonicos/anti-spyware/reset'
        self.initial_base = {
        	"anti_spyware": {
        		"enable": False,
        		"signature_group": {
        			"high_danger": {
        				"prevent_all": False,
        				"detect_all": False,
        				"log_redundancy": {}
        			},
        			"medium_danger": {
        				"prevent_all": False,
        				"detect_all": False,
        				"log_redundancy": {}
        			},
        			"low_danger": {
        				"prevent_all": False,
        				"detect_all": False,
        				"log_redundancy": {}
        			}
        		},
        		"inspection": {
        			"inbound": {
        				"http": True,
        				"ftp": True,
        				"imap": True,
        				"smtp": True,
        				"pop3": True
        			},
        			"outbound": True
        		},
				"smtp_responses": False,
				"http_clientless_notification": True,
				"message": "This request is blocked by the Firewall Anti-Spyware Service."
        	}
        }
        self.initial_exclusion = {
            "anti_spyware": {
                "exclusion": {
                    "list": False
                }
            }
        }
        self.anti_spy_profile = {
            "anti_spyware_prevention_profiles": [
                {
                    "name": "",
                    "negate": False,
                    "uuid": "00000000-0000-0003-3a00-00401039cf9d",
                    "signature": [],
                    "category": []
                }
            ]
        }
        self.initial_exclusion = {
            "anti_spyware": {
                "exclusion": {
                    "list": False
                }
            }
        }
        

    def build_json_antispyware_base(self, **kwargs):
        json_string = {}

        try:
            json_string = copy.deepcopy(self.initial_base)

            if 'enable' in kwargs:
                json_string['anti_spyware']['enable'] = kwargs['enable']
            if 'high_danger_prevent' in kwargs:
                json_string['anti_spyware']['signature_group']['high_danger']['prevent_all'] = kwargs['high_danger_prevent']
            if 'medium_danger_prevent' in kwargs:
                json_string['anti_spyware']['signature_group']['medium_danger']['prevent_all'] = kwargs['medium_danger_prevent']
            if 'low_danger_prevent' in kwargs:
                json_string['anti_spyware']['signature_group']['low_danger']['prevent_all'] = kwargs['low_danger_prevent']				
            if 'high_danger_detect' in kwargs:
                 json_string['anti_spyware']['signature_group']['high_danger']['detect_all'] = kwargs['high_danger_detect']
            if 'medium_danger_detect' in kwargs:
                 json_string['anti_spyware']['signature_group']['medium_danger']['detect_all'] = kwargs['medium_danger_detect']
            if 'low_danger_detect' in kwargs:
                 json_string['anti_spyware']['signature_group']['low_danger']['detect_all'] = kwargs['low_danger_detect']


            if 'high_log_redu_val' in kwargs:
                 json_string['anti_spyware']['signature_group']['high_danger']['log_redundancy']['value'] = kwargs['high_log_redu_val']
            if 'medium_log_redu_val' in kwargs:
                 json_string['anti_spyware']['signature_group']['medium_danger']['log_redundancy']['value'] = kwargs['medium_log_redu_val']
            if 'low_log_redu_val' in kwargs:
                json_string['anti_spyware']['signature_group']['low_danger']['log_redundancy']['value'] = kwargs['low_log_redu_val']

            if 'high_log_redu_val' in kwargs:
                 json_string['anti_spyware']['signature_group']['high_danger']['log_redundancy']['value'] = kwargs['high_log_redu_val']
            if 'medium_log_redu_val' in kwargs:
                 json_string['anti_spyware']['signature_group']['medium_danger']['log_redundancy']['value'] = kwargs['medium_log_redu_val']
            if 'low_log_redu_val' in kwargs:
                json_string['anti_spyware']['signature_group']['low_danger']['log_redundancy']['value'] = kwargs['low_log_redu_val']
            if 'smtp' in  kwargs:
                json_string['anti_spyware']['inspection']['inbound']['smtp'] = kwargs['smtp']
            if 'http' in  kwargs:
                json_string['anti_spyware']['inspection']['inbound']['http'] = kwargs['http']
            if 'ftp' in  kwargs:
                json_string['anti_spyware']['inspection']['inbound']['ftp'] = kwargs['ftp']
            if 'imap' in  kwargs:
                json_string['anti_spyware']['inspection']['inbound']['imap'] = kwargs['imap']
            if 'pop3' in  kwargs:
                json_string['anti_spyware']['inspection']['inbound']['pop3'] = kwargs['pop3']
            if 'smtp_responses' in  kwargs:
                json_string['anti_spyware']['smtp_responses'] = kwargs['smtp_responses']
            if 'http_clientless_notification' in  kwargs:
                json_string['anti_spyware']['http_clientless_notification'] = kwargs['http_clientless_notification']
            if 'message' in  kwargs:
                json_string['anti_spyware']['message'] = kwargs['message']

        except KeyError:
            logger.error("ERROR: json string cannot be constructed")
        logger.info(json_string)
        return json_string

    def build_json_antispyware_exclusion_list(self, **kwargs):
        json_string = {}

        try:
            json_string = copy.deepcopy(self.initial_exclusion)

            json_string['anti_spyware']['exclusion']['list'] = kwargs['enable']
            if kwargs['enable']:
                json_string['anti_spyware']['exclusion']['address'] = kwargs['address_type']
                if kwargs['address_type'] == 'object':
                    json_string['anti_spyware']['exclusion']['address_object'] = {}
                    json_string['anti_spyware']['exclusion']['address_object']['name'] = kwargs['address']

        except KeyError:
            logger.error("ERROR: json string cannot be constructed")
        logger.info(json_string)
        return json_string

    def config_antispyware(self, msg=False, **kwargs):
        json_string = self.build_json_antispyware_base(**kwargs)
        retval = self.fw.api_put(self.base_url, msg, data=json_string)
        return retval

    def get_antispyware(self, msg=False):
        retval = self.fw.api_get(self.base_url)
        return retval

    def config_antispyware_exclu_list(self, msg=False, **kwargs):
        json_string = self.build_json_antispyware_exclusion_list(**kwargs)
        retval = self.fw.api_put(self.exclusion_url, msg, data=json_string)
        return retval

    def reset_antispyware(self, msg=False, **kwargs):
        retval = self.fw.api_post(self.reset_url, msg)
        return retval
    
    def add_antispyware_profile(self, msg=False, **kwargs):
        retval = self.fw.api_post(self.profile_url, msg, data=kwargs)
        return retval
    
    def delete_antispyware_profile(self, msg=False, name= None):
        json_string =  {
            "anti_spyware_prevention_profiles": [
                {
                    "name": name
                }
            ]
        }
        retval = self.fw.api_delete(self.profile_url, msg, data=json_string)
        return retval

    def edit_antispyware_profile(self, msg=False, **kwargs):
        url = self.profile_url + '/name/' + kwargs['name']
        json_get = self.fw.api_get(url, msg)
        logger.info('get json :{}'.format(json_get))
        json_input = copy.deepcopy(json_get)
        try:
            if 'new_name' in kwargs:
                json_input['anti_spyware_prevention_profiles'][0]['name'] = kwargs['new_name']
            if 'negate' in kwargs:
                json_input['anti_spyware_prevention_profiles'][0]['negate'] = kwargs['negate']
            if 'signature' in kwargs:
                json_input['anti_spyware_prevention_profiles'][0]['signature'] = kwargs['signature']
            if 'category' in kwargs:
                json_input['anti_spyware_prevention_profiles'][0]['category'] = kwargs['category']


        except KeyError:
            logger.error("ERROR: json string cannot be constructed")

        logger.info('json input:{}'.format(json_input))
        retval = self.fw.api_put(url, msg, data=json_input)
        return retval
    
    def get_antispyware_profile(self, msg=False, name= None):
        url = self.profile_url + '/name/' + name
        retval = self.fw.api_get(url, msg)
        return retval
    
    def get_antispyware_profile_all(self, msg=False):
        url = self.profile_url
        retval = self.fw.api_get(url, msg)
        return retval
    
    def get_antispyware_signature_detail(self, msg=False, id=None):
        url = self.object_url + '/' + id
        retval = self.fw.api_get_extranet(url, msg)
        return retval
    
    def get_antispyware(self, msg=False):
        retval = self.fw.api_get(self.base_url)
        return retval

    def config_antispyware_exclu_list(self, msg=False, **kwargs):
        json_string = self.build_json_antispyware_exclusion_list(**kwargs)
        retval = self.fw.api_put(self.exclusion_url, msg, data=json_string)
        return retval

    def reset_antispyware(self, msg=False, **kwargs):
        retval = self.fw.api_post(self.reset_url, msg)
        return retval

    def add_exclusion_entry(self, msg=False, **kwargs):
        retval = self.fw.api_post(self.exclusion_entry_url, msg, data=kwargs)
        return retval

    def delete_exclusion_entry(self, be_ip, end_ip, msg=False):
        exclusion_entry_url = self.exclusion_entry_url + f'/from/{be_ip}/to/{end_ip}'
        retval = self.fw.api_delete(exclusion_entry_url, msg)
        return retval


class IPSApi:
    '''IPSApi class'''
    default_ips_exclusionlist_entries = {
        'from': 'None',
        'to': 'None'
    }

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/intrusion-prevention/base'
        self.exclusion_list_url = 'api/sonicos/intrusion-prevention/exclusion-list/base'
        self.exclusionlist_entries_url = 'api/sonicos/intrusion-prevention/exclusion-list/entries'
        self.ips_categories_url = 'api/sonicos/intrusion-prevention/categories'
        self.ips_policy_url = 'api/sonicos/intrusion-prevention/policies'
        self.ips_update_signatures = 'api/sonicos/intrusion-prevention/update-signatures'
        self.ips_reset = 'api/sonicos/intrusion-prevention/reset'
        self.ips_reporting = 'api/sonicos/reporting/intrusion-prevention'

        self.initial_base = {
            'intrusion_prevention': {
                'enable': True,
                'signature_group': {
                    'high_priority': {
                        'prevent_all' : True,
                        'detect_all': True,
                        'log_redundancy': {}
                    },
                    'medium_priority':{
                        'prevent_all' : True,
                        'detect_all': True,
                        'log_redundancy': {}
                    },
                    'low_priority': {
                        'prevent_all' : True,
                        'detect_all': True,
                        'log_redundancy': {'value': 60}
                    }
                }
            }
        }

        self.exclusion_list = {
            "intrusion_prevention": {
                "exclusion": {
                    "list": True,
                    'address': 'object',
                    'name': 'X0 IP'
                    # 'group': 'None'
                }
            }
        }

        self.exclusionlist_entries = {
            'intrusion_prevention': {
                'exclusion': {
                    'entry': [
                        {
                            'from': 'None',
                            'to': 'None'
                        }
                    ]
                }
            }
        }

        self.ips_categories_list = {
            'intrusion_prevention': {
                'category': [
                    {
                        'name': 'BACKDOOR',
                        'id': 2,
                        'prevention': {
                        },
                        'detection': {
                        },
                        'included': {
                            'ip': {
                                'name': 'X0 Subnet'
                            },
                            'users': {
                                'group': 'Everyone'
                            }
                        },
                        'excluded': {
                            'ip': {},
                            'users': {}
                        },
                        'schedule': {
                            'always_on': True
                        },
                        'log_redundancy': {
                            'global': True
                        }
                    }
                ]
            }
        }

        self.ips_policy_list = {
            'intrusion_prevention': {
                'policy': [
                    {
                        'category': 'BACKDOOR',
                        'name': 'Q ICMP',
                        'id': 49,
                        'priority': 'medium',
                        'prevention': {
                        },
                        'detection': {
                        },
                        'included': {
                            'ip': {
                                'name': 'X0 Subnet'
                            },
                            'users': {
                                'group': 'Trusted Users'
                            }
                        },
                        'excluded': {
                            'ip': {},
                            'users': {}
                        },
                        'schedule': {
                            'always_on': True
                        },
                        'log_redundancy': {
                            'filter': {}
                            # 'global': True
                        }
                    }
                ]
            }
        }

    def build_json_policy_list(self, **args):
        json_string = {}

        try:
            json_string = copy.deepcopy(self.ips_policy_list)
            logger.info(json_string)

            if 'value' in args:
                json_string['intrusion_prevention']['policy'][0]['log_redundancy']['filter']['value'] = args['value']
            if 'prevention_category' in args:
                json_string['intrusion_prevention']['policy'][0]['prevention']['category'] = args['prevention_category']
            if 'detection_enable' in args:
                json_string['intrusion_prevention']['policy'][0]['detection']['enable'] = args['detection_enable']
            if 'schedule_name' in args:
                json_string['intrusion_prevention']['policy'][0]['schedule']['name'] = args['schedule_name']
            if 'policy_ip_name' in args:
                json_string['intrusion_prevention']['policy'][0]['included']['ip']['name'] = args['policy_ip_name']
            if 'policy_users_group' in args:
                json_string['intrusion_prevention']['policy'][0]['included']['users']['group'] = args['policy_users_group']

        except KeyError:
            logger.error("ERROR: json string cannot be constructed for policy list")

        return json_string

    def build_json_categories_list(self, **kwargs):
        json_input = {}

        try:
            json_input = copy.deepcopy(self.ips_categories_list)
            if 'prevention_global' in kwargs:
                json_input['intrusion_prevention']['category'][0]['prevention']['global'] = kwargs['prevention_global']
            if 'prevention_enable' in kwargs:
                json_input['intrusion_prevention']['category'][0]['prevention']['enable'] = kwargs['prevention_enable']
            if 'detection_global' in kwargs:
                json_input['intrusion_prevention']['category'][0]['detection']['global'] = kwargs['detection_global']
            if 'detection_enable' in kwargs:
                json_input['intrusion_prevention']['category'][0]['detection']['enable'] = kwargs['detection_enable']
            if 'included_ip_name' in kwargs:
                json_input['intrusion_prevention']['category'][0]['included']['ip']['name'] = kwargs['included_ip_name']
            if 'included_users' in kwargs:
                json_input['intrusion_prevention']['category'][0]['included']['users']['group'] = kwargs['included_users']
            if 'excluded_ip_name' in kwargs:
                json_input['intrusion_prevention']['category'][0]['excluded']['ip']['name'] = kwargs['excluded_ip_name']
            if 'excluded_users' in kwargs:
                json_input['intrusion_prevention']['category'][0]['excluded']['users']['group'] = kwargs['excluded_users']

        except KeyError as ke:
            logger.info('Error: in creating JSON for IPS categoties list')
        logger.info(json_input)
        return json_input

    def build_json_exclusionlist_entries(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.exclusionlist_entries)
        logger.info(json_input)
        try:
            json_input['intrusion_prevention']['exclusion']['entry'][0]['from'] = kwargs['from']
            json_input['intrusion_prevention']['exclusion']['entry'][0]['to'] = kwargs['to']

        except KeyError as ke:
            logger.info('Error: in creating JSON for IPS exclusion entries')

        return json_input

    def build_json_exclusion_list(self, **args):
        json_string = {}

        try:
            json_string = copy.deepcopy(self.exclusion_list)

            if 'enable_list' in args:
                json_string['intrusion_prevention']['exclusion']['list'] = args['enable_list']
            if 'exclusion_address' in args:
                json_string['intrusion_prevention']['exclusion']['address'] = args['exclusion_address']
            if 'exclusion_name' in args:
                json_string['intrusion_prevention']['exclusion']['name'] = args['exclusion_name']
            if 'exclusion_group' in args:
                json_string['intrusion_prevention']['exclusion']['group'] = args['exclusion_group']

        except KeyError:
            logger.error("ERROR: json string cannot be constructed")
        logger.info(json_string)
        return json_string

    def build_json_ips_base(self, **api):
        json_string = {}

        try:
            json_string = copy.deepcopy(self.initial_base)

            if 'ips_enable' in api:
                json_string['intrusion_prevention']['enable'] = api['ips_enable']
            if 'high_prevent_all' in api:
                json_string['intrusion_prevention']['signature_group']['high_priority']['prevent_all'] = api['high_prevent_all']
            if 'high_detect_all' in api:
                json_string['intrusion_detection']['signature_group']['high_priority']['detect_all'] = api['high_detect_all']
            if 'high_log_redundancy' in api:
                json_string['intrusion_log_redundancyion']['signature_group']['high_priority']['log_redundancy']['value'] = api['high_log_redundancy']
            if 'low_prevent_all' in api:
                json_string['intrusion_prevention']['signature_group']['low_priority']['prevent_all'] = api['low_prevent_all']
            if 'low_detect_all' in api:
                json_string['intrusion_detection']['signature_group']['low_priority']['detect_all'] = api['low_detect_all']
            if 'low_log_redundancy' in api:
                json_string['intrusion_prevention']['signature_group']['low_priority']['log_redundancy']['value'] = api['low_log_redundancy']
            if 'medium_prevent_all' in api:
                json_string['intrusion_prevention']['signature_group']['medium_priority']['prevent_all'] = api['medium_prevent_all']
            if 'medium_detect_all' in api:
                json_string['intrusion_detection']['signature_group']['medium_priority']['detect_all'] = api['medium_detect_all']
            if 'medium_log_redundancy' in api:
                json_string['intrusion_log_redundancyion']['signature_group']['medium_priority']['log_redundancy']['value'] = api['medium_log_redundancy']

        except KeyError:
            logger.error("ERROR: json string cannot be constructed")
        logger.info(json_string)
        return json_string

    def config_base_IPS(self, msg=False, **api):
        json_string = self.build_json_ips_base(**api)
        retval = self.fw.api_put(self.base_url, msg, data=json_string)
        return retval
        
    def get_IPS_global(self):
        out = self.fw.api_get(self.base_url)
        return out

    def config_IPS_global(self, msg=False, **kwargs):
        kws = self.fw.api_get(self.base_url)
        kws.update(kwargs)
        resp = self.fw.api_put(self.base_url, msg, data=kws)
        return resp

    def get_exclusion_list_global(self):
        out = self.fw.api_get(self.exclusion_list_url)
        return out

    def config_exclusion_list_global(self, msg=False, **kwargs):
        kws = self.fw.api_get(self.exclusion_list_url)
        kws.update(kwargs)
        resp = self.fw.api_put(self.exclusion_list_url, msg, data=kws)
        return resp

    def config_exclusion_list(self, msg=False, **args):
        json_string = self.build_json_exclusion_list(**args)
        retval = self.fw.api_put(self.exclusion_list_url, msg, data=json_string)
        return retval

    def get_IPS_exclusionlist_entries(self):
        get_response = self.fw.api_get(self.exclusionlist_entries_url)
        return get_response

    def post_IPS_exclusionlist_entries(self, msg=False, url=None, **kwargs):
        self.options = dict(IPSApi.default_ips_exclusionlist_entries)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_exclusionlist_entries(**kwargs)
        logger.info(json_input)
        IPS_resp = self.fw.api_post(self.exclusionlist_entries_url, msg, data=json_input)
        return IPS_resp

    def config_IPS_exclusionlist_entries(self, msg=False, url=None, **kwargs):
        self.options = dict(IPSApi.default_ips_exclusionlist_entries)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_exclusionlist_entries(**kwargs)
        logger.info(json_input)
        IPS_resp = self.fw.api_put(self.exclusionlist_entries_url, msg, data=json_input)
        return IPS_resp

    def delete_IPS_exclusionlist_entries(self, from1=None, to=None):
        if from1:
            url = self.exclusionlist_entries_url + '/from/' + str(from1) + '/to/' + str(to)
        else:
            logger.error('id should be specified for config ips signatures.')
            return False
        resp = self.fw.api_delete(url)
        return resp

    def get_ips_categories(self, id=None):
        if id:
            url = self.ips_categories_url + '/id/' + str(id)
        else:
            url = self.ips_categories_url
        resp = self.fw.api_get(url)
        return resp

    def config_ips_categories(self, msg=False, **args):
        json_string = self.build_json_categories_list(**args)
        logger.info(json_string)
        retval = self.fw.api_put(self.ips_categories_url, msg, data=json_string)
        return retval

    def get_ips_signatures(self, id = None):
        if id:
            url = self.ips_policy_url + '/id/' + str(id)
        else:
            url = self.ips_policy_url
        resp = self.fw.api_get(url)
        return resp

    def modify_ips_signatures(self, msg=False, **args):
        json_string = self.build_json_policy_list(**args)
        logger.info(json_string)
        retval = self.fw.api_put(self.ips_policy_url, msg, data=json_string)
        return retval

    def config_ips_signatures(self, id, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        # org name example: Suspicious JavaScript/VBScript Code 39
        name = json_input['intrusion_prevention']['policy'][0]['name'].replace(' ','%20').replace('/','%2F')
        if id:
            url = self.ips_policy_url + '/name/' + name
        else:
            logger.error('id should be specified for config ips signatures.')
            return False
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp
    def update_IPS_signatures(self):
        post_response = self.fw.api_post(self.ips_update_signatures)
        return post_response

    def reset_IPS(self):
        post_response = self.fw.api_post(self.ips_reset)
        return post_response

    def get_IPS_report(self):
        get_response = self.fw.api_get(self.ips_reporting)
        return get_response


class GAVCloudApi:
    '''GAVCloudApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/gateway-antivirus/cloud/base'
        self.exclusion_list_url = 'api/sonicos/gateway-antivirus/cloud/exclusions'
        self.get_sig = 'api/sonicos/dynamic-file/getCloudAVStats.json'

    def get_gav_cloud_base(self):
        out = self.fw.api_get(self.base_url)
        return out
        
    def get_sig_of_cloudav_part(self):
        out = self.fw.api_get(self.get_sig)
        return out

    def config_gav_cloud_base(self, msg=False, **kwargs):
        kws = self.fw.api_get(self.base_url)
        kws.update(kwargs)
        resp = self.fw.api_put(self.base_url, msg, data=kws)
        return resp

    def get_exclusion_list_global(self):
        out = self.fw.api_get(self.exclusion_list_url)
        return out

    def add_exclusion_list(self, msg=False, **kwargs):
        resp = self.fw.api_post(self.exclusion_list_url, msg, data=kwargs)
        return resp

    def del_exclusion_list(self, msg=False, **kwargs):
        resp = self.fw.api_delete(self.exclusion_list_url, msg, data=kwargs)
        return resp


class GeoIP:

    # default_values = {
    #     'block_countries':False
    #     'logging': False,
    #     'block_details': True,
    #     'alert_text': "This site has been blocked by the network administrator.",
    #     'data': "data:image/gif;base64,R0lGODlhlgAoALMAAPHw8Dw8PNLS06mqqpSVlvRvJvqaZfu2j3V1doSEhuHh4rm6uv3Uv8TFxWVmaP///yH5BAAAAAAALAAAAACWACgAAAT/8MlJKSAuo1XnRdoAdMLQSYojTAlxKgToIIQiLbNbJeBINbkfgnZ68BLFGMI3GSwGuqLUk1k0FhhkBecgDAaJzIoicHA6qcbEoaUMMolv2PxIZZj1DJ0iO0vmDngTIAhFc4ICV1FTUkMVCiZuDiIUCmFqE3ZjlQ6YDwhtEhiUFBh/VZJwFnqcepEVIKGldx2CjEWdjGWvO4GZejacnqAUOH6PI1yhgL43GYtveoUdYbITGM232hSTjI5SXb8NYXhpg6FstwB6PnZ6fnObn2zY8hKxSbTb+w8Y9sJTTKFwYCMDwHttyvw7ge0Mlxjp8swgg+oZtYgdsNniF/BZA0FA/4IVCTmQQ4o25u5FebOxA5CIhzQ+4MJL5iFYGCvI5LhPADY2InG0lEAyD6YyOlJ+avNmH6sHFrlwmCMSasSXx4zknJWN5z4AC0AEK1pE6EBPQEwoJeZsqE4xZXLZIbBu4gSsAADYkYWPoT6vPL+t43VRnKQVuRD+yiolboKbWmlkiATgQIHLmDMbMMDg3tZrfwHzw8HCQeM9Rt/iGLYIxD4ZFp3p8WUgs+3aRAZ9FmVQ9BTGWqlMe5RTaWkV5zgtKoYnmhgqepBYtl2As4SnpxAo0KtAJLbu27f75oZ8wupWHyUAeLPkIM5NbO/OkCfAdavex3NRP1Ah2rDZemDy0/9shIlmCRx91MJMbJwAt44fdpEhwxAaVOVZOMWw80BtmNlS13AAvnNKiMuNBwkBXlhYCRZObATJQg8IsIkTRZSA4gAwljCAhevR+AADmHV2whOkEEnkF2N94YSSMI7n5JNQdsChW1FWaeWV49VmAJZcduklT5bx9+WYZJb5YwFimqnmmlEeICSbcMYp55x01mnnnXjmqeeefPbp55+ABirooGvmReg2VHq1wDENNDleGEWAlaKTF6jIyAKWMhJHP45+hUAAwxQIZQy4EFDCcL516lIA1tyyqQCJarNOAgH4gICoDzQQgG88nKArlxto81itHG1apQq9fhKJTzjm+mn/DZE0esMIzGLSKI6mQCKSAAHsWAkUaHmxwgIjrFdHAw2IsCN7OGKiQFYK7IqhAuh6Ue6OKAbjxUw2nEhurunWoB4U/56oxjqw0nHrA28kEgCsAwTQHbEBLJECwyoAwQEIH/EQL2ERB+BLCgvs0g9BAywx8q661gCAxLvQ64uxa7igazLdllBrvAkk0s2mCn+EolU+53WrAAlgasYuCOcqMdAffeD0dYveAcYDD0vArbKiiJzjHQQkkBcQ64hUdh21/iqBxJ9wgPDZmUg8QrczNcPGyz6UYYQJdJQRQMWfuFA2adeIDQDZ5c0hwgw8DK32ArQymwvbaLfdNWon1EoA4augJJACE59X3sA0L9sQbD8EjL4DKJ2bFhYL2u2qtWn7ghrvCkBYDtWppXD+2O6D0J1sAmqo/bJp3MqeLDEICLgE3fKNgAEAZYzwBVSFQAKVGpuDNRzbe8SLOdwPlK4rB9wKEK8OxEAdb0GFnK5CvGqUXD3DfG/yciSbB6DDOqDiGlT+1z8tEE8UhdifB2jFqmAs4G/NYKALkre5XLWBbbqSnQOI1QTTUKAFXPjbCtb3Nx3sKxchS5kRMIGAEUKwfhCM1aFcVaKyoKpyM/wT3rahukrILod82hyufCWLeI0pAgA7",
    #     'enable': False,
    #     'override_countries':False
    #
    # }

    def __init__(self, fw):
        self.fw = fw
        self.settings_url = 'api/sonicos/geo-ip/base'
        self.custom_url = 'api/sonicos/geo-ip/addresses'
        self.settings_url_countries = 'api/sonicos/geo-ip/countries'
        self.initial_json_Geoip_coutries = {
            "geo_ip": {
                "block": {
                    "country": None
                }
            }
        }
        self.initial_json_Geoip_settings = {
            "geo_ip": {
                "block": {
                    "connections": {"all": True},
                    "countries": {
                        "unknown": False
                    }
                },
                "logging": False,
                "exclude": {},
                "include": {
                    "block_details": True
                },
                "alert_text": "This site has been blocked by the network administrator.",
                "logo_icon": {
                    "data": "data:image/gif;base64,R0lGODlhlgAoALMAAPHw8Dw8PNLS06mqqpSVlvRvJvqaZfu2j3V1doSEhuHh4rm6uv3Uv8TFxWVmaP///yH5BAAAAAAALAAAAACWACgAAAT/8MlJKSAuo1XnRdoAdMLQSYojTAlxKgToIIQiLbNbJeBINbkfgnZ68BLFGMI3GSwGuqLUk1k0FhhkBecgDAaJzIoicHA6qcbEoaUMMolv2PxIZZj1DJ0iO0vmDngTIAhFc4ICV1FTUkMVCiZuDiIUCmFqE3ZjlQ6YDwhtEhiUFBh/VZJwFnqcepEVIKGldx2CjEWdjGWvO4GZejacnqAUOH6PI1yhgL43GYtveoUdYbITGM232hSTjI5SXb8NYXhpg6FstwB6PnZ6fnObn2zY8hKxSbTb+w8Y9sJTTKFwYCMDwHttyvw7ge0Mlxjp8swgg+oZtYgdsNniF/BZA0FA/4IVCTmQQ4o25u5FebOxA5CIhzQ+4MJL5iFYGCvI5LhPADY2InG0lEAyD6YyOlJ+avNmH6sHFrlwmCMSasSXx4zknJWN5z4AC0AEK1pE6EBPQEwoJeZsqE4xZXLZIbBu4gSsAADYkYWPoT6vPL+t43VRnKQVuRD+yiolboKbWmlkiATgQIHLmDMbMMDg3tZrfwHzw8HCQeM9Rt/iGLYIxD4ZFp3p8WUgs+3aRAZ9FmVQ9BTGWqlMe5RTaWkV5zgtKoYnmhgqepBYtl2As4SnpxAo0KtAJLbu27f75oZ8wupWHyUAeLPkIM5NbO/OkCfAdavex3NRP1Ah2rDZemDy0/9shIlmCRx91MJMbJwAt44fdpEhwxAaVOVZOMWw80BtmNlS13AAvnNKiMuNBwkBXlhYCRZObATJQg8IsIkTRZSA4gAwljCAhevR+AADmHV2whOkEEnkF2N94YSSMI7n5JNQdsChW1FWaeWV49VmAJZcduklT5bx9+WYZJb5YwFimqnmmlEeICSbcMYp55x01mnnnXjmqeeefPbp55+ABirooGvmReg2VHq1wDENNDleGEWAlaKTF6jIyAKWMhJHP45+hUAAwxQIZQy4EFDCcL516lIA1tyyqQCJarNOAgH4gICoDzQQgG88nKArlxto81itHG1apQq9fhKJTzjm+mn/DZE0esMIzGLSKI6mQCKSAAHsWAkUaHmxwgIjrFdHAw2IsCN7OGKiQFYK7IqhAuh6Ue6OKAbjxUw2nEhurunWoB4U/56oxjqw0nHrA28kEgCsAwTQHbEBLJECwyoAwQEIH/EQL2ERB+BLCgvs0g9BAywx8q661gCAxLvQ64uxa7igazLdllBrvAkk0s2mCn+EolU+53WrAAlgasYuCOcqMdAffeD0dYveAcYDD0vArbKiiJzjHQQkkBcQ64hUdh21/iqBxJ9wgPDZmUg8QrczNcPGyz6UYYQJdJQRQMWfuFA2adeIDQDZ5c0hwgw8DK32ArQymwvbaLfdNWon1EoA4augJJACE59X3sA0L9sQbD8EjL4DKJ2bFhYL2u2qtWn7ghrvCkBYDtWppXD+2O6D0J1sAmqo/bJp3MqeLDEICLgE3fKNgAEAZYzwBVSFQAKVGpuDNRzbe8SLOdwPlK4rB9wKEK8OxEAdb0GFnK5CvGqUXD3DfG/yciSbB6DDOqDiGlT+1z8tEE8UhdifB2jFqmAs4G/NYKALkre5XLWBbbqSnQOI1QTTUKAFXPjbCtb3Nx3sKxchS5kRMIGAEUKwfhCM1aFcVaKyoKpyM/wT3rahukrILod82hyufCWLeI0pAgA7"
                },
                "custom_list": {
                    "enable": False,
                    "override_countries": False
                }
            }
        }

    def build_json_Geoip_settings(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_Geoip_settings)
        logger.info(json_input)

        try:

            if 'block_countries' in kwargs.keys():
                json_input['geo_ip']['block']['countries']['unknown'] = kwargs['block_countries']
            if 'logging1' in kwargs.keys():
                json_input['geo_ip']['logging'] = kwargs['logging1']
            if 'block_details' in kwargs.keys():
                json_input['geo_ip']['block_details'] = kwargs['block_details']
            if 'alert_text' in kwargs.keys():
                json_input['geo_ip']['alert_text'] = kwargs['alert_text']
            if 'data' in kwargs.keys():
                json_input['geo_ip']['logo_icon']['data'] = kwargs['data']
            if 'enable' in kwargs.keys():
                json_input['geo_ip']['enable'] = kwargs['enable']
            if 'override_countries' in kwargs.keys():
                json_input['geo_ip']['override_countries'] = kwargs['override_countries']
            else:
                logger.error('Error: While creating base setting')
        except KeyError:
            logger.error('Error: Creating JSON for GEOIP settings')
        return json_input

    def get_security_services_base(self):
        get_response = self.fw.api_get(self.settings_url)
        return get_response

    def configure_Geoip_settings(self, msg=False, **kwargs):

        json_input = self.build_json_Geoip_settings(**kwargs)
        logger.info('The json input build is', json_input)
        Geoip_response = self.fw.api_put(self.settings_url, msg, data=json_input)
        return Geoip_response

    def configure_geoip_settings_json(self, **kwargs):

        json_input = copy.deepcopy(kwargs)
        put_response = self.fw.api_put(self.settings_url, data=json_input)
        return put_response

    def add_geoip_custom_list(self, **kwargs):
        json_input = copy.deepcopy(kwargs)
        response = self.fw.api_post(self.custom_url, data=json_input)
        return response

    def edit_Geoip_countries_json(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        Geoip_response = self.fw.api_put(self.settings_url_countries, msg, data=json_input)
        return Geoip_response

    def delete_Geoip_custom_list(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        Geoip_response = self.fw.api_delete(self.custom_url, msg, data=json_input)
        return Geoip_response

    def get_Geoip_custom_list(self):
        Geoip_response = self.fw.api_get(self.custom_url)
        return Geoip_response

    def edit_Geoip_countries(self, msg=False, **kwargs):

        json_input = {}
        json_input = copy.deepcopy(self.initial_json_Geoip_coutries)
        if 'countries' in kwargs.keys():
            json_input['geo_ip']['block']['country'] = kwargs['countries']

        else:
            logger.info("please give the correct the country name")
        logger.info('The json input build is', json_input)
        Geoip_response = self.fw.api_put(self.settings_url_countries, msg, data=json_input)
        return Geoip_response

    def unblock_all_Geoip_countries(self, msg=False):

        json_input = {}
        json_input = self.get_geo_ip_countries()
        logger.info('The json input build is', json_input)
        Geoip_response = self.fw.api_delete(self.settings_url_countries, msg, data=json_input)
        return Geoip_response

    def unblock_Geoip_countries(self, msg=False, **kwargs):

        json_input = {}
        json_input = copy.deepcopy(self.initial_json_Geoip_coutries)
        if 'countries' in kwargs.keys():
            json_input['geo_ip']['block']['country'] = kwargs['countries']

        else:
            logger.info("please give the correct the country name")
        logger.info('The json input build is', json_input)
        Geoip_response = self.fw.api_delete(self.settings_url_countries, msg, data=json_input)
        return Geoip_response

    def get_geo_ip_countries(self):
        get_response = self.fw.api_get(self.settings_url_countries)
        return get_response

    def delete_Geoip_countries(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        Geoip_response = self.fw.api_delete(self.settings_url_countries, msg, data=json_input)
        return Geoip_response


class ContentFilterApi:
    '''ContentFilterApi class'''
    default_values = {
        'content_filter': None,
        'cfs': None,
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/content-filter/cfs/base'
        self.cfs_settings = 'api/sonicos/content-filter/settings'
        self.initial_json_cfs_filter = {
            'content_filter': {
                'cfs': {
                    # 'max_url_caches': 25600, different platform has different value
                    "enable": True,
                    "block_if_server_unavailable": False,
                    "server_timeout": 5,
                    "local_server": {
                        "enable": False,
                        "primary": "",
                        "secondary": ""
                    },
                    "exclude": {
                        "administrator": True,
                        "address": {}
                    }
                }    
            }
        }

    def build_json_content_filter(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_cfs_filter)
        try:
            if 'exclude_administrator' in kwargs.keys(): 
                json_input['content_filter']['cfs']['exclude']['administrator'] = kwargs['exclude_administrator']
            if 'exclude_address' in kwargs.keys():
                json_input['content_filter']['cfs']['exclude']['address'] = kwargs['exclude_address'] 
            if 'address_exclude' in kwargs.keys():
                json_input['content_filter']['cfs']['exclude']['address']['name'] = kwargs['address_exclude']
            if 'max_url_caches' in kwargs.keys():   
                json_input['content_filter']['cfs']['max_url_caches'] = kwargs['max_url_caches']
            if 'enable' in kwargs.keys():
                json_input['content_filter']['cfs']['enable'] = kwargs['enable']
            if 'block_if_server_unavailable' in kwargs.keys():
                json_input['content_filter']['cfs']['block_if_server_unavailable'] = kwargs['block_if_server_unavailable']
            if 'server_timeout' in kwargs.keys():
                json_input['content_filter']['cfs']['server_timeout'] = kwargs['server_timeout']
            if 'local_server_enable' in kwargs.keys():
                json_input['content_filter']['cfs']['local_server']['enable'] = kwargs['local_server_enable']
            if 'local_server_secondary' in kwargs.keys():
                json_input['content_filter']['cfs']['local_server']['primary'] = kwargs['local_server_secondary']
            if 'local_server_secondary' in kwargs.keys():
                json_input['content_filter']['cfs']['local_server']['secondary'] = kwargs['local_server_secondary']
            if 'local_server_secondary' in kwargs.keys():
                json_input['content_filter']['cfs']['local_server']['secondary'] = kwargs['local_server_secondary']      

        except KeyError:
            logger.error('Error: in creating JSON for content filter settings')
            logger.info(json_input)

        return json_input

    def get_cfs_content_filter(self):
        get_response = self.fw.api_get(self.url)
        return get_response

    def configure_cfs_content_filter(self, msg=False, **kwargs):
        # self.options = dict(ContentFilterApi.default_values)
        # self.options.update(kwargs)
        # kwargs = self.options
        json_input = self.build_json_content_filter(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        cfs_content_filter_res = self.fw.api_put(self.cfs_settings, msg, data=json_input)
        return cfs_content_filter_res


    def edit_cfs_setting(self, msg=False, **kwargs):
        json_put = self.build_json_content_filter(**kwargs)
        put_url = 'api/sonicos/content-filter/settings'
        putcfs_resp = self.fw.api_put(put_url, msg, data=json_put)
        return putcfs_resp

    def edit_cfs_settings(self, msg=False, **kwargs):
        json_put = copy.deepcopy(kwargs)
        put_url = 'api/sonicos/content-filter/settings'
        putcfs_resp = self.fw.api_put(put_url, msg, data=json_put)
        return putcfs_resp  

    def get_cfs_settings(self):
        url = 'api/sonicos/content-filter/settings'
        getcfs_resp = self.fw.api_get(url)
        return getcfs_resp
        
    def get_cfs_content_filter_websense(self):
        url = 'api/sonicos/content-filter/websense'
        getcfs_resp = self.fw.api_get(url)
        return getcfs_resp
    
    def get_cfs_server_status(self):
        url = 'api/sonicos/dynamic-file/getCFSServerStatus.json'
        resp = self.fw.api_get(url)
        return resp

class ContentFilterPolicyApi:
    '''ContentFilterPolicyApi class'''
    
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/content-filter/cfs/policies'
        self.url_statistics = 'api/sonicos/reporting/content-filter/cfs/policies/statistics'

    def add_cfs_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp
    
    def show_statistics_of_cfs_policy(self, name=None):
        if name:
            url = self.url_statistics + '/name/' + name
        else:
            url = self.url_statistics
        resp = self.fw.api_get(url)
        return resp
    
    def del_statistics_by_name(self, name=None):
        if name:
            url = self.url_statistics + '/name/' + name
        else:
            url = self.url_statistics
        resp = self.fw.api_delete(url)
        return resp
    
    def get_cfs_policy(self, name=None):
        if name:
            url = self.url + '/name/' + name
        else:
            url = self.url
        resp = self.fw.api_get(url)
        return resp

    def edit_cfs_policy_by_name(self, msg=False, name=None, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if name:
            url = self.url + '/name/' + str(name)
        else:
            logger.error('name should be specified for edit the cfs policy.')
            return False
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def delete_cfs_policy_by_name(self, name=None):
        if name:
            url = self.url + '/name/' + name
        else:
            logger.error('name shoule be specified for delete_cfs_policy_by_name.')
            return False
        resp = self.fw.api_delete(url)
        return resp

        
class CFSCustomCategoryApi:
    '''CFSCustomCategoryApi class'''
    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/content-filter/cfs/custom-category/base'
        self.export = 'api/sonicos/export/content-filter/cfs/custom-category'
        self.url = 'api/sonicos/content-filter/cfs/custom-category/category-entries'

    def get_cfs_custom_category_sattus(self):
        resp = self.fw.api_get(self.base_url)
        return resp

    def export_cfs_custom_category(self):
        resp = self.fw.api_get(self.export)
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
        
        
class GatewayAntiVirusApi:

    '''GatewayAntiVirusApi class'''
    
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/gav-prevention-profiles'

    def add_GAV_profiles(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def edit_GAV_profiles(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp

    def get_gav_profile(self):
        resp = self.fw.api_get(self.url)
        return resp

    def del_gav_profile(self, name, msg=False):
        if name:
            url = self.url + '/name/'+ name
        else:
            logger.error('name shoule be specified for delete gav profile.')
            return False
        resp = self.fw.api_delete(url,msg)
        return resp


class Botnet:
    '''Botnet class'''

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/botnet/base'
        self.custom_list_address = 'api/sonicos/botnet/custom-list-addresses'
        self.download_list_url = 'api/sonicos/raw'
        self.dynamic_list_url = 'api/sonicos/dynamic-file/getDynBotnetList.json'
        self.botnet_reporting_status = 'api/sonicos/reporting/botnet/status'
        self.botnet_resolved_locations = 'api/sonicos/reporting/botnet/resolved-locations'
        self.botnet_cache_status = 'api/sonicos/reporting/botnet/cache'

    def get_botnet_setting(self):
        resp = self.fw.api_get(self.base_url)
        return resp
    
    def download_list(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        post_response = self.fw.api_post(self.download_list_url, msg, data=json_input)
        return post_response
    
    def config_botnet_base(self, msg=False, **kwargs):
        kws = self.fw.api_get(self.base_url)
        kws.update(kwargs)
        resp = self.fw.api_put(self.base_url, msg, data=kws)
        return resp
    
    def get_botnet_dynamic_list(self):
        resp = self.fw.api_get(self.dynamic_list_url)
        return resp

    def get_botnet_custom_list_addresses(self):
        resp = self.fw.api_get(self.custom_list_address)
        return resp

    def get_botnet_custom_list_addresses_by_name(self, name=None):
        if name:
            url = self.custom_list_address + '/name/' + name
        else:
            logger.error('name should be specified')
            return False
        resp = self.fw.api_get(url)
        return resp

    def add_custom_list(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        post_response = self.fw.api_post(self.custom_list_address, msg, data=json_input)
        return post_response

    def del_botnet_custom_list_addresses(self, name=None, msg=False):
        if name:
            url = self.custom_list_address + '/name/' + name
        else:
            logger.error('name should be specified for delete custom list address.')
            return False
        resp = self.fw.api_delete(url,msg)
        return resp

    def del_botnet_custom_list_addresses_group(self, name=None, msg=False):
        if name:
            url = self.custom_list_address + '/group/' + name
        else:
            logger.error('name should be specified for delete custom list address group.')
            return False
        resp = self.fw.api_delete(url,msg)
        return resp

    def delete_botnet_custom_list_addresses(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        post_response = self.fw.api_delete(self.custom_list_address, msg, data=json_input)
        return post_response

    def get_botnet_reporting_status(self):
        resp = self.fw.api_get(self.botnet_reporting_status)
        return resp

    def get_botnet_resolved_locations(self):
        resp = self.fw.api_get(self.botnet_resolved_locations)
        return resp

    def get_botnet_cache_statistics(self):
        resp = self.fw.api_get(self.botnet_cache_status)
        return resp


class AppControl:
 
    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/app-control/base'
 
    def get_app_control_settings(self):
        resp = self.fw.api_get(self.base_url)
        return resp
   
    def config_app_control_base(self, msg=False, **kwargs):
        kws = self.fw.api_get(self.base_url)
        kws.update(kwargs)
        resp = self.fw.api_put(self.base_url, msg, data=kws)
        return resp
