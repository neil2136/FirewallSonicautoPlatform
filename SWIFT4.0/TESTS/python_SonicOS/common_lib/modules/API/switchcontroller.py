from runner.settings import logger
from runner.utils.assertion import Assertion
from collections import OrderedDict
from runner.settings import Params, logger
from switch import *
import urllib3
import requests
import json
import copy
import time
import sys
import re
import os

sys.path.append(os.environ["PYTHON_COMMON_HOME"])

class Switch():

    def __init__(self, fw):
        self.fw = fw
        self.switch_url = '/switch-controller/switch'
        self.firmware_upgrade_url = '/switch-controller/firmware-cloud'
        self.restart_url="/switch-controller/restart"
        self.authorize_url="/switch-controller/authorize"
        self.general_url = 'api/sonicos'

        self.default_options = {
            "switch_controller": {
                "switch": [
                    {
                        "id": "",
                        "name": "",

                    }
                ]
            }
        }

        #initializing the initial dictionary
        self.initial_switch_json = {
            "switch_controller": {
                "switch": [
                    {
                        "id": "",
                        "name": "",
                        "model": "",
                        "serial": "",
                        "comment": "Test",
                        "ip": "",
                        "user_name": "admin",
                        "password": "Password@123",
                        #"active_partition": 1,
                        "switch_mode": "standalone",
                        "uplink": "",
                        "management": "",
                        "firewall_uplink": "",
                        "stp": True,
                        "stp_mode": "multiple",
                        #"switch_8021x": True,
                        #"switch_8021x_guest_vlan": False,
                        "jumbo_frame_size": 1523
                    }
                ]
            }
        }
        self.initial_daisy_chain_switch_json={
            "switch_controller": {
                "switch": [
                    {
                        "id": "",
                        "name": "",
                        "model": "",
                        "serial": "",
                        "comment": "Test",
                        "ip": "",
                        "user_name": "admin",
                        "password": "Password@123",
                        #"active_partition": 1,
                        "switch_mode": "daisy-chain",
                        "parent_switch_uplink":"",
                        "parent_switch_name":"",
                        'uplink': "",
                        "stp": True,
                        "stp_mode": "multiple",
                        #"switch_8021x": True,
                        #"switch_8021x_guest_vlan": False,
                        "jumbo_frame_size": 1523
                    }
                ]
            }
        }

    def build_json_switch(self,update=False,**kwargs):
        if update :
            copy_initial_switch_json = copy.deepcopy(self.default_options)
        
        elif kwargs["switch_mode"] =="daisy-chain":
            copy_initial_switch_json = copy.deepcopy(self.initial_daisy_chain_switch_json)

        else:
            copy_initial_switch_json = copy.deepcopy(self.initial_switch_json)

        try:
            for keys in kwargs.keys():
                if keys in ["id", "name", "model", "serial", "comment", "ip", "user_name", "password", "active_partition", "switch_mode","parent_switch_name","parent_switch_uplink" ,"uplink", "management", "firewall_uplink", "stp", "switch_8021x", "switch_8021x_guest_vlan", "jumbo_frame_size"]:
                    copy_initial_switch_json['switch_controller']["switch"][0][keys] = kwargs[keys]
            return copy_initial_switch_json
        except KeyError:
            logger.error('Error: In creating JSON for switch')

    
    def config_switch(self, msg=False, **kwargs):

        url = self.general_url+self.switch_url+ '/' + 'id' + '/' + kwargs['name']
        initial_switch_json = self.build_json_switch(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_switch_json)
        post_response = self.fw.api_put(url, data=initial_switch_json)

        return post_response

    def delete_switch(self, switch_name, msg=False, data=None):
        """
        /switch-controller/switch/id/2CB8ED4AF4BA
        """
        url = self.general_url+self.switch_url + '/' + 'id' + '/' + switch_name
        logger.debug("URL for Delete:- ", url)
        delete_resp = self.fw.api_delete(url, data=data)
        return delete_resp
    
    def restart_fw(self):
        response=self.fw.api_restart()
        return response

    def get_switch(self):
        """
        """
        url = self.general_url+self.switch_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        return get_response

    def get_switch_name(self, name):
        url = self.general_url+self.switch_url + '/' + 'id' + '/' + name
        get_response = self.fw.api_get(url)
        return get_response

    def add_switch(self, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.switch_url
        initial_switch_json = self.build_json_switch(**kwargs)

        logger.debug("URL for posting {}".format(url))
        logger.debug("data for posting {}".format(initial_switch_json))
        post_response = self.fw.api_post(url, data=initial_switch_json)

        return post_response

    def add_daisy_chain_switch(self, msg=False,timeout=120, **kwargs):
        """
        """
        url = self.general_url+self.switch_url
        initial_switch_json = self.build_json_switch(**kwargs)

        logger.debug("URL for posting {}".format(url))
        logger.debug("data for posting {}".format(initial_switch_json))
        post_response = self.fw.api_post(url, data=initial_switch_json)

        return post_response

    def firmware_upgrade_cloud(self, switch_name, partition, build, msg=False):
        """
        provide the 'switch name','partition','build number' as manditory
        https://10.5.193.114/api/sonicos/switch-controller/firmware-cloud/2CB8ED4AF4BE/partition/1/version/1.0.0.1-4
        /switch-controller/firmware-cloud/{NAME}/partition/{PARTITION_NUM}/version/{VERSION}
        """
        url = self.general_url+self.firmware_upgrade_url + '/' + switch_name + \
            '/' + "partition" + '/' + \
            str(partition) + '/' + 'version' + '/' + build
        logger.info("URL for posting", url)
        post_response = self.fw.api_post(url, data=None)
        return post_response

    def restart(self, switch_name,msg=False):
        """
        /switch-controller/restart/{NAME}
        """
        url = self.general_url+self.restart_url + '/' + switch_name 
        logger.info("URL for posting", url)
        post_response = self.fw.api_post(url, data=None)
        return post_response
    
    def authorize(self, switch_name, msg=False):
        """
        /switch-controller/authorize/{NAME}
        """
        url = self.general_url+self.authorize_url + '/' + switch_name 
        logger.info("URL for posting", url)
        post_response = self.fw.api_post(url, data=None)
        return post_response


class Static_routes():
    
    def __init__(self, fw):
        self.fw = fw
        self.staticroute_url = 'api/sonicos/switch-controller/route'
        self.initial_staticroutes_json = {
            "switch_controller": {
                "route": [
                    {
                        "switch": "",
                        "destination": "",
                        "netmask": "",
                        "gateway": ""
                        
                    }
                ]
            }
        }

    
    def build_json_static_route(self,update=False,**kwargs):
       
        copy_initial_static_route_json = copy.deepcopy(self.initial_staticroutes_json)
        try:
            for keys in kwargs.keys():
                # print(keys)
                if keys in ["switch", "destination", "netmask", "gateway"]:
                    copy_initial_static_route_json['switch_controller']["route"][0][keys] = kwargs[keys]
            # print(copy_initial_switch_json)
            return copy_initial_static_route_json
        except KeyError:
            logger.error('Error: In adding static route')


    def delete_static_route(self, msg=False, **kwargs):
        """
        /switch-controller/switch/id/2CB8ED4AF4BA
        """
        url = self.staticroute_url
        initial_static_route_json = self.build_json_static_route(**kwargs)

        logger.debug("URL for Delete:- ", url)
        delete_resp = self.fw.api_delete(url, data=initial_static_route_json)
        return delete_resp

    def get_static_route(self):
        """
        """
        url = self.staticroute_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        new_get_response={'switch_controller':{'route':{}}}
        for key in get_response['switch_controller']['route']:
            logger.info(key['switch'])
            k=key['switch']
            if k not in new_get_response['switch_controller']['route']:
                new_get_response['switch_controller']['route'][k]=[]
        
            new_get_response['switch_controller']['route'][k].append(key)

        logger.info(new_get_response)
        return new_get_response

    def edit_static_route(self, msg=False, **kwargs):
        """
        """
        url =self.staticroute_url
        initial_static_route_json = self.build_json_static_route(**kwargs)

        logger.debug("URL for put {}".format(url))
        logger.debug("data for put {}".format(initial_static_route_json))
        put_response = self.fw.api_put(url, data=initial_static_route_json)

        return put_response

    def add_static_route(self, msg=False, **kwargs):
        """
        """
        url = self.staticroute_url
        initial_static_route_json = self.build_json_static_route(**kwargs)

        logger.debug("URL for posting {}".format(url))
        logger.debug("data for posting {}".format(initial_static_route_json))
        post_response = self.fw.api_post(url, data=initial_static_route_json)

        return post_response

    def restart_fw(self):
        response=self.fw.api_restart()
        return response


class QOS():
    
    def __init__(self, fw):
        self.fw = fw
        self.qos_url = 'api/sonicos/switch-controller/qos'

        #initializing the initial dictionary
        self.initial_qos_WRR_json = {
            
            "switch_controller": {
                "qos": [
                {
                        "switch": "",
                        "enable": True,
                        "schedule_method": "weighted-round-robin",
                        "trust_mode": "",
                        "round_robin_weight1": 0,
                        "round_robin_weight2": 0,
                        "round_robin_weight3": 0,
                        "round_robin_weight4": 0,
                        "round_robin_weight5": 0,
                        "round_robin_weight6": 0,
                        "round_robin_weight7": 0,
                        "round_robin_weight8": 0
                    }
                ]
            }
        }

        self.initial_qos_strict_priority_json = {
            
            "switch_controller": {
                "qos": [
                {
                        "switch": "",
                        "enable": True,
                        "schedule_method": "strict-priority",
                        "trust_mode": "dscp-8021p",
                    
                    }
                ]
            }
        }


        self.initial_qos_dscp_json = {
            
            "switch_controller": {
                "qos_dscp": [
               {
                    "switch": "",
                    "dscp_id": None,
                    "queue_id": None
               
               }
            ]
        }
    }

        self.initial_qos_cos_json = {
            
            "switch_controller": {
                "qos_cos": [
               {
                    "switch": "",
                    "cos_id": None,
                    "queue_id": None
               
               }
            ]
        }
    }


    def build_json_qos(self,**kwargs):
        if  "schedule_method" in kwargs.keys():
            if kwargs["schedule_method"]=="strict-priority" :
                copy_initial_qos_strict_priority_json = copy.deepcopy(self.initial_qos_strict_priority_json)

                try:
                    for keys in kwargs.keys():
                        if keys in ["switch", "enable", "schedule_method", "trust_mode"]:
                            copy_initial_qos_strict_priority_json['switch_controller']["qos"][0][keys] = kwargs[keys]
                
                    return copy_initial_qos_strict_priority_json
                except KeyError:
                    logger.error('Error: In adding qos')
            
            elif kwargs["schedule_method"]=="weighted-round-robin" :
                copy_initial_qos_WRR_json = copy.deepcopy(self.initial_qos_WRR_json)

                try:
                    for keys in kwargs.keys():
                        if keys in ["switch", "enable", "schedule_method", "trust_mode", "round_robin_weight1", "round_robin_weight2","round_robin_weight3",
                        "round_robin_weight4","round_robin_weight5","round_robin_weight6","round_robin_weight7","round_robin_weight8"]:
                            copy_initial_qos_WRR_json['switch_controller']["qos"][0][keys] = kwargs[keys]
                    return copy_initial_qos_WRR_json
                except KeyError:
                    logger.error('Error: In adding qos')

        elif "dscp_id" in kwargs.keys():
            copy_initial_qos_dscp_json = copy.deepcopy(self.initial_qos_dscp_json)
            try:
                for keys in kwargs.keys():
                    if keys in ["switch", "dscp_id", "queue_id"]:
                        copy_initial_qos_dscp_json['switch_controller']["qos_dscp"][0][keys] = kwargs[keys]
                return copy_initial_qos_dscp_json
            except KeyError:
                logger.error('Error: In adding qos')

        else:
            copy_initial_qos_cos_json = copy.deepcopy(self.initial_qos_cos_json)
            try:
                for keys in kwargs.keys():
                    if keys in ["switch", "cos_id", "queue_id"]:
                        copy_initial_qos_cos_json['switch_controller']["qos_cos"][0][keys] = kwargs[keys]
                return copy_initial_qos_cos_json
            except KeyError:
                logger.error('Error: In adding qos')


    def config_qos(self, msg=False, **kwargs):
    
        url = self.qos_url
        initial_qos_json = self.build_json_qos(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_qos_json)
        put_response = self.fw.api_put(url, data=initial_qos_json)

        return put_response

    def config_qos_by_switch_name(self, msg=False,**kwargs):
        """
        """
        url = self.qos_url + '/' +  'switch' + '/' + kwargs['switch']
        initial_qos_switch_json = self.build_json_qos(**kwargs)

        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_qos_switch_json)
        put_response = self.fw.api_put(url, data=initial_qos_switch_json)
        
        return put_response

    def config_qos_dscp(self, msg=False, **kwargs):
        
        url = self.qos_url + '-' + 'dscp'
        initial_dscp_json = self.build_json_qos(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_dscp_json)
        put_response = self.fw.api_put(url, data=initial_dscp_json)

        return put_response

    def config_qos_dscp_by_switch_name(self, msg=False, **kwargs):
        
        url = self.qos_url + '/' +  'switch' + '/' + kwargs['switch']
        initial_dscp_json = self.build_json_qos(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_dscp_json)
        put_response = self.fw.api_put(url, data=initial_dscp_json)

        return put_response

    def config_qos_cos(self, msg=False, **kwargs):
        
        url = self.qos_url + '-' + 'cos'
        initial_cos_json = self.build_json_qos(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_cos_json)
        put_response = self.fw.api_put(url, data=initial_cos_json)

        return put_response

    def config_qos_cos_by_switch_name(self, msg=False,  **kwargs):
        
        url = self.qos_url + '/' +  'switch' + '/' + kwargs['switch']
        initial_cos_json = self.build_json_qos(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_cos_json)
        put_response = self.fw.api_put(url, data=initial_cos_json)

        return put_response
    
    def get_qos(self):
        """
        """
        url = self.qos_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        new_get_response={'switch_controller':{'qos':{}}}
        for key in get_response['switch_controller']['qos']:
            k=key['switch']
            new_get_response['switch_controller']['qos'][k]=[]
        
            new_get_response['switch_controller']['qos'][k].append(key)

        logger.info(new_get_response)
        return new_get_response

    def get_qos_by_switch_name(self):
        url = self.qos_url + '/' +  'switch' + '/' + switch_name
        get_response = self.fw.api_get(url)
        new_get_response={'switch_controller':{'qos':{}}}
        for key in get_response['switch_controller']['qos']:
            k=key['switch']
        #     if k not in newget['switch_controller']['route']:
            new_get_response['switch_controller']['qos'][k]=[]
        
            new_get_response['switch_controller']['qos'][k].append(key)

        logger.info(new_get_response)
        return new_get_response

    def get_qos_dscp(self):
        """
        """
        url = self.qos_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        new_get_response={'switch_controller':{'qos_dscp':{}}}
        for key in get_response['switch_controller']['qos_dscp']:
            k=key['switch']
            new_get_response['switch_controller']['qos_dscp'][k]=[]
        
            new_get_response['switch_controller']['qos_dscp'][k].append(key)

        logger.info(new_get_response)
        return new_get_response

    def get_qos_dscp_by_switch_name(self, switch_name):
        """
        """
        url = self.qos_url + '/' +  'switch' + '/' + switch_name
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        new_get_response={'switch_controller':{'qos_dscp':{}}}
        for key in get_response['switch_controller']['qos_dscp']:
            k=key['switch']
            new_get_response['switch_controller']['qos_dscp'][k]=[]
        
            new_get_response['switch_controller']['qos_dscp'][k].append(key)

        logger.info(new_get_response)
        return new_get_response

    def get_qos_cos(self):
        """
        """
        url = self.qos_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        new_get_response={'switch_controller':{'qos_cos':{}}}
        for key in get_response['switch_controller']['qos_cos']:
            k=key['switch']
            new_get_response['switch_controller']['qos_cos'][k]=[]
        
            new_get_response['switch_controller']['qos_cos'][k].append(key)

        logger.info(new_get_response)
        return new_get_response

    def get_qos_cos_by_switch_name(self):
        """
        """
        url = self.qos_url + '/' +  'switch' + '/' + switch_name
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        new_get_response={'switch_controller':{'qos_cos':{}}}
        for key in get_response['switch_controller']['qos_cos']:
            k=key['switch']
            new_get_response['switch_controller']['cos'][k]=[]
        
            new_get_response['switch_controller']['cos'][k].append(key)

        logger.info(new_get_response)
        return new_get_response

    def restart_fw(self):
        response=self.fw.api_restart()
        return response

