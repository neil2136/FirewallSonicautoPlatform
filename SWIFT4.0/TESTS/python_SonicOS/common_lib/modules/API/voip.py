import copy
import json

from runner.settings import logger


class VoipSettingApi:
    '''VoipSettingApi Class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/voip'
        self.voip_initial_json = {
            "voip": {
                "consistent_nat": False,
                "sip": {
                    "enable": False,
                    "access_rule_based": False,
                    "tcp": True,
                    "non_sip_packets": True,
                    "b2bua_support": True,
                    "signaling_timeout": 1800,
                    "media_timeout": 120,
                    "signaling_port": {},
                    "endpoint_registration_anomaly_tracking": False,
                    "registration_tracking_interval": 300,
                    "failed_registration_threshold": 5,
                    "endpoint_block_interval": 3600,
                    "transforms_in_service_object": {
                        "name": "SIP UDP"
                    }
                },
                "h323": {
                    "enable": False,
                    "access_rule_based": False,
                    "only_gatekeeper_calls": True,
                    "inactivity_timeout": 300,
                    "gatekeeper_ip": "0.0.0.0"
                }
            }
        }

    def set_voip(self, msg=False, **kwargs):
        json_input = copy.deepcopy(self.voip_initial_json)
        json_input.update(kwargs)
        voip_resp = self.fw.api_put(self.url, msg, data=json_input)
        return voip_resp

    def show_voip_setting(self):
        get_response = self.fw.api_get(self.url)
        return get_response