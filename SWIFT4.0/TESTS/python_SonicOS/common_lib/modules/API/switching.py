import copy
import json
import re
from runner.settings import logger


class VlanTrunkApi():
    ''' Vlan Trunk class'''

    default_options = {
        'port': None,
        # 'vlan_id': [],
        }
        
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/switch/trunk/ports'    
        self.initial_vlan_json ={
            "switch": {
                "trunk": [
                    {
                        "port": "",
                        # "vlan": [
                        #     # {
                        #     #     "id": 100,
                        #     # }
                        # ]
                    }
                ]
            }
        }
        self.initial_portshield_json= {
            "switch": {
                "portshield": [
                    {
                        "port": "",
                        "vlan": 0,
                        "trunked": False,
                    }
                ]
            }
        }
    
    def add_trunk_ports(self, msg=False, **kwargs):
        self.options = dict(VlanTrunkApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options
        if not kwargs['port']:
            logger.error('Please specify the port.')
            return False
        json_input = self.build_vlan_json(**kwargs)
        vlan_resp = self.fw.api_post(self.url, msg, data=json_input)       
        return vlan_resp

    def edit_trunk_ports(self, msg=False, **kwargs):
        self.options = dict(VlanTrunkApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options
        if not kwargs['port']:
            logger.error('Please specify the port.')
            return False
        json_input = self.build_vlan_json(**kwargs)
        vlan_resp = self.fw.api_put(self.url, msg, data=json_input)       
        return vlan_resp

    def build_vlan_json(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_vlan_json)
            json_input['switch']['trunk'][0]['port'] = kwargs['port']
            if 'vlan_id' in kwargs:
                json_input['switch']['trunk'][0]['vlan'] =[]
                for id in kwargs['vlan_id']:
                    json_input['switch']['trunk'][0]['vlan'].append({"id": int(id)})
        except KeyError:
            logger.info("Error: In creating JSON for vlan trunk")  
        return json_input
    
    def delete_vlan_trunk(self, msg=False, **kwargs):
        self.options = dict(VlanTrunkApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options
        if not kwargs['port']:
            logger.error('Please specify the port.')
            return False
        json_input = self.build_vlan_json(**kwargs)
        vlan_resp = self.fw.api_delete(self.url, msg, data=json_input)       
        return vlan_resp

    def show_vlan_trunk(self,port=None):
        # if not port:
        #     url = self.url + '/interface/'+ port ##not complete
        # else:
        url = self.url
        vlan_resp = self.fw.api_get(url)
        return vlan_resp       
        
    def show_vlan_table(self):
        url = 'api/sonicos/reporting/switch/l2-vlans'
        vlan_resp = self.fw.api_get(url)
        return vlan_resp

    def enable_vlan(self,interface=None, vlan=None, msg=False):
        if not interface or not vlan:
            logger.error('Please specify interface and vlan')
            return False
        vlan_url = f'api/sonicos/switch/trunk/interface/{interface}/vlan/{vlan}'
        vlan_resp = self.fw.api_post(vlan_url, msg, data={})
        return vlan_resp

    def disable_vlan(self,interface=None, vlan=None, msg=False):
        if not interface or not vlan:
            logger.error('Please specify interface and vlan')
            return False
        vlan_url = f'api/sonicos/switch/trunk/interface/{interface}/vlan/{vlan}'
        vlan_resp = self.fw.api_delete(vlan_url, msg, data=None)
        return vlan_resp
        
    def edit_trunk_table(self, interface=None, vlan=None, trunk=False, msg=False):
        url = 'api/sonicos/switch/portshield/ports'
        if not vlan or not interface:
            logger.error('Please specify interface and vlan when edit vlan table.')
            return False
        json_input = {}
        json_input = copy.deepcopy(self.initial_portshield_json)
        json_input['switch']['portshield'][0]['port'] = interface
        json_input['switch']['portshield'][0]['vlan'] = int(vlan)
        json_input['switch']['portshield'][0]['trunked'] = trunk
        vlan_resp = self.fw.api_put(url, msg, data=json_input)
        return vlan_resp
        

class SwitchingPortMirror():

    def __init__(self, fw):
        self.fw = fw
        self.arp_url = '/switch/port/mirrors'
        self.general_url = 'api/sonicos'

        #initializing the initial dictionary
        self.initial_mirror_json = {
                "switch": {
                    "port": [
                    {
                        "direction": "ingress",
                        "enable": True,
                        "mirror": "New Group",
                        "mirror_port": "X2",
                        "mirrored_port": [
                        {
                            "name": "X0"
                        }
                        ]
                    }
                    ]
                }
                }
        

    def config_mirror_json(self, mirror_json, **kwargs):
        for i in kwargs:
            mirror_json["switch"]["port"][0][i] = kwargs[i]
        return mirror_json

    def add_new_mirror_group(self, msg =False, **kwargs):
        mirror_group=self.initial_mirror_json
        mirror_group = self.config_mirror_json(mirror_group,**kwargs)
        url = self.general_url+self.arp_url
        post_response = self.fw.api_post(url, msg, data=mirror_group)
        return post_response
    
    def del_mirror_group(self,name):
        url = self.general_url+self.arp_url+"/name/"+name
        post_response = self.fw.api_delete(url)
        return post_response

    def config_mirror_group(self, name, msg=False,**kwargs,):
        mirror_group=self.get_mirror_group(name)
        mirror_group = self.config_mirror_json(mirror_group,**kwargs)
        url = self.general_url+self.arp_url+"/name/"+name
        post_response = self.fw.api_put(url, msg, data=mirror_group)
        return post_response

    def get_mirror_group(self,name):
        url = self.general_url+self.arp_url+"/name/"+name
        post_response = self.fw.api_get(url)
        return post_response
        
        
class LinkAggregationApi():
    ''' Link Aggregation  class'''

    def __init__(self, fw):
        self.fw = fw
        self.config_link_aggregation = 'api/sonicos/switch/link-aggregation/ports'

    def add_LAG_ports(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.config_link_aggregation, msg, data=json_input)
        return resp    

    def del_LAG_Port(self,interface=None, msg=False):
        if not interface:
            logger.error('Please specify interface')
            return False
        lag_url = f'api/sonicos/switch/link-aggregation/ports/name/{interface}'
        lag_resp = self.fw.api_delete(lag_url, msg, data=None)
        return lag_resp

    def show_LAG_Port(self):
        LAG_resp = self.fw.api_get(self.config_link_aggregation)
        return LAG_resp


class L2DiscoveryApi():
    ''' L2 Discovery  class'''

    def __init__(self, fw):
        self.fw = fw
        self.lldp = 'api/sonicos/switch/lldp'
        self.lldp_profile = 'api/sonicos/switch/lldp-profiles'
        self.l2discover_interfaces = 'api/sonicos/switch/l2-discover/interfaces'

    def config_lldp_status(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_put(self.lldp, msg, data=json_input)
        return resp    

    def show_lldp_status(self):
        lldp_status = self.fw.api_get(self.lldp)
        return lldp_status

    def add_lldp_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.lldp_profile, msg, data=json_input)
        return resp

    def show_lldp_profile(self):
        lldp_status = self.fw.api_get(self.lldp_profile)
        return lldp_status

    def del_lldp_profile(self,name,msg=False):
        if not name:
            logger.info('pls enter profile name')
            return False
        else:
            url = self.lldp_profile + '/name/' + name
        post_response = self.fw.api_delete(url,msg)
        return post_response

    def edit_lldp_profile(self, name,msg=False,**kwargs):
        if not name:
            logger.info('pls enter profile name')
            return False
        else:
            url = self.lldp_profile + '/name/' + name
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp
    
    def get_l2_discovery(self):
        url = 'api/sonicos/dynamic-file/getL2DNeighbors.json'
        l2_discovery = self.fw.api_get(url)
        return l2_discovery
    
    def config_l2discover_interfaces(self,msg=False,**kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_put(self.l2discover_interfaces, msg, data=json_input)
        return resp 