class Radius_server():
    
    def __init__(self, fw):
        self.fw = fw
        self.radius_url = '/switch-controller/radius'
        self.general_url = 'api/sonicos'

        #initializing the initial dictionary
        self.initial_radius_server_json = {
            "switch_controller": {
                "radius": [
                    {
                        "server_ip": "",
                        "switch": "",
                        "authorized_port": 1,
                        "key_string": "",
                        "timeout_reply": 1,
                        "retry": 1,
                    
                    }
                    
                ]
           
            }   
        }

    
    def build_json_radius_server(self,update=False,**kwargs):
            
        copy_initial_radius_json = copy.deepcopy(self.initial_radius_server_json)

        try:
            for keys in kwargs.keys():
                if keys in ["server_ip", "switch", "authorized_port", "key_string", "timeout_reply", "retry"]:
                    copy_initial_radius_json['switch_controller']["radius"][0][keys] = kwargs[keys]
                    
            return copy_initial_radius_json
        except KeyError:
            logger.error('Error: In adding radius_server')
            

    def config_radius_server(self, msg=False,url="/switch-controller/radius", **kwargs):
        
        url = self.general_url+url
        initial_radius_json = self.build_json_radius_server(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_radius_json)
        post_response = self.fw.api_post(url, data=initial_radius_json)

        return post_response

    def config_radius_server_by_switch_name(self, msg=False,url="/switch-controller/qos",**kwargs):
        """
        """
        url = self.general_url+url + '/' + 'server-ip' + '/' + kwargs['ip'] + '/' +  'switch' + '/' + kwargs['switch']
        initial_radius_switch_json = self.build_json_radius_server(**kwargs)

        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_radius_switch_json)
        post_response = self.fw.api_post(url, data=initial_radius_switch_json)

        return post_response

        return post_response

    def configure_radius_server(self, msg=False, url="/switch-controller/radius", **kwargs):
        
        url = self.general_url+url
        initial_radius_json = self.build_json_radius_server(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_radius_json)
        post_response = self.fw.api_put(url, data=initial_radius_json)

        return post_response

    def configure_radius_server_by_switch_name(self, msg=False,url="/switch-controller/radius",**kwargs):
        """
        """
        url = self.general_url+url + '/' + 'server-ip' + '/' + kwargs['ip'] + '/' +  'switch' + '/' + kwargs['switch']
        initial_radius_switch_json = self.build_json_radius(**kwargs)

        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_radius_switch_json)
        post_response = self.fw.api_put(url, data=initial_radius_switch_json)

        return post_response

    def delete_radius_server(self, msg=False, url="/switch-controller/radius", **kwargs):
        
        url = self.general_url+url
        initial_radius_json = self.build_json_radius_server(update=True,**kwargs)
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_radius_json)
        post_response = self.fw.api_delete(url, data=initial_radius_json)

        return post_response

    def delete_multiple_radius_server(self, msg=False, url="/switch-controller/radius", **kwargs):
        
        url = self.general_url+url
        initial_radius_json = kwargs
        logger.debug("URL for PUT", url)
        logger.debug("data for PUT", initial_radius_json)
        post_response = self.fw.api_delete(url, data=initial_radius_json)

        return post_response

    def delete_radius_server_by_switch_name(self, msg=False,url="/switch-controller/radius",**kwargs):
        """
        """
        url = self.general_url+url + '/' + 'server-ip' + '/' + kwargs['ip'] + '/' +  'switch' + '/' + kwargs['switch']
        initial_radius_switch_json = self.build_json_radius(**kwargs)

        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_radius_switch_json)
        post_response = self.fw.api_delete(url, data=initial_radius_switch_json)

        return post_response
    
    def restart_fw(self):
        response=self.fw.api_restart()
        return response

       
    
    def get_radius_server(self, url='/switch-controller/radius'):
        """
        """
        url = self.general_url+url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        if get_response["switch_controller"] != {} :
            newget={'switch_controller':{'radius':{}}}
            for keys in get_response.keys():
                if keys in ["switch_controller","radius"]:
                    for i in get_response['switch_controller']['radius']:
                        print(i)
                        print(i['switch'])
                        k=i['switch']
                        newget['switch_controller']['radius'][k]=[]
            
                        newget['switch_controller']['radius'][k].append(i)
                else:
                    print(newget)
            
            return newget
        
        else:
            return get_response

    def get_radius_server_by_switch_name(self, ip ,switch_name,url='/switch-controller/radius'):
        url = self.general_url+url + '/' + 'server-ip' + '/' + ip + '/' +  'switch' + '/' + switch_name
        get_response = self.fw.api_get(url)
        newget={'switch_controller':{'radius':{}}}
        for i in get_response['switch_controller']['radius']:
            k=i['switch']
            newget['switch_controller']['radius'][k]=[]
        
            newget['switch_controller']['radius'][k].append(i)

        return newget


