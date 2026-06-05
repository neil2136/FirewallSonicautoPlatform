import os
import sys
import re
import time

FIREWALL = '192.168.168.168'
from lib.modules.API.wireguard import WireguardPeerBaseSettingAPI, WireguardTunnelInterfaceAPI, \
    WireguardGeneralSettingAPI
from utm import Firewall


fw = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')


PC1_ETH0_IP = '192.168.168.169'
PC2_wg0_IP = '192.168.2.10'
PC2_ETH0_IP = '172.16.1.200'
PC2_ETH1_IP = '10.0.1.200'


wg_tunnel_edit_dict = {
    "comment": "Default WireGuard",
    "ip": "192.168.2.5",
    "netmask": "255.255.255.0",
    "listen_port": 51820,
    "public_key": "",
    "private_key": "",
    "mtu": 1420
}

wg_base_setting_dict = {
    "enable": True,
    "allowedipsany": True
}

wg_peer_dict = {
    "name": "autotest10",
    "ip": PC2_wg0_IP,
    "public_key": "",
    "preshared_key": "",
    "private_key": ""
}


#wgpeerbasesetting = WireguardPeerBaseSettingAPI(fw)
#wgpeerbasesetting.add_wireguard_peer(**wg_peer_dict)
#wgpeerbasesetting.del_all_peers()
#wgpeerbasesetting.export_wireguard_peer(wg_peer_dict['name'])
#wgpeerbasesetting.show_wireguard_peer()

#wgtunnelinterface = WireguardTunnelInterfaceAPI(fw)
#wgtunnelinterface.show_wireguard_tunnel()
#wgtunnelinterface.edit_wireguard_tunnel(**wg_tunnel_edit_dict)


#wgbasesetting = WireguardGeneralSettingAPI(fw)
#wgbasesetting.edit_base_setting(**wg_base_setting_dict)
#wgbasesetting.show_base_status()

