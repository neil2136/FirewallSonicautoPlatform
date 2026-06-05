''' __author__ = 'chu' '''
import copy
import time
import json
from pprint import pprint
from runner.settings import logger

class StatusApi:
    '''StatusApi class'''
    def __init__(self, fw):
        self.fw = fw
        self.url_status = 'api/sonicos/reporting/high-availability'
        self.url_settings = 'api/sonicos/high-availability/base'

    def show_ha_status(self):
        output = self.fw.api_get(self.url_status)
        return output

    def show_ha_settings(self):
        output = self.fw.api_get(self.url_settings)
        return output


class SettingsApi:
    '''SettingsApi class'''

    default_active_active_dpi_options = {
        'mode'                      : 'active_standby',         # None, active_standby
        'control_interface'         : 'X6',                     # HA control port
        'data_interface'            : 'X4',                     # Data port
        'secondary_serial'          : '000000000099',
        'stateful_synchronization'  : False,
        'preempt'                   : False,
        'virtual_mac'               : False,
        'encryption'                : False,
        # 'dpi_interface'             : [{'id': 1, 'interface': 'X4'}],
        # 'generate_backup_firmware'  : False,
    }

    default_clustering_dpi_options = {
        'mode': 'active_active_clustering_dpi',
        'stateful_synchronization': True,
        'active_active_cluster_link': [{'interface': 'X3', 'link': 1}, {'interface': 'X4', 'link': 2}],
        'control_interface': 'X2',
        'data_interface': 'X5',
        'dpi_interface': [{'id': 1, 'interface': 'X6'}],
        'generate_backup_firmware': False,
        'node_num': 2,
        'switched_link': False,
        'rank': [{'node': 1, 'rank': 'owner', 'virtual_group': 1},
                 {'node': 1, 'rank': 'standby', 'virtual_group': 2},
                 {'node': 2, 'rank': 'standby', 'virtual_group': 1},
                 {'node': 2, 'rank': 'owner', 'virtual_group': 2}],
        'serial': [
                   {'node': 1, 'secondary': '000000000001'},
#                   {'node': 2, 'primary': '000000000003'},
                   {'node': 2, 'secondary': '00:00:00:00:00:04'}],
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/high-availability/base'

        self.initial_clustring_dpi_json = {
            'high_availability': {
                'mode': {'active_active_clustering_dpi': {
                    'active_active_cluster_link': [
                        {'interface': 'X3', 'link': 1},
                        {'interface': 'X4', 'link': 2}],
                    'control_interface': 'X2',
                    'data_interface': 'X5',
                    'dpi_interface': [{'id': 1, 'interface': 'X6'}],
                    'generate_backup_firmware': False,
                    'node_num': 2,
                    'rank': [{'node': 1, 'rank': 'owner', 'virtual_group': 1},
                             {'node': 1, 'rank': 'standby', 'virtual_group': 2},
                             {'node': 2, 'rank': 'standby', 'virtual_group': 1},
                             {'node': 2, 'rank': 'owner', 'virtual_group': 2}],
                    'serial': [
                        {'node': 1, 'secondary': '000000000001'},
                        {'node': 2, 'primary': '000000000002'},
                        {'node': 2, 'secondary': '00:00:00:00:00:00'}],
                    'switched_link': False}}}
        }

    def show_ha_settings(self):
        output = self.fw.api_get(self.url)
        return output

    def config_mode_active(self, msg=False, **kwargs):
        logger.info(kwargs)
        json_input = self.fw.api_get(self.url)

        try:
            keys = list(json_input['high_availability']['mode'].keys())
            if keys:
                if 'mode' in kwargs.keys():
                    mode = kwargs['mode']
                    kwargs.pop('mode')
                else:
                    mode = keys[0]
            else:                               # If firewall is in None mode
                if 'mode' in kwargs.keys():
                    mode = kwargs['mode']
                    json_input['high_availability']['mode'][mode] = {}
                    kwargs.pop('mode')
                else:
                    logger.error('The DUT is None mode now, it need mode param.')
                    return False

            if mode == 'active_standby':
                path = json_input['high_availability']['mode'][mode]

                if not path.keys():
                    if 'control_interface' not in kwargs.keys() or 'secondary_serial' not in kwargs.keys():
                        logger.error('>> Error! << Must have control interface and secondary serial')
                        raise KeyError

                if 'stateful_synchronization' in kwargs.keys():
                    stateful = kwargs['stateful_synchronization']
                else:
                    if 'stateful_synchronization' in path.keys():
                        stateful = path['stateful_synchronization']
                    else:    # from None mode
                        stateful = False

                if stateful:
                    if 'data_interface' not in kwargs.keys() and 'data_interface' not in path.keys():
                        logger.error('>> Error! << Data interface need to input.')
                        raise KeyError
                else:
                    if 'data_interface' in path.keys():
                        path.pop('data_interface')
                    if 'data_interface' in kwargs.keys():
                        kwargs.pop('data_interface')

                for kwd in kwargs.keys():
                    path[kwd] = kwargs[kwd]

                json_input['high_availability']['mode'][mode] = path

            #### need to update later ####
            ## update the mode-key from "active_active_dpi" to the real mode in json_input

            if mode == 'None':
                json_input['high_availability']['mode'] = {}
        except KeyError:
            logger.error("----->>>>>> KeyError in creating JSON for mode active setting")
            return False

        pprint(json_input)
        ha_mode_resp = self.fw.api_put(self.url, msg, data=json_input)
        return ha_mode_resp

    def config_mode_active_clustering(self, msg=False, **kwargs):
        self.options = dict(SettingsApi.default_clustering_dpi_options)
        self.options.update(kwargs)
        kwargs = self.options
        logger.info(kwargs)
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_clustring_dpi_json)
            # update the mode-key from "active_active_clustering_dpi" to the real mode in json_input
            if json_input['high_availability']['mode']['active_active_clustering_dpi']:
                json_input['high_availability']['mode'][kwargs['mode']] = json_input['high_availability']['mode'].pop("active_active_clustering_dpi")
            path = json_input['high_availability']['mode'][kwargs['mode']]
            path['active_active_cluster_link'] = kwargs['active_active_cluster_link']
            path['control_interface'] = kwargs['control_interface']
            path['generate_backup_firmware'] = kwargs['generate_backup_firmware']
            path['node_num'] = kwargs['node_num']
            path['switched_link'] = kwargs['switched_link']
            path['rank'] = kwargs['rank']
            path['serial'] = kwargs['serial']
            if kwargs['mode'] == 'active_active_clustering':
                del path['data_interface']
                del path['dpi_interface']
                path['stateful_synchronization'] = kwargs['stateful_synchronization']
            if kwargs['mode'] == 'active_active_clustering_dpi':
                path['data_interface'] = kwargs['data_interface']
                path['dpi_interface'] = kwargs['dpi_interface']
        except KeyError:
            logger.error("----->>>>>> Error in creating JSON for mode clustering setting")
        pprint(json_input)
        ha_mode_resp = self.fw.api_put(self.url, msg, data=json_input)
        return ha_mode_resp