class Authorize():

    def __init__(self, fw):
        self.fw = fw
        self.authorize_url = '/raw'
        self.dynamic_authorize_url ="/dynamic-file/getSnwlSwitchInfo.json"
        self.get_firmware_url="/dynamic-file/getExtSwitchInfo.json?type=128&switchId=9&latest=1"
        self.switch_url = '/switch-controller/switch'
        self.general_url = 'api/sonicos'

    def get_discover_switch(self):
        """
        """
        url = self.general_url+self.dynamic_authorize_url
        get_response = self.fw.api_get(url,log_switch=False)
        return get_response
        
    def post_authorize(self, index,firmware=None, msg=False):
        """
        /switch-controller/authorize/{NAME}
        """
        head  = OrderedDict([('Accept', 'application/json'),
                        ('Content-Type', 'application/json'),
                        ('Accept-Encoding', 'application/json'),
                        ('X-SNWL-API-Scope', 'extended'),
                        ('charset', 'UTF-8')])  
        url = self.general_url+self.authorize_url 
        logger.debug("URL for posting", url)
        if firmware :
            value="cgiaction=addSnwlSwitch&switchindex="+index+"&upgradeUrl="+firmware
        else:
            value="cgiaction=addSnwlSwitch&switchindex="+index+"&upgradeUrl="
        data={"stream":value}
        post_response = self.fw.api_post("api/sonicos/raw", data={"stream":"cgiaction=addSnwlSwitch&switchindex=0&upgradeUrl="},headers=head)
    
        return post_response
    
    def post_authorize_latest(self, index,firmware=None, msg=False):
        """
        /switch-controller/authorize/{NAME}
        """
        head  = OrderedDict([('Accept', 'application/json'),
                        ('Content-Type', 'application/json'),
                        ('Accept-Encoding', 'application/json'),
                        ('X-SNWL-API-Scope', 'extended'),
                        ('charset', 'UTF-8')])  
        url = self.general_url+self.authorize_url 
        logger.debug("URL for posting", url)
        if firmware :
            value="cgiaction=addSnwlSwitch&switchindex="+index+"&upgradeUrl="+firmware
        else:
            value="cgiaction=addSnwlSwitch&switchindex="+index+"&upgradeUrl="
        data={"stream":value}
        #post_response = self.fw.api_post("api/sonicos/raw", data={"stream":"cgiaction=addSnwlSwitch&switchindex=0&upgradeUrl="},headers=head)
        post_response = self.fw.api_post("api/sonicos/raw", data={"stream": "cgiaction=addSnwlSwitch&switchindex=0&upgradeUrl=https%3A%2F%2Fapi.mysonicwall.com%2Fapi%2Fdownloads%2Fdownload-software%3Fusername%3Danonymous%26swID%3D15786%26swGrpID%3D10966%26isRNotes%3D0%26sessionID%3D%26%2520appName%3DMSW%26oemCode%3DSNWL"},headers=head)

        #"cgiaction=addSnwlSwitch&switchindex=0&upgradeUrl=https%3A%2F%2Fapi.mysonicwall.com%2Fapi%2Fdownloads%2Fdownload-software%3Fusername%3Danonymous%26swID%3D21201%26swGrpID%3D15592%26isRNotes%3D0%26sessionID%3D%26%2520appName%3DMSW%26oemCode%3DSNWL"
        return post_response

    def get_firmware_details(self):

        params=OrderedDict([('type',128),('switchId',10),('latest',1)])

        url= self.general_url+self.get_firmware_url
        get_response=self.fw.api_get(url,params)
        return get_response

    def post_alert_switch(self,url):
        url=self.general_url+self.authorize_url
        post_response=self.fw.api_post(url,data="cgiaction=addSnwlSwitch&switchindex=1&upgradeUrl=https%3A%2F%2Fapi.mysonicwall.com%2Fapi%2Fdownloads%2Fdownload-software%3Fusername%3Danonymous%26swID%3D21091%26swGrpID%3D15506%26isRNotes%3D0%26sessionID%3D%26%2520appName%3DMSW%26oemCode%3DSNWL")
        return post_response
    
    
    def get_switch(self):
        """
        """
        url = self.general_url+self.switch_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        return get_response

    def get_switch_ui(self):
        """
        """
        url = self.general_url+self.dynamic_authorize_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        return get_response

    def restart_fw(self):
        response=self.fw.api_restart()
        return response

