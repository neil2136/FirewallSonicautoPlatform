import os
import sys
import copy
import re
import time
import paramunittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/SSHv2_Support_in_FIPS')
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from lib.modules.API import network,system, firewallsettings, firewall
from lib.modules.CLI.firewallsettings import CiphercontrolCli
from utm import Firewall
from lib.modules.CLI.system import LicenseCli, SettingCli, AdminCli
from lib.modules.API import vpn

OpenS = Openstack(Params.testbed)
PC1 = Host(Params.testbed + '-PC1')
TESTPLAN = os.environ['PYTHON_SONICOS_HOME'] + '/Network/SSHv2_Support_in_FIPS/testplan/SSHv2_Support_in_FIPS.json'
def_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/SSHv2_Support_in_FIPS/definition/'
ssh_cp_path = os.environ['PYTHON_SONICOS_HOME'] + '/Network/SSHv2_Support_in_FIPS/definition/ssh_config'
ssh_file = '/etc/ssh/ssh_config'
ssh_file_back = '/etc/ssh/ssh_config.back'
DUT_X0_IPV4 = '192.168.168.168'
DUT_X0_IPV6 = '2001:db0::193'
DUT_X1_IPV4 = '13.0.0.10'
DUT_X1_IPV6 = '2001:db1::193'
DUT_MGMT = '192.168.1.168'

