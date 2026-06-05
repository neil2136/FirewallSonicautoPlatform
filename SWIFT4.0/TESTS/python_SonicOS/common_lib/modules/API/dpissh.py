#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)
from runner.settings import logger
from runner.utils.assertion import Assertion

import copy
import json


class DpiSSHApi:
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/dpi-ssh'
        self.initial_general_settings_json = {
            "dpi_ssh": {
                "enable": False,
                "application_firewall": False,
                "intrusion_prevention": False,
                "gateway": {
                    "anti_virus": False,
                    "anti_spyware": False
                },
                "block_port_forwarding": {
                    "global": False,
                    "local": False,
                    "remote": False,
                    "x11": False
                },
                "include": {
                    "address": {
                        "all": True
                    },
                    "service": {
                        "all": True
                    },
                    "user": {
                        "all": True
                    }
                },
                "exclude": {
                    "address": {},
                    "service": {},
                    "user": {}
                }
            }
        }


    def config_general_settings(self, msg=False, **api):
        json_string = self.build_json_general_settings(**api)
        retval = self.fw.api_put(self.url, msg, data=json_string)
        return retval

    def build_json_general_settings(self, **api):
        json_string = {}
        logger.info(api)

        try:
            json_string = copy.deepcopy(self.initial_general_settings_json)

            if 'enable' in api:
                json_string['dpi_ssh']['enable'] = api['enable']

            if 'application_firewall' in api:
                json_string['dpi_ssh']['application_firewall'] = api['application_firewall']

            if 'intrusion_prevention' in api:
                json_string['dpi_ssh']['intrusion_prevention'] = api['intrusion_prevention']

            if 'gateway_anti_virus' in api:
                json_string['dpi_ssh']['gateway']['anti_virus'] = api['gateway_anti_virus']

            if 'gateway_anti_spyware' in api:
                json_string['dpi_ssh']['gateway']['anti_spyware'] = api['gateway_anti_spyware']

            if 'block_port_forwarding_global' in api:
                logger.info('6666666666')
                json_string['dpi_ssh']['block_port_forwarding']['global'] = api['block_port_forwarding_global']

            if 'block_port_forwarding_local' in api:
                json_string['dpi_ssh']['block_port_forwarding']['local'] = api['block_port_forwarding_local']

            if 'block_port_forwarding_remote' in api:
                json_string['dpi_ssh']['block_port_forwarding']['remote'] = api['block_port_forwarding_remote']

            if 'block_port_forwarding_x11' in api:
                logger.info('6666666666')
                json_string['dpi_ssh']['block_port_forwarding']['x11'] = api['block_port_forwarding_x11']

            if 'exclude_address' in api and 'exclude_address_type' in api:
                json_string['dpi_ssh']['exclude']['address'][api['exclude_address_type']] = api['exclude_address']

            if 'exclude_address_name' in api:
                json_string['dpi_ssh']['exclude']['address']['name'] = api['exclude_address_name']

            if 'include_address_name' in api :
                json_string['dpi_ssh']['include']['address']['name'] = api['include_address_name']
                del json_string['dpi_ssh']['include']['address']['all']

                
            if 'include_user_name' in api:
                json_string['dpi_ssh']['include']['user']['name'] = api['include_user_name']

            if 'exclude_user_name' in api:
                json_string['dpi_ssh']['exclude']['user']['name'] = api['exclude_user_name']

            if 'include_service_name' in api:
                json_string['dpi_ssh']['include']['service']['name'] = api['include_service_name']

            if 'exclude_service_name' in api:
                json_string['dpi_ssh']['exclude']['service']['name'] = api['exclude_service_name']

            if 'exclude_address_group' in api:
                json_string['dpi_ssh']['exclude']['address']['group'] = api['exclude_address_group']

            if 'exclude_user' in api and 'exclude_user_type' in api:
                json_string['dpi_ssh']['exclude']['user'][api['exclude_user_type']] = api['exclude_user']

            if 'exclude_service' in api and 'exclude_service_type' in api:
                json_string['dpi_ssh']['exclude']['service'][api['exclude_service_type']] = api['exclude_service']

            if 'include_address' in api and api['include_address_type'] != 'all':
                json_string['dpi_ssh']['include']['address'][api['include_address_type']] = api['include_address']
                del json_string['dpi_ssh']['include']['address']['all']

            if 'include_service' in api and api['include_service_type'] != 'all':
                json_string['dpi_ssh']['include']['service'][api['include_service_type']] = api['include_service']
                del json_string['dpi_ssh']['include']['service']['all']

            if 'include_user' in api and api['include_user_type'] != 'all':
                json_string['dpi_ssh']['include']['user'][api['include_user_type']] = api['include_user']
                del json_string['dpi_ssh']['include']['user']['all']

        except KeyError:
            logger.error("ERROR: json string cannot be constructed")
        logger.info(json_string)

        return json_string

    def get_dpi_ssh_status(self):
        rc = self.fw.api_get(self.url)
        return rc