class Upgrade_firmware():
    
    uuid = 'NonTC'
    def __init__(self,sw):
        
        
        self.sw=sw
        self.url='api/sonicswitch/firmware/upload/1'
        self.url_fw='api/system/firmware' 

                   
    def config_uploadswitchfirmware(self,ip,msg=False):
        
        ########### Build path#####################
        
        build_path= '/DEV_TESTS/python_SonicOS/sw_SWS-14_1.0.0.5-16.imag.sig'
        
        
        ##########switch login starts##############################
        urllib3.disable_warnings()
        url = 'https://' + ip + '/api/system/login'
        header={'accept': 'application/json'}
        payload= {'user':'admin','password':'password'} 
        response = requests.patch(url, headers=header, data=json.dumps(payload),verify=False)
        logger.info(response.content)
        login_responsejson = json.loads(response.content)
        token = login_responsejson['restful_res']['token']
        token = 'Bearer ' + token
        header['Authorization'] = token
        
       ###########getting the status of switch#######################
        url_dev= 'https://'+ ip +'/api/sonicswitch/firmware/upload/1'
        url_get_fw= 'https://'+ ip + '/api/system/firmware'
        header={'Content-Type':'application/pgp-signature','Authorization': token}    
        get_data={}
        get_check= requests.get(url_get_fw,headers=header,data=get_data,verify=False)
        logger.info(get_check.content) 
        resp_get={}
        resp= get_check.content.decode('utf-8')
        resp_get = json.loads(resp)
        logger.info(resp)
        
       ##############Checking & Pushing the build to the switch################ 
        if 'activePartition' in resp_get['restful_res']['fwConfs']:
             check_active=(resp_get['restful_res']['fwConfs']['activePartition'])
             logger.info(check_active) 
             if check_active==1: 
                 if 'partition1Version' in resp_get['restful_res']['fwConfs']:
                     check_build= resp_get['restful_res']['fwConfs']['partition1Version']
                     logger.info(check_build)
                     build= Params.switch_build
                     logger.info("##################")
                     logger.info(build)
                     if check_build != ('IMG-' + build): 
                         logger.info("upload will start")      
                         logger.info("#######################")       
                         data= open(build_path,'rb').read()
                         upload_request= requests.post(url_dev,headers=header,data=data,verify=False)
                         time.sleep(20)
                         logger.info(upload_request)
                        #  #upload_request1= self.sw.api_post(self.url,msg,self.headers,data=data)
                        #  time.sleep(30)
                         
                        #  response = requests.patch(url, headers=header, data=json.dumps(payload),verify=False)
                        #  logger.info(response.content)
                        #  login_responsejson = json.loads(response.content)
                        #  token = login_responsejson['restful_res']['token']
                        #  token = 'Bearer ' + token
                        #  header['Authorization'] = token
                         #response=requests.get(url_get_fw,headers=header,data=get_data,verify=False)
                         #response = self.sw.api_get(self.url_fw)
                         if response == 200:
                            logger.info("upload successful")
                            logger.info(response)
                         else:
                            time.sleep(30)
                        #     response=requests.get(url_get_fw,headers=header,data=get_data,verify=False)
                        #     #response = self.sw.api_get(self.url_fw)
                        #     logger.info(response)   
                        #     if response==200:
                        #         logger.info("upload successful")    
                        #     else: 
                        #         logger.info("upload not working") 
        
                     else:
                          logger.info("existing build is latest.")
                          #need to work on reset for switch and adding ip to switch
                          pass
                 else:
                      logger.info("missing the partition key")         
             elif check_active==2: 
                 if 'partition2Version' in resp_get['restful_res']['fwConfs']:
                     check_build= resp_get['restful_res']['fwConfs']['partition2Version']
                     logger.info(check_build)
                     if check_build != 'IMG-1.1.0.0-9':
                         logger.info("upload will start")      
                         logger.info("#######################")       
                         data= open(build_path,'rb').read()
                         upload_request= requests.post(url_dev,headers=header,data=data,verify=False)
                         time.sleep(20)
                         logger.info(upload_request)
                         upload_request= self.sw.api_post(self.url,msg,self.headers,data=data)
                         time.sleep(30)
                         response = self.sw.api_get(self.url_fw)
                         if response == 200:
                            logger.info("upload successful")
                            logger.info(response)
                         else:
                            time.sleep(30)
                            #get_check_resp= requests.get(url_get_fw,headers=header,data=get_data,verify=False)
                            response = self.sw.api_get(self.url_fw)
                            logger.info(response)   
                            if response==200:
                                logger.info("upload successful")    
                            else: 
                                logger.info("upload not working")
                     else:
                          logger.info("existing build is latest.")
                          pass
                 else:
                      logger.info("missing the partition key")
        else:
            logger.info("missing active partiiton key")
            
        return response

    def restart_fw(self):
        response=self.fw.api_restart()
        return response
   
    

