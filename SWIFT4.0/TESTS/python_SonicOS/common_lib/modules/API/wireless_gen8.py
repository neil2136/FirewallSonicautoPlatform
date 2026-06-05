import copy
from runner.settings import logger


class StatusApi:
    def __init__(self, fw):
        self.fw = fw
        self.wireless_setting = 'api/sonicos/dynamic-file/getWirelessSetting.json'
        self.wireless_status = 'api/sonicos/dynamic-file/getWirelessStatus.json'
        self.station_status = 'api/sonicos/reporting/wireless/v2/stations'
        self.delete_station = 'api/sonicos/wireless/v2/disassociate-station'

    def get_wireless_setting(self):
        return self.fw.api_get(self.wireless_setting)

    def get_wireless_status(self):
        return self.fw.api_get(self.wireless_status)

    def get_station_status(self):
        return self.fw.api_get(self.station_status)

    def get_station_mac_by_ssid(self, ssid=''):
        output = False
        for station in self.get_station_status():
            if station['ssid'] == ssid:
                logger.info(f'station mac is: {station["mac"]}')
                output = station['mac']
                break
        else:
            logger.info('ERR: station mac not found')
        return output

    def del_station(self, mac='', msg=False):
        url = f'{self.delete_station}/{mac}'
        output = self.fw.api_post(url, msg=msg)
        return output


