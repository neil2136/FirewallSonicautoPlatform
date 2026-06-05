import copy
import json
import re
from runner.settings import logger


class WireguardPeerBaseSettingAPI:
    """VpnbasesettingApi class"""
    default_wireguard_peer_json = {
        "name": "autotest1",
        "ip": "192.168.2.12",
        "public_key": "",
        "preshared_key": "",
        "private_key": ""
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/wireguard/peers'
        self.exporturl = 'api/sonicos/export/wireguard/peer'
        self.delurl = 'api/sonicos/wireguard/peers-all'
        self.initial_wireguard_peer_json = {
            "wireguard": {
                "peer": [{
                    "name": "autotest0",
                    "ip": "192.168.2.11",
                    "public_key": "",
                    "preshared_key": "",
                    "private_key": ""
                }]}}

    def add_wireguard_peer(self, msg=False, **kwargs):
        self.options = dict(WireguardPeerBaseSettingAPI.default_wireguard_peer_json)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_wireguard_peer(**kwargs)

        addvpnpolicy_resp = self.fw.api_post(self.url, msg, data=json_input)
        return addvpnpolicy_resp

    def edit_wireguard_peer(self, msg=False, **kwargs):
        self.options = dict(WireguardPeerBaseSettingAPI.default_wireguard_peer_json)
        self.options.update(kwargs)
        kwargs = self.options
        if kwargs['originalname']:
            self.url = self.url + '/name/' + kwargs['originalname']
            json_input = self.build_json_wireguard_peer(**kwargs)

            output = self.fw.api_put(self.url, msg, data=json_input)
            return output
        else:
            logger.error('not original name in wireguard peer input dict! ')
            return False

    def del_all_peers(self, msg=False):
        dels2svpn_resp = self.fw.api_delete(self.delurl, msg, data={})
        return dels2svpn_resp

    def export_wireguard_peer(self, exportname):
        if exportname:
            self.exporturl = self.exporturl + '/' + exportname
            output = self.fw.api_get(self.exporturl)
            return output

    def show_wireguard_peer(self):
        output = self.fw.api_get(self.url)
        return output

    def build_json_wireguard_peer(self, **kwargs):
        json_input = copy.deepcopy(self.initial_wireguard_peer_json)
        logger.info(kwargs)
        try:
            # json_input = copy.deepcopy(self.initial_wireguard_peer_json)
            logger.info("\n\nInitial Json is :\n")
            path = json_input['wireguard']['peer'][0]
            path['name'] = kwargs['name']
            path['ip'] = kwargs['ip']
            path['public_key'] = kwargs['public_key']
            path['preshared_key'] = kwargs['preshared_key']
            path['private_key'] = kwargs['private_key']

        except KeyError:
            logger.info("Error in creating JSON for wireguard peer setting")
        logger.info("wireguard peer json obtained")
        logger.info(json_input)
        return json_input


class WireguardTunnelInterfaceAPI:
    """WireguardTunnelInterfaceAPI class"""
    default_wireguard_tunnel_json = {
        "comment": "Default WireGuard",
        "ip": "192.168.2.1",
        "netmask": "255.255.255.0",
        "listen_port": 51820,
        "public_key": "",
        "private_key": "",
        "mtu": 1420
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/tunnel-interfaces/wireguard'
        self.interface = 'api/sonicos/interfaces/ipv4'

        self.initial_wireguard_tunnel_json = {
            "tunnel_interfaces": [
                {
                    "wireguard": {
                        "comment": "Default WireGuard",
                        "fragment_packets": False,
                        "ip_assignment": {
                            "mode": {
                                "static": {
                                    "ip": "192.168.2.1",
                                    "netmask": "255.255.255.0"
                                }
                            },
                            "zone": "WIREGUARD"
                        },
                        "listen_port": 51820,
                        "mtu": 1420,
                        "private_key": "",
                        "public_key": ""
                    }
                }
            ]
        }

    def show_wireguard_tunnel(self):
        # self.fw.api_get(self.interface)
        output = self.fw.api_get(self.url)
        return output

    def edit_wireguard_tunnel(self, msg=False, **kwargs):
        self.options = dict(WireguardTunnelInterfaceAPI.default_wireguard_tunnel_json)
        self.options.update(kwargs)
        kwargs = self.options

        json_input = self.build_json_wireguard_tunnel(**kwargs)
        output = self.fw.api_put(self.url + '/name/WG0', msg, data=json_input)
        return output

    def build_json_wireguard_tunnel(self, **kwargs):
        json_input = copy.deepcopy(self.initial_wireguard_tunnel_json)
        # logger.info(kwargs)
        try:
            logger.info("\n\nInitial Json is :\n")
            path = json_input['tunnel_interfaces'][0]['wireguard']
            path['comment'] = kwargs['comment']
            path['ip_assignment']['mode']['static']['ip'] = kwargs['ip']
            path['ip_assignment']['mode']['static']['netmask'] = kwargs['netmask']
            path['listen_port'] = kwargs['listen_port']
            if kwargs['public_key'] and kwargs['private_key']:
                path['public_key'] = kwargs['public_key']
                path['private_key'] = kwargs['private_key']
            else:
                loggin.error('can not get the public_key and private_key')
            path['mtu'] = kwargs['mtu']

        except KeyError:
            logger.error("Error in creating JSON for wireguard tunnel setting")
        logger.info("wireguard tunnel json obtained")
        # logger.info(json_input)
        return json_input


class WireguardGeneralSettingAPI:
    """WireguardGeneralSettingAPI class"""
    default_wireguard_base_json = {
        "enable": True,
        "allowedipsany": True,
        "primarydns": "0.0.0.0",
        "secondarydns": "0.0.0.0",
        "tertiarydns": "0.0.0.0"
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/wireguard/base'
        self.searchurl = 'api/sonicos/wireguard/search-list'
        self.initial_wireguard_base_json = {
            "wireguard": {
                "enable": True,
                "peer_allowed_ips": {
                    "any": True
                },
                "peer_dns": {
                    "server": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    }
                }
            }
        }
        self.initial_wireguard_search_list_json = {
            "wireguard": {
                "peer_dns": {}
            }
        }

    def show_base_status(self):
        output = self.fw.api_get(self.url)
        return output

    def show_search_list_setting(self):
        output = self.fw.api_get(self.searchurl)
        return output

    def edit_base_setting(self, msg=False, **kwargs):
        self.options = dict(WireguardGeneralSettingAPI.default_wireguard_base_json)
        self.options.update(kwargs)
        kwargs = self.options

        json_input = self.build_json_wireguard_base(**kwargs)
        output = self.fw.api_put(self.url, msg, data=json_input)
        return output

    def build_json_wireguard_base(self, **kwargs):
        json_input = copy.deepcopy(self.initial_wireguard_base_json)
        logger.info(kwargs)
        try:
            logger.info("\n\nInitial Json is :\n")
            path = json_input['wireguard']
            path['enable'] = kwargs['enable']
            path['peer_allowed_ips']['any'] = kwargs['allowedipsany']
            if kwargs['allowedipsname']:
                path['peer_allowed_ips']['name'] = kwargs['allowedipsname']
                del path['peer_allowed_ips']['any']
            path['peer_dns']['server']['primary'] = kwargs['primarydns']
            path['peer_dns']['server']['primary'] = kwargs['secondarydns']
            path['peer_dns']['server']['primary'] = kwargs['tertiarydns']

        except KeyError:
            logger.error("Error in creating JSON for wireguard base setting")
        logger.info("wireguard base json obtained.")
        logger.info(json_input)
        return json_input