class Network_fw():


    def __init__(self, fw):
        self.fw = fw

    def restart_fw(self):
        response=self.fw.api_restart()
        return response



class Port():

    def __init__(self, fw):
        self.fw = fw
        self.port_url = '/switch-controller/port'
        self.general_url = 'api/sonicos'

        #initializing the initial dictionary
        self.old_initial_port_json = {
            "switch_controller": {
                "port": [
                    {
                        "name": "",
                        "switch": "",
                        "enable": True,
                        "stp": True,
                        "poe": True,
                        "link_speed": {
                            "auto_negotiate": True
                        },
                        "poe_priority": "medium",
                        "port_isolation": False,
                        "voice_vlan": False,
                        "poe_limit_type": "auto-class",
                        "voice_vlan_cos_mode": "src",
                        # "port_8021x_mode": "force-authorized",
                        # "port_8021x_reauth": False,
                        # "port_8021x_reauth_period": 3600,
                        # "port_8021x_guest_vlan": False,
                        # "port_8021x_radius_vlan_assign": True,
                        "vlan_trunk": False
                    }
                ]
            }
        }
        self.initial_port_json ={
            "switch_controller": {
                "port": [
                    {
                        "name": None,
                        "switch": None,
                        "enable": True,
                        "stp": True,
                        "poe": True,
                        "link_speed": {
                            "auto_negotiate": True
                        },
                        "poe_priority": "medium",
                        "port_isolation": False,
                        "voice_vlan": False,
                        "poe_limit_type": "auto-class",
                        "voice_vlan_cos_mode": "src",
                        "cos_value": 0,
                        "trust": False,
                        "storm_control": {},
                        "portshield": "",
                        "port_8021x": {
                            "config": "force-authorized",
                            "reauth": False,
                            "reauth_period": 3600,
                            "guest_vlan": False,
                            "radius_vlan_assignment": True
                        },
                        
                        "vlan_trunk": False
                    }
                ]
            }
        }
        self.initial_portshielding_json ={
            "switch_controller": {
                "port": [
                    {
                        "name": None,
                        "switch": None,
                        "portshield":None
                
            }]}}
        self.initial_json_disable_enable ={
            "switch_controller": {
                "port": [
                    {      
                        "name": None,
                        "switch": None,
                        "enable":None
                
            }]}}
        self.initial_port_json_name ={
            "switch_controller": {
                "port": [
                    {
                        "name": None,
                        "switch": None,
                        "enable": True,
                        "port_description": "",
                        "stp": True,
                        "poe": True,
                        "link_speed": {
                            "auto_negotiate": True
                        },
                        "poe_priority": "medium",
                        "port_isolation": False,
                        "voice_vlan": False,
                        "poe_limit_type": "auto-class",
                        "voice_vlan_cos_mode": "src",
                        "cos_value": 0,
                        "trust": False,
                        "bandwidth_ingress": 0,
                        "bandwidth_egress": 0,
                        "security_count": 0,
                        "storm_control": {
                            "broadcast": 0,
                            "unknown_multicast": 0,
                            "unknown_unicast": 0
                        },
                        "portshield": "",
                        "vlan_trunk": False,
                        
                    }
                ]
            }
        }


    def build_json_port(self, **kwargs):
        copy_initial_port_json = copy.deepcopy(self.initial_port_json)
        #try:
        for keys in kwargs.keys():
            if keys in ["name","switch","enable","stp","poe","poe_priority","port_isolation","voice_vlan","poe_limit_type","voice_vlan_cos_mode","bw_ingress","bw_egress","security_count","sc_broadcast","sc_unknown_multicast","sc_unknown_unicast","portshield","portshield_uplink","port_8021x_mode","port_8021x_reauth","port_8021x_reauth_period","port_8021x_guest_vlan","port_8021x_radius_vlan_assign","vlan_trunk","vlan_list"]:
                copy_initial_port_json['switch_controller']["port"][0][keys] = kwargs[keys]
            if "link_speed" in kwargs.keys():
                if kwargs['link_speed'] == 'auto':
                    copy_initial_port_json['switch_controller']["port"][0]['link_speed']['auto_negotiate'] = True
                elif 'full' in kwargs['link_speed'] or 'half' in kwargs['link_speed']:
                    m = re.match(r'(full|half)(\d*)',
                                    kwargs['link_speed'], re.I)
                    copy_initial_port_json['interface']['ipv4']['link_speed'][m.group(
                        1)] = m.group(2)

                else:
                    logger('Error: link_speed invalid!')
        return copy_initial_port_json
        #except Exception as e:
        #    print(e)
        #    logger.error('Error: In creating JSON for port')

    def build_json_port_name(self, **kwargs):
        copy_initial_port_json_name = copy.deepcopy(self.initial_port_json_name)
        #try:
        for keys in kwargs.keys():
            if keys in ["name","switch","enable","stp","poe","poe_priority","port_isolation","voice_vlan","poe_limit_type","voice_vlan_cos_mode","bw_ingress","bw_egress","security_count","sc_broadcast","sc_unknown_multicast","sc_unknown_unicast","portshield","portshield_uplink","port_8021x_mode","port_8021x_reauth","port_8021x_reauth_period","port_8021x_guest_vlan","port_8021x_radius_vlan_assign","vlan_trunk","vlan_list"]:
                copy_initial_port_json_name['switch_controller']["port"][0][keys] = kwargs[keys]
            if "link_speed" in kwargs.keys():
                if kwargs['link_speed'] == 'auto':
                    copy_initial_port_json_name['switch_controller']["port"][0]['link_speed']['auto_negotiate'] = True
                elif 'full' in kwargs['link_speed'] or 'half' in kwargs['link_speed']:
                    m = re.match(r'(full|half)(\d*)',
                                    kwargs['link_speed'], re.I)
                    copy_initial_port_json_name['interface']['ipv4']['link_speed'][m.group(
                        1)] = m.group(2)

                else:
                    logger('Error: link_speed invalid!')
        return copy_initial_port_json_name
    
    def build_json_portshielding(self, **kwargs):
        copy_initial_portshielding_json = copy.deepcopy(self.initial_portshielding_json)
        #try:
        for keys in kwargs.keys():
            copy_initial_portshielding_json['switch_controller']["port"][0][keys] = kwargs[keys]
        return copy_initial_portshielding_json

    def build_json_disable_enable(self, **kwargs):
        copy_initial_json_disable_enable = copy.deepcopy(self.initial_json_disable_enable)
        #try:
        for keys in kwargs.keys():
            copy_initial_json_disable_enable['switch_controller']["port"][0][keys] = kwargs[keys]
        return copy_initial_json_disable_enable

    def config_port(self, msg=False, **kwargs):
        url = self.general_url+self.port_url
        initial_port_json = self.build_json_port(**kwargs)
        logger.debug("URL for posting", url)
        post_response = self.fw.api_post(url, data=initial_port_json)

        return post_response

    def get_port(self):
        """
        """
        url = self.general_url+self.port_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        return get_response

    def get_port_info(self, port_number, switch_name,):
        url = self.general_url+self.port_url + '/' + 'name' + \
            '/' + port_number + '/' + 'switch' + '/' + switch_name
        get_response = self.fw.api_get(url)
        return get_response

    def configure_port(self, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.port_url
        initial_port_json = self.build_json_port(**kwargs)
        print(initial_port_json)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_port_json)
        post_response = self.fw.api_put(url, data=initial_port_json)

        return post_response

    def configure_port_name(self,port_number, switch_name, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.port_url + '/' + 'name' + \
            '/' + port_number + '/' + 'switch' + '/' + switch_name
        initial_port_json_name = self.build_json_port_name(**kwargs)
        print(initial_port_json_name)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_port_json_name)
        post_response = self.fw.api_put(url, data=initial_port_json_name)

        return post_response

    def configure_port_disable_enable(self,port_number, switch_name, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.port_url + '/' + 'name' + \
            '/' + port_number + '/' + 'switch' + '/' + switch_name
        initial_json_disable_enable = self.build_json_disable_enable(**kwargs)
        print(initial_json_disable_enable)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_json_disable_enable)
        post_response = self.fw.api_put(url, data=initial_json_disable_enable)

        return post_response

    def configure_portshield(self, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.port_url
        initial_portshielding_json = self.build_json_portshielding(**kwargs)
        print(initial_portshielding_json)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_portshielding_json)
        post_response,result = self.fw.api_put(url, data=initial_portshielding_json,msg=True)

        return post_response,result

    def restart_fw(self):
        post_response=self.fw.api_restart()
        return post_response


