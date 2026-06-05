import copy
from modules.API.firewallsettings import AdvanceApi
from modules.API.firewallsettings import BwmApi
from modules.API.firewallsettings import FloodprotectionApi
from modules.API.firewallsettings import MulticastApi
from modules.API.firewallsettings import SslcontrolApi
from modules.API.firewallsettings import QosmappingApi
from modules.API.firewallsettings import CipherctrlApi
from runner.settings import logger


class AdvanceApi(AdvanceApi):
    '''Advanced Api class'''

        
class BwmApi(BwmApi):
    '''Bwm Api class'''

        
class FloodprotectionApi(FloodprotectionApi):
    '''Flood protection Api class'''

        
class MulticastApi(MulticastApi):
    '''Multicast Api class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/multicast/settings'
        self.url_base = 'api/sonicos/multicast/base'
        self.url_state_table = 'api/sonicos/reporting/multicast/state-entries'
        self.initial_multicast_json = {
            "multicast": {
                "enable": False,
                "require_igmp_membership": True,
                "require_igmp_membership_timeout": 5,
                "reception": {
                    "all": True
                }
             }
        }

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
        
        
class SslcontrolApi(SslcontrolApi):
    '''Ssl control Api class'''

        
class QosmappingApi(QosmappingApi):
    '''Qos mapping Api class'''


class CipherctrlApi(CipherctrlApi):
    '''Cipher control Api class'''
