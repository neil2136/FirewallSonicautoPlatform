import copy
import json
import re
import ipaddress
import sys
import os
from netaddr import IPAddress
from collections import OrderedDict
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from runner.settings import logger
from runner.utils.assertion import Assertion
import time
from utm import Firewall


class WirelessApi:
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos'
        self.wire_settings = 'api/sonicos/wireless/radio'
        self.wire_settings_ui8 = 'api/sonicos/wireless/v2/base'
        self.ids = 'api/sonicos/wireless/ids/base'
        self.wire_status = 'api/sonicos/reporting/wireless/status'
        self.station_status = 'api/sonicos/reporting/wireless/stations'
        self.macfilter_list = 'api/sonicos/address-objects/mac'
        self.vap_object = 'api/sonicos/wireless/virtual-access-point/objects'
        self.vap_groups_ui8 = 'api/sonicos/wireless/virtual-access-point/groups'
        self.vap_groups = 'api/sonicos/wireless/virtual-access-point/groups/name'


        self.initial_settings_json = {
            "wireless":{
                "radio_role":{
                    "access_point":{
                        "ssid":"sonicwall-2B08",
                        "wds":False,
                        "enable":False,
                        "country_code":"United States-US",
                        "radio":{
                            "mode":{"ngb_mixed":True},
                            "band":"auto"
                        },
                        "channel":{"primary":"auto","secondary":"auto"},
                        # "short_guard_interval": False,
                        # "aggregation": False,
                        "virtual_access_point":{"group":""}
                    }
                }
            }
        }
        self.initial_mesh_json = {
            "wireless": {
                "radio_role": {
                    "access_point_mesh": {
                        "ssid": "sonicwall-2B08",
                        "wds": False,
                        "enable": False,
                        "schedule": {
                            "always_on": True
                        },
                        "country_code": "United States-US",
                        "radio":{
                            "mode":{"ngb_mixed":False},
                            "band":"auto"
                        },
                        "channel":{ "primary": "auto","secondary": "auto"},
                        "short_guard_interval": False,
                        "aggregation": False,
                        "dfs_channel": False,
                        "virtual_access_point": {
                            "group": ""
                        }
                    }
                }
            }
        }
        self.initial_advanced_json = {
            "wireless": {
                "radio_role": {
                    "access_point_mesh": {
                        "enable": False,
                        "dfs_channel": False,
                        "ssid": "sonicwall-2B08",
                        "schedule": {
                            "always_on": False
                        },
                        "country_code": "United States-US",
                        "radio": {
                            "mode": {
                                "ngb_mixed": False
                            },
                            "band": "auto"
                        },
                        "channel": {
                            "primary": "auto",
                            "secondary": "auto"
                        },
                        "short_guard_interval": False,
                        "aggregation": False,
                        "wds": False,
                        "virtual_access_point": {
                            "group": ""
                        },
                        "hide_ssid": False,
                        "interval": {
                            "beacon": 200,
                            "dtim": 1
                        },
                        "green_ap": {
                            "enable": False,
                            "timeout": 20
                        },
                        "ieee802_11r": False,
                        "ftoverds": False,
                        "ftmixmode": False,
                        "bsstransmgmt": False,
                        "wnmsleep": False,
                        "short_slot_time": False,
                        "antenna_diversity": "best",
                        "transmit_power": "full",
                        "preamble_length": "long",
                        "threshold": {
                            "fragmentation": 2346,
                            "rts": 2346
                        },
                        "association_timeout": 300,
                        "max_clients": 128,
                        "data_rate": "best",
                        "protection": {
                            "mode": {
                                "auto": False
                            },
                            "rate": "11",
                            "type": "cts-only"
                        },
                        "access_list": {
                            "enable": False,
                            "allow": {
                                "all": False
                            },
                            "deny": {}
                        },
                        "authentication_type": {
                            "wpa2": {
                                "auto": "psk"
                            }
                        },
                        "wpa": {
                            "cipher_type": "auto",
                            "group_key": {
                                "update": {
                                    "interval": 86400
                                }
                            },
                            "passphrase": "6,fb85d4d5a771e8db00bff579623bc9a0fe7adde92d2b6925301f1832d14341630b8bc08df700d5820e477e93e92591b069f91651f3a6c8c4a3eb06db2a49e6267b20269e572b5b9392448a7b027e240cdd2f4cdfc1ac36b70babd14f6c8dced2"
                        },
                        "eapol_version": "v2"
                    }
                }
            }
        }
        self.initial_vap_json = {
            "wireless": {
                "virtual_access_point": {
                    "object": [
                        {
                            "name": "",
                            "max_clients": 16,
                            "ssid": "",
                            "vlan_id": "",
                            "suppress_ssid": False,
                            "enable": True,
                            "wds": False,
                            "profile": {},
                            "allow_b": False,
                            "radio_type": "wireless",
                            "schedule": {
                                "always_on": True
                            },
                            "access_list": {
                                "mac_filter_list": False,
                                "use_global_access_list": False,
                                "allow": {
                                    "all": True
                                },
                                "deny": {}
                            },
                            'authentication_type': {
                                "wpa2": {
                                    "auto": "psk"
                                }
                            },
                            "wpa": {
                                "passphrase": "",
                                "group_key_interval": 86400
                            }, 
                            "cipher_type": {"auto": True},
                            "80211r": {
                                "enable": False,
                                "ft_over_ds": False,
                                "mix_mode": False
                            },
                            "80211v": {
                                "bss_trans_mgmt": False,
                                "wnm_sleep": False
                            }
                        }
                    ]
                }
            }
        }
        self.initial_vap_group_json = {
            "wireless": {
                "virtual_access_point": {
                    "group": [
                        {
                            "name": "Internal AP Group",
                            "virtual_access_point": [
                                {
                                    "name": "sonicwall-2B08"
                                },
                            ]
                        }
                    ]
                }
            }
        }
    def get_ids_settings(self):
        response = self.fw.api_get(self.ids)
        return response

    def get_wireless_station_status(self):
        response = self.fw.api_get(self.station_status)
        return response

    def get_wireless_status(self):
        response = self.fw.api_get(self.wire_status)
        return response

    def get_mac_filter_list(self):
        response = self.fw.api_get(self.macfilter_list)
        return response

    def get_vap_groups(self):
        url = self.url + '/wireless/virtual-access-point/groups'
        response = self.fw.api_get(url)
        return response

    # add_by_jlian
    def get_vap(self):
        url = self.vap_object
        response = self.fw.api_get(url)
        return response

    # add by JLian
    def get_wireless_settings_ui8(self):
        url = self.wire_settings_ui8
        response = self.fw.api_get(url)
        return response

    def post_vap_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url = self.url + '/wireless/virtual-access-point/profiles'
        response = self.fw.api_post(url, msg, data=json_input)
        return response

    def delete_vap_profile(self, name, msg=False):
        url = self.url + '/wireless/virtual-access-point/profiles/' + 'name' + '/' + name
        response = self.fw.api_delete(url, msg)
        return response

    def ids_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.ids, msg, data=json_input)
        return resp

    # add by JLian
    def delete_vap_object_by_name(self, name:str, msg=False):
        if not name or name.strip() == "":
            logger.error('vap object name must be defined')
            return (False, {}) if msg else False
        name = name.strip().replace(' ', '%20')
        url = self.vap_object + '/name' + '/' + name
        response = self.fw.api_delete(url, msg)
        return response

    # add by JLian
    def delete_vap_groups_by_name(self, name: str, msg=False):
        if not name or name.strip() == "":
            logger.error('vap group name must be defined')
            return (False, {}) if msg else False
        name = name.strip().replace(' ', '%20')
        url = self.vap_groups + '/' + name
        response = self.fw.api_delete(url, msg)
        return response

    def build_json_wireless(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_settings_json)
        if 'ssid' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['ssid'] = kwargs['ssid']
        if 'wds' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['wds'] = kwargs['wds']
        if 'enable' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['enable'] = kwargs['enable']
        if 'country_code' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['country_code'] = kwargs['country_code']
        if 'mode' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['radio']['mode'] = kwargs['mode']
        if 'access_list' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['access_list'] = kwargs['access_list']
        if 'aggregation' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['aggregation'] = kwargs['aggregation']
        if 'short_guard_interval' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['short_guard_interval'] = kwargs['short_guard_interval']
        return json_input
    
    def build_mesh_wireless(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_mesh_json)
        if 'ssid' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['ssid'] = kwargs['ssid']
        if 'wds' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['wds'] = kwargs['wds']
        if 'enable' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['enable'] = kwargs['enable']
        if 'country_code' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['country_code'] = kwargs['country_code']
        if 'mode' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['radio']['mode'] = kwargs['mode']
        if 'band' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['radio']['band'] = kwargs['band']
        if 'channel' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['channel'] = kwargs['channel']
        if 'short_guard_interval' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['short_guard_interval'] = kwargs['short_guard_interval']
        if 'aggregation' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['aggregation'] = kwargs['aggregation']
        if 'dfs_channel' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['dfs_channel'] = kwargs['dfs_channel']
        if 'virtual_access_point' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point_mesh']['virtual_access_point'] = kwargs['virtual_access_point']
        return json_input


    def config_radio_settings(self, msg=False, **kwargs):
        json_input = self.build_json_wireless(**kwargs)
        url = self.url + '/wireless/radio'
        response = self.fw.api_put(url, msg, data=json_input)
        return response
    
    
    def change_radio_settings_with_payload_key(self, radio_role="access_point",msg=False ,**kwargs):
        radio_settings = self.get_radio_settings()
        radio_json= copy.deepcopy(radio_settings)
        if radio_role != "access_point":
            radio_json["wireless"]["radio_role"]={}
            radio_json["wireless"]["radio_role"][radio_role]={}
            radio_json["wireless"]["radio_role"][radio_role].update(kwargs)
        else:
            radio_json["wireless"]["radio_role"][radio_role].update(kwargs)
        url = self.url + '/wireless/radio'
        response = self.fw.api_put(url, msg, data=radio_json)
        return response


    def get_radio_settings(self):
        url = self.url + '/wireless/radio'
        response = self.fw.api_get(url)
        return response

    def get_ap_wireless_settings(self):
        url = self.url + '/reporting/wireless/mix-mode/status/ap'
        response = self.fw.api_get(url)
        return response

    def config_internal_mesh_settings(self, msg=False, **kwargs):
        json_input = self.build_mesh_wireless(**kwargs)
        url = self.url + '/wireless/radio'
        response = self.fw.api_put(url, msg, data=json_input)
        return response
    
    def config_radio_mesh_settings(self, msg=False, **kwargs):
        json_input = self.get_radio_settings()
        logger.info(json_input)
        url = self.url + '/wireless/radio'
        if 'ieee802_11r' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['ieee802_11r'] = kwargs['ieee802_11r']
        if 'bsstransmgmt' in kwargs.keys():
            json_input['wireless']['radio_role']['access_point']['bsstransmgmt'] = kwargs['bsstransmgmt']
        logger.info(r'======='*10)
        logger.info(json_input)
        response = self.fw.api_put(url, msg, data=json_input)
        return response

    def add_virtual_access_point_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(self.initial_vap_json)
        logger.info(json_input)
        if 'vap_name' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['name'] = kwargs['vap_name']
        if 'vap_ssid' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['ssid'] = kwargs['vap_ssid']
        if 'vap_vlan' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['vlan_id'] = kwargs['vap_vlan']
        if 'wpa_password' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['wpa']['passphrase']= kwargs['wpa_password']
        logger.info(json_input)
        response = self.fw.api_post(self.vap_object, msg, data=json_input)
        return response

    def config_virtual_access_point_group(self, msg=False, **kwargs):
        try:
            base_dict = kwargs['wireless']['virtual_access_point']['group'][0]
            if 'name' in base_dict.keys():
                name = base_dict['name'].replace(' ', '%20')
            else:
                logger.error('the key: name must be exist in kwargs.')
                return (False, {}) if msg else False
            url = self.vap_groups + '/{}'.format(name)
            logger.info(url)
            res = self.fw.api_put(url, msg, data=kwargs)
            return res
        except Exception as e:
            logger.error(repr(e))
            logger.error('the kwargs was not a valid vap group json')
            return (False, {}) if msg else False

    # add by JLian
    def config_virtual_access_point_group_ui8(self, msg=False, **kwargs):
        # kwargs = {
        #     "name": "customvapgroup2",
        #     "virtual_access_point": [
        #         {
        #             "name": "vap20"
        #         }
        #     ],
        #     "group": [
        #         {
        #             "name": "customvapgroup1"
        #         }
        #     ]
        # }
        try:
            group_config_dict = {"wireless": {"virtual_access_point": {"group": [kwargs]}}}
            if 'name' not in kwargs.keys():
                logger.error('the key: name must be exist in kwargs.')
                return (False, {}) if msg else False
            url = self.vap_groups_ui8
            logger.info(url)
            res = self.fw.api_post(url, msg, data=group_config_dict)
            return res
        except Exception as e:
            logger.error(repr(e))
            logger.error('the kwargs was not a valid vap group json')
            return (False, {}) if msg else False
            
    def get_discovered_ap(self):
        url = self.url + '/reporting/wireless/discovered-access-points'
        response = self.fw.api_get(url)
        print(response)
        return response

    def scan(self):
        url = self.url + '/wireless/ids/scan'
        response = self.fw.api_post(url)
        print(response)

    def wireless_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.wire_settings, msg, data=json_input)
        return resp
        

if __name__ == '__main__':
    firewall_ip = '192.168.168.168'
    fw = Firewall(firewall_ip, user='admin', password='password')
    wireless = Wireless(fw)
    #wireless.scan()
    #time.sleep(5)
    #wireless.get_discovered_ap()
    settings = {
        'ssid': 'terry-wireless-internal'
    }
    settings = {
        'access_list': {
            'allow':{
                'all':True,
            },
            'deny':{}
        
        }
    }
    wireless.config_radio_settings(**settings)