class VAPApi:
    def __init__(self, fw):
        self.fw = fw
        self.vap_object = 'api/sonicos/wireless/virtual-access-point/objects'
        self.vap_groups = 'api/sonicos/wireless/virtual-access-point/groups'
        self.vap_profile = 'api/sonicos/wireless/virtual-access-point/profiles'
        self.initial_add_object_json = {
            "wireless": {
                "virtual_access_point": {
                    "object": [
                        {
                            "80211r": {"enable": False, "ft_over_ds": False, "mix_mode": False},
                            "80211v": {"bss_trans_mgmt": False, "wnm_sleep": False},
                            "access_list": {
                                "allow": {"all": True},
                                "deny": {},
                                "mac_filter_list": False,
                                "use_global_access_list": False,
                            },
                            "allow_b": True,
                            "authentication_type": {"wpa2": {"psk": True}},
                            "cipher_type": {"aes": True},
                            "enable": True,
                            "max_clients": 16,
                            "name": "sonicwall_test01",
                            "profile": {},
                            "radio_type": "wireless",
                            "schedule": {"always_on": True},
                            "ssid": "sonicwall_test01",
                            "suppress_ssid": False,
                            "vlan_id": "",
                            "wds": False,
                            "wpa": {"group_key_interval": 86400, "passphrase": "12345678"},
                        }
                    ]
                }
            }
        }
        self.add_vap_profile_json = {
            "wireless": {
                "virtual_access_point": {
                    "profile": [
                        {
                            "80211r": {
                                "enable": False,
                                "ft_over_ds": False,
                                "mix_mode": False,
                            },
                            "80211v": {
                                "bss_trans_mgmt": False,
                                "wnm_sleep": False,
                            },
                            "access_list": {
                                "allow": {"all": True},
                                "deny": {},
                                "mac_filter_list": False,
                                "use_global_access_list": False,
                            },
                            "allow_b": True,
                            "authentication_type": {"wpa2": {"auto": "psk"}},
                            "cipher_type": {"auto": True},
                            "max_clients": 16,
                            "name": "only test",
                            "radio_type": "wireless",
                            "schedule": {"always_on": True},
                            "wds": False,
                            "wpa": {
                                "group_key_interval": 86400,
                                "passphrase": "password",
                            },
                        }
                    ]
                }
            }
        }
        self.initial_vap_groups_json = {
            "wireless": {
                "virtual_access_point": {
                    "group": [
                        {
                            "name": "Internal AP Group",
                            "virtual_access_point": [
                                # {"name": "sonicwall"},
                                # {"name": "sonicwall_profile_test01"}
                            ]
                        }
                    ]
                }
            }
        }
        

    def get_vap_object(self):
        url = self.vap_object
        return self.fw.api_get(url) 
    
    def get_vap_groups(self):
        url = self.vap_groups
        return self.fw.api_get(url) 

    def add_vap_object(self, msg=False, **kwargs): 
        # kwargs is {
        #     'name': 'sonicwall_test01',
        #     'ssid': 'sonicwall_test01',
        #     'enable': True,
        #     'passphrase': '12345678',
        # }
        if 'name' not in kwargs.keys() and 'ssid' not in kwargs.keys():
            logger.error('ERR: name or ssid is not in kwargs')
            return False
        json_input = copy.deepcopy(self.initial_add_object_json)
        json_input['wireless']['virtual_access_point']['object'][0]['name'] = kwargs['name']
        json_input['wireless']['virtual_access_point']['object'][0]['ssid'] = kwargs['ssid']

        if 'vlan_id' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['vlan_id'] = kwargs['vlan_id']
        if 'suppress_ssid' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['suppress_ssid'] = kwargs['suppress_ssid']
        if 'enable' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['enable'] = kwargs['enable']
        if 'profile' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['profile'] = kwargs['profile']
        if 'schedule' in kwargs.keys(): 
            json_input['wireless']['virtual_access_point']['object'][0]['schedule'] = kwargs['schedule']
        if 'radio_type' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['radio_type'] = kwargs['radio_type']
        if 'authentication_type' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['authentication_type'] = kwargs['authentication_type']
        if 'cipher_type' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['cipher_type'] = kwargs['cipher_type']
        if 'max_clients' in kwargs.keys():  
            json_input['wireless']['virtual_access_point']['object'][0]['max_clients'] = kwargs['max_clients']
        if 'passphrase' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['wpa']['passphrase'] = kwargs['passphrase']
        if 'allow_b' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['allow_b'] = kwargs['allow_b']
        if 'wds' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['wds'] = kwargs['wds']
        if 'mac_filter_list' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['access_list']['mac_filter_list'] = kwargs['mac_filter_list']
        if 'use_global_access_list' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['access_list']['use_global_access_list'] = kwargs['use_global_access_list']
        if 'allow' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['access_list']['allow'] = kwargs['allow']
        if 'deny' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['access_list']['deny'] = kwargs['deny']
        if '80211r' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['80211r'] = kwargs['80211r']
        if '80211v' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['80211v'] = kwargs['80211v']
        if 'wpa' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['wpa'] = kwargs['wpa']
        if 'allow_b' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['allow_b'] = kwargs['allow_b']
        if 'wds' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['wds'] = kwargs['wds']
        if 'access_list' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['access_list'] = kwargs['access_list']
        if '80211r' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['80211r'] = kwargs['80211r']
        if '80211v' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['object'][0]['80211v'] = kwargs['80211v']

        logger.info(f'add object json_input result: {json_input}')
        output = self.fw.api_post(self.vap_object, msg=msg, data=json_input)
        return output

    def edit_vap_object(self, msg=False, **kwargs): 
        # kwargs is {
        #     'name': 'sonicwall',
        #     'ssid': 'sonicwall',
        #     'enable': True,
        #     'mac_filter_list': True,
        #     'allow': {'group': 'sonicwall_test03_gp'},
        #     'passphrase': '12345678',
        # }
        loop_sequence = 0
        json_input = {'wireless': {'virtual_access_point': {'object': []}}}
        if 'name' not in kwargs.keys():
            logger.error('ERR: name is not in kwargs')
            return False
        object_url = self.vap_object + '/name/' + kwargs['name']
        get_object_list = self.get_vap_object()
        for temp_object in get_object_list['wireless']['virtual_access_point']['object']:
            if temp_object['name'] == kwargs['name']:
                logger.info('find the except object in object list.')
                if 'new_name' in kwargs.keys():
                    temp_object['name'] = kwargs['new_name']
                if 'ssid' in kwargs.keys():
                    temp_object['ssid'] = kwargs['ssid']
                if 'vlan_id' in kwargs.keys():
                    temp_object['vlan_id'] = kwargs['vlan_id']
                if 'suppress_ssid' in kwargs.keys():
                    temp_object['suppress_ssid'] = kwargs['suppress_ssid']
                if 'enable' in kwargs.keys():
                    temp_object['enable'] = kwargs['enable']
                if 'profile' in kwargs.keys():
                    temp_object['profile'] = kwargs['profile']
                if 'schedule' in kwargs.keys():
                    temp_object['schedule'] = kwargs['schedule']
                if 'radio_type' in kwargs.keys():
                    temp_object['radio_type'] = kwargs['radio_type']
                if 'authentication_type' in kwargs.keys():
                    temp_object['authentication_type'] = kwargs['authentication_type']
                if 'cipher_type' in kwargs.keys():
                    temp_object['cipher_type'] = kwargs['cipher_type']
                if 'max_clients' in kwargs.keys():
                    temp_object['max_clients'] = kwargs['max_clients']
                if 'passphrase' in kwargs.keys():
                    temp_object['wpa']['passphrase'] = kwargs['passphrase']
                if 'allow_b' in kwargs.keys():
                    temp_object['allow_b'] = kwargs['allow_b']
                if 'wds' in kwargs.keys():
                    temp_object['wds'] = kwargs['wds']
                if 'mac_filter_list' in kwargs.keys():
                    temp_object['access_list']['mac_filter_list'] = kwargs['mac_filter_list']
                if 'use_global_access_list' in kwargs.keys():
                    temp_object['access_list']['use_global_access_list'] = kwargs['use_global_access_list']
                if 'allow' in kwargs.keys():
                    temp_object['access_list']['allow'] = kwargs['allow']
                if 'deny' in kwargs.keys():
                    temp_object['access_list']['deny'] = kwargs['deny']
                if '80211r' in kwargs.keys():
                    temp_object['80211r'] = kwargs['80211r']
                if '80211v' in kwargs.keys():
                    temp_object['80211v'] = kwargs['80211v']
                if 'wpa' in kwargs.keys():
                    temp_object['wpa'] = kwargs['wpa']
                if 'allow_b' in kwargs.keys():
                    temp_object['allow_b'] = kwargs['allow_b']
                if 'wds' in kwargs.keys():
                    temp_object['wds'] = kwargs['wds']
                if 'access_list' in kwargs.keys():
                    temp_object['access_list'] = kwargs['access_list']
                if '80211r' in kwargs.keys():
                    temp_object['80211r'] = kwargs['80211r']
                if '80211v' in kwargs.keys():
                    temp_object['80211v'] = kwargs['80211v']
                json_input['wireless']['virtual_access_point']['object'] = [temp_object]
                break
            else:
                loop_sequence += 1
        else:
            logger.info('loop end for object list, can not find object name.')
        
        logger.info(f'edit json_input result: `{json_input}')
        output = self.fw.api_put(object_url, msg=msg, data=json_input)
        return output

    def del_vap_object(self, name='', msg=False):
        json_input = {'wireless': {'virtual_access_point': {'object': [{"name": name}]}}}
        output = self.fw.api_delete(self.vap_object, msg=msg, data=json_input)
        return output

    def get_vap_profile(self):
        return self.fw.api_get(self.vap_profile)
    
    def add_vap_profile(self, msg=False, **kwargs):
        object_url = self.vap_profile
        if 'name' not in kwargs.keys():
            logger.error('ERR: name is not in kwargs')
            return False
        json_input = copy.deepcopy(self.add_vap_profile_json)
        json_input['wireless']['virtual_access_point']['profile'][0]['name'] = kwargs['name']
        if 'schedule' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['schedule'] = kwargs['schedule']
        if 'radio_type' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['radio_type'] = kwargs['radio_type']
        if 'authentication_type' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['authentication_type'] = kwargs['authentication_type']
        if 'radio_type' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['radio_type'] = kwargs['radio_type']
        if 'cipher_type' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['cipher_type'] = kwargs['cipher_type']
        if 'max_clients' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['max_clients'] = kwargs['max_clients']
        if 'allow_b' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['allow_b'] = kwargs['allow_b']
        if 'wds' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['wds'] = kwargs['wds']
        if 'passphrase' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['wpa']['passphrase'] = kwargs['passphrase']
        if 'mac_filter_list' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['access_list']['mac_filter_list'] = kwargs['mac_filter_list']
        if 'use_global_access_list' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['access_list']['use_global_access_list'] = kwargs['use_global_access_list']
        if 'allow' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['access_list']['allow'] = kwargs['allow']
        if 'deny' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['access_list']['deny'] = kwargs['deny']
        if '80211r' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['80211r'] = kwargs['80211r']
        if '80211v' in kwargs.keys():
            json_input['wireless']['virtual_access_point']['profile'][0]['80211v'] = kwargs['80211v']
        output = self.fw.api_post(object_url, msg=msg, data=json_input)
        return output

    def edit_vap_profile(self, msg=False, **kwargs):
        loop_sequence = 0
        json_input = {'wireless': {'virtual_access_point': {'profile': []}}}
        if 'name' not in kwargs.keys():
            logger.error('ERR: name is not in kwargs')
            return False
        profile_url = self.vap_profile + '/name/' + kwargs['name']
        get_profile_list = self.get_vap_profile()
        for temp_object in get_profile_list['wireless']['virtual_access_point']['profile']:
            if temp_object['name'] == kwargs['name']:
                logger.info('find the except object in profile list.')
                if 'new_name' in kwargs.keys():
                    temp_object['name'] = kwargs['new_name']
                if 'max_clients' in kwargs.keys():
                    temp_object['max_clients'] = kwargs['max_clients']
                if 'allow_b' in kwargs.keys():
                    temp_object['allow_b'] = kwargs['allow_b']
                if 'radio_type' in kwargs.keys():
                    temp_object['radio_type'] = kwargs['radio_type']
                if 'schedule' in kwargs.keys():
                    temp_object['schedule'] = kwargs['schedule']
                if 'access_list' in kwargs.keys():
                    temp_object['access_list'] = kwargs['access_list']
                if 'authentication_type' in kwargs.keys():
                    temp_object['authentication_type'] = kwargs['authentication_type']
                if 'cipher_type' in kwargs.keys():
                    temp_object['cipher_type'] = kwargs['cipher_type']
                if 'wpa' in kwargs.keys():
                    temp_object['wpa'] = kwargs['wpa']
                if '80211r' in kwargs.keys():
                    temp_object['80211r'] = kwargs['80211r']
                if '80211v' in kwargs.keys():
                    temp_object['80211v'] = kwargs['80211v']
                json_input['wireless']['virtual_access_point']['profile'] = [temp_object]
                logger.info(f'edit json_input result: `{json_input}')
                output = self.fw.api_put(profile_url, msg=msg, data=json_input)
                return output
            else:
                loop_sequence += 1
        else:
            logger.info('loop end for profile list, can not find profile name.')
        
        return False

    def add_vap_object_with_profile(self, msg=False, **kwargs):
        profile_list = self.get_vap_profile()
        logger.info(f'profile_list result: {profile_list}')
        for profile in profile_list['wireless']['virtual_access_point']['profile']:
            if profile['name'] == kwargs['profile']:
                logger.info(f'find the except profile in profile list.')
                add_object_json = copy.deepcopy(self.initial_add_object_json)
                add_object_json['wireless']['virtual_access_point']['object'][0].update(profile)
                add_object_json['wireless']['virtual_access_point']['object'][0]['name'] = kwargs['name']
                add_object_json['wireless']['virtual_access_point']['object'][0]['ssid'] = kwargs['ssid']
                add_object_json['wireless']['virtual_access_point']['object'][0]['profile']['wireless'] = kwargs['profile']
                logger.info(f'add object json_input result: {add_object_json}')
                output = self.fw.api_post(self.vap_object, msg=msg, data=add_object_json)
                return output
        else:
            logger.info('loop end for profile list, can not find profile name.')
        
        return False

    def edit_default_vap_groups(self, msg=False, name_list=[]):
        object_url = self.vap_groups + '/name/Internal%20AP%20Group'
        json_input = copy.deepcopy(self.initial_vap_groups_json)
        for name in name_list:
            json_input['wireless']['virtual_access_point']['group'][0]['virtual_access_point'].append({'name': name})
        logger.info(f'edit json_input result: {json_input}')
        output = self.fw.api_put(object_url, msg=msg, data=json_input)
        return output
        