class Voice_vlan():

    def __init__(self, fw):
        self.fw = fw
        self.voice_vlan_url = '/switch-controller/voice-vlan'
        self.general_url = 'api/sonicos'

        #initializing the initial dictionary
        self.initial_voice_vlan_json = {
            "switch_controller": {
                "voice_vlan": [
                    {
                        "switch": "",
                        "state": "disabled",
                        "vlan": 0,
                        "priority_tag": 5,
                        "dscp": 46
                    }
                ]
            }
        }

    def build_json_voice_vlan(self, **kwargs):
        copy_initial_voice_vlan_json = copy.deepcopy(self.initial_voice_vlan_json)
        try:
            for keys in kwargs.keys():
                if keys in ["switch","state","vlan","priority_tag","dscp"]:
                    copy_initial_voice_vlan_json['switch_controller']["voice_vlan"][0][keys] = kwargs[keys]
            return copy_initial_voice_vlan_json
        except KeyError as e:
            logger.error('Error: In creating JSON for voice_vlan')

    def config_voice_vlan(self, msg=False, **kwargs):
        url = self.general_url+self.voice_vlan_url
        initial_voice_vlan_json = self.build_json_voice_vlan(**kwargs)
        logger.debug("URL for posting", url)
        post_response = self.fw.api_post(url, data=initial_voice_vlan_json)

        return post_response

    def get_voice_vlan(self):
        """
        """
        url = self.general_url+self.voice_vlan_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        return get_response

    def get_voice_vlan_by_switch_name(self, switch_name,):
        url = self.general_url+self.voice_vlan_url + '/' +  'switch' + '/' + switch_name
        get_response = self.fw.api_get(url)
        return get_response

    def configure_voice_vlan(self, msg=False, **kwargs):
        """
        """
        url = self.general_url+self.voice_vlan_url
        initial_voice_vlan_json = self.build_json_voice_vlan(**kwargs)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_voice_vlan_json)
        post_response = self.fw.api_put(url, data=initial_voice_vlan_json)

        return post_response
    def configure_voice_vlan_by_switch_name(self, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.voice_vlan_url + '/' +  'switch' + '/' + kwargs['name']
        initial_voice_vlan_json = self.build_json_voice_vlan(**kwargs)

        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_voice_vlan_json)
        post_response = self.fw.api_put(url, data=initial_voice_vlan_json)

        return post_response

    def restart_fw(self):
        response=self.fw.api_restart()
        return response

