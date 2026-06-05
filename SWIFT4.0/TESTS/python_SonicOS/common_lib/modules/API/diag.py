import copy
import json
import re
from collections import OrderedDict
from runner.settings import logger

class DiagApi:
    def __init__(self, fw):
        self.fw = fw
        self.url_raw = 'api/sonicos/raw'
        self.url_backend = 'api/sonicos/diag/advanced/backend'
        self.headers = OrderedDict([('Accept', 'application/json'),
                        ('Content-Type', 'application/json'),
                        ('Accept-Encoding', 'application/json'),
                        ('X-SNWL-API-Scope', 'extended'),
                        ('charset', 'UTF-8')])

        self.backend_json = {
            "diag": {
                "advanced": {
                    "backend": {
                        "enable": "",
                        "force_through": {
                            "any": True
                        }
                    }
                }
            }
        }

    def dns_proxy_setting(self, msg=False, **kwargs):
        options ={
            'dnsProxySupportFragment' : '',
            'dns_pry_cache_lifetime': '10',
            'dns_svr_fail_times': '10',
            'dnsOverTCP_enable': '',
            'excludeVPNtraffic': '',
        }
        options.update(kwargs)
        kwargs=options
        json_input = {"stream": ''}
        for item in kwargs.keys():
            json_input['stream'] += item + '=' + str(kwargs[item]) + '&'
        json_input['stream'] = json_input['stream'][:-1]
        res = self.fw.api_post(self.url_raw, msg, data=json_input, headers=self.headers)
        return res    
# {"stream":"dns_svr_fail_times=101&dns_pry_cache_lifetime=101&dnsProxySupportFragment=on&excludeVPNtraffic=&dnsOverTCP_enable=0"}

    def zerotouch_settings(self, msg=False, **kwargs):
        options ={
            "zeroTouchEnable": "CHECKED",
            "zeroTouchTTFqdn": "",
            "ztServerIPUseMode": "",
            "ztServerIPUseMode_0": "",
            "ztServerIPUseMode_1": "",
            "zeroTouchServerIp": "0.0.0.0",
            "zeroTouchReconnDelay": "60",
            "zeroTouchReconnNum": "0",
            "zeroTouchSkipCertCheck": "",
            "zeroTouchConfigMode": "",
            "zeroTouchShowDiagPage": "",
            "zeroTouchDebugLevel": "0"
        }
        options.update(kwargs)
        json_input = {"stream": ''}
        for item in options.keys():
            logger.info(json_input['stream'])
            json_input['stream'] += item + '=' + str(options[item]) + '&'
        json_input['stream'] = json_input['stream'][:-1]
        res = self.fw.api_post(self.url_raw, msg, data=json_input, headers=self.headers)
        return res

    def geo_ip_settings(self, msg=False, **kwargs):

        options ={
            "locRemoteIPUseMode": "",
            "allowMapDbUpload": "",
            "locMapServerRemoteIP":"204.212.170.21"
        }
        options.update(kwargs)
        kwargs=options
        json_input = {"stream": ''}
        for item in kwargs.keys():
            json_input['stream'] += item + '=' + str(kwargs[item]) + '&'
        json_input['stream'] = json_input['stream'][:-1]
        res = self.fw.api_post(self.url_raw, msg, data=json_input, headers=self.headers)
        return res

    def config_backend_server_communication(self, msg=False, **kwargs):
        json_input = copy.deepcopy(self.backend_json)
        if 'enable' in kwargs.keys():
            json_input['diag']['advanced']['backend']['enable'] = kwargs['enable']
        print(json_input)

        if 'interface' in kwargs.keys():
            del json_input['diag']['advanced']['backend']['force_through']['any']
            print(json_input)

            json_input['diag']['advanced']['backend']['force_through']['interface'] = kwargs['interface']
        print(json_input)
        res = self.fw.api_put(self.url_backend, msg, data=json_input)
        return res
    
    def get_backend_server_communication(self, msg=False):
        res = self.fw.api_get(self.url_backend, msg)
        return res

    def get_backend_server_communication_interface(self, msg=False):
        url = 'api/sonicos/dynamic-file/getBkendSrvrCommunicationInfo.json'
        res = self.fw.api_get(url)
        return res 
    
    def set_IPv6_ready(self, msg=False, ipv6_ready=False):
        json_input = {"stream": ''}
        if ipv6_ready or ipv6_ready == 'on':
            json_input['stream'] = 'enforceIPv6Ready=on'
        else:
            json_input['stream'] = 'enforceIPv6Ready=off'
        res = self.fw.api_post(self.url_raw, msg, data=json_input, headers=self.headers)
        return res         

    def config_raw_api(self, msg=False, **kwargs):
        json_input = {"stream": ''}
        json_input['stream'] = kwargs['stream'] 
        res = self.fw.api_post(self.url_raw, msg, data=json_input, headers=self.headers)
        return res  

    def get_diag_info(self,):
        url = 'api/sonicos/dynamic-file/getDiagDefs.json'
        res = self.fw.api_get(url)
        return res 

    def show_coredump_list(self):
        url = 'api/sonicos/completer/core-dumps/file/'
        res = self.fw.api_get(url)
        print(res)
        rc = False
        output = []
        try:
            if res['complete']['count'] > 0:
                output = res['complete']['options']
            rc = True
        except Exception as e:
            logger.error(e)
            return rc, output

        logger.info(output)
        return rc, output

    def config_vpn_setting(self, msg=False, **kwargs):
        # {"stream":"VpnNoTcpMssAdjust=on&ipsecDHInteropMode=&ipsecFragmentAfterEsp=on&UsePIForPassThru=&AcceptReservedIDType=&sendNotifyFromBlankSa=&UpdateCppAfterObjCfg=&debugCSEConnector=on"}
        json_input = {"stream": ''}
        for item in kwargs.keys():
            json_input['stream'] += item + '=' + str(kwargs[item]) + '&'
        json_input['stream'] = json_input['stream'][:-1]
        res = self.fw.api_post(self.url_raw, msg, data=json_input, headers=self.headers)
        return res  