import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from accesspoint import AccessPoint

if __name__ == '__main__':
    firewall_ip = '192.168.168.168'
    fw = Firewall(firewall_ip, user='admin', password='password')
    apApi = AccessPoint(fw)
    sonicwave_wep = {
        'enable': False,
        'name': "SonicWave 231o e9479d",
        '5g_radio': True,
        '5g_mode': "ac-na-mixed",
        '5g_ssid': "sonic-terry",
#        '5g_radio_band': "auto",
#        '5g_auth_type': "wep",
#        '5g_wep_mode': "none",
#        '5g_wep_none': "shared-key",
        '5g_wep': 'shared-key', 
        '5g_wep_type' : "64", 
        '5g_wep_method': "hexadecimal",
        '5g_wep_default': "1",
        '5g_wep_pass_1' : "1111111111",
        '5g_wep_pass_2' : "1111111111",
        '5g_wep_pass_3' : "1111111111",
#        '5g_wep_pass_4' : "1111111111",
        '5g_hide_ssid': False,
        '5g_min_data_rate': "best",
        '5g_transmit_power': "full",
        '5g_beacon_interval': 100,
        '5g_dtim_interval': 1,
        '5g_rts_threshold': -65,
        '5g_max_clients': 32,
        '5g_inactive_timeout': 300,
        '5g_enable_wds': False,
        '5g_enable_green': False,
        '5g_enable_rssi': False,
        '5g_enable_air_time_fairness':False,
        '5g_enable_802.11r': False,
        '5g_enable_neighbour_report': False,
        '5g_enable_bss': False,
        '5g_enable_wnm_sleep': False
    }
    sonicwave_wpa = {
        'enable': False,
        'name': "SonicWave 231o e9479d",
        '5g_radio': True,
        '5g_mode': "ac-na-mixed",
        '5g_ssid': "sonic-terry",
        'wpa_auth_type': '5g_wpa_auto_psk',
        '5g_cipher_type': 'auto', 
        '5g_group_key_interval': 86400,
        '5g_passwd': 'password',
#        '5g_auth_method': 'remote-radius-only',
    }
    apApi.config_accesspoint(**sonicwave_wpa)
    n-only|na-mixed|a-only|ac-na-mixed|ac-only
    
"""
sonicwave_wep_bbb = {
    'enable': True,
    'name': "SonicWave 231o e9479d",
    'country_code': "United Kingdom",
    '5g_mode': "n-only",
    '5g_ssid': "bbb",
    '5g_wep_none': "both",
    '2g_mode': "n_only",
    '2g_ssid': "bbb",
    '2g_wep_none': "both",
}

sonicwave_wep_ngb = {
    'enable': True,
    'name': "SonicWave 231o e9479d",
    'country_code': "United Kingdom",
    '2g_mode': 'ngb_mixed',
    '2g_ssid': 'terry-ngb-2G',
    '5g_wep_none': "both",
    '2g_wep_none': "both",
}

sonicwave_wep_na = {
    'enable': True,
    'name': "SonicWave 432o 7b8e46",
    'country_code': "United States",
    '5g_mode': 'na-mixed',
    '5g_ssid': 'terry-na-5G',
    '5g_wep_none': "both",
    '2g_wep_none': "both",
}

sonicwave_wep_hide = {
    'enable': True,
    'name': "SonicWave 432o 7b8e46",
    'country_code': "United States",
    '2g_ssid': 'terry-hide-2G',
    '2g_hide_ssid': True,
    '5g_wep_none': "both",
    '2g_wep_none': "both",
}

sonicwave_wep_5g_auto = {
    'enable': True,
    'name': "SonicWave 432o 7b8e46",
    'country_code': "United States",
    '5g_mode': 'na-mixed',
    '5g_radio_band': 'auto',
    '5g_ssid': 'terry-na-5G-auto',
    '5g_wep_none': "both",
    '2g_wep_none': "both",
}

sonicwave_wep_5g_manual = {
    'enable': True,
    'name': "SonicWave 432o 7b8e46",
    'country_code': "United States",
    '5g_mode': 'na-mixed',
    '5g_radio_band': '40',
    '5g_primary_channel': '40',
    '5g_ssid': 'terry-na-5G-manual',
    '5g_wep_none': "both",
    '2g_wep_none': "both",
}

    sonicwave_wpa_psk = {
        'enable': True,
        'name': "SonicWave 432o 7b8e46",
        'country_code': "United States",
        '5g_wep_none': "both",
        'wpa_auth_type': '2g_wpa_psk',
        '2g_cipher_type': 'AES',
        '5g_ssid': "bbb",
        '2g_ssid': 'terry-aaa'
    }
    
    sonicwave_wpa_auto_psk = {
        'enable': True,
        'name': "SonicWave 432o 7b8e46",
        'country_code': "United States",
        '5g_ssid': "aaa",
        '5g_wep_none': "both",
        '2g_ssid': 'terry-aaa',
        'wpa_auth_type': '2g_wpa_auto_psk',
        '2g_cipher_type': 'AUTO',
    }
    
    sonicwave_wpa_auto_eap = {
        'enable': True,
        'name': "SonicWave 432o 7b8e46",
        'country_code': "United States",
        '5g_ssid': "aaa",
        '5g_wep_none': "both",
        '2g_ssid': 'terry-aaa',
        'wpa_auth_type': '2g_wpa_auto_eap',
        '2g_cipher_type': 'AUTO',
        'radius_server1_ip': '10.8.116.178',
        'radius_server1_pass': 'password'
    }
"""