class Arp():

    def __init__(self, fw):
        self.fw = fw
        self.arp_url = '/switch-controller/arp'
        self.dynamic_arp_url ="/dynamic-file/getSnwlDynamicMacAddress.json?switchId="
        self.arp_aging_url ="/switch-controller/arp-aging-time"
        self.general_url = 'api/sonicos'

        #initializing the initial dictionary
        self.initial_arp_json = {
            "switch_controller": {
                "arp": [
                    {
                        "mac": "",
                        "vlan": 0,
                        "switch": "",
                        "port": 0
                    }
                ]
            }
        }

    def build_json_arp(self, **kwargs):
        copy_initial_arp_json = copy.deepcopy(self.initial_arp_json)
        try:
            for keys in kwargs.keys():
                if keys in ["mac","vlan","switch","port"]:
                    copy_initial_arp_json['switch_controller']["arp"][0][keys] = kwargs[keys]

            return copy_initial_arp_json
        except KeyError:
            logger.error('Error: In creating JSON for arp')

    def config_arp(self, msg=False, **kwargs):
        url = self.general_url+self.arp_url
        initial_arp_json = self.build_json_arp(**kwargs)
        logger.debug("URL for posting", url)
        post_response = self.fw.api_post(url, data=initial_arp_json)

        return post_response

    def get_static_arp(self):
        """
        """
        url = self.general_url+self.arp_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        return get_response

    def get_static_arp_by_switch_name(self, switch_name,):
        url = self.general_url+self.arp_url + '/' +  'switch' + '/' + switch_name
        get_response = self.fw.api_get(url)
        return get_response
    
    def get_dynamic_arp(self,swichid):
        
        url = self.general_url+self.dynamic_arp_url +swichid
        get_response = self.fw.api_get(url)
        return get_response

    def add_static_arp(self, msg=False, **kwargs):
        """
        """
        url = self.general_url+self.arp_url
        initial_arp_json = self.build_json_arp(**kwargs)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_arp_json)
        post_response = self.fw.api_post(url, data=initial_arp_json)
        return post_response
    
    def delete_static_arp(self, msg=False, **kwargs):
        """
        """
        url = self.general_url+self.arp_url+"/mac/"+kwargs["mac"]+"/vlan/"+str(kwargs["vlan"])+"/switch/"+kwargs["switch"]
        logger.debug("URL for deleting", url)
        post_response = self.fw.api_delete(url)
        return post_response

    def add_static_arp_by_switch_name(self, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.arp_url + '/' +  'switch' + '/' + kwargs['name']
        initial_arp_json = self.build_json_arp(**kwargs)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_arp_json)
        post_response = self.fw.api_put(url, data=initial_arp_json)
        return post_response

    def configure_static_arp(self, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.arp_url 
        initial_arp_json = self.build_json_arp(**kwargs)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_arp_json)
        post_response = self.fw.api_put(url, data=initial_arp_json)
        return post_response

    def get_aging_time(self):
        """
        """
        url = self.general_url+self.arp_aging_url
        get_response = self.fw.api_get(url)
        return get_response

    def configure_aging_time(self,switch,aging_time):
        """
        """
        payload={"switch_controller":{"arp_aging_time":[{"switch":switch,"aging_time":int(aging_time)}]}}
        url = self.general_url+self.arp_aging_url
        get_response = self.fw.api_put(url,data=payload)
        return get_response 

    def restart_fw(self):
        response=self.fw.api_restart()
        return response