fw_api = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0_IPV4, user='admin', password='sonicauto',ssh_version=2, supported_config_mode='cli-ssh')
fw_ipv6_cli = Firewall(DUT_X0_IPV6, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
mgmt_cli = Firewall(DUT_MGMT, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_wan_cli = Firewall(DUT_X1_IPV4, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

interfacev4api = network.InterfaceIPv4Api(fw_api)
interfacev6api = network.InterfaceIPv6Api(fw_api)
dyn_route = network.DynamicRoutingApi(fw_api)
license_obj = LicenseCli(fw_cli)
diag_api = system.DiagnosticApi(fw_api)
cipher_ssh = firewallsettings.CipherctrlApi(fw_api)
cipher_cli = CiphercontrolCli(fw_cli)
admin_cli = AdminCli(fw_cli)
fips_obj = firewall.FipsApi(fw_api)
fips_cli = SettingCli(fw_cli)
restartobj = system.RestartApi(fw_api)
setting_obj = system.SettingApi(fw_api)
Lvpn = vpn.VpnbasesettingApi(fw_api)


x0_ipv6 = {'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': DUT_X0_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'ra_max': 30
        }
x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUT_X1_IPV4,
            'netmask': '255.255.255.0',
            'gateway': '13.0.0.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https':True,
        }
x1_ipv6 = {'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': DUT_X1_IPV6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'ra_max': 30
            }
MGMT = {
        'if': 'MGMT',
        'zone': 'MGMT',
        'mode': 'static',
        'ip': DUT_MGMT,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
}

cipher_ssh_config1={
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
cipher_ssh_config2={
        "key_exchange":{
            "diffie_hellman_group1_sha1":False,
            "diffie_hellman_group14_sha1":False,
            "diffie_hellman_group_exchange_sha1":False,
            "diffie_hellman_group_exchange_sha256":False,
            "ecdh_sha2_nistp256":True,
            "ecdh_sha2_nistp384":False,
            "ecdh_sha2_nistp521":False,
            },
        "public_key":{
            "ssh_rsa":False,
            "rsa_sha2_256":True,
            "rsa_sha2_512":False,
        },
        "encryption":{
             "aes128_ctr":True,
             "aes192_ctr":False,
             "aes256_ctr":False,
             "aes128_gcm":False,
             "aes256_gcm":False,
             "chacha20_poly1305":False,
        },
         "mac":{
             "hmac_sha1":True,
             "hmac_sha2_256":False,
             "hmac_sha2_512":False
         }
    }
cipher_ssh_config3={
        "key_exchange":{
            "diffie_hellman_group1_sha1":False,
            "diffie_hellman_group14_sha1":False,
            "diffie_hellman_group_exchange_sha1":False,
            "diffie_hellman_group_exchange_sha256":False,
            "ecdh_sha2_nistp256":False,
            "ecdh_sha2_nistp384":True,
            "ecdh_sha2_nistp521":False,
            },
        "public_key":{
            "ssh_rsa":False,
            "rsa_sha2_256":True,
            "rsa_sha2_512":False,
        },
        "encryption":{
             "aes128_ctr":False,
             "aes192_ctr":False,
             "aes256_ctr":False,
             "aes128_gcm":False,
             "aes256_gcm":True,
             "chacha20_poly1305":False,
        },
         "mac":{
             "hmac_sha1":False,
             "hmac_sha2_256":True,
             "hmac_sha2_512":False
         }
    }
cipher_ssh_config4={
        "key_exchange":{
            "diffie_hellman_group1_sha1":False,
            "diffie_hellman_group14_sha1":False,
            "diffie_hellman_group_exchange_sha1":False,
            "diffie_hellman_group_exchange_sha256":False,
            "ecdh_sha2_nistp256":False,
            "ecdh_sha2_nistp384":False,
            "ecdh_sha2_nistp521":True,
            },
        "public_key":{
            "ssh_rsa":False,
            "rsa_sha2_256":False,
            "rsa_sha2_512":True,
        },
        "encryption":{
             "aes128_ctr":False,
             "aes192_ctr":False,
             "aes256_ctr":False,
             "aes128_gcm":False,
             "aes256_gcm":False,
             "chacha20_poly1305":True,
        },
         "mac":{
             "hmac_sha1":False,
             "hmac_sha2_256":False,
             "hmac_sha2_512":True
         }
    }
cipher_ssh_config5={
        "key_exchange":{
            "diffie_hellman_group1_sha1":False,
            "diffie_hellman_group14_sha1":False,
            "diffie_hellman_group_exchange_sha1":False,
            "diffie_hellman_group_exchange_sha256":False,
            "ecdh_sha2_nistp256":True,
            "ecdh_sha2_nistp384":True,
            "ecdh_sha2_nistp521":True,
            },
        "public_key":{
            "ssh_rsa":False,
            "rsa_sha2_256":True,
            "rsa_sha2_512":True,
        },
        "encryption":{
             "aes128_ctr":False,
             "aes192_ctr":False,
             "aes256_ctr":False,
             "aes128_gcm":True,
             "aes256_gcm":True,
             "chacha20_poly1305":False,
        },
         "mac":{
             "hmac_sha1":True,
             "hmac_sha2_256":True,
             "hmac_sha2_512":True
         }
    }

disable_nistp384 =  {
        "key_exchange":{
            "diffie_hellman_group1_sha1":True,
            "diffie_hellman_group14_sha1":True,
            "diffie_hellman_group_exchange_sha1":True,
            "diffie_hellman_group_exchange_sha256":True,
            "ecdh_sha2_nistp256":True,
            "ecdh_sha2_nistp384":False,
            "ecdh_sha2_nistp521":True,
            }
    }
disable_nistp256 =  {
        "key_exchange":{
            "diffie_hellman_group1_sha1":True,
            "diffie_hellman_group14_sha1":True,
            "diffie_hellman_group_exchange_sha1":True,
            "diffie_hellman_group_exchange_sha256":True,
            "ecdh_sha2_nistp256":False,
            "ecdh_sha2_nistp384":True,
            "ecdh_sha2_nistp521":False,
            }
    }
cipher_cli_json1 = {
    'key-exchange ecdh-sha2-nistp256': False,
    'key-exchange ecdh-sha2-nistp384': False,
    'key-exchange ecdh-sha2-nistp521': False,
}
cipher_cli_json2 = {
    'key-exchange ecdh-sha2-nistp256': True,
    'key-exchange ecdh-sha2-nistp384': True,
    'key-exchange ecdh-sha2-nistp521': True,
}
cipher_cli_json3 = {
    'key-exchange diffie-hellman-group1-sha1': True,
    'key-exchange diffie-hellman-group14-sha1': True,
    'key-exchange diffie-hellman-group-exchange-sha1': True,
    'key-exchange diffie-hellman-group-exchange-sha256': True,
    'public-key ssh-rsa': True,
    'encryption aes128-ctr': True,
    'encryption aes192-ctr': True,
    'encryption aes256-ctr': True,
    'encryption chacha20-poly1305': True,
}
cipher_cli_json4 = {
    'key-exchange diffie-hellman-group1-sha1': False,
    'key-exchange diffie-hellman-group14-sha1': False,
    'key-exchange diffie-hellman-group-exchange-sha1': False,
    'key-exchange diffie-hellman-group-exchange-sha256': False,
    'key-exchange ecdh-sha2-nistp256': True,
    'key-exchange ecdh-sha2-nistp384': False,
    'key-exchange ecdh-sha2-nistp512': False,
    'public-key ssh-rsa': False,
    'public-key rsa-sha2-256': True,
    'public-key rsa-sha2-512': False,
    'encryption aes128-ctr': False,
    'encryption aes192-ctr': False,
    'encryption aes256-ctr': False,
    'encryption aes128-gcm': True,
    'encryption aes256-gcm': False,
    'encryption chacha20-poly1305': False,
    'mac hmac-sha1': False,
    'mac hmac-sha2-256': True,
    'mac hmac-sha2-512': False,
}
cipher_cli_json5 = {
    'key-exchange diffie-hellman-group1-sha1': False,
    'key-exchange diffie-hellman-group14-sha1': False,
    'key-exchange diffie-hellman-group-exchange-sha1': False,
    'key-exchange diffie-hellman-group-exchange-sha256': False,
    'key-exchange ecdh-sha2-nistp256': False,
    'key-exchange ecdh-sha2-nistp384': True,
    'key-exchange ecdh-sha2-nistp512': False,
    'public-key ssh-rsa': False,
    'public-key rsa-sha2-256': False,
    'public-key rsa-sha2-512': True,
    'encryption aes128-ctr': False,
    'encryption aes192-ctr': False,
    'encryption aes256-ctr': False,
    'encryption aes128-gcm': True,
    'encryption aes256-gcm': False,
    'encryption chacha20-poly1305': False,
    'mac hmac-sha1': False,
    'mac hmac-sha2-256': False,
    'mac hmac-sha2-512': True,
}
cipher_cli_json6 = {
    'key-exchange diffie-hellman-group1-sha1': False,
    'key-exchange diffie-hellman-group14-sha1': False,
    'key-exchange diffie-hellman-group-exchange-sha1': False,
    'key-exchange diffie-hellman-group-exchange-sha256': False,
    'key-exchange ecdh-sha2-nistp256': False,
    'key-exchange ecdh-sha2-nistp384': False,
    'key-exchange ecdh-sha2-nistp512': True,
    'public-key ssh-rsa': False,
    'public-key rsa-sha2-256': True,
    'public-key rsa-sha2-512': False,
    'encryption aes128-ctr': False,
    'encryption aes192-ctr': False,
    'encryption aes256-ctr': False,
    'encryption aes128-gcm': False,
    'encryption aes256-gcm': True,
    'encryption chacha20-poly1305': False,
    'mac hmac-sha1': True,
    'mac hmac-sha2-256': False,
    'mac hmac-sha2-512': False,
}

fips_dict = {'fips': True}
disable_fips = {'fips': False}
content_json={
    "1524810":"Host * \n    KexAlgorithms ecdh-sha2-nistp256 \n    \
        HostKeyAlgorithms  rsa-sha2-256 \n    Ciphers aes128-ctr \n    MACs hmac-sha1",
    "1524811":"Host * \n    KexAlgorithms ecdh-sha2-nistp384 \n    \
        HostKeyAlgorithms  rsa-sha2-256 \n    Ciphers aes256-gcm@openssh.com \n    MACs hmac-sha2-256",
    "1524812":"Host * \n    KexAlgorithms ecdh-sha2-nistp521 \n    \
        HostKeyAlgorithms  rsa-sha2-512 \n    Ciphers chacha20-poly1305@openssh.com \n    MACs hmac-sha2-512",
    "1524813":"Host * \n    KexAlgorithms ecdh-sha2-nistp256 \n    \
        HostKeyAlgorithms  rsa-sha2-256 \n    Ciphers aes128-gcm@openssh.com \n    MACs hmac-sha2-256",
    "1524814":"Host * \n    KexAlgorithms ecdh-sha2-nistp384 \n    \
        HostKeyAlgorithms  rsa-sha2-512 \n    Ciphers aes128-gcm@openssh.com \n    MACs hmac-sha2-512",
    "1524815":"Host * \n    KexAlgorithms ecdh-sha2-nistp521 \n    \
        HostKeyAlgorithms  rsa-sha2-256 \n    Ciphers aes256-gcm@openssh.com \n    MACs hmac-sha1",
}
api_dict = {
    'sonicos-api': True,
    'basic': False,      
    'digest': False,      
    'enable': False,      
    'chap': False,      
}
api_enable_dict = {
    'sonicos-api': True,
    'basic': True,      
    'digest': True,      
    'enable': True,      
    'chap': True,      
}
wan_groupvpn = {
            'enable': False,
            'secret': 'password',
            'auth_mode': 'shared_secret',
            'ike_encryption': 'aes-128',
            'ike_auth': 'sha-256',
            'ike_dh_group': '14',
            'ike_lifetime': 28800,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_128',
            'ipsec_auth': 'sha_256',
            'management_https':False,
            'management_ssh':False,
            'management_snmp':False,
            }
wlan_groupvpn = {
            'enable': False,
            'secret': 'password',
            'auth_mode': 'shared_secret',
            'ike_encryption': 'aes-128',
            'ike_auth': 'sha-256',
            'ike_dh_group': '14',
            'ike_lifetime': 28800,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_128',
            'ipsec_auth': 'sha_256',
            'management_https':False,
            'management_ssh':False,
            'management_snmp':False,
        }
vpn_base_dict={"vpn":{
            "ikev2":{
                "send_cookie":False,
                "send_invalid_spi":True,
                "proposal":{
                    "dh_group":"14",
                    "encryption":"aes-256",
                    "authentication":"sha-256"
                    }
                }
            }
        }
