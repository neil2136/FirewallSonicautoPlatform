import copy
import json
from pprint import pprint
from runner.settings import logger
#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)


class AdvanceApi:
    '''AdvanceApi'''
    default_adv_options = {
        'stealth_mode': False,
        'randomize_id': False,
        'decrement ttl': False,
#        'icmp time_exceeded_packets': True,#move to func config_advance_access_rule
        'ftp_transforms_in_service_object': {'group': 'FTP (All)'},
        'sqlnet': False,
        'rtsp_transformations': True,
        'drop source_routed': True,
        'connections': 'optimized',
        'ip checksum_enforcement': False,
        'udp checksum_enforcement': False,
        'control_plane_flood_protection': {},
        'jumbo_frame': False,
    }

    default_adv_access_rule_options = {
        'force_ftp_data': False,
        'apply_rules_for_intra_lan': False,
        'issue_rst_for_outgoing_discards': True,
        'icmp redirect_on_lan': True,
        'icmp time_exceeded_packets': True,
    }

    default_adv_ipv6_options = {
        'ipv6 drop all_traffic': False,
        'ipv6 drop routing_header_0': True,
        'ipv6 decrement hop_limit': False,
        'ipv6 drop reserved_address_packets': False,
        'ipv6 icmp time_exceeded': False,
        'ipv6 icmp destination_unreachable': False,
        'ipv6 icmp redirect': False,
        'ipv6 icmp parameter_problem': False,
        'ipv6 site_local_unicast': True,
        'ipv6 extension_header_check': False,
        'ipv6 extension_header_order_check': False,
        'ipv6 netbios_for_isatap': False,
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/firewall'
        self.initial_firewall_json = {
            'firewall': {
                'stealth_mode': False,
                'randomize_id': False,
                'decrement': {'ttl': False},
                'ftp_transforms_in_service_object': {'group': 'FTP (All)'},
                'sqlnet': False,
                'rtsp_transformations': True,
                'drop': {'source_routed': True},
                'connections': 'optimized',
                'ip': {'checksum_enforcement': False},
                'udp': {'checksum_enforcement': False},
                'jumbo_frame': False,
                'control_plane_flood_protection': {},
            }
        }
        self.initial_firewall_access_rule_json = {
            'firewall': {
                'force_ftp_data': False,
                'apply_rules_for_intra_lan': False,
                'issue_rst_for_outgoing_discards': True,
                'icmp': {'redirect_on_lan': True,
                         'time_exceeded_packets': True
                },
            }
        }
        self.initial_firewall_ipv6_json = {
            'firewall': {'ipv6': {'decrement': {'hop_limit': False},
                                  'drop': {
                                       'all_traffic': False,
                                       'reserved_address_packets': False,
                                       'routing_header_0': True},
                                  'extension_header_check': False,
                                  'extension_header_order_check': False,
                                  'icmp': {'destination_unreachable': False,
                                           'parameter_problem': False,
                                           'redirect': False,
                                           'time_exceeded': False},
                                  'netbios_for_isatap': False},
                         }
        }

    def show_adv_setttings(self):
        output = self.fw.api_get(self.url)
        return output

    def config_advance(self, msg=False, **kwargs):
        self.options = dict(AdvanceApi.default_adv_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_firewall_json)
            json_input['firewall']['stealth_mode'] = kwargs['stealth_mode']
            json_input['firewall']['randomize_id'] = kwargs['randomize_id']
            json_input['firewall']['decrement']['ttl'] = kwargs['decrement ttl']
            json_input['firewall']['ftp_transforms_in_service_object'] = kwargs['ftp_transforms_in_service_object']
            json_input['firewall']['sqlnet'] = kwargs['sqlnet']
            json_input['firewall']['rtsp_transformations'] = kwargs['rtsp_transformations']
            json_input['firewall']['drop']['source_routed'] = kwargs['drop source_routed']
            json_input['firewall']['connections'] = kwargs['connections']
            json_input['firewall']['ip']['checksum_enforcement'] = kwargs['ip checksum_enforcement']
            json_input['firewall']['udp']['checksum_enforcement'] = kwargs['udp checksum_enforcement']
            json_input['firewall']['jumbo_frame'] = kwargs['jumbo_frame']
            json_input['firewall']['control_plane_flood_protection'] = kwargs['control_plane_flood_protection']
        except KeyError:
            logger.error("Error in creating JSON for advance setting")
        pprint(json_input)
        advance_resp = self.fw.api_put(self.url, msg, data=json_input)
        return advance_resp

    def config_advance_access_rule(self, msg=False, **kwargs):
        self.options = dict(AdvanceApi.default_adv_access_rule_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_firewall_access_rule_json)
            json_input['firewall']['force_ftp_data'] = kwargs['force_ftp_data']
            json_input['firewall']['apply_rules_for_intra_lan'] = kwargs['apply_rules_for_intra_lan']
            json_input['firewall']['issue_rst_for_outgoing_discards'] = kwargs['issue_rst_for_outgoing_discards']
            json_input['firewall']['icmp']['redirect_on_lan'] = kwargs['icmp redirect_on_lan']
            json_input['firewall']['icmp']['time_exceeded_packets'] = kwargs['icmp time_exceeded_packets']
        except KeyError:
            logger.error("Error in creating JSON for advance access rule setting")
        pprint(json_input)
        advance_access_rule_resp = self.fw.api_put(self.url, msg, data=json_input)
        return advance_access_rule_resp

    def config_advance_ipv6(self, msg=False, **kwargs):
        self.options = dict(AdvanceApi.default_adv_ipv6_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_firewall_ipv6_json)
            json_input['firewall']['ipv6']['decrement']['hop_limit'] = kwargs['ipv6 decrement hop_limit']
            json_input['firewall']['ipv6']['drop']['all_traffic'] = kwargs['ipv6 drop all_traffic']
            json_input['firewall']['ipv6']['drop']['reserved_address_packets'] = kwargs['ipv6 drop reserved_address_packets']
            json_input['firewall']['ipv6']['drop']['routing_header_0'] = kwargs['ipv6 drop routing_header_0']
            json_input['firewall']['ipv6']['extension_header_check'] = kwargs['ipv6 extension_header_check']
            json_input['firewall']['ipv6']['extension_header_order_check'] = kwargs['ipv6 extension_header_order_check']
            json_input['firewall']['ipv6']['icmp']['destination_unreachable'] = kwargs['ipv6 icmp destination_unreachable']
            json_input['firewall']['ipv6']['icmp']['parameter_problem'] = kwargs['ipv6 icmp parameter_problem']
            json_input['firewall']['ipv6']['icmp']['redirect'] = kwargs['ipv6 icmp redirect']
            json_input['firewall']['ipv6']['icmp']['time_exceeded'] = kwargs['ipv6 icmp time_exceeded']
            json_input['firewall']['ipv6']['netbios_for_isatap'] = kwargs['ipv6 netbios_for_isatap']
        except KeyError:
            logger.error("Error in creating JSON for ipv6 advance setting")
        pprint(json_input)
        adv_ipv6_resp = self.fw.api_put(self.url, msg, data=json_input)
        return adv_ipv6_resp


class BwmApi:
    '''BwmApi class'''
    default_bwm_options = {
        'guaranteed': {'realtime': 0,
                       'highest': 0,
                       'high': 30,
                       'medium_high': 0,
                       'medium': 50,
                       'medium_low': 0,
                       'low': 20,
                       'lowest': 0,
                       },
        'maximum': {'realtime': 100,
                    'highest': 100,
                    'high': 100,
                    'medium_high': 100,
                    'medium': 100,
                    'medium_low': 100,
                    'low': 100,
                    'lowest': 100,
                    },
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/bandwidth-management'
        self.initial_bwm_json = {'bandwidth_management':
                                     {'priority':
                                          {'high': {'guaranteed': 30,
                                                    'maximum': 100},
                                           'highest': {'guaranteed': 0,
                                                    'maximum': 100},
                                           'low': {'guaranteed': 20,
                                                   'maximum': 100},
                                           'lowest': {'guaranteed': 0,
                                                      'maximum': 100},
                                           'medium': {'guaranteed': 50,
                                                      'maximum': 100},
                                           'medium_high': {'guaranteed': 0,
                                                           'maximum': 100},
                                           'medium_low': {'guaranteed': 0,
                                                          'maximum': 100},
                                           'realtime': {'guaranteed': 0,
                                                        'maximum': 100}},
                                      'type': {'global': True}
                                     }
        }

    def show_bwm(self):
        output = self.fw.api_get(self.url)
        return output
        
    def add_bwm(self, msg=False, **kwargs):
        url = 'api/sonicos/bandwidth-objects'
        json_input = copy.deepcopy(kwargs)
        logger.info(f"\n{' kwargs print ':=^60}\n{json_input}")
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp    

    def config_bwm(self, msg=False, **kwargs):
        self.options = dict(BwmApi.default_bwm_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_bwm_json)
            json_kwargs = copy.deepcopy(kwargs)
            if 'type' in kwargs.keys():
                if kwargs['type'] == 'none':
                    json_input = {'bandwidth_management': {'type': {}}}
                if kwargs['type'] == 'advanced':
                    json_input = {'bandwidth_management': {'type': {'advanced': True}}}
                elif kwargs['type'] == 'global':
                    del json_kwargs['type']
                    json_input['bandwidth_management']['type'] = {'global': True}
                    for key in json_kwargs:
                        for key1 in json_kwargs[key]:
                            json_input['bandwidth_management']['priority'][key1][key] = json_kwargs[key][key1]
                            if json_kwargs['guaranteed'][key1] == 0:
                                json_input['bandwidth_management']['priority'][key1] = {}
                    for key in json_input['bandwidth_management']['priority']:
                        if json_input['bandwidth_management']['priority'][key]['guaranteed'] == 0:
                            json_input['bandwidth_management']['priority'][key] = {}
                else:
                    logger.error("type key-value is not right")
            else:
                logger.error("type key-value has to be specified")
        except KeyError:
            logger.error("Error in creating JSON for bwm setting")
        pprint(json_input)
        bwm_resp = self.fw.api_put(self.url, msg, data=json_input)
        return bwm_resp


class FloodprotectionApi:
    '''FloodprotectionApi'''
    default_udp_icmp_options = {
        'flood protection': False,
        'flood block-timeout': 2,
    }

    default_tcp_options = {
        'enforce_strict_compliance': False,
        'handshake_enforcement': False,
        'checksum_enforcement': False,
        'drop syn_with_data': False,
        'handshake_timeout': 30,
        'default_connection_timeout': 15,
        'maximum_segment_lifetime': 8,
        'syn_flood_protection_mode': 'watch-and-report',
        'syn_attack_threshold': 300,
        'support_tcp_sack': False,
        'limit_mss': {},
        'always_log_syn_packets': False,
        'syn_flood_blacklisting': False,
        'blacklist_threshold': 1000,
        'never_blacklist_wan': False,
        'always_allow_management': False,
        'ddos_on_wan_interfaces': False,
        'ddos_threshold': 1000,
        'ddos_fliter_bypass_rate': 0,
        'ddos_allow_list_timeout': 0,
        'ddos_always_allow_management': False,
        'ddos_always_allow_negotiation': False,
    }

    def __init__(self, fw):
        self.fw = fw
        self.reports_tcp_url = 'api/sonicos/reporting/tcp'
        self.reports_udp_url = 'api/sonicos/reporting/udp'
        self.initial_tcp_json = {
            'tcp': {'always_allow_management': True,
                    'always_log_syn_packets': True,
                    'blacklist_threshold': 1000,
                    'checksum_enforcement': True,
                    'ddos': {'allow_list_timeout': 0,
                             'always_allow_management': True,
                             'always_allow_negotiation': True,
                             'fliter_bypass_rate': 0,
                             'on_wan_interfaces': True,
                             'threshold': 1000},
                    'default_connection_timeout': 15,
                    'drop': {'syn_with_data': True},
                    'enforce_strict_compliance': True,
                    'handshake_enforcement': True,
                    'enable_handshake_timeout': True,
                    'handshake_timeout': 30,
                    'limit_mss': {'max': 1460},
                    'maximum_segment_lifetime': 8,
                    'never_blacklist_wan': True,
                    'proxy_connections': {},
                    'support_tcp_sack': True,
                    'syn_attack_threshold': 300,
                    'syn_flood_blacklisting': True,
                    'syn_flood_protection_mode': 'proxy-suspect-attack'
            }
        }
        self.initial_udp_json = {
            "udp": {
                "default_connection_timeout": 30,
                "flood": {
                    "protection": True,
                    "attack_threshold": 1000,
                    "block_timeout": 2,
                    "protected_dest_list": {
                        "any": True
                    }
                }

            }
        }
        self.initial_icmp_json = {
            "icmp": {
                "flood": {
                    "protection": True,
                    "attack_threshold": 200,
                    "block_timeout": 2,
                    "protected_dest_list": {
                        "any": True
                    }
                }

            }
        }

    def show_flood_protection(self, msg=False, **kwargs):
        if 'type' in kwargs.keys():
            url = 'api/sonicos/' + kwargs['type']
            output = self.fw.api_get(url)
            pprint(output)
            return output
        else:
            logger.error("type has to be specified")

    def show_reporting_flood_protection(self, msg=False, **kwargs):
        if 'type' in kwargs.keys():
            url = 'api/sonicos/' + 'reporting/' + kwargs['type']
            response = self.fw.api_get(url)
            logger.info(response)
            return response
        else:
            logger.error("Type has to be specified")

    def delete_reporting_flood_protection(self, msg=False, **kwargs):
        if 'type' in kwargs.keys():
            url = 'api/sonicos/' + 'reporting/' + kwargs['type']
            response = self.fw.api_delete(url)
            logger.info(response)
            return response
        else:
            logger.error("Type has to be specified")

    def show_tcp(self):
        url = 'api/sonicos/tcp'
        output = self.fw.api_get(url)
        pprint(output)
        return output

    def config_tcp(self, msg=False, **kwargs):
        url = 'api/sonicos/tcp'
        self.options = dict(FloodprotectionApi.default_tcp_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_tcp_json)
            if not kwargs['enforce_strict_compliance']:
                del json_input['tcp']['handshake_enforcement']
            else:
                json_input['tcp']['handshake_enforcement'] = kwargs['handshake_enforcement']
            if kwargs['syn_flood_protection_mode'] == 'watch-and-report':
                del json_input['tcp']['support_tcp_sack']
                del json_input['tcp']['limit_mss']
                del json_input['tcp']['always_log_syn_packets']
                del json_input['tcp']['proxy_connections']
                json_input['tcp']['syn_flood_protection_mode'] = 'watch-and-report'
            else:
                json_input['tcp']['syn_flood_protection_mode'] = kwargs['syn_flood_protection_mode']
                json_input['tcp']['support_tcp_sack'] = kwargs['support_tcp_sack']
                json_input['tcp']['limit_mss'] = kwargs['limit_mss']
                json_input['tcp']['always_allow_management'] = kwargs['always_allow_management']
                json_input['tcp']['always_log_syn_packets'] = kwargs['always_log_syn_packets']
            json_input['tcp']['syn_attack_threshold'] = kwargs['syn_attack_threshold']
            if not kwargs['syn_flood_blacklisting']:
                del json_input['tcp']['blacklist_threshold']
                del json_input['tcp']['never_blacklist_wan']
                del json_input['tcp']['always_allow_management']
                json_input['tcp']['syn_flood_blacklisting'] = False
            else:
                json_input['tcp']['blacklist_threshold'] = kwargs['blacklist_threshold']
                json_input['tcp']['never_blacklist_wan'] = kwargs['never_blacklist_wan']
                json_input['tcp']['always_allow_management'] = kwargs['always_allow_management']
                json_input['tcp']['syn_flood_blacklisting'] = True
            if not kwargs['ddos_on_wan_interfaces']:
                json_input['tcp']['ddos'] = {'on_wan_interfaces': False}
            else:
                json_input['tcp']['ddos']['on_wan_interfaces'] = True
                json_input['tcp']['ddos']['threshold'] = kwargs['ddos_threshold']
                json_input['tcp']['ddos']['fliter_bypass_rate'] = kwargs['ddos_fliter_bypass_rate']
                json_input['tcp']['ddos']['allow_list_timeout'] = kwargs['ddos_allow_list_timeout']
                json_input['tcp']['ddos']['always_allow_management'] = kwargs['ddos_always_allow_management']
                json_input['tcp']['ddos']['always_allow_negotiation'] = kwargs['ddos_always_allow_negotiation']
            json_input['tcp']['enforce_strict_compliance'] = kwargs['enforce_strict_compliance']
            json_input['tcp']['checksum_enforcement'] = kwargs['checksum_enforcement']
            json_input['tcp']['drop']['syn_with_data'] = kwargs['drop syn_with_data']
            json_input['tcp']['enable_handshake_timeout'] = kwargs['enable_handshake_timeout']
            json_input['tcp']['handshake_timeout'] = kwargs['handshake_timeout']
            json_input['tcp']['default_connection_timeout'] = kwargs['default_connection_timeout']
            json_input['tcp']['maximum_segment_lifetime'] = kwargs['maximum_segment_lifetime']
        except KeyError:
            logger.error("Error in creating JSON for tcp setting")
        pprint(json_input)
        tcp_resp = self.fw.api_put(url, msg, data=json_input)
        return tcp_resp

    def config_udp_icmp(self, msg=False, **kwargs):
        self.options = dict(FloodprotectionApi.default_udp_icmp_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            if 'type' in kwargs.keys():
                url = 'api/sonicos/' + kwargs['type']
                if kwargs['type'] == 'udp':
                    json_input = copy.deepcopy(self.initial_udp_json)
                    if 'default-connection-timeout' in kwargs.keys():
                        json_input['udp']['default_connection_timeout'] = kwargs['default-connection-timeout']
                    else:
                        pass
                elif kwargs['type'] == 'icmp':
                    json_input = copy.deepcopy(self.initial_icmp_json)
                else:
                    logger.error("type value is not correct")
                if not kwargs['flood protection']:
                    json_input[kwargs['type']]['flood'] = {"protection": False}
                else:
                    json_input[kwargs['type']]['flood']['protection'] = True
                    if 'flood attack-threshold' in kwargs.keys():
                        json_input[kwargs['type']]['flood']['attack_threshold'] = kwargs['flood attack-threshold']
                    if 'flood block-timeout' in kwargs.keys():
                        json_input[kwargs['type']]['flood']['block_timeout'] = kwargs['flood block-timeout']
                    if 'flood protected-dest-list' in kwargs.keys():
                        json_input[kwargs['type']]['flood']['protected_dest_list'] = kwargs['flood protected-dest-list']
                    else:
                        pass
            else:
                logger.error("type value has to be specified")
        except KeyError:
            logger.error("Error in creating JSON for kwargs['type'] setting")
        pprint(json_input)
        udp_resp = self.fw.api_put(url, msg, data=json_input)
        return udp_resp

    def clear_tcp_reports(self, msg=False):
        resp = self.fw.api_delete(self.reports_tcp_url, msg)
        return resp
    
    def clear_udp_reports(self, msg=False):
        resp = self.fw.api_delete(self.reports_udp_url, msg)
        return resp

    def get_tcp_reports(self):
        resp = self.fw.api_get(self.reports_tcp_url)
        return resp

    def get_udp_reports(self):
        resp = self.fw.api_get(self.reports_udp_url)
        return resp
    


class MulticastApi:
    '''MulticastApi class'''
    default_multicast_options = {
        'multicast': False,
        'require_igmp_membership': True,
        'timeout': '5',
        'reception_name': 'all',
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/multicast/settings'
        self.url_base = 'api/sonicos/multicast/base'
        self.url_state_table = 'api/sonicos/reporting/multicast/state-entries'
        self.initial_multicast_json = {
            "multicast": {
                "enable": False,
                "enable_require_igmp_membership": True,
                "require_igmp_membership_timeout": 5,
                "reception": {
                    "all": True
                }
             }
        }

    def show_multicast(self):
        output = self.fw.api_get(self.url_base)
        return output

    def config_multicast(self, msg=False, **kwargs):
        self.options = dict(MulticastApi.default_multicast_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_multicast_json)
            if 'multicast' in kwargs.keys():
                if not kwargs['multicast']:
                    json_input['multicast']['enable'] = False
                else:
                    json_input['multicast']['enable'] = True
                    if 'require_igmp_membership' in kwargs.keys():
                        json_input['multicast']['enable_require_igmp_membership'] = kwargs['require_igmp_membership']
                    if 'timeout' in kwargs.keys():
                        json_input['multicast']['require_igmp_membership_timeout'] = int(kwargs['timeout'])
                    if 'reception_name' in kwargs.keys() and kwargs['reception_name'] != 'all':
                        json_input['multicast']['reception'] = {"name": kwargs['reception_name']}
                    else:
                        pass
            else:
                logger.error("multicast key-value has to be specified")
        except KeyError:
            logger.error("Error in creating JSON for multicast setting")
        pprint(json_input)
        multicast_resp = self.fw.api_put(self.url_base, msg, data=json_input)
        return multicast_resp

    def config_multicast_new(self, msg=False, **kwargs):
        self.options = dict(MulticastApi.default_multicast_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_multicast_json)
            if 'multicast' in kwargs.keys():
                if not kwargs['multicast']:
                    json_input['multicast']['enable'] = False
                else:
                    json_input['multicast']['enable'] = True
                    if 'require_igmp_membership' in kwargs.keys():
                        json_input['multicast']['require_igmp_membership'] = kwargs['require_igmp_membership']
                    if 'timeout' in kwargs.keys():
                        json_input['multicast']['require_igmp_membership_timeout'] = kwargs['timeout']
                    if 'reception_name' in kwargs.keys() and kwargs['reception_name'] != 'all':
                        json_input['multicast']['reception'] = {"name": kwargs['reception_name']}
                    else:
                        pass
            else:
                logger.error("multicast key-value has to be specified")
        except KeyError:
            logger.error("Error in creating JSON for multicast setting")
        multicast_resp = self.fw.api_put(self.url_base, msg, data=json_input)
        return multicast_resp

    def show_state_table(self, msg=False):
        output = self.fw.api_get(self.url_state_table)
        return output

    def delete_state_entry(self, msg=False, **kwargs):
        if kwargs['delete_way'] == 'designated':
            url = 'api/sonicos/multicast/state-entry/at/' + kwargs['address'] + '/if/' + kwargs['interface']
            output = self.fw.api_delete(url)
        elif kwargs['delete_way'] == 'all':
            url = 'api/sonicos/multicast/state-entries'
            output = self.fw.api_delete(url)
        else:
            logger.error("please specify the right delete_way")
        return output


class SslcontrolApi:
    '''SslcontrolApi class'''
    default_customlists_options = {
        'action': 'add',
        'black_name': [],
        'white_name': [],
    }

    default_sslcontrol_options = {
        'enable': False,
        'action': 'block',
        'blacklist': True,
        'whitelist': True,
        'detect_ssl_v2': True,
        'detect_ssl_v3': False,
        'detect_weak_ciphers': False,
        'detect_self_signed': False,
        'detect_weak_digest_cert': True,
        'detect_expired': False,
        'detect_untrusted_ca': True,
        'detect_tls_v1': False,
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/ssl-control/base'
        self.whitelist = 'api/sonicos/ssl-control/whitelist-certificates'
        self.blacklist = 'api/sonicos/ssl-control/blacklist-certificates'
        self.initial_customlists_json = {
            "ssl_control": {
                "blacklist_certificate": [],
                "whitelist_certificate": []
            }
        }
        self.initial_sslcontrol_json = {
            "ssl_control": {
                "enable": False,
                "action": "block",
                "blacklist": True,
                "whitelist": True,
                "detect": {
                    "ssl_v2": True,
                    "ssl_v3": False,
                    "weak_ciphers": False,
                    "self_signed": False,
                    "weak_digest_cert": True,
                    "expired": False,
                    "untrusted_ca": True,
                    "tls_v1": False
                }
            }
        }

    def show_ssl_control(self):
        output = self.fw.api_get(self.url)
        return output

    def show_ssl_whitelist(self):
        output = self.fw.api_get(self.whitelist)
        return output

    def show_ssl_blacklist(self):
        output = self.fw.api_get(self.blacklist)
        return output

    def config_customlists(self, msg=False, **kwargs):
        self.options = dict(SslcontrolApi.default_customlists_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_customlists_json)
            if 'black_name' in kwargs.keys():
                for i in range(len(kwargs['black_name'])):
                    json_input['ssl_control']['blacklist_certificate'].append({"common_name": kwargs['black_name'][i]})
            if 'white_name' in kwargs.keys():
                for i in range(len(kwargs['white_name'])):
                    json_input['ssl_control']['whitelist_certificate'].append({"common_name": kwargs['white_name'][i]})
        except KeyError:
            logger.error("Error in creating JSON for multicast setting")
        pprint(json_input)
        if 'action' in kwargs.keys():
            if kwargs['action'] == 'add':
                customlists_resp = self.fw.api_post(self.url, msg, data=json_input)
                return customlists_resp
            else:
                customlists_resp = self.fw.api_delete(self.url, msg, data=json_input)
                return customlists_resp
        else:
            logger.error("please specify the action")

    def config_ssl_control(self, msg=False, **kwargs):
        self.options = dict(SslcontrolApi.default_sslcontrol_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_sslcontrol_json)
            json_input['ssl_control']['enable'] = kwargs['enable']
            json_input['ssl_control']['action'] = kwargs['action']
            json_input['ssl_control']['blacklist'] = kwargs['blacklist']
            json_input['ssl_control']['whitelist'] = kwargs['whitelist']
            json_input['ssl_control']['detect']['ssl_v2'] = kwargs['detect_ssl_v2']
            json_input['ssl_control']['detect']['ssl_v3'] = kwargs['detect_ssl_v3']
            json_input['ssl_control']['detect']['weak_ciphers'] = kwargs['detect_weak_ciphers']
            json_input['ssl_control']['detect']['self_signed'] = kwargs['detect_self_signed']
            json_input['ssl_control']['detect']['weak_digest_cert'] = kwargs['detect_weak_digest_cert']
            json_input['ssl_control']['detect']['expired'] = kwargs['detect_expired']
            json_input['ssl_control']['detect']['untrusted_ca'] = kwargs['detect_untrusted_ca']
            json_input['ssl_control']['detect']['tls_v1'] = kwargs['detect_tls_v1']
        except KeyError:
            logger.error("Error in creating JSON for multicast setting")
        pprint(json_input)
        ssl_control_resp = self.fw.api_put(self.url, msg, data=json_input)
        return ssl_control_resp
    
    def config_custom_lists(self, msg=False, **kwargs):
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_customlists_json)
            if 'action' in kwargs:
                if kwargs['action'] == 'add':
                    logger.info(json_input)
                    logger.info('========================================')
                    if 'black_name' in kwargs:
                        for name in kwargs['black_name']:
                            json_input['ssl_control']['blacklist_certificate'].append({"common_name": name})
                        del  json_input['ssl_control']['whitelist_certificate']
                        logger.info(json_input)
                        customlists_resp = self.fw.api_post(self.blacklist, msg, data=json_input)
                        return customlists_resp
                    elif 'white_name' in kwargs :
                        for name in kwargs['white_name']:
                            json_input['ssl_control']['whitelist_certificate'].append({"common_name": name})
                        del  json_input['ssl_control']['blacklist_certificate']
                        logger.info(json_input)
                        customlists_resp = self.fw.api_post(self.whitelist, msg, data=json_input)
                        return customlists_resp
                elif kwargs['action'] == 'edit':
                    logger.info(json_input)
                    logger.info('========================================')
                    white_used_new_names = []
                    black_used_new_names = []
                    if 'black_old_name' in kwargs:
                        for old_name, new_name in zip(kwargs['black_old_name'], kwargs['black_new_name']):
                            json_input = copy.deepcopy(json_input)
                            json_input['ssl_control'].pop('whitelist_certificate', None)
                            url = f"{self.blacklist}/common-name/{old_name}"
                            json_input['ssl_control']['blacklist_certificate'].append({"common_name": new_name})

                            if black_used_new_names:
                                blacklist_certificates = json_input["ssl_control"]["blacklist_certificate"]
                                json_input["ssl_control"]["blacklist_certificate"] = [
                                    cert for cert in blacklist_certificates if cert["common_name"] != black_used_new_names[-1]
                                ]
                            logger.info(json_input)
                            customlists_resp = self.fw.api_put(url, msg, data=json_input)
                            black_used_new_names.append(new_name)  
                        return customlists_resp

                    elif 'white_old_name' in kwargs :
                        for old_name, new_name in zip(kwargs['white_old_name'], kwargs['white_new_name']):
                            json_input = copy.deepcopy(json_input)
                            json_input['ssl_control'].pop('blacklist_certificate', None)
                            url = f"{self.whitelist}/common-name/{old_name}"
                            json_input['ssl_control']['whitelist_certificate'].append({"common_name": new_name})

                            if white_used_new_names:
                                whitelist_certificates = json_input["ssl_control"]["whitelist_certificate"]
                                json_input["ssl_control"]["whitelist_certificate"] = [
                                    cert for cert in whitelist_certificates if cert["common_name"] != white_used_new_names[-1]
                                ]
                            logger.info(json_input)
                            customlists_resp = self.fw.api_put(url, msg, data=json_input)
                            white_used_new_names.append(new_name)  
                        return customlists_resp

                else:
                    if 'black_name' in kwargs:
                        for name in kwargs['black_name']:
                            json_input['ssl_control']['blacklist_certificate'].append({"common_name": name})
                        del  json_input['ssl_control']['whitelist_certificate']
                        logger.info(json_input)
                        customlists_resp = self.fw.api_delete(self.blacklist, msg, data=json_input)
                        return customlists_resp
                    elif 'white_name' in kwargs :
                        for name in kwargs['white_name']:
                            json_input['ssl_control']['whitelist_certificate'].append({"common_name": name})
                        del  json_input['ssl_control']['blacklist_certificate']
                        logger.info(json_input)
                        customlists_resp = self.fw.api_delete(self.whitelist, msg, data=json_input)
                        return customlists_resp
            else:
                logger.error("please specify the action")     
        except KeyError:
            logger.error("Error in creating JSON for multicast setting")

class CipherctrlApi:
    '''CipherctrlApi class'''

    default_cipherssh_options = {
        "key_exchange":{
            "diffie_hellman_group1_sha1":True,
            "diffie_hellman_group14_sha1":True,
            "diffie_hellman_group_exchange_sha1":True,
            "diffie_hellman_group_exchange_sha256":True,
            "ecdh_sha2_nistp256":True,
            "ecdh_sha2_nistp384":True,
            "ecdh_sha2_nistp521":True,
            },
        "public_key":{
            "ssh_rsa":True,
            "rsa_sha2_256":True,
            "rsa_sha2_512":True,
        },
        "encryption":{
        "aes128_ctr":True,
        "aes192_ctr":True,
        "aes256_ctr":True,
        "aes128_gcm":True,
        "aes256_gcm":True,
        "chacha20_poly1305":True,
        },
         "mac":{
        "hmac_sha1":True,
        "hmac_sha2_256":True,
        "hmac_sha2_512":True
         }
    }
    
    def __init__(self, fw):
        self.fw = fw
        self.sshcipher = 'api/sonicos/cipher-control/ssh'
        self.tlsciphers = 'api/sonicos/cipher-control/tls-ciphers'
        self.tlscipher_list = 'api/sonicos/reporting/cipher-control/tls-cipher-list'
        self.initial_cipherssh_json = {
        "cipher_control":
                {
                    "ssh":{
                        "key_exchange":{
                            "diffie_hellman_group1_sha1":True,
                            "diffie_hellman_group14_sha1":True,
                            "diffie_hellman_group_exchange_sha1":True,
                            "diffie_hellman_group_exchange_sha256":True,
                            "ecdh_sha2_nistp256":True,
                            "ecdh_sha2_nistp384":True,
                            "ecdh_sha2_nistp521":True
                            },
                        "public_key":{
                            "ssh_rsa":True,
                            "rsa_sha2_256":True,
                            "rsa_sha2_512":True
                            },
                        "encryption":{
                            "aes128_ctr":True,
                            "aes192_ctr":True,
                            "aes256_ctr":True,
                            "aes128_gcm":True,
                            "aes256_gcm":True,
                            "chacha20_poly1305":True
                            },
                        "mac":{
                            "hmac_sha1":True,
                            "hmac_sha2_256":True,
                            "hmac_sha2_512":True
                            }
                        }
                    }
                }

        self.initial_cipher_tls_json = {
            "cipher_control": {
                "tls": {
                    "cipher": [
                        {
                            "name": "",
                            "block": False
                        }
                    ]
                }
            }
        }

        
    def block_unblock_tls_cipher(self, msg=False, **kwargs):
        json_input = copy.deepcopy(self.initial_cipher_tls_json)
        logger.info(json_input)
        json_input["cipher_control"]["tls"]["cipher"][0]["name"] = kwargs["name"]
        json_input["cipher_control"]["tls"]["cipher"][0]["block"] = kwargs["block"]
        resp = self.fw.api_put(self.tlsciphers, msg, data=json_input)
        return resp

    def block_unblock_multiple_tls_ciphers(self, msg=False, **kwargs):
        json_input = kwargs
        logger.info(json_input)
        resp = self.fw.api_put(self.tlsciphers, msg, data=json_input)
        return resp
    
    def block_tlscipher(self, cipher_name, msg=False):
        url = 'api/sonicos/cipher-control/tls/cipher/' + cipher_name
        output = self.fw.api_delete(url)
        return output

    def unblock_tlscipher(self, cipher_name, msg=False):
        url = 'api/sonicos/cipher-control/tls/cipher/' + cipher_name
        output = self.fw.api_post(url)
        return output

    def show_ssh_cipher(self):
        response = self.fw.api_get(self.sshcipher)
        return response
   
    def show_tls_ciphers(self):
        response = self.fw.api_get(self.tlsciphers)
        return response
    
    def show_tls_cipher_list(self):
        response = self.fw.api_get(self.tlscipher_list)
        return response
    
    def edit_sshcipher_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        response = self.fw.api_put(self.sshcipher, msg, data=json_input)
        return response

    def config_cipher_ssh(self,msg=False,**kwargs):
        url =  'api/sonicos/cipher-control/ssh'
        options = dict(CipherctrlApi.default_cipherssh_options)
        options.update(kwargs)
        kwargs = options
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_cipherssh_json)
            for key in kwargs:
                for sub_key in kwargs[key]:
                    # logger.info(f'----{key}---{sub_key}')
                    json_input['cipher_control']['ssh'][key][sub_key]=kwargs[key][sub_key]
            logger.info(json_input)
        except Exception as e:
            logger.error(f'----{e}---')
            logger.error("Error in creating JSON for cipher control ssh setting")
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp


class QosmappingApi:
    '''QosmappingApi class'''
    default_qos_options = {
        0: {'from_dscp': {'begin': 0, 'end': 7}, 'to_dscp': 0},
        1: {'from_dscp': {'begin': 8, 'end': 15},'to_dscp': 8},
        2: {'from_dscp': {'begin': 16, 'end': 23},'to_dscp': 16},
        3: {'from_dscp': {'begin': 24, 'end': 31},'to_dscp': 24},
        4: {'from_dscp': {'begin': 32, 'end': 39},'to_dscp': 32},
        5: {'from_dscp': {'begin': 40, 'end': 47},'to_dscp': 40},
        6: {'from_dscp': {'begin': 48, 'end': 55},'to_dscp': 48},
        7: {'from_dscp': {'begin': 56, 'end': 63},'to_dscp': 56},
    }

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/qos-mapping/base'
        self.url = 'api/sonicos/qos-mapping/settings'
        self.initial_qos_json = {'qos_mappings': [
                  {'cos': 0,
                   'from_dscp': {'begin': 0, 'end': 7},
                   'to_dscp': 0},
                  {'cos': 1,
                   'from_dscp': {'begin': 8, 'end': 15},
                   'to_dscp': 8},
                  {'cos': 2,
                   'from_dscp': {'begin': 16, 'end': 23},
                   'to_dscp': 16},
                  {'cos': 3,
                   'from_dscp': {'begin': 24, 'end': 31},
                   'to_dscp': 24},
                  {'cos': 4,
                   'from_dscp': {'begin': 32, 'end': 39},
                   'to_dscp': 32},
                  {'cos': 5,
                   'from_dscp': {'begin': 40, 'end': 47},
                   'to_dscp': 40},
                  {'cos': 6,
                   'from_dscp': {'begin': 48, 'end': 55},
                   'to_dscp': 48},
                  {'cos': 7,
                   'from_dscp': {'begin': 56, 'end': 63},
                   'to_dscp': 56}]}

    def show_qosmapping(self):
        output = self.fw.api_get(self.url)
        return output

    def config_qosmapping(self, msg=False, **kwargs):
        """
        this def is used to config the default 802.1p Class Of Service of QoS Marking
        key <cos> in kwargs is necessary!
        exp:
        opt = {
            "cos": 4,
            "to_dscp": 43
        }
        """
        json_input = {'qos_mappings': [{}]}
        if 'cos' not in kwargs:
            logger.error("key <cos> is necessary")
            return False
        json_input['qos_mappings'][0].update(QosmappingApi.default_qos_options[kwargs['cos']])
        json_input['qos_mappings'][0].update(kwargs)
        print(json_input)
        return self.fw.api_put(self.base_url, msg, data = json_input)

    def reset_qosmapping(self):
        url = 'api/sonicos/qos-mapping/reset'
        output = self.fw.api_put(url)
        return output

    def get_all_qos_mapping(self):
        return self.fw.api_get(self.base_url)
    
    def get_qos_mapping_by_cos_value(self, cos_value=0):
        '''
        return example:
        {"cos": 4, "to_dscp": 43, "from_dscp": {"begin": 32, "end": 39}}
        '''
        resp = self.get_all_qos_mapping()
        try:
            for qos_mapping in resp["qos_mappings"]:
                if cos_value == qos_mapping["cos"]:
                    return qos_mapping
            else:
                logger.error(f'not found the cos <{cos_value}> qos mapping')
                return False
        except Exception as e:
            return False