class SettingsApi:
    def __init__(self, fw):
        self.fw = fw
        self.base_settings = 'api/sonicos/wireless/v2/base'
        self.init_settings_json = {
            "wireless": {
                "access_list": {
                    "allow": {},
                    "deny": {}
                },
                "country_code": "United States-US",
                "enable": False,
                "radio_2400mhz": {
                    "aggregation": True,
                    "association_timeout": 300,
                    "band": "auto",
                    "channel": {
                        "primary": "auto",
                        "secondary": "auto"
                    },
                    "data_rate": "best",
                    "enable": False,
                    "green_ap": {
                        "enable": False,
                        "timeout": 20
                    },
                    "interval": {
                        "beacon": 200,
                        "dtim": 1
                    },
                    "max_clients": 128,
                    "mode": "ax-mixed",
                    "preamble_length": "long",
                    "short_guard_interval": True,
                    "threshold": {
                        "rts": 2346
                    },
                    "transmit_power": "full",
                    "virtual_access_point": {
                        "group": "Internal AP Group"
                    }
                },
                "radio_5000mhz": {
                    "aggregation": True,
                    "association_timeout": 300,
                    "band": "auto",
                    "channel": {
                        "standard": "auto"
                    },
                    "data_rate": "best",
                    "dfs_channel": False,
                    "enable": False,
                    "green_ap": {
                        "enable": False,
                        "timeout": 20
                    },
                    "interval": {
                        "beacon": 200,
                        "dtim": 1
                    },
                    "max_clients": 128,
                    "mode": "ax-mixed",
                    "preamble_length": "long",
                    "short_guard_interval": True,
                    "threshold": {
                        "rts": 2346
                    },
                    "transmit_power": "full",
                    "virtual_access_point": {
                        "group": "Internal AP Group"
                    }
                },
                "radio_role": "access-point",
                "station": {
                    "authentication_type": {
                        "open": True
                    },
                    "connectivity_check": False,
                    "enable": False,
                    "mode": "2400mhz",
                    "remote_ip": "0.0.0.0",
                    "ssid": "",
                    "transmit_power": "full",
                    "vlan_id": 0,
                    "wds": False,
                    "wireless_interface_as_wan": False
                }
            }
        }

    def get_base_settings(self):
        url = self.base_settings
        return self.fw.api_get(url)

    def config_wireless_settings(self, msg=False, **kwargs):
        json_input = self.get_base_settings()
        logger.info(f'get base settings result: {json_input}')
        if 'enable' in kwargs.keys():
            json_input['wireless']['enable'] = kwargs['enable']
        if 'country_code' in kwargs.keys():
            json_input['wireless']['country_code'] = kwargs['country_code']
        if 'radio_2400mhz_enable' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['enable'] = kwargs['radio_2400mhz_enable']
        if 'radio_2400mhz_mode' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['mode'] = kwargs['radio_2400mhz_mode']
        if 'radio_2400mhz_band' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['band'] = kwargs['radio_2400mhz_band']
        if 'radio_2400mhz_channel' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['channel'] = kwargs['radio_2400mhz_channel']
        if 'radio_2400mhz_short_guard_interval' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['short_guard_interval'] = kwargs['radio_2400mhz_short_guard_interval']
        if 'radio_2400mhz_virtual_access_point' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['virtual_access_point'] = kwargs['radio_2400mhz_virtual_access_point']
        if 'radio_2400mhz_transmit_power' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['transmit_power'] = kwargs['radio_2400mhz_transmit_power']
        if 'radio_5000mhz_enable' in kwargs.keys():
            json_input['wireless']['radio_5000mhz']['enable'] = kwargs['radio_5000mhz_enable']
        if 'radio_5000mhz_mode' in kwargs.keys():
            json_input['wireless']['radio_5000mhz']['mode'] = kwargs['radio_5000mhz_mode']
        if 'radio_5000mhz_band' in kwargs.keys():
            json_input['wireless']['radio_5000mhz']['band'] = kwargs['radio_5000mhz_band']
        if 'radio_5000mhz_channel' in kwargs.keys():
            json_input['wireless']['radio_5000mhz']['channel'] = kwargs['radio_5000mhz_channel']
        if 'radio_5000mhz_short_guard_interval' in kwargs.keys():
            json_input['wireless']['radio_5000mhz']['short_guard_interval'] = kwargs['radio_5000mhz_short_guard_interval']
        if 'radio_5000mhz_virtual_access_point' in kwargs.keys():
            json_input['wireless']['radio_5000mhz']['virtual_access_point'] = kwargs['radio_5000mhz_virtual_access_point']
        if 'radio_5000mhz_transmit_power' in kwargs.keys():
            json_input['wireless']['radio_5000mhz']['transmit_power'] = kwargs['radio_5000mhz_transmit_power']
        
        logger.info(f'json_input: {json_input}')
        output = self.fw.api_put(self.base_settings, msg, data=json_input)
        return output

    def config_mac_filter_list(self, msg=False, **kwargs):
        json_input = self.get_base_settings()
        if 'allow' in kwargs.keys():
            json_input['wireless']['access_list']['allow'] = kwargs['allow']
        if 'deny' in kwargs.keys():
            json_input['wireless']['access_list']['deny'] = kwargs['deny']
        logger.info(f'json_input: {json_input}')
        output = self.fw.api_put(self.base_settings, msg, data=json_input)
        return output

    def config_radio_2400mhz_basic(self, msg=False, **kwargs):
        json_input = self.get_base_settings()
        logger.info(f'get base settings result: {json_input}')
        if 'enable' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['enable'] = kwargs['enable']
        if 'mode' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['mode'] = kwargs['mode']
        if 'band' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['band'] = kwargs['band']
        if 'channel_primary' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['channel']['primary'] = kwargs['channel_primary']
        if 'channel_secondary' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['channel']['secondary'] = kwargs['channel_secondary']
        if 'short_guard_interval' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['short_guard_interval'] = kwargs['short_guard_interval']
        if 'virtual_access_point' in kwargs.keys():
            json_input['wireless']['radio_2400mhz']['virtual_access_point']['group'] = kwargs['virtual_access_point']

        logger.info(f'json_input: {json_input}')
        output = self.fw.api_put(self.base_settings, msg, data=json_input)
        return output


class IDSApi:
    def __init__(self, fw):
        self.fw = fw
        self.ids = 'api/sonicos/wireless/ids/base'

    def show_ids(self):
        url = self.ids
        return self.fw.api_get(url) 