class AdvancedApi:
    '''AdvancedApi class'''
    default_advanced_options = {
        'heartbeat_interval'            : 1000,         # default 1000, min 1000, max 300000.
        'failover_trigger_level'        : 5,            # default 5, min 4, max 99.
        'probe_interval'                : 20,           # default 20, min 5, max 255
        'probe_count'                   : 3,            # default 3, min 3, max 10.
        'election_delay_time'           : 3,            # default 3, min 3, max 255.
        'sdwan_hold_down_time'          : 10,
        'failover_when_aggregate_down'  : False,
        'include_certificates_keys'     : True,
        # 'mgmt_heartbeat'                : True,
        # 'route_hold_down_time'          : 45,
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/high-availability/base'
        self.sync_settings_url = 'api/sonicos/high-availability/synchronize/settings'
        self.sync_firmware_url = 'api/sonicos/high-availability/synchronize/firmware'
        self.force_failover_url = 'api/sonicos/high-availability/force-failover'

    def show_ha_advanced(self):
        output = self.fw.api_get(self.url)
        return output

    def config_ha_advanced(self, msg=False, **kwargs):
        logger.info(kwargs)
        json_input = self.fw.api_get(self.url)
        try:
            path = json_input['high_availability']
            for kwd in kwargs.keys():
                if kwd == 'route_hold_down_time' :
                    path['route_hold_down_time']['value'] = kwargs['route_hold_down_time']
                elif kwd == 'probe_interval':
                    path['probe']['interval'] = kwargs['probe_interval']
                elif kwd == 'probe_count':
                    path['probe']['count'] = kwargs['probe_count']
                else:
                    path[kwd] = kwargs[kwd]
            json_input['high_availability'] = path
        except KeyError:
            logger.error("----->>>>>> KeyError in creating JSON for ha_advanced setting")
            return False

        pprint(json_input)
        ha_advanced_resp = self.fw.api_put(self.url, msg, data=json_input)
        return ha_advanced_resp

    def synchronize_settings(self):
        resp = self.fw.api_post(url=self.sync_settings_url)
        if resp:
            res = self._is_peer_boot_up()
        else:
            return resp
        return res

    # only trigger sync and get sync msg
    def synchronize_settings_by_msg(self, msg=True):
        return self.fw.api_post(url=self.sync_settings_url, msg=msg)

    def synchronize_firmware(self):
        resp = self.fw.api_post(url=self.sync_firmware_url)
        if resp:
            res = self._is_peer_boot_up()
        else:
            return resp
        return res

    def force_failover(self):
        resp = self.fw.api_post(url=self.force_failover_url)
        return resp

    def _is_peer_boot_up(self):
        logger.info('---> Please waiting for 300s <---')
        time.sleep(300)
        for i in range(10):
            out = StatusApi(self.fw).show_ha_status()
            if 'STANDBY' in str(out):
                logger.info('--->>> Peer boots up!')
                return True
            logger.info(" {} ".center(20, '-').format('Sleep 30s for firewall up'))
            time.sleep(30)
        return False

class MonitoringApi:
    '''MonitoringApi class'''
    default_monitoring_options = {
        'interface'                     : '',                   # like X0, X1, X2...
        'version'                       : '',                   # like ipv4, ipv6
        'link_monitoring'               : True,
        'primary'                       : '0.0.0.0',
        'secondary'                     : '0.0.0.0',
        'allow_management'              : False,
        'logical_probe_enable'          : False,
        'logical_probe_ip'              :'0.0.0.0',
        'override_virtual_mac_enable'   : False,                # need to enable 'virtual_mac' in SettingsApi
        'override_virtual_mac'          :'00:00:00:00:00:00',
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/high-availability/monitoring/'

    def show_monitoring(self, msg=False, **kwargs):  # can extend
        try:
            if 'version' not in kwargs.keys() or 'interface' not in kwargs.keys():
                logger.error('>> Error! << Version and interface must have!')
                raise KeyError
            url_monitoring = self.url + kwargs['version'] + '/interface/' + kwargs['interface']
            output = self.fw.api_get(url_monitoring)
            return output
        except KeyError:
            logger.error(">> Error! << Please specify the right IP version and interface")
            return False

    def config_ha_monitoring(self, msg=False, **kwargs):
        logger.info(kwargs)
        try:
            if 'version' not in kwargs.keys() or 'interface' not in kwargs.keys():
                logger.error('>> Error! << Version and interface must have!')
                raise KeyError

            version =  kwargs['version']
            if version in ['ipv4','ipv6']:
                url_monitoring = self.url + kwargs['version'] + '/interface/' + kwargs['interface']
                json_input = self.fw.api_get(url_monitoring)
            else:
                logger.error(">> Error! << please specify the right IP version")
                raise KeyError

            path = json_input['high_availability']['monitoring']['interface'][0][version]
            path['name'] = kwargs['interface']
            kwargs.pop('interface')
            kwargs.pop('version')

            if 'allow_management' in kwargs.keys() and path['allow_management'] != kwargs['allow_management']:
                if kwargs['allow_management']:
                    if 'primary' not in kwargs.keys() or 'secondary' not in kwargs.keys():
                        logger.error('Both Pri and Sec IPs need to be configured for Management to be enabled')
                        return False

            if 'logical_probe_enable' in kwargs.keys() and path['logical_probe']['enable'] != kwargs[
                'logical_probe_enable']:
                if kwargs['logical_probe_enable']:
                    if 'logical_probe_ip' in kwargs.keys():
                        if 'primary' not in kwargs.keys() or 'secondary' not in kwargs.keys():
                            logger.error('Both Pri and Sec IPs need to be configured for Probe to be enabled')
                            return False
                        else:
                            path['logical_probe']['ip'] = kwargs['logical_probe_ip']
                    else:
                        logger.error('Logical probe ip need to config')
                        return False
                else:
                    path['logical_probe']['ip'] = ''
                path['logical_probe']['enable'] = kwargs['logical_probe_enable']
                kwargs.pop('logical_probe_enable')
            else:
                if path['logical_probe']['enable'] and 'logical_probe_ip' in kwargs.keys():
                    path['logical_probe']['ip'] = kwargs['logical_probe_ip']

            if 'override_virtual_mac_enable' in kwargs.keys():
                path['override_virtual_mac']['enable'] = kwargs['override_virtual_mac_enable']
                if kwargs['override_virtual_mac_enable']:
                    if 'override_virtual_mac' in kwargs.keys():
                        path['override_virtual_mac']['mac'] = kwargs['override_virtual_mac']
                    else:
                        logger.error('Override virtual mac need to config')
                        return False
                kwargs.pop('override_virtual_mac_enable')
            else:
                if path['override_virtual_mac']['enable'] and 'override_virtual_mac' in kwargs.keys():
                    path['override_virtual_mac']['mac'] = kwargs['override_virtual_mac']

            for kwd in kwargs.keys():
                if kwd in ['logical_probe_ip', 'override_virtual_mac']:
                    continue
                path[kwd] = kwargs[kwd]
            json_input['high_availability']['monitoring']['interface'][0][version] = path
        except KeyError:
            logger.error("----->>>>>> KeyError in creating JSON for monitoring setting")
            return False

        pprint(json_input)
        monitoring_resp = self.fw.api_put(url_monitoring, msg, data=json_input)
        return monitoring_resp
