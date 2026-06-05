import copy
import json
import re
import ipaddress
import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from netaddr import IPAddress
from collections import OrderedDict
from runner.settings import logger
from runner.utils.assertion import Assertion
from utm import Firewall


class AccessPointApi:
    """AccessPointApi class"""
    """
    default_options = {
        'enable': True,
        'name': "SonicWave 231o e9479d",
        'radius_server1_ip': "0.0.0.0",
        'radius_server1_port': 1812,
        'radius_server1_secret': "",
        'radius_server2_ip': "0.0.0.0",
        'radius_server2_port': 1812,
        'radius_server2_secret': "",
        'account_server1_ip': "0.0.0.0",
        'account_server1_port': 1812,
        'account_server1_secret': "",
        'account_server2_ip': "0.0.0.0",
        'account_server2_port': 1812,
        'account_server2_secret': "",

        'country_code': "United Kingdom",
        'band_steering': {},
        'sslvpn_server': "",
        'sslvpn_user': "",
        'sslvpn_pass': "",
        'sslvpn_domain': "",
        'admin_name': "",
        'admin_pass': "",
        '5g_radio': True,
        '5g_mode': "ac-na-mixed",
        '5g_ssid': "sonicwall-terry",
        '5g_radio_band': "auto",
        '5g_auth_type': "wep",
        '5g_wep_mode': "none",
        '5g_hide_ssid': False,
        '5g_ids_scan': {},
        '5g_min_data_rate': "best",
        '5g_transmit_power': "full",
        '5g_beacon_interval': 100,
        '5g_dtim_interval': 1,
        '5g_rts_threshold': -95,
        '5g_max_clients': 32,
        '5g_inactive_timeout': "",
        '5g_enable_wds': False,
        '5g_enable_green': False,
        '5g_enable_rssi': False,
        '5g_enable_air_time_fairness':False,
        '5g_enable_802.11r': False,
        '5g_enable_neighbour_report': "",
        '5g_enable_bss': False,
        '5g_enable_wnm_sleep': False
        '2g_radio': "",
        '2g_mode': "",
        '2g_ssid': "",
        '2g_radio_band': "",
        '2g_radio_band': "",
        '2g_primary_channel': "",
        '2g_secondary_channel': "",
        '2g_enable_short_guard_interval': "",
        '2g_enable_aggregation': "",
        '2g_auth_type': "",
        '2g_wep_mode': "",
        '2g_enable_mac_access_control': "",
        '2g_hide_ssid': "",
        '2g_ids_scan': "",
        '2g_min_data_rate': "",
        '2g_transmit_power': "",
        '2g_beacon_interval': "",
        '2g_dtim_interval': "",
        '2g_rts_threshold': "",
        '2g_max_clients': "",
        '2g_inactive_timeout': "",
        '2g_preamble_length': "",
        '2g_protection_type': "",
        '2g_protection_rate': "",
        '2g_protection_type': "",
        '2g_enable_wds': True,
        '2g_enable_green': true,
        '2g_enable_rssi': "",
        '2g_enable_air_time_fairness':"",
        '2g_enable_802.11r': "",
        '2g_enable_neighbour_report': "",
        '2g_enable_bss': "",
        '2g_enable_wnm_sleep': "",
        'enable_widp_sensor': "",
        'enable_advertisment': "",
        'enable_ibeacon': "",
    }
    """

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/sonicpoint'
        self.discover_ap = 'api/sonicos/reporting/sonicpoint/discovered-access-points'
        self.schedule = 'api/sonicos/schedules'
        self.sp_object = 'api/sonicos/sonicpoint/sonicpoints'
        self.rep_url = 'api/sonicos/reporting/sonicpoint'
        
        
        self.init_sonic_profile = {
            "sonicpoint": {
                "profile": [{
                    "wave2": {"name_prefix": "SonicWave"},
                    "enable": True,
                    "radius": {
                        "retries": 4,
                        "retry_interval": {},
                        "server": {
                            "server1": {
                                "ip": "1.1.1.1",
                                "port": {"value": 1812},
                                "secret": "11111111"},
                            "server2": {
                                "ip": "0.0.0.0",
                                "port": {"value": 1812},
                                "secret": "11111111"}
                        },
                        "accouting": {
                            "server1": {
                                "ip": "0.0.0.0",
                                "port": {"value": 1813},
                                "secret": ""},
                            "server2": {
                                "ip": "0.0.0.0",
                                "port": {"value": 1813},
                                "secret": "0"}
                        },
                        "nas": {"identifier": {}, "ip": "0.0.0.0"}
                    },
                    "rf_monitoring": False,
                    "led": True,
                    "country_code": "United States",
                    "eapol_version": "v2",
                    "poe_out": False,
                    "low_power": False,
                    "band_steering": {},
                    "sslvpn": {
                        "server": "",
                        "user_name": "",
                        "password": "",
                        "domain": "",
                        "auto_reconnect": False},
                    "administrator": {"name": "", "password": ""},
                    "retain": {},
                    "radio_2400mhz": {
                        "virtual_access_point": {"group": ""},
                        "enable": False,
                        "ssid": "sonicwall-4D6C-1",
                        "short_guard_interval": True,
                        "aggregation": True,
                        "schedule": {"always_on": True},
                        "band": "auto",
                        "channel": {"primary": "auto", "secondary": "auto"},
                        "mode": {"n_only": True},
                        "access_list": {},
                        "mic_failure": {"acl_blacklist": False, "frequency": 3},
                        "dynamic_vlan": False,
                        "authentication_type": {"wpa3": {"eap_192b": True}},
                        "wpa": {
                            "cipher_type": "gcmp",
                            "group_key_interval": 86400,
                            "auth_balance_method": "remote-radius-only"},
                        "hide_ssid": False,
                        "data_rate": "best",
                        "transmit_power": "full",
                        "interval": {"beacon": 100, "dtim": 1},
                        "threshold": {"rts": 2346},
                        "max_clients": 32,
                        "station_inactivity_timeout": 300,
                        "wmm": "",
                        "airtime_fairness": False,
                        "wds_ap": False,
                        "green_ap": {"enable": False, "timeout": 20},
                        "ids_scan": {"schedule": {}},
                        "rssi": {"enable": False, "threshold": -95},
                        "80211r": {
                            "enable": False,
                            "ft_over_ds": False,
                            "mix_mode": False},
                        "80211k": {"neighbour_report": False},
                        "80211v": {
                            "bss_trans_mgmt": False,
                            "wnm_sleep": False},
                        "preamble_length": "long"
                    },
                    "radio_5000mhz": {
                        "virtual_access_point": {"group": ""},
                        "enable": True,
                        "ssid": "sonicwall-4D6C",
                        "short_guard_interval": True,
                        "aggregation": True,
    #                    "remote_mac_access_control": False,
                        "schedule": {"always_on": True},
                        "band": "40",
                        "channel": {"primary": "40", "secondary": "auto"},
                        "dfs_channel": False, "mode": {"5000mhz": "na-mixed"},
                        "access_list": {},
                        "mic_failure": {
                            "acl_blacklist": False,
                            "frequency": 3},
                        "authentication_type": {"wep": "both"},
                        "wep_key": {"type": "none"},
                        "hide_ssid": False,
                        "data_rate": "best",
                        "transmit_power": "full",
                        "interval": {"beacon": 100, "dtim": 1},
                        "threshold": {"rts": 2346},
                        "max_clients": 32,
                        "station_inactivity_timeout": 300,
                        "wmm": "",
                        "airtime_fairness": False,
                        "wds_ap": False,
                        "green_ap": {"enable": False, "timeout": 20},
                        "ids_scan": {"schedule": {}},
                        "rssi": {"enable": False, "threshold": -95},
                        "80211r": {
                            "enable": False,
                            "ft_over_ds": False,
                            "mix_mode": False},
                        "80211k": {"neighbour_report": False},
                        "80211v": {"bss_trans_mgmt": False, "wnm_sleep": False}
                    },
                    "widp_sensor": {},
                    "wwan": {"enable": False, "bound_to": ""},
                    "connection_profile": {
                        "enable": False, "country": "",
                        "service_provider": "",
                        "plan_type": "",
                        "dialed_number": "",
                        "user_name": "",
                        "user_password": "",
                        "apn": ""
                    },
                    "ble": {
                        "advertisement": False,
                        "ibeacon": {
                            "enable": False,
                            "uuid": "", "major": {},
                            "minor": {}}
                    },
                    "mesh": {"2400mhz": {"enable": False},
                             "5000mhz": {"enable": False}}
                }]
            }
        }

        self.initial_sonicwave_json = {
            "sonicpoint": {
                "sonicpoint": [{
                    "wave2": {"name": "SonicWave 231o e9479d"},
                    "enable": True,
                    "radius": {
                        "retries": 4,
                        "retry_interval": {},
                        "server": {
                            "server1": {
                                "ip": "0.0.0.0",
                                "port": {"value": 1812},
                                "secret": ""
                            },
                            "server2": {
                                "ip": "0.0.0.0",
                                "port": {"value": 1812},
                                "secret": ""
                            }
                        },
                        "accouting": {
                            "server1": {
                                "ip": "0.0.0.0",
                                "port": {"value": 1813},
                                "secret": ""
                            },
                            "server2": {
                                "ip": "0.0.0.0",
                                "port": {"value": 1813},
                                "secret": ""
                            }
                        },
                        "nas": {"identifier": {}, "ip": "0.0.0.0"}
                    },
                    "rf_monitoring": False,
                    "led": False,
                    "country_code": "United Kingdom",
                    "eapol_version": "v2",
                    #"poe_out": False,
                    "low_power": False,
                    "band_steering": {},
                    "sslvpn": {
                        "server": "",
                        "user_name": "",
                        "password": "",
                        "domain": "",
                        "auto_reconnect": False
                    },
                    "administrator": {
                        "name": "",
                        "password": ""
                    },
                    "retain": {},
                    "radio_2400mhz": {
                        "virtual_access_point": {"group": ""},
                        "enable": True,
                        "ssid": "sonicwall-terry-1",
                        "short_guard_interval": True,
                        "aggregation": True,
        #                "remote_mac_access_control": False,
                        "schedule": {"always_on": True},
                        "band": "auto",
                        "channel": {
                            "primary": "auto",
                            "secondary": "auto"
                        },
                        "mode": {"ngb_mixed": True},
                        "access_list": {},
                        "mic_failure": {"acl_blacklist": False, "frequency": 3},
                #        "authentication_type": {"wep": "both"},
                #        "wep_key": {"type": "none"},
                        "authentication_type": {},
                        "wpa": {},
                        "hide_ssid": False,
                        "data_rate": "best",
                        "transmit_power": "full",
                        "interval": {"beacon": 100, "dtim": 1},
                        "threshold": {"rts": 2346},
                        "max_clients": 32,
                        "station_inactivity_timeout": 300,
                        "wmm": "",
                        "airtime_fairness": False,
                        "wds_ap": False,
                        "green_ap": {"enable": False, "timeout": 20},
                        "ids_scan": {"schedule": {}
                                     },
                        "rssi": {"enable": False, "threshold": -95},
                        "80211r": {"enable": False,
                                   "ft_over_ds": False,
                                   "mix_mode": False},
                        "80211k": {"neighbour_report": False},
                        "80211v": {"bss_trans_mgmt": False, "wnm_sleep": False},
                        "preamble_length": "long",
                        #                    "protection":{"mode":{},"rate":"1","type":"cts-only"},
                        #                    "short_slot_time":False,"deny_b":False},
                    },
                    "radio_5000mhz": {
                        "virtual_access_point": {"group": ""},
                        "enable": True,
                        "ssid": "sonicwall-terry",
                        "short_guard_interval": True,
                        "aggregation": True,
                        #"remote_mac_access_control": False,
                        "schedule": {"always_on": True},
                        "band": "auto",
                        "channel": {
                            "primary": "auto",
                            "secondary": "auto"
                        },
                        #    "channel":{"standard":"auto"},
                        "dfs_channel": False,
                        "mode": {"5000mhz": "na-mixed"},
                        "access_list": {},
                        "mic_failure": {"acl_blacklist": False,
                                        "frequency": 3},
                        #    "authentication_type":{"wep":"both"},
                        #    "wep_key":{"type":"none"},
                        "authentication_type": {},
                        #    "wep_key":{},
                        "wpa": {},
                        "hide_ssid": False,
                        "data_rate": "best",
                        "transmit_power": "full",
                        "interval": {"beacon": 100, "dtim": 1},
                        "threshold": {"rts": 2346},
                        "max_clients": 32,
                        "station_inactivity_timeout": 300,
                        "wmm": "",
                        "airtime_fairness": False,
                        "wds_ap": False,
                        "green_ap": {"enable": False, "timeout": 20},
                        "ids_scan": {"schedule": {}},
                        "rssi": {"enable": False, "threshold": -95},
                        "80211r": {"enable": False,
                                   "ft_over_ds": False,
                                   "mix_mode": False},
                        "80211k": {"neighbour_report": False},
                        "80211v": {"bss_trans_mgmt": False, "wnm_sleep": False}
                    },
                    "widp_sensor": {},
                    "ble": {
                        "advertisement": False,
                        "ibeacon": {
                            "enable": False,
                            "uuid": "",
                            "major": {}, 
                            "minor": {}
                        }
                    }
                }]
            }
        }

        self.initial_sonicwave_firmware_management_json = {
            "sonicpoint": {
                "firmware_management": {
                    "override_download_url": {
                    "sonicpoint": {"n":"","nv":"","ndr":"","ac":""},
                    "sonicwave200":"","sonicwave400":"","sonicwaveax":""
                    }
                }
            }

        }
        self.initial_idp_json = {
            "sonicpoint": {
                "widp": {
                    "enable": True,
                    "authorized_access_point": {
                        "all": True
                    },
                    "rogue_access_point": {
                        "all": True
                    },
                    "unauthorized_access_point": {
                        "any": False,
                        "connected": False
                    },
                    "evil_twin": False,
                    "block_traffic": {},
                    "disassociate": {
                        "rogue": False,
                        "krack": False
                    }
                }
            }
        }

        self.initial_sonicwave_json_vap = {
            "sonicpoint": {
                "sonicpoint": [
                    {
                        "wave2": {
                            "name": "SonicWave 231c 212ae3"
                        },
                        "enable": True,
                        "radius": {
                            "retries": 4,
                            "retry_interval": {},
                            "server": {
                                "server1": {
                                    "ip": "0.0.0.0",
                                    "port": {
                                        "value": 1812
                                    },
                                    "secret": ""
                                },
                                "server2": {
                                    "ip": "0.0.0.0",
                                    "port": {
                                        "value": 1812
                                    },
                                    "secret": ""
                                }
                            },
                            "coa": False,
                            "accouting": {
                                "server1": {
                                    "ip": "0.0.0.0",
                                    "port": {
                                        "value": 1813
                                    },
                                    "secret": ""
                                },
                                "server2": {
                                    "ip": "0.0.0.0",
                                    "port": {
                                        "value": 1813
                                    },
                                    "secret": ""
                                }
                            },
                            "nas": {
                                "identifier": {},
                                "ip": "0.0.0.0"
                            }
                        },
                        "rf_monitoring": False,
                        "led": False,
                        "country_code": "United Kingdom",
                        "eapol_version": "v2",
                        "low_power": False,
                        "dns_proxy": False,
                        "band_steering": {},
                        "sslvpn": {
                            "server": "",
                            "user_name": "",
                            "password": "",
                            "domain": "",
                            "auto_reconnect": False
                        },
                        "administrator": {
                            "name": "",
                            "password": ""
                        },
                        "retain": {},
                        "radio_2400mhz": {
                            "virtual_access_point": {
                                "group": "vap_gp",
                                "wep_key": {
                                    "method": "alphanumeric",
                                    "default": "1",
                                    "key1": {},
                                    "key2": {},
                                    "key3": {},
                                    "key4": {}
                                }
                            },
                            "enable": True,
                            "short_guard_interval": True,
                            "aggregation": True,
                            "band": "auto",
                            "channel": {
                                "primary": "auto",
                                "secondary": "auto"
                            },
                            "mode": {
                                "ngb_mixed": True
                            },
                            "access_list": {
                                "mac_filter_list": False,
                                "allow": {
                                    "all": True
                                },
                                "deny": {}
                            },
                            "mic_failure": {
                                "acl_blacklist": False,
                                "frequency": 3
                            },
                            "data_rate": "best",
                            "transmit_power": "full",
                            "interval": {
                                "beacon": 100,
                                "dtim": 1
                            },
                            "threshold": {
                                "rts": 2346
                            },
                            "max_clients": 32,
                            "station_inactivity_timeout": 300,
                            "wmm": "",
                            "airtime_fairness": False,
                            "wds_ap": False,
                            "green_ap": {
                                "enable": False,
                                "timeout": 20
                            },
                            "ids_scan": {
                                "schedule": {}
                            },
                            "rssi": {
                                "enable": False,
                                "threshold": -95
                            },
                            "80211r": {
                                "enable": False,
                                "ft_over_ds": False,
                                "mix_mode": False
                            },
                            "80211k": {
                                "neighbour_report": False
                            },
                            "80211v": {
                                "bss_trans_mgmt": False,
                                "wnm_sleep": False
                            },
                            "preamble_length": "long",
                            "protection": {
                                "mode": {},
                                "rate": "1",
                                "type": "cts-only"
                            },
                            "short_slot_time": False,
                            "deny_b": False
                        },
                        "radio_5000mhz": {
                            "virtual_access_point": {
                                "group": "vap_gp",
                                "wep_key": {
                                    "method": "alphanumeric",
                                    "default": "1",
                                    "key1": {},
                                    "key2": {},
                                    "key3": {},
                                    "key4": {}
                                }
                            },
                            "enable": True,
                            "short_guard_interval": True,
                            "aggregation": True,
                            "band": "auto",
                            "channel": {
                                "standard": "auto"
                            },
                            "dfs_channel": False,
                            "mode": {
                                "5000mhz": "ac-na-mixed"
                            },
                            "access_list": {
                                "mac_filter_list": False,
                                "allow": {
                                    "all": True
                                },
                                "deny": {}
                            },
                            "mic_failure": {
                                "acl_blacklist": False,
                                "frequency": 3
                            },
                            "data_rate": "best",
                            "transmit_power": "full",
                            "interval": {
                                "beacon": 100,
                                "dtim": 1
                            },
                            "threshold": {
                                "rts": 2346
                            },
                            "max_clients": 32,
                            "station_inactivity_timeout": 300,
                            "wmm": "",
                            "airtime_fairness": False,
                            "wds_ap": False,
                            "green_ap": {
                                "enable": False,
                                "timeout": 20
                            },
                            "ids_scan": {
                                "schedule": {}
                            },
                            "rssi": {
                                "enable": False,
                                "threshold": -95
                            },
                            "80211r": {
                                "enable": False,
                                "ft_over_ds": False,
                                "mix_mode": False
                            },
                            "80211k": {
                                "neighbour_report": False
                            },
                            "80211v": {
                                "bss_trans_mgmt": False,
                                "wnm_sleep": False
                            }
                        },
                        "widp_sensor": {},
                        "wwan": {
                            "enable": False,
                            "bound_to": ""
                        },
                        "connection_profile": {
                            "enable": False,
                            "country": "",
                            "service_provider": "",
                            "plan_type": "",
                            "dialed_number": "",
                            "user_name": "",
                            "user_password": "",
                            "apn": ""
                        },
                        "ble": {
                            "advertisement": False,
                            "ibeacon": {
                                "enable": False,
                                "uuid": "",
                                "major": {},
                                "minor": {}
                            }
                        }
                    }
                ]
            }
        }

    
    
    def get_sonicpoint_profile(self, msg=False):
        url = 'api/sonicos/sonicpoint/profiles'
        response = self.fw.api_get(url)
        return response

    def get_firmware_management(self, msg=False):
        url = 'api/sonicos/sonicpoint/firmware-management'
        response = self.fw.api_get(url)
        return response

    def get_advanced_idp(self):
        url = 'api/sonicos/sonicpoint/widp'
        response = self.fw.api_get(url)
        return response
        
    def _get_auth_wep_none_json(self, json_input, **kwargs):
        if '2g_wep_none' in kwargs.keys():
            json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type']['wep'] = kwargs['2g_wep_none']
            json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key'] = {
                'type': 'none'}
            if kwargs['2g_wep_none'] == 'open-system':
                if "wep_key" in json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz'].keys():
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key']
                if "wpa" in json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz'].keys():
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wpa']
        if '5g_wep_none' in kwargs.keys():
            json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type']['wep'] = kwargs['5g_wep_none']
            json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key'] = {
                'type': 'none'}
            if kwargs['5g_wep_none'] == 'open-system':
                if "wep_key" in json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz'].keys():
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key']
                if "wpa" in json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz'].keys():
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wpa']

    def _get_auth_wep_json(self, json_input, **kwargs):
        "if wep key is not both and none"
        try:
            if '2g_wep' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type']['wep'] = kwargs['2g_wep']
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key'] = {}
            if '2g_wep_type' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key']['type'] = kwargs['2g_wep_type']
            if '2g_wep_method' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key']['method'] = kwargs['2g_wep_method']
            if '2g_wep_default' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key']['default'] = kwargs['2g_wep_default']
            if '2g_wep_pass_1' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key']['key1'] = {
                    'value': kwargs['2g_wep_pass_1']}
            if '2g_wep_pass_2' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key']['key2'] = {
                    'value': kwargs['2g_wep_pass_2']}
            if '2g_wep_pass_3' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key']['key3'] = {
                    'value': kwargs['2g_wep_pass_3']}
            if '2g_wep_pass_4' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wep_key']['key4'] = {
                    'value': kwargs['2g_wep_pass_4']}
            if '5g_wep' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type']['wep'] = kwargs['5g_wep']
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key'] = {}
            if '5g_wep_type' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key']['type'] = kwargs['5g_wep_type']
            if '5g_wep_method' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key']['method'] = kwargs['5g_wep_method']
            if '5g_wep_default' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key']['default'] = kwargs['5g_wep_default']
            if '5g_wep_pass_1' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key']['key1'] = {
                    'value': kwargs['5g_wep_pass_1']}
            if '5g_wep_pass_2' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key']['key2'] = {
                    'value': kwargs['5g_wep_pass_2']}
            if '5g_wep_pass_3' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key']['key3'] = {
                    'value': kwargs['5g_wep_pass_3']}
            if '5g_wep_pass_4' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wep_key']['key4'] = {
                    'value': kwargs['5g_wep_pass_4']}
        except KeyError:
            logger.info("Error: In creating JSON for wep auth")

    def _get_wpa_auth_json(self, json_input, auth_type, **kwargs):
        try:
            if '2g_wpa_psk' in auth_type:
                wpa2_psk_json = {"wpa2": {"psk": True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa2_psk_json
            elif '2g_wpa_auto_psk' in auth_type:
                wpa2_auto_psk_json = {"wpa2": {"auto": "psk"}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa2_auto_psk_json
            elif '2g_wpa_eap' in auth_type:
                wpa2_eap_json = {"wpa2": {"eap": True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa2_eap_json
            elif '2g_wpa_auto_eap' in auth_type:
                wpa2_auto_eap_json = {"wpa2": {"auto": "eap"}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa2_auto_eap_json
            elif '2g_wpa3_owe' in auth_type:
                wpa3_owe_json = {"wpa3": {"owe": True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa3_owe_json
                del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wpa']
            elif '2g_wpa3_psk' in auth_type:
                wpa3_psk_json = {"wpa3": {"psk": True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa3_psk_json
            elif '2g_wpa3_eap' in auth_type:
                wpa3_eap_json = {'wpa3': {'eap': True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa3_eap_json
            elif '2g_wpa3_wpa2_psk' in auth_type:
                wpa3_wpa2_psk_json = {'wpa3': {'wpa2_auto': 'psk'}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa3_wpa2_psk_json
            elif '2g_wpa3_wpa2_eap' in auth_type:
                wpa3_wpa2_eap_json = {'wpa3': {'wpa2_auto': 'eap'}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['authentication_type'] = wpa3_wpa2_eap_json
            if '5g_wpa_psk' in auth_type:
                wpa2_psk_json = {"wpa2": {"psk": True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa2_psk_json
            elif '5g_wpa_auto_psk' in auth_type:
                wpa2_auto_psk_json = {"wpa2": {"auto": "psk"}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa2_auto_psk_json
            elif '5g_wpa_eap' in auth_type:
                wpa2_eap_json = {"wpa2": {"eap": True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa2_eap_json
                if 'remote_mac_access_control' in json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz'].keys():
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['remote_mac_access_control']
            elif '5g_wpa_auto_eap' in auth_type:
                wpa2_auto_eap_json = {"wpa2": {"auto": "eap"}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa2_auto_eap_json
                if 'remote_mac_access_control' in json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz'].keys():
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['remote_mac_access_control']
            elif '5g_wpa3_owe' in auth_type:
                wpa3_owe_json = {"wpa3": {"owe": True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa3_owe_json
                del json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wpa']
            elif '5g_wpa3_psk' in auth_type:
                wpa3_psk_json = {"wpa3": {"psk": True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa3_psk_json
            elif '5g_wpa3_eap' in auth_type:
                wpa3_eap_json = {'wpa3': {'eap': True}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa3_eap_json
            elif '5g_wpa3_wpa2_psk' in auth_type:
                wpa3_wpa2_psk_json = {'wpa3': {'wpa2_auto': 'psk'}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa3_wpa2_psk_json
            elif '5g_wpa3_wpa2_eap' in auth_type:
                wpa3_wpa2_eap_json = {'wpa3': {'wpa2_auto': 'eap'}}
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['authentication_type'] = wpa3_wpa2_eap_json
        except KeyError:
            logger.info("Error: In Creating JSON for wpa auth")

    def build_json_sonicwave(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_sonicwave_json)
            if 'enable' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['enable'] = kwargs['enable']
            if 'name' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['wave2']['name'] = kwargs['name']
            if 'country_code' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['country_code'] = kwargs['country_code']
            if 'radius_server1_ip' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radius']['server']['server1']['ip'] = kwargs['radius_server1_ip']
            if 'radius_server1_pass' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radius']['server']['server1']['secret'] = kwargs['radius_server1_pass']
            if 'radius_server2_ip' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radius']['server']['server2']['ip'] = kwargs['radius_server2_ip']
            if 'radius_server2_pass' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radius']['server']['server2']['secret'] = kwargs['radius_server2_pass']
            if 'sslvpn_server' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['sslvpn']['server'] = kwargs['sslvpn_server']
            if 'sslvpn_user' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['sslvpn']['user_name'] = kwargs['sslvpn_user']
            if 'sslvpn_pass' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['sslvpn']['password'] = kwargs['sslvpn_pass']
            if 'sslvpn_domain' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['sslvpn']['domain'] = kwargs['sslvpn_domain']
            if 'admin_name' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['administrator']['name'] = kwargs['admin_name']
            if 'admin_pass' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['administrator']['password'] = kwargs['admin_pass']
            if '5g_radio' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['enable'] = kwargs['5g_radio']
            if '5g_mode' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['mode']['5000mhz'] = kwargs['5g_mode']
                if kwargs['5g_mode'] == 'a-only':
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['band']
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['short_guard_interval']
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['aggregation']
                    if kwargs['5g_channel']:
                        json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['channel'] = {
                            "standard": kwargs['5g_channel']}
                    else:
                        json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['channel'] = {
                            "standard": "auto"}
                elif 'ac' in kwargs['5g_mode']:
                    json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['channel'] = {
                        "standard": "auto"}
                elif '5g_radio_band' in kwargs.keys():
                    json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['band'] = kwargs['5g_radio_band']
                    if kwargs['5g_radio_band'] == "20":
                        json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['channel'] = {
                            "standard": "auto"}
                    elif '5g_primary_channel' in kwargs.keys():
                        json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['channel']['primary'] = kwargs['5g_primary_channel']
                    elif '5g_secondary_channel' in kwargs.keys():
                        json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['channel']['secondary'] = kwargs['5g_secondary_channel']
                elif '5g_enable_short_guard_interval' in kwargs.keys():
                    json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['short_guard_interval'] = kwargs['5g_enable_short_guard_interval']
                elif '5g_enable_aggregation' in kwargs.keys():
                    json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['aggregation'] = kwargs['5g_enable_aggregation']
            if '5g_ssid' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['ssid'] = kwargs['5g_ssid']
            self._get_auth_wep_none_json(json_input, **kwargs)
            self._get_auth_wep_json(json_input, **kwargs)
            if 'wpa_auth_type' in kwargs.keys():
                self._get_wpa_auth_json(
                    json_input, kwargs['wpa_auth_type'], **kwargs)
                #if '2g' in kwargs['wpa_auth_type']:
                    #json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wpa'] = {}
                #if '5g' in kwargs['wpa_auth_type']:
                    #json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wpa'] = {}
            if '5g_cipher_type' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wpa']['cipher_type'] = kwargs['5g_cipher_type']
            if '5g_group_key_interval' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wpa']['group_key_interval'] = kwargs['5g_group_key_interval']
            if '5g_passwd' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wpa']['passphrase'] = kwargs['5g_passwd']
            if '5g_pmf' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wpa']['pmf'] = kwargs['5g_pmf']
            if '5g_auth_method' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wpa']['auth_balance_method'] = kwargs['5g_auth_method']
            if '5g_wep_mode' in kwargs.keys():
                pass
            if '5g_hide_ssid' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['hide_ssid'] = kwargs['5g_hide_ssid']
            if '5g_ids_scan' in kwargs.keys():
                pass
            if '5g_min_data_rate' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['data_rate'] = kwargs['5g_min_data_rate']
            if '5g_transmit_power' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['transmit_power'] = kwargs['5g_transmit_power']
            if '5g_beacon_interval' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['interval']['beacon'] = kwargs['5g_beacon_interval']
            if '5g_dtim_interval' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['interval']['dtim'] = kwargs['5g_dtim_interval']
            if '5g_rts_threshold' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['interval']['dtim'] = kwargs['5g_dtim_interval']
            if '5g_max_clients' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['max_clients'] = kwargs['5g_max_clients']
            if '5g_inactive_timeout' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['station_inactivity_timeout'] = kwargs['5g_inactive_timeout']
            if '5g_enable_wds' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['wds_ap'] = kwargs['5g_enable_wds']
            if '5g_enable_green' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['green_ap']['enable'] = kwargs['5g_enable_green']
            if '5g_enable_rssi' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['rssi']['enable'] = kwargs['5g_enable_rssi']
            if '5g_rssi_threshold' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['rssi']['threshold'] = kwargs['5g_rssi_threshold']
            if '5g_enable_air_time_fairness' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['airtime_fairness'] = kwargs['5g_enable_air_time_fairness']
            if '5g_enable_802.11r' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['80211r']['enable'] = kwargs['5g_enable_802.11r']
            if '5g_enable_neighbour_report' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['80211k']['neighbour_report'] = kwargs['5g_enable_neighbour_report']
            if '5g_enable_bss' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['80211v']['bss_trans_mgmt'] = kwargs['5g_enable_bss']
            if '5g_enable_wnm_sleep' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['80211v']['wnm_sleep'] = kwargs['5g_enable_wnm_sleep']
            if '2g_radio' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['enable'] = kwargs['2g_radio']
            if '2g_primary_channel' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel']['primary'] = kwargs['2g_primary_channel']
            if '2g_secondary_channel' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel']['secondary'] = kwargs['2g_secondary_channel']
            if '2g_auth_type' in kwargs.keys():
                pass
            if '2g_cipher_type' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wpa']['cipher_type'] = kwargs['2g_cipher_type']
            if '2g_group_key_interval' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wpa']['group_key_interval'] = kwargs['2g_group_key_interval']
            if '2g_passwd' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wpa']['passphrase'] = kwargs['2g_passwd']
            if '2g_auth_method' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wpa']['auth_balance_method'] = kwargs['2g_auth_method']
            if '2g_wep_mode' in kwargs.keys():
                pass
            if '2g_enable_mac_access_control' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['remote_mac_access_control'] = kwargs['2g_enable_mac_access_control']
            if '2g_preamble_length' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['preamble_length'] = kwargs['2g_preamble_length']
            if '2g_protection_type' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['protection']['type'] = kwargs['2g_protection_type']
            if '2g_protection_rate' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['protection']['rate'] = kwargs['2g_protection_rate']
            if '2g_protection_mode' in kwargs.keys():
                pass
            if '2g_radio' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['enable'] = kwargs['2g_radio']
            if '2g_mode' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['mode'] = {
                    kwargs['2g_mode']: True}
                if kwargs['2g_mode'] == 'g_only':
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['band']
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['short_guard_interval']
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['aggregation']
                    del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel']
                    json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel'] = {
                        "standard": "auto"}
                elif '2g_radio_band' in kwargs.keys():
                    json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['band'] = kwargs['2g_radio_band']
                    if kwargs['2g_radio_band'] == "20":
                        #json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel'] = {
                            #"standard": "auto"}
                    #else:
                        #json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel']['primary'] = kwargs['2g_primary_channel']
                        #json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel']['secondary'] = kwargs
                        #['2g_secondary_channel']
                        del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel']['primary']
                        del json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel']['secondary']
                        json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel'] = {
                            "standard": kwargs['2g_channel']}
                elif '2g_enable_short_guard_interval' in kwargs.keys():
                    json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['short_guard_interval'] = kwargs['2g_enable_short_guard_interval']
                elif '2g_enable_aggregation' in kwargs.keys():
                    json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['aggregation'] = kwargs['2g_enable_aggregation']
                # elif kwargs['2g_mode'] == 'ngb_mixed':
                #     if kwargs['2g_channel']:
                #         json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel'] = {
                #             "standard": kwargs['2g_channel']}
                #     else:
                #         json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['channel'] = {
                #             "standard": "auto"}
            if '2g_ssid' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['ssid'] = kwargs['2g_ssid']
            if '2g_auth_type' in kwargs.keys():
                pass
            if '2g_wep_mode' in kwargs.keys():
                pass
            if '2g_hide_ssid' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['hide_ssid'] = kwargs['2g_hide_ssid']
            if '2g_ids_scan' in kwargs.keys():
                pass
            if '2g_min_data_rate' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['data_rate'] = kwargs['2g_min_data_rate']
            if '2g_transmit_power' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['transmit_power'] = kwargs['2g_transmit_power']
            if '2g_beacon_interval' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['interval']['beacon'] = kwargs['2g_beacon_interval']
            if '2g_dtim_interval' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['interval']['dtim'] = kwargs['2g_dtim_interval']
            if '2g_rts_threshold' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['threshold']['rts'] = kwargs['2g_rts_threshold']
            if '2g_max_clients' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['max_clients'] = kwargs['2g_max_clients']
            if '2g_inactive_timeout' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['station_inactivity_timeout'] = kwargs['2g_inactive_timeout']
            if '2g_enable_wds' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['wds_ap'] = kwargs['2g_enable_wds']
            if '2g_enable_green' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['green_ap']['enable'] = kwargs['2g_enable_green']
            if '2g_enable_rssi' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['rssi']['enable'] = kwargs['2g_enable_rssi']
            if '2g_rssi_threshold' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['rssi']['threshold'] = kwargs['2g_rssi_threshold']
            if '2g_enable_air_time_fairness' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['airtime_fairness'] = kwargs['2g_enable_air_time_fairness']
            if '2g_enable_802.11r' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['80211r']['enable'] = kwargs['2g_enable_802.11r']
            if '2g_enable_neighbour_report' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['80211k']['neighbour_report'] = kwargs['2g_enable_neighbour_report']
            if '2g_enable_bss' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['80211v']['bss_trans_mgmt'] = kwargs['2g_enable_bss']
            if '2g_enable_wnm_sleep' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['80211v']['wnm_sleep'] = kwargs['2g_enable_wnm_sleep']
            if 'enable_widp_sensor' in kwargs.keys():
                pass
            if 'enable_advertisement' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['ble']['advertisement'] = kwargs['enable_advertisement']
            if 'enable_ibeacon' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['ble']['ibeacon']['enable'] = kwargs['enable_ibeacon']
        except KeyError:
            logger.info("Error: In Creating JSON for sonicwave")
        return json_input

    def build_json_advanced_idp(self, **kwargs):
        """
        Builds an advanced JSON configuration for SonicPoint with optional parameters.
        """
        try:
            json_input = copy.deepcopy(self.initial_idp_json)

            json_input['sonicpoint']['widp']['enable'] = kwargs.get('enable', json_input['sonicpoint']['widp']['enable'])

            json_input['sonicpoint']['widp']['authorized_access_point']['all'] = kwargs.get(
                'authorized_access_point_all', json_input['sonicpoint']['widp']['authorized_access_point']['all'])

            json_input['sonicpoint']['widp']['rogue_access_point']['all'] = kwargs.get(
                'rogue_access_point_all', json_input['sonicpoint']['widp']['rogue_access_point']['all'])

            json_input['sonicpoint']['widp']['unauthorized_access_point']['any'] = kwargs.get(
                'unauthorized_access_point_any', json_input['sonicpoint']['widp']['unauthorized_access_point']['any'])

            json_input['sonicpoint']['widp']['unauthorized_access_point']['connected'] = kwargs.get(
                'unauthorized_access_point_connected', json_input['sonicpoint']['widp']['unauthorized_access_point']['connected'])

            json_input['sonicpoint']['widp']['evil_twin'] = kwargs.get(
                'evil_twin', json_input['sonicpoint']['widp']['evil_twin'])

            json_input['sonicpoint']['widp']['block_traffic'] = kwargs.get(
                'block_traffic', json_input['sonicpoint']['widp']['block_traffic'])

            json_input['sonicpoint']['widp']['disassociate']['rogue'] = kwargs.get(
                'disassociate_rogue', json_input['sonicpoint']['widp']['disassociate']['rogue'])

            json_input['sonicpoint']['widp']['disassociate']['krack'] = kwargs.get(
                'disassociate_krack', json_input['sonicpoint']['widp']['disassociate']['krack'])

            return json_input

        except KeyError as e:
            logger.error(f"Error updating JSON structure: {e}")
            return None     




    def build_json_sonic_profile(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.init_sonic_profile)
            if 'country_code' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['country_code'] = kwargs['country_code']
            if '2g_radio' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_2400mhz']['enable'] = kwargs['2g_radio']
            if '5g_radio' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_5000mhz']['enable'] = kwargs['5g_radio']
            if '5g_vap' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_5000mhz']['virtual_access_point'] = kwargs['5g_vap']
                logger.info(json_input)
            if '5g_mesh' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['mesh']['5000mhz'] = kwargs['5g_mesh']
            if '5g_ssid' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_5000mhz']['ssid'] = kwargs['5g_ssid']
            if '5g_mode' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_5000mhz']['mode']['5000mhz'] = kwargs['5g_mode']
            if '5g_wpa_auto' in kwargs.keys():
                del json_input['sonicpoint']['profile'][0]['radio_5000mhz']
                json_input['sonicpoint']['profile'][0]['radio_5000mhz']['authentication_type'] =  {"wpa2": {"auto": "psk"}}
                json_input['sonicpoint']['profile'][0]['radio_5000mhz']['wpa'] = kwargs['5g_wpa_auto']
            if '5g_band' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_5000mhz']['band'] = kwargs['5g_band']
            if '5g_channel' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_5000mhz']['channel'] = kwargs['5g_channel']
            if '2g_ssid' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_2400mhz']['ssid'] = kwargs['2g_ssid']
            if '2g_mesh' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['mesh']['2400mhz'] = kwargs['2g_mesh']
            if '2g_mode' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_2400mhz']['mode'] = kwargs['2g_mode']
            if '2g_wpa_auto' in kwargs.keys():
                # del json_input['sonicpoint']['profile'][0]['radio_2400mhz']
                json_input['sonicpoint']['profile'][0]['radio_2400mhz']['authentication_type'] =  {"wpa2": {"auto": "psk"}}
                json_input['sonicpoint']['profile'][0]['radio_2400mhz']['wpa'] = kwargs['2g_wpa_auto']
            if '2g_band' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_2400mhz']['band'] = kwargs['2g_band']
            if '2g_channel' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['radio_2400mhz']['channel'] = kwargs['2g_channel']
            if 'admin_name' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['administrator']['name'] = kwargs['admin_name']
            if 'admin_pass' in kwargs.keys():
                json_input['sonicpoint']['profile'][0]['administrator']['password'] = kwargs['admin_pass']
            logger.info(json_input)
        except KeyError:
            logger.info("Error: In Creating Json for sonicwave profile")
        return json_input

    def config_accesspoint(self, msg=False, **kwargs):
        json_input = self.build_json_sonicwave(**kwargs)
        url = self.url + '/sonicpoints/name/' + kwargs['name']
        response = self.fw.api_put(url, msg, data=json_input)
        return response

    def config_general_profile(self, name, msg=False, **kwargs):
        json_input = self.build_json_sonic_profile(**kwargs)
        if name:
            url = 'api/sonicos/sonicpoint/profiles/name/' + name
        else:
            logger.info('name should be specified for edit zone object.')
            return False
        response = self.fw.api_put(url, msg, data=json_input)
        return response

    def get_ap_status(self):
        sonicwave_status = []
        url = 'api/sonicos/reporting/sonicpoint/status'
        response = self.fw.api_get(url)
        return response
    
    def config_advanced_idp(self, msg=False, **kwargs):
        json_input = self.build_json_advanced_idp(**kwargs)
        url = 'api/sonicos/sonicpoint/widp'
        response = self.fw.api_put(url, msg, data=json_input)
        return response

    def get_discovered_ap(self):
        url = 'api/sonicos/reporting/sonicpoint/discovered-access-points'
        response = self.fw.api_get(url)
        return response

    def get_discovered_ap_name(self, name):
        url = 'api/sonicos/reporting/sonicpoint/discovered-access-points/sonicpoints/name/' + name
        response = self.fw.api_get(url)
        return response

    def get_discovered_ap_name_5g(self, name):
        url = 'api/sonicos/sonicpoint/ids/scan/radio/5000mhz/sonicpoints/name/' + name
        response = self.fw.api_post(url)
        return response

    def get_discovered_ap_name_24g(self, name):
        url = 'api/sonicos/sonicpoint/ids/scan/radio/2400mhz/sonicpoints/name/' + name
        response = self.fw.api_post(url)
        return response

    def get_discovered_ap_name_both(self, name):
        url = 'api/sonicos/sonicpoint/ids/scan/radio/both/sonicpoints/name/' + name
        response = self.fw.api_post(url)
        return response


    def scan_all(self):
        url = 'api/sonicos/sonicpoint/ids/scan/all'
        response = self.fw.api_post(url)
        return response

    def get_ap_sonicpoints(self):
        sonicwave = []
        url = self.url + '/sonicpoints'
        response = self.fw.api_get(url)
        for wave in response['sonicpoint']['sonicpoint']:
            sonicwave.append(wave['wave2']['name'])
        return sonicwave

    def get_station_sonicpoints(self):
        url = self.rep_url + '/station/status'
        response = self.fw.api_get(url)
        return response

    def get_general_profile(self, name, msg=False):
        url = 'api/sonicos/sonicpoint/profiles/name/' + name
        response = self.fw.api_get(url)
        return response

    def config_sonicwave_profile(self,name, msg=False, **kwargs):
        json_input=  self.get_general_profile(name)
        url = 'api/sonicos/sonicpoint/profiles/name/' + name
        logger.info(json_input)
        if 'country_code' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['country_code'] = kwargs['country_code']
        if '2g_radio' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_2400mhz']['enable'] = kwargs['2g_radio']
        if '5g_radio' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_5000mhz']['enable'] = kwargs['5g_radio']
        if '5g_mesh' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['mesh']['5000mhz'] = kwargs['5g_mesh']
        if '5g_ssid' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_5000mhz']['ssid'] = kwargs['5g_ssid']
        if '5g_mode' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_5000mhz']['mode']['5000mhz'] = kwargs['5g_mode']
        if '5g_wpa_auto' in kwargs.keys():
            del json_input['sonicpoint']['profile'][0]['radio_5000mhz']
            json_input['sonicpoint']['profile'][0]['radio_5000mhz']['authentication_type'] =  {"wpa2": {"auto": "psk"}}
            json_input['sonicpoint']['profile'][0]['radio_5000mhz']['wpa'] = kwargs['5g_wpa_auto']
        if '5g_band' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_5000mhz']['band'] = kwargs['5g_band']
        if '5g_channel' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_5000mhz']['channel'] = kwargs['5g_channel']
        if '2g_ssid' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_2400mhz']['ssid'] = kwargs['2g_ssid']
        if '2g_mesh' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['mesh']['2400mhz'] = kwargs['2g_mesh']
        if '2g_mode' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_2400mhz']['mode'] = kwargs['2g_mode']
        if '2g_wpa_auto' in kwargs.keys():
            # del json_input['sonicpoint']['profile'][0]['radio_2400mhz']
            json_input['sonicpoint']['profile'][0]['radio_2400mhz']['authentication_type'] =  {"wpa2": {"auto": "psk"}}
            json_input['sonicpoint']['profile'][0]['radio_2400mhz']['wpa'] = kwargs['2g_wpa_auto']
        if '2g_band' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_2400mhz']['band'] = kwargs['2g_band']
        if '2g_channel' in kwargs.keys():
            json_input['sonicpoint']['profile'][0]['radio_2400mhz']['channel'] = kwargs['2g_channel']
        logger.info('==='.center(20))
        logger.info(json_input)
        response = self.fw.api_put(url, msg, data=json_input)
        return response

    def get_discoverd_ap(self):
        response = self.fw.api_get(self.discover_ap)
        return response
        
    def config_schedule(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.schedule, msg, data=json_input)
        return resp
        
    def config_sonicpoint_profile(self, name, msg=False, **kwargs):
        url = 'api/sonicos/sonicpoint/profiles/name/' + name
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp
        
    def get_schedules(self):
        response = self.fw.api_get(self.schedule)
        return response
        
    def config_sonicpoint_object(self, name, msg=False, **kwargs):
        url = str(self.sp_object + '/name/' + name)
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def synchronize(self):
        url = self.url + '/synchronize'
        response = self.fw.api_post(url)
        return response

    def reboot_sonicpoint(self, name):
        url = self.url + f'/reboot/sonicpoint/{name}'
        response = self.fw.api_post(url)
        return response

    def get_sonicpoint_status(self, name):
        url = self.rep_url + f'/status/sonicpoints/name/{name}'
        response = self.fw.api_get(url)
        return response

    def get_sonicpoint_stat_radio(self, name):
        url = self.rep_url + f'/statistics/radio/sonicpoint/{name}'
        response = self.fw.api_get(url)
        return response

    def get_sonicpoint_stat_traffic(self, name):
        url = self.rep_url + f'/statistics/traffic/sonicpoint/{name}'
        response = self.fw.api_get(url)
        return response

    def get_sonicpoint_firmware_status(self):
        url = 'api/sonicos/dynamic-file/getSonicPointFirmwareStatus.json'
        response = self.fw.api_get(url)
        return response

    def config_sonicpoint_firmware_management(self, msg=False, **kwargs):
        '''
            input example:
            kwargs = {
                "sonicpoint":{"n":"","nv":"","ndr":"","ac":""},
                "sonicwave200":"10.8.13.151/231_fw/sw_spw_eng_9.1.3.0_56.bin.sig",
                "sonicwave400":"",
                "sonicwaveax":""
            }
        '''
        
        json_input = copy.deepcopy(self.initial_sonicwave_firmware_management_json)
        json_input['sonicpoint']['firmware_management']['override_download_url'].update(**kwargs)
        url = 'api/sonicos/sonicpoint/firmware-management'
        response = self.fw.api_put(url, msg, data=json_input)
        return response
    
    def get_sonicpoints(self):
        response = self.fw.api_get(self.sp_object)
        return response
    
    def build_json_ap_vap(self, name, country_code, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_sonicwave_json_vap)
            json_input['sonicpoint']['sonicpoint'][0]['wave2']['name'] = name
            if 'enable' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['enable'] = kwargs['enable']
            json_input['sonicpoint']['sonicpoint'][0]['country_code'] = country_code
            if '5g_vap_group' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_5000mhz']['virtual_access_point']['group'] = kwargs[
                    '5g_vap_group']
            if '2g_vap_group' in kwargs.keys():
                json_input['sonicpoint']['sonicpoint'][0]['radio_2400mhz']['virtual_access_point']['group'] = kwargs[
                    '2g_vap_group']
        except KeyError:
            logger.info("Error: In Creating JSON for sonicpoint")
        return json_input

    def config_accesspoint_vap(self, name, country_code, msg=False, **kwargs):
        json_input = self.build_json_ap_vap(name, country_code, **kwargs)
        url = self.url + '/sonicpoints/name/' + name
        response = self.fw.api_put(url, msg, data=json_input)
        return response

    def get_ap_country_code(self):
        try:
            logger.info("get ap country code.")
            url = self.url + '/sonicpoints'
            response = self.fw.api_get(url)
            return str(response['sonicpoint']['sonicpoint'][0]['country_code'])
        except:
            logger.info("can not get ap country code!")
        return False

    def get_ap_info(self):
        try:
            logger.info("get ap status and name.")
            url = 'api/sonicos/reporting/sonicpoint/status'
            resp = self.fw.api_get(url)
            ap_name = str(resp[0]['sonicpoint'])
            status = str(resp[0]['status'])
            return status, ap_name
        except:
            logger.info("can not get ap info!")
        return False

class FloorPlanViewApi:
    '''FloorPlanViewApi class'''
    default_options = {
        'name': 'test',
        'comment': 'New floorplan',
        'image_width': 200,
        'image_height': 200,
        'scale': 1,
        # 'access_point_name':'',
        # 'x_axis':'',
        # 'y_axis':'',
        }

    def __init__(self, fw):
        self.fw = fw
        self.flpl_url = 'api/sonicos/sonicpoint/floor-plans/name/'
        self.initial_flpl_json = {
            "sonicpoint": {
                "floor_plan": [{
                    "name": "test1",
                    "comment": "New floorplan",
                    # "image": "",
                    "image_width": 1400,
                    "image_height": 900,
                    "scale": 1.000000,
                    # "access_point": [{
                        # "name": "SonicPoint ACe b5bdc2",
                        # "x_axis": 200,
                        # "y_axis": 200
                    # }]
                }]
            }
        }

    def add_floor_plan(self, msg=False, **kwargs):
        self.options = dict(FloorPlanViewApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options
        name = kwargs['name']
        comment = kwargs['comment']
        image_width = kwargs['image_width']
        image_height = kwargs['image_height']
        scale = kwargs['scale']
        url = 'https://192.168.168.168/api/sonicos/raw'
        data = f'{{"stream":"floorPlanName_-1={name}&'\
            f'floorPlanComment_-1={comment}&'\
            f'floorPlanImgWidth_-1=%d&'\
            f'floorPlanImgHeight_-1=%d&'\
            f'floorPlanApList_-1=&'\
            f'floorPlanScale_-1={scale}"}}'\
            %(image_width, image_height)
        self.fw.api_login()
        curl_command = f"curl -k -i -H 'X-SNWL-API-Scope: extended' \
           -H 'Content-Type: */*' -H 'Accept: */*' \
           -X POST -d '{data}' {url}"

        logger.info(f'--------curl command: {curl_command}')
        resp = os.popen(curl_command).read()
        logger.info(resp)
        if re.search('HTTP/1.0 200 OK', resp, re.I):
            return True
        return False

    def add_sp_to_floor_plan(self, msg=False, **kwargs):
        self.options = dict(FloorPlanViewApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options
        name = kwargs['name']
        comment = kwargs['comment']
        image_width = kwargs['image_width']
        image_height = kwargs['image_height']
        scale = kwargs['scale']
        sp_name = kwargs['sp_name']
        x_axis = kwargs['x_axis']
        y_axis = kwargs['y_axis']
        url = 'https://192.168.168.168/api/sonicos/raw'
        data = f'{{"stream":"floorPlanName_-2={name}&'\
            f'floorPlanComment_-2={comment}&'\
            f'floorPlanImgWidth_-2={image_width}&'\
            f'floorPlanImgHeight_-2={image_height}&'\
            f'floorPlanApList_-2={sp_name}%2C{x_axis}%2C{y_axis}&'\
            f'floorPlanScale_-2={scale}&'\
            f'floorPlanName_1={name}&'\
            f'floorPlanComment_1={comment}&'\
            f'floorPlanImgWidth_1={image_width}&'\
            f'floorPlanApList_1={sp_name}%2C{x_axis}%2C{y_axis}&'\
            f'floorPlanScale_1={scale}"}}'
        self.fw.api_login()
        curl_command = f"curl -k -i -H 'X-SNWL-API-Scope: extended' \
            -H 'Content-Type: */*' -H 'Accept: */*' \
            -X POST -d '{data}' {url}"

        logger.info(f'--------curl command: {curl_command}')
        resp = os.popen(curl_command).read()
        logger.info(resp)
        if re.search('HTTP/1.0 200 OK', resp, re.I):
            return True
        return False

    def edit_floor_plan(self, msg=False, **kwargs):
        url = self.flpl_url + kwargs['name']
        json_input = self.get_floor_plan(kwargs['name'])
        plan_path = json_input['sonicpoint']['floor_plan'][0]
        try:
            if 'rename' in kwargs:
                plan_path['name'] = kwargs['rename']
            if 'comment' in kwargs:
                plan_path['comment'] = kwargs['comment']
            if 'image_width' in kwargs:
                plan_path['image_width'] = int(kwargs['image_width'])
            if 'image_height' in kwargs:
                plan_path['image_height'] = int(kwargs['image_height'])
            if 'scale' in kwargs:
                plan_path['scale'] = int(kwargs['scale'])
            if 'access_point_name' in kwargs:
                plan_path['access_point'] = []
                plan_path['access_point'][0] = {}
                logger.info(json_input)
                plan_path['access_point'][0]['name'] = int(kwargs['access_point_name'])
                logger.info(json_input)
                plan_path['access_point'][0]['x_axis'] = int(kwargs['x_axis'])
                plan_path['access_point'][0]['y_axis'] = int(kwargs['y_axis'])
            flpl_resp = self.fw.api_put(url, msg, data=json_input)
        except KeyError as e:
            logger.info("Error: didn't get json")
            logger.info(f"error info: {e}")
            return False
        return flpl_resp

    def get_floor_plan(self, name, msg=False):
        url = self.flpl_url + name
        flpl_resp = self.fw.api_get(url) 
        return flpl_resp

    def del_floor_plan(self, name, msg=False):
        url = self.flpl_url + name
        flpl_resp = self.fw.api_delete(url) 
        return flpl_resp

    def del_sp_in_floor_plan(self, msg=False, **kwargs):
        self.options = dict(FloorPlanViewApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options
        name = kwargs['name']
        comment = kwargs['comment']
        image_width = kwargs['image_width']
        image_height = kwargs['image_height']
        scale = kwargs['scale']
        sp_name = ''
        x_axis = ''
        y_axis = ''
        url = 'https://192.168.168.168/api/sonicos/raw'
        data = f'{{"stream":"floorPlanName_-2={name}&'\
            f'floorPlanComment_-2={comment}&'\
            f'floorPlanImgWidth_-2={image_width}&'\
            f'floorPlanImgHeight_-2={image_height}&'\
            f'floorPlanApList_-2=&'\
            f'floorPlanScale_-2={scale}&'\
            f'floorPlanName_1={name}&'\
            f'floorPlanComment_1={comment}&'\
            f'floorPlanImgWidth_1={image_width}&'\
            f'floorPlanImgHeight_1={image_height}&'\
            f'floorPlanApList_1=&'\
            f'floorPlanScale_1={scale}"}}'
        self.fw.api_login()
        curl_command = f"curl -k -i -H 'X-SNWL-API-Scope: extended' \
            -H 'Content-Type: */*' -H 'Accept: */*' \
            -X POST -d '{data}' {url}"

        logger.info(f'--------curl command: {curl_command}')
        resp = os.popen(curl_command).read()
        logger.info(resp)
        if re.search('HTTP/1.0 200 OK', resp, re.I):
            return True
        return False


class VirtualAccessPointApi:
    """VirtualAccessPointApi class"""

    def __init__(self, fw):
        self.fw = fw
        self.url = "api/sonicos/sonicpoint/virtual-access-point/"
#         self.initial_object_json = {
#         "sonicpoint": {
#             "virtual_access_point": {
#                 "object": [
#                     {
#                         "name": None,
#                         "ssid": None,
#                         "vlan_id": "",
#                         "suppress_ssid": False,
#                         "enable": True,
#                         "profile": {},
#                         "schedule": {
#                             "always_on": True
#                         },
#                         "radio_type": "sonicpoint",
#                         "authentication_type": {
#                             "wep": "open-system"
#                         },
#                         "cipher_type": {},
#                         "max_clients": 16,
#                         "remote_mac_access_control": False,
#                         "wds": False,
#                         "access_list": {
#                             "mac_filter_list": False
#                         },
#                         "80211r": {
#                             "enable": False,
#                             "ft_over_ds": False,
#                             "mix_mode": False
#                         },
#                         "80211k": {
#                             "neighbour_report": False
#                         },
#                         "80211v": {
#                             "bss_trans_mgmt": False,
#                             "wnm_sleep": False
#                     }
#                 }
#             ]
#         }
#     }
# }
        self.initial_vap_object_json = {
            "sonicpoint": {
                "virtual_access_point": {
                    "object": [
                        {
                            "name": None,
                            "ssid": None,
                            "vlan_id": "",
                            "suppress_ssid": False,
                            "enable": True,
                            "profile": {},
                            "schedule": {
                                "always_on": True
                            },
                            "radio_type": "sonicpoint",
                            "authentication_type": {
                                "open": True                # 8.0.0
                            },
                            "cipher_type": {},
                            "max_clients": 16,
                            "remote_mac_access_control": False,
                            "wds": False,
                            "access_list": {
                                "mac_filter_list": False
                            },
                            "80211r": {
                                "enable": False,
                                "ft_over_ds": False,
                                "mix_mode": False
                            },
                            "80211k": {
                                "neighbour_report": False
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
        self.initial_profile_json = {
            "sonicpoint": {
                "virtual_access_point": {
                    "profile": [
                        {
                            "name": None,
                            "schedule": {
                                "always_on": True
                            },
                            "radio_type": "sonicpoint",
                            "mbo": {
                                "enable": False
                            },
                            "authentication_type": {},
                            "cipher_type": {},
                            "max_clients": 16,
                            "remote_mac_access_control": False,
                            "wds": False,
                            "access_list": {
                                "mac_filter_list": False
                            },
                            "80211r": {
                                "enable": False,
                                "ft_over_ds": False,
                                "mix_mode": False
                            },
                            "80211k": {
                                "neighbour_report": False
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
        self.initial_group_json = {
            "sonicpoint": {
                "virtual_access_point": {
                    "group": [
                        {
                            "name": "VAP Group",
                            "virtual_access_point": [
                                {
                                    "name": None
                                }
                            ]
                        }
                    ]
                }
            }
        }

    def build_json_object(self, **object):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_vap_object_json)
            logger.info("object json obtained")
            logger.info(json_input)
            if 'name' in object.keys() and object['name']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['name'] = object['name']
            else:
                logger.error('name must be specified')
            if 'ssid' in object.keys() and object['ssid']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['ssid'] = object['ssid']
            else:
                logger.error('ssid must be specified')
            if 'vlan_id' in object.keys() and object['vlan_id']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['vlan_id'] = object['vlan_id']
            if 'enable' in object.keys():
                json_input['sonicpoint']['virtual_access_point']['object'][0]['enable'] = object['enable']
            if 'enasuppress_ssidble' in object.keys():
                json_input['sonicpoint']['virtual_access_point']['object'][0]['suppress_ssid'] = object['suppress_ssid']
            if 'schedule' in object.keys() and object['schedule']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['schedule'][object['schedule']] = True
            if 'radio_type' in object.keys() and object['radio_type']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['radio_type'] = object['radio_type']
            if 'profile' in object.keys() and object['profile']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['profile']['sonicpoint'] = object['profile']
            if 'authentication_type' in object.keys() and object['authentication_type']:
                if object['authentication_type'].lower() == 'open':
                    json_input['sonicpoint']['virtual_access_point']['object'][0]['authentication_type'] = {"open": True}
                if object['authentication_type'] == 'wpa2-psk':
                    json_input['sonicpoint']['virtual_access_point']['object'][0]['authentication_type'] = {"wpa2": {"psk": True}}
                    json_input['sonicpoint']['virtual_access_point']['object'][0]['cipher_type'] = {"aes": True}
                    json_input['sonicpoint']['virtual_access_point']['object'][0]['wpa'] = {
                        "passphrase": object.get('wpa_pwd', "password"),
                        "group_key_interval": 86400,
                        "pmf": {}
                    }
            if 'max_clients' in object.keys() and object['max_clients']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['max_clients'] = object['max_clients']
            if 'cipher_type' in object.keys() and object['cipher_type']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['cipher_type'] = object['cipher_type']
            if 'remote_mac_access_control' in object.keys() and object['remote_mac_access_control']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['remote_mac_access_control'] = True
            if 'wds' in object.keys() and object['wds']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['wds'] = True
            if 'mac_filter_list' in object.keys() and object['mac_filter_list']:
                json_input['sonicpoint']['virtual_access_point']['object'][0]['access_list']['mac_filter_list'] = True
                if 'use_global_access_list' in object.keys() and object['use_global_access_list']:
                    json_input['sonicpoint']['virtual_access_point']['object'][0]['access_list']['use_global_access_list'] = True
                if 'allow' in object.keys() and object['allow']:
                    json_input['sonicpoint']['virtual_access_point']['object'][0]['access_list']['allow'][ object['allow']] = True
                if 'deny' in object.keys() and object['deny']:
                    json_input['sonicpoint']['virtual_access_point']['object'][0]['access_list']['allow'][object['deny']] = True
        except:
            logger.info("In creating JSON error!")
        return json_input

    def build_json_profile(self, **object):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_profile_json)
            logger.info("profile json obtained")
            logger.info(json_input)
            if 'name' in object.keys() and object['name']:
                json_input['sonicpoint']['virtual_access_point']['profile'][0]['name'] = object['name']
            else:
                logger.error('name must be specified')
            if 'authentication_type' in object.keys() and object['authentication_type']:
                if object['authentication_type'].lower() == 'open':
                    json_input['sonicpoint']['virtual_access_point']['profile'][0]['authentication_type'] = {"open": True}
                if object['authentication_type'].lower() == 'wpa2-psk':
                    json_input['sonicpoint']['virtual_access_point']['profile'][0]['authentication_type'] = {"wpa2":{"psk": True}}
                    json_input['sonicpoint']['virtual_access_point']['profile'][0]['wpa'] = {
                        "passphrase": "password",
                        "group_key_interval": 86400,
                        "pmf": {}
                    }
            if object['authentication_type'].lower() == 'wpa2-psk' or object['authentication_type'].lower() == 'wpa2-eap':
                json_input['sonicpoint']['virtual_access_point']['profile'][0]['cipher_type'] = {"aes": True}
            if 'mac_filter_list' in object.keys() and object['mac_filter_list']:
                json_input['sonicpoint']['virtual_access_point']['profile'][0]['access_list']['mac_filter_list'] = True
                if 'use_global_access_list' in object.keys() and object['use_global_access_list']:
                    json_input['sonicpoint']['virtual_access_point']['profile'][0]['access_list']['use_global_access_list'] = True
                if 'allow' in object.keys() and object['allow']:
                    json_input['sonicpoint']['virtual_access_point']['profile'][0]['access_list']['allow'][ object['allow']] = True
                if 'deny' in object.keys() and object['deny']:
                    json_input['sonicpoint']['virtual_access_point']['profile'][0]['access_list']['allow'][object['deny']] = True
        except:
            logger.info("In creating JSON error!")
        return json_input

    def build_json_group(self, multiple=False, **object):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_group_json)
            logger.info("group json obtained")
            logger.info(json_input)
            if 'group_name' in object.keys() and object['group_name']:
                json_input['sonicpoint']['virtual_access_point']['group'][0]['name'] = object['group_name']
            else:
                logger.error('name must be specified')
            if 'group' in object.keys() and object['group']:
                if multiple:
                    obj_list = []
                    for obj_name in object['group']:
                        obj_dict = {"name": obj_name}
                        obj_list.append(obj_dict)
                    json_input['sonicpoint']['virtual_access_point']['group'][0]['virtual_access_point'] = obj_list
                else:
                    json_input['sonicpoint']['virtual_access_point']['group'][0]['virtual_access_point'][0]['name'] = object["group"]
        except:
            logger.info("In creating JSON error!")
        return json_input

    def get_VAP_object(self):
        url = 'api/sonicos/sonicpoint/virtual-access-point/objects'
        response = self.fw.api_get(url)
        return response
        
    def add_VAP_Object(self,msg=False,**kwargs):
        json_input = self.build_json_object(**kwargs)
        obj_url = self.url + 'objects'
        resp = self.fw.api_post(obj_url,msg,data=json_input)
        return resp

    def del_VAP_Object(self,name,msg=False):
        obj_url = self.url + 'objects/name/' + name
        resp = self.fw.api_delete(obj_url,msg=False)
        return resp

    def get_vap_groups(self):
        url = self.url + 'groups'
        response = self.fw.api_get(url)
        return response

    def config_vap_group(self, gp_name, msg=False, multiple=False, **kwargs):
        url = self.url + 'groups/name/' + gp_name
        json_input = self.build_json_group(multiple, **kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def add_vap_group(self, msg=False, multiple=False, **kwargs):
        json_input = self.build_json_group(multiple, **kwargs)
        obj_url = self.url + 'groups'
        resp = self.fw.api_post(obj_url, msg, data=json_input)
        return resp

    def get_vap_profiles(self):
        url = self.url + 'profiles'
        response = self.fw.api_get(url)
        return response

    def get_vap_profile(self, name, msg=False):
        url = self.url + 'profiles/name/' + name
        response = self.fw.api_get(url)
        return response

    def add_vap_profile(self, msg=False, **kwargs):
        json_input = self.build_json_profile(**kwargs)
        url = self.url + 'profiles'
        response = self.fw.api_post(url, msg, data=json_input)
        return response

    def config_vap_profile(self, pro_name, msg=False, **kwargs):
        url = self.url + 'profiles/name/' + pro_name
        json_input = self.build_json_profile(**kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def delete_vap_profile(self, name, msg=False):
        url = self.url + 'profiles/' + 'name' + '/' + name
        response = self.fw.api_delete(url, msg)
        return response

    def get_vap_objects(self):
        url = self.url + 'objects'
        response = self.fw.api_get(url)
        return response

    def get_vap_object(self, name, msg=False):
        url = self.url + 'objects/name/' + name
        response = self.fw.api_get(url)
        return response

    def config_vap_object(self, obj_name, msg=False, **kwargs):
        url = self.url + 'objects/' + 'name/' + obj_name
        json_input = self.build_json_object(**kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def del_VAP_Objects(self, msg=False, objs_name=None):
        obj_url = self.url + 'objects'
        objs_list = []
        for name in objs_name:
            objs_list.append({"name": name})
        json_input = {"sonicpoint": {"virtual_access_point": {"object": objs_list}}}
        resp = self.fw.api_delete(obj_url, msg, data=json_input)
        return resp

    def del_vap_group(self, name, msg=False):
        gp_url = self.url + 'groups/name/' + name
        resp = self.fw.api_delete(gp_url, msg)
        return resp


if __name__ == '__main__':
    firewall_ip = '192.168.168.168'
    fw = Firewall(firewall_ip, user='admin', password='password')
    apApi = AccessPoint(fw)
    sonic_profile = {
        '2g_radio': False
    }
    apApi.config_general_profile('SonicWave',**sonic_profile)
#    apApi.get_ap_status()
    rc = apApi.get_ap_sonicpoints()
    print('*' * 100)
    print(rc)
#    apApi.synchronize()
#    sonicwave = {
#        'enable': False,
#        'name': "SonicWave 231o e9479d",
#        '5g_radio': True,
#        '5g_mode': "ac-na-mixed",
#        '5g_ssid': "sonic-terry",
#        #        '5g_radio_band': "auto",
#        #        '5g_auth_type': "wep",
#        #        '5g_wep_mode': "none",
#        '5g_hide_ssid': False,
#        '5g_min_data_rate': "best",
#        '5g_transmit_power': "full",
#        '5g_beacon_interval': 100,
#        '5g_dtim_interval': 1,
#        '5g_rts_threshold': -65,
#        '5g_max_clients': 32,
#        '5g_inactive_timeout': 300,
#        '5g_enable_wds': False,
#        '5g_enable_green': False,
#        '5g_enable_rssi': False,
#        '5g_enable_air_time_fairness': False,
#        '5g_enable_802.11r': False,
#        '5g_enable_neighbour_report': False,
#        '5g_enable_bss': False,
#        '5g_enable_wnm_sleep': False
#    }
#    name1 = "SonicWave%20432o%207b8e46"
#    name2 = "SonicWave%20231o%20e9479d"
#    apApi.config_accesspoint(name1, **sonicwave)