class Users():

    def __init__(self, fw):
        self.fw = fw
        self.user_url = '/switch-controller/user'
        self.general_url = 'api/sonicos'

        #initializing the initial dictionary
        self.initial_user_json = {
     "switch_controller": {
         "user": [
             {
                 "user_name": ""
                ,"switch": ""
                ,"password": ""
                ,"privilege_type": ""
             }
         ]
     }
}

    def build_json_user(self, **kwargs):
        copy_initial_user_json = copy.deepcopy(self.initial_user_json)
        try:
            for keys in kwargs.keys():
                if keys in ["user_name","switch","password","privilege_type"]:
                    copy_initial_user_json['switch_controller']["user"][0][keys] = kwargs[keys]

            return copy_initial_user_json
        except KeyError:
            logger.error('Error: In creating JSON for user')

    def config_user(self, msg=False, **kwargs):
        url = self.general_url+self.user_url
        initial_user_json = self.build_json_user(**kwargs)
        logger.debug("URL for posting", url)
        post_response = self.fw.api_post(url, data=initial_user_json)

        return post_response

    def get_user(self):
        """
        """
        url = self.general_url+self.user_url
        logger.debug("URL for Get:- ", url)
        get_response = self.fw.api_get(url)
        return get_response

    def get_user_by_switch_name(self, switch_name,):
        url = self.general_url+self.user_url + '/' +  'switch' + '/' + switch_name
        get_response = self.fw.api_get(url)
        return get_response
    
    def add_user(self, msg=False, **kwargs):
        """
        """
        url = self.general_url+self.user_url
        initial_user_json = self.build_json_user(**kwargs)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_user_json)
        post_response = self.fw.api_post(url, data=initial_user_json)
        return post_response

    def add_user_by_switch_name(self, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.user_url + '/' +  'switch' + '/' + kwargs['name']
        initial_user_json = self.build_json_user(**kwargs)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_user_json)
        post_response = self.fw.api_put(url, data=initial_user_json)
        return post_response

    def configure_user(self, msg=False,**kwargs):
        """
        """
        url = self.general_url+self.user_url 
        initial_user_json = self.build_json_user(**kwargs)
        logger.debug("URL for posting", url)
        logger.debug("data for posting", initial_user_json)
        post_response = self.fw.api_put(url, data=initial_user_json)
        return post_response
    
    def delete_user(self, msg=False,**kwargs):
        """
        /switch-controller/user/user-name/{USERNAME}/switch/{SWITCHNAME}
        """
        url = self.general_url+self.user_url+  '/user-name' + '/' +  kwargs['user_name']  + '/' +  'switch' + '/' + kwargs['switch']
        logger.debug("URL for delete", url)
        delete_response = self.fw.api_delete(url)
        return delete_response

    def restart_fw(self):
        response=self.fw.api_restart()
        return response
