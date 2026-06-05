import copy
import json
from re import T
import sys
from runner.settings import logger

class SDWANGroupAPI:
    '''Sdwan Group class'''
    default_options = {
        'name': None,
        'interface_name' : None

         }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/sdwan/groups'
        self.url1 = 'api/sonicos/dynamic-file/'
        self.url_del = 'api/sonicos/sdwan/all-groups'
        self.initial_json_sdwan_groups = {
    "sdwan": {
        "group": [
            {
                "name": '',
                "interface": [
                    {
                        "name": '',
                        "priority": 0,
                        "cost": 0,
                        "ingress_bandwidth": 0.0,
                        "egress_bandwidth": 0.0
                    }
                ]
            }
        ]
    }
}
    #Build json for sdwan group Page
    def build_json_sdwan_group(self, **kwargs):
        json_input = {}
        group_list = []
        json_input = copy.deepcopy(self.initial_json_sdwan_groups)
        try:
            json_input['sdwan']['group'][0]['name'] = kwargs['name']
            try:
                count =0
                if 'interface_name' in kwargs.keys():
                    for access_name in kwargs['interface_name']:
                        access_gt = {'name': access_name}
                        count = count + 1
                        logger.info(group_list.append(access_gt))
                    json_input['sdwan']['group'][0]['interface'] = group_list
                logger.info(count)
                if 'priority' in kwargs.keys():
                    json_input['sdwan']['group'][0]['interface'][0]['priority'] = kwargs['priority']
                else:

                    priority = count
                    while(count > 0):
                        count = count -1
                        json_input['sdwan']['group'][0]['interface'][count]['priority'] = priority
                        priority = priority -1

                if 'cost' in kwargs.keys():
                    json_input['sdwan']['group'][0]['interface'][0]['cost'] = kwargs['cost']
                else:

                    cost = count
                    while (count > 0):
                        count = count - 1
                        json_input['sdwan']['group'][0]['interface'][count]['cost'] = cost
                        cost = cost - 1

                if 'ingress_bandwidth' in kwargs.keys():
                    json_input['sdwan']['group'][0]['interface'][0]['ingress_bandwidth'] = kwargs['ingress_bandwidth']
                else:

                    ingress_bandwidth = count
                    while (count > 0):
                        count = count - 1
                        json_input['sdwan']['group'][0]['interface'][count]['ingress_bandwidth'] = ingress_bandwidth
                        ingress_bandwidth = ingress_bandwidth - 1
                if 'egress_bandwidth' in kwargs.keys():
                    json_input['sdwan']['group'][0]['interface'][0]['egress_bandwidth'] = kwargs['egress_bandwidth']
                else:

                    egress_bandwidth = count
                    while (count > 0):
                        count = count - 1
                        json_input['sdwan']['group'][0]['interface'][count]['egress_bandwidth'] = egress_bandwidth
                        egress_bandwidth = egress_bandwidth - 1




            except KeyError as ke:
                logger.info.info('Error: In Creating the Json for sdwan groups')
        except KeyError:
            logger.info('Error: In Creating the Json for sdwan groups')

        return json_input

    def get_sdwan_group(self):
        get_response = self.fw.api_get(self.url)
        return get_response

    def get_sdwan_group_name(self, name):
        url = self.url + '/' + 'name' + '/' + name
        logger.info(url)
        get_response = self.fw.api_get(url)
        return get_response
       
    
    def get_sdwan_dynamicfile(self,name):
        urldynamic = self.url1 + name
        get_response = self.fw.api_get(urldynamic)
        return get_response

    def get_sdwan_probe_stats(self, name=None, iface=None):
        dynamic_url = 'getSdwanStats.json?type=2&statsType=1'
        resp = self.get_sdwan_dynamicfile(dynamic_url)
        # Below is the output contained in resp
        # {  "sdwanProbeStats":
        # "name,		handle,	iface,	latency,	jitter,	loss,	state|
        # \"Probe1\",	1,		1,		0.453,		0.056,	0.000,	2|
        # \"Probe1\",	1,		2,		0.350,		0.019,	0.000,	2",
        # "systime": 1732247501,
        # "loggedin": true }
        resp = resp['sdwanProbeStats']
        if name and iface:
            for policy in resp.split('|'):
                if policy.split(',')[0] == name and policy.split(',')[2] == iface:
                    resp = policy.split(',')
                    break
        return resp

    def configure_sdwan_group(self, msg=False, **kwargs):
        self.options = dict(SDWANGroupAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_group(**kwargs)
        logger.info('The json input build is',json_input)
        sdwangrp_resp = self.fw.api_post(self.url, msg, data=json_input)
        return sdwangrp_resp

    def delete_sdwan_group(self, name, msg=False):
        url = self.url + '/' + 'name' + '/'  + name
        sdwan_grp_resp = self.fw.api_delete(url, msg)
        return sdwan_grp_resp

    def delete_all_sdwan_group(self, msg=False):
        sdwan_grp_resp = self.fw.api_delete(self.url_del, msg)
        return sdwan_grp_resp

    def edit_sdwan_group(self, msg=False, **kwargs):
        self.options = dict(SDWANGroupAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_group(**kwargs)
        logger.info('The json input build is',json_input)
        sdwangrp_resp = self.fw.api_put(self.url, msg, data=json_input)
        return sdwangrp_resp

    def edit_sdwan_group_name(self,name, msg=False, **kwargs):
        self.options = dict(SDWANGroupAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_group(**kwargs)
        logger.info('The json input build is',json_input)
        url_edit=self.url + '/' + 'name' + '/'  + name
        sdwangrp_resp = self.fw.api_put(url_edit, msg, data=json_input)
        return sdwangrp_resp

class SDWANProbesAPI:
    '''Sdwan Performance Probes'''
    default_options = {
        'name': None,
        'comment' : '',
        'sdwan_group' :None,
        'probe_target' :None,
        'probe_type':'icmp', #icmp, tcp
        'port' :None,
        'interval': 3,
        'reply_timeout': 1,
        'missed': 3,
        'successful': 1,
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/sdwan/sla-probes/ipv4'
        self.url_del = 'api/sonicos/sdwan/all-sla-probes/ipv4'
        self.initial_json_sdwan_probes = {
            'sdwan': {
                'sla_probe': [
                    {
                    'ipv4': {
                        'name': '',
                        'comment': '',
                        'sdwan_group': '',
                        'probe': {
                        'target': {
                        'name': ''
                        },
                        'type': {
                            'ping': {
                                'explicit': False
                                    }
                                 },
                            'interval': 3
                                },
                        'reply_timeout': 1,
                        'interval': {
                        'missed': 3,
                        'successful': 1
                                        },
                        # 'rst_as_miss': False
                                    }
                                }
                            ]
                        }
                    }

#Build json for sdwan performance probe Page
    def build_json_sdwan_probes(self, **kwargs):
        json_input = copy.deepcopy(self.initial_json_sdwan_probes)
        try:
            json_input['sdwan']['sla_probe'][0]['ipv4']['name'] = kwargs['name']
            if('interval' in kwargs.keys()):
                json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['interval'] = kwargs['interval']
            if('reply_timeout' in kwargs.keys()):
                json_input['sdwan']['sla_probe'][0]['ipv4']['reply_timeout'] = kwargs['reply_timeout']
            if('missed' in kwargs.keys()):
                json_input['sdwan']['sla_probe'][0]['ipv4']['interval']['missed'] = kwargs['missed']
            json_input['sdwan']['sla_probe'][0]['ipv4']['sdwan_group'] = kwargs['sdwan_group']
            if('probe_target' in kwargs.keys()):
                json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['target']['name'] = kwargs['probe_target']

            if('comment' in kwargs.keys()):
                json_input['sdwan']['sla_probe'][0]['ipv4']['comment'] = kwargs['comment']
            if('probe_type' in kwargs.keys()):
                if kwargs['probe_type'] == 'ping':
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['ping']['explicit'] = True
                elif kwargs['probe_type'] == 'http':
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['http'] = json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['ping']
                    del json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['ping']
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['http']['explicit'] = True
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['http']['port'] = kwargs['port']
                elif kwargs['probe_type'] == 'https':
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['https'] = json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['ping']
                    del json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['ping']
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['https']['explicit'] = True
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['https']['port']=kwargs['port']
                else:
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['tcp'] = json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['ping']
                    del json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['ping']
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['tcp']['explicit'] = True
                    json_input['sdwan']['sla_probe'][0]['ipv4']['probe']['type']['tcp']['port'] = kwargs['port']
            if('rst_as_miss' in kwargs.keys()):
                json_input['sdwan']['sla_probe'][0]['ipv4']['rst_as_miss'] = kwargs['rst_as_miss']
        except KeyError:
            logger.info.error('Error: in creating JSON for sdwan probes settings')
            logger.info.info(json_input)
            logger.info('Error: In Creating the Json for sdwan probes')

        return json_input

    def get_sdwan_probes(self):
        get_response = self.fw.api_get(self.url)
        return get_response

    def get_sdwan_probes_name(self,name):
        url = self.url + '/' + 'name' + '/'  + name
        get_response = self.fw.api_get(url)
        return get_response

    def configure_sdwan_probes(self, msg=False, **kwargs):
        self.options = dict(SDWANProbesAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_probes(**kwargs)
        sdwanprobe_resp = self.fw.api_post(self.url, msg, data=json_input)
        return sdwanprobe_resp

    def delete_sdwan_probes(self, name, msg=False):
        url = self.url + '/' + 'name' + '/'  + name
        sdwanprobe_resp = self.fw.api_delete(url, msg)
        return sdwanprobe_resp

    def delete_all_sdwan_probes(self, msg=False):
        sdwanprobe_resp = self.fw.api_delete(self.url_del, msg)
        return sdwanprobe_resp

    def edit_sdwan_probes(self, msg=False, **kwargs):
        self.options = dict(SDWANProbesAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_probes(**kwargs)
        logger.info('The json input build is',json_input)
        sdwanprobe_resp = self.fw.api_put(self.url, msg, data=json_input)
        return sdwanprobe_resp

    def edit_sdwan_probes_name(self, name, msg=False, **kwargs):
        self.options = dict(SDWANProbesAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_probes(**kwargs)
        logger.info('The json input build is',json_input)
        url_probe = self.url + '/' + 'name' + '/'  + name
        sdwanprobe_resp = self.fw.api_put(url_probe, msg, data=json_input)
        return sdwanprobe_resp


class SDWANPerfClassAPI:
    '''Sdwan Performance Class Object'''
    default_options = {
        'name': None,
        'comment' : '',
        'latency' :None,
        'jitter' :None,
        'packet_loss':None
        }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/sdwan/sla-class-objects'
        self.url_del = 'api/sonicos/sdwan/all-sla-class-objects'
        self.initial_json_sdwan_perf_class = {
             'sdwan': {
                'sla_class_object': [
                    {
                        'name': '',
                        'latency': 0,
                        'jitter': 0,
                        'packet_loss': 0,
                        'include': {
                            'latency': True,
                            'jitter': True,
                            'packet_loss': True
                        },
                        'comment': ''
                    }
                ]
            }
        }

#Build json for sdwan performance class object Page
    def build_json_sdwan_perf_class(self, **kwargs):
        json_input = copy.deepcopy(self.initial_json_sdwan_perf_class)
        try:
            json_input['sdwan']['sla_class_object'][0]['name'] = kwargs['name']
            json_input['sdwan']['sla_class_object'][0]['latency'] = kwargs['latency']
            json_input['sdwan']['sla_class_object'][0]['jitter'] = kwargs['jitter']
            json_input['sdwan']['sla_class_object'][0]['packet_loss'] = kwargs['packet_loss']
            if 'include' in kwargs.keys():
                json_input['sdwan']['sla_class_object'][0]['include']['latency'] = kwargs['include']['latency']
                json_input['sdwan']['sla_class_object'][0]['include']['jitter'] = kwargs['include']['jitter']
                json_input['sdwan']['sla_class_object'][0]['include']['packet_loss'] = kwargs['include']['packet_loss']
            if 'comment' in kwargs.keys():
                json_input['sdwan']['sla_class_object'][0]['comment'] = kwargs['comment']
        except KeyError:
            logger.info.error('Error: in creating JSON for sdwan probes settings')
            logger.info.info(json_input)
            logger.info('Error: In Creating the Json for sdwan probes')

        return json_input

    def get_sdwan_perf_class(self):
        get_response = self.fw.api_get(self.url)
        return get_response

    def get_sdwan_perf_class_name(self, name):
        url = self.url + '/' + 'name' + '/' + name
        get_response = self.fw.api_get(url)
        return get_response

    def configure_sdwan_perf_class(self, msg=False, **kwargs):
        self.options = dict(SDWANPerfClassAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_perf_class(**kwargs)
        logger.info('The json input build is',json_input)
        sdwanperf_resp = self.fw.api_post(self.url, msg, data=json_input)
        return sdwanperf_resp

    def delete_sdwan_perf_class(self, name, msg=False):
        url = self.url + '/' + 'name' + '/'  + name
        sdwanperf_resp = self.fw.api_delete(url, msg)
        return sdwanperf_resp

    def delete_all_sdwan_perf_class(self, msg=False):
        sdwanperf_resp = self.fw.api_delete(self.url_del, msg)
        return sdwanperf_resp

    def edit_sdwan_perf_class(self, msg=False, **kwargs):
        self.options = dict(SDWANPerfClassAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_perf_class(**kwargs)
        logger.info('The json input build is',json_input)
        sdwanperf_resp = self.fw.api_put(self.url, msg, data=json_input)
        return sdwanperf_resp

    def edit_sdwan_perf_class_name(self, name, msg=False, **kwargs):
        self.options = dict(SDWANPerfClassAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_perf_class(**kwargs)
        logger.info('The json input build is',json_input)
        url_probe = self.url + '/' + 'name' + '/'  + name
        sdwanperf_resp = self.fw.api_put(self.url, msg, data=json_input)
        return sdwanperf_resp

class SDWANPathSelectionAPI:
    '''Sdwan Path Selection Profiles'''
    default_options = {
        'name': None,
        'sdwan_group': None,
        'sla_probe': None,
        'sla_class': None,
        # "load_balancing": "ratio",
        # "percent": [
        #     {
        #         "interface": "X1",
        #         "percent": 100.000000
        #     },
        #   ],

        'backup_interface':  "Drop_TunnelIf",
        'probe_default_up': True,
        #'reset_connections': False,
        "sla_strategy": "best",
        # "include_cost": False
        }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/sdwan/path-selection-profiles'
        self.url_del = 'api/sonicos/sdwan/all-path-selection-profiles'
        self.initial_ratio_json = {
    "sdwan": {
        "path_selection_profile": [
            {
                "name": None,
                "sdwan_group": None,
                "sla_probe": None,
                "sla_class": None,
                "load_balancing": "ratio",
                "percent": [
                    {
                        "interface": None,
                        "percent": 0.0
                    },
                    {
                        "interface": None,
                        "percent": 0.0
                    }
                ],
                "backup_interface": "Drop_TunnelIf",
                "probe_default_up": True,
                "reset_connections": False,
                "sla_strategy": "custom",
                # "include_cost": False
            }
        ]
    }
}
        self.initial_spill_over_json = {
            "sdwan": {
                "path_selection_profile": [
                    {
                        "name": None,
                        "sdwan_group": None,
                        "sla_probe": None,
                        "sla_class": None,
                        "load_balancing": "spillover",
                        "ingress": {
                            "interface": None,
                            "ingress": 0.00
                        },
                        "egress": {
                            "interface": None,
                            "egress": 0.00
                        },
                        "backup_interface": "Drop_TunnelIf",
                        "probe_default_up": True,
                        "reset_connections": False,
                        "sla_strategy": "custom",
                        # "include_cost": False
                    }
                ]
            }
        }
        self.initial_volume_json = {
            "sdwan": {
                "path_selection_profile": [
                    {
                        "name": None,
                        "sdwan_group": None,
                        "sla_probe": None,
                        "sla_class": None,
                        "load_balancing": "volume",
                        "weight": [
                            {
                                "interface": None,
                                "weight": 0
                            },
                            {
                                "interface": None,
                                "weight": 0
                            }
                        ],
                        "backup_interface": None,
                        "probe_default_up": True,
                        "reset_connections": False,
                        "sla_strategy": "custom",
                        # "include_cost": False
                    }
                ]
            }
        }

        self.initial_json_sdwan_path_selection = {
    "sdwan": {
        "path_selection_profile": [
            {
                "name": None,
                "sdwan_group": None,
                "sla_probe": None,
                "sla_class": None,
                # "load_balancing": "ratio",
                # "percent": [
                #     {
                #         "interface": "X1",
                #         "percent": 100.000000
                #     },
                # ],
                "backup_interface": "Drop_TunnelIf",
                "probe_default_up": True,
                #"reset_connections": False,
                "sla_strategy": "best",
                # "include_cost": False
            }
        ]
    }
}

#Build json for Sdwan Path Selection Profiles
    def build_json_sdwan_path_selection(self, **kwargs):

        json_input = copy.deepcopy(self.initial_json_sdwan_path_selection)


        try:
            if 'name' in kwargs.keys():
                json_input['sdwan']['path_selection_profile'][0]['name'] = kwargs['name']
            if 'sdwan_group' in kwargs.keys():
                json_input['sdwan']['path_selection_profile'][0]['sdwan_group'] = kwargs['sdwan_group']
            if 'sla_probe' in kwargs.keys():
                json_input['sdwan']['path_selection_profile'][0]['sla_probe'] = kwargs['sla_probe']

            if 'sla_class' in kwargs.keys():
                json_input['sdwan']['path_selection_profile'][0]['sla_class'] = kwargs['sla_class']

            if 'backup_interface' in kwargs.keys():
                json_input['sdwan']['path_selection_profile'][0]['backup_interface'] = kwargs['backup_interface']

            if 'probe_default_up' in kwargs.keys():
                json_input['sdwan']['path_selection_profile'][0]['probe_default_up'] = kwargs['probe_default_up']
            if 'reset_connections' in kwargs.keys():
                json_input['sdwan']['path_selection_profile'][0]['reset_connections'] = kwargs['reset_connections']


            if 'sla_strategy' in kwargs.keys():
                json_input['sdwan']['path_selection_profile'][0]['sla_strategy'] = kwargs['sla_strategy']

            if 'load_balancing' in kwargs.keys():
                if kwargs['load_balancing'] == 'ratio':
                    json_input = copy.deepcopy(self.initial_ratio_json)
                    json_input['sdwan']['path_selection_profile'][0]['name'] = kwargs['name']
                    json_input['sdwan']['path_selection_profile'][0]['sdwan_group'] = kwargs['sdwan_group']
                    json_input['sdwan']['path_selection_profile'][0]['sla_probe'] = kwargs['sla_probe']
                    json_input['sdwan']['path_selection_profile'][0]['sla_class'] = kwargs['sla_class']
                    json_input['sdwan']['path_selection_profile'][0]['backup_interface'] = kwargs['backup_interface']
                    json_input['sdwan']['path_selection_profile'][0]['probe_default_up'] = kwargs['probe_default_up']
                    json_input['sdwan']['path_selection_profile'][0]['reset_connections'] = kwargs['reset_connections']
                    json_input['sdwan']['path_selection_profile'][0]['sla_strategy'] = kwargs['sla_strategy']
                    json_input['sdwan']['path_selection_profile'][0]['load_balancing'] = kwargs['load_balancing']
                    json_input['sdwan']['path_selection_profile'][0]['percent'] = kwargs['percent']
                elif kwargs['load_balancing'] == 'spillover':
                    json_input = copy.deepcopy(self.initial_spill_over_json)
                    json_input['sdwan']['path_selection_profile'][0]['name'] = kwargs['name']
                    json_input['sdwan']['path_selection_profile'][0]['sdwan_group'] = kwargs['sdwan_group']
                    json_input['sdwan']['path_selection_profile'][0]['sla_probe'] = kwargs['sla_probe']
                    json_input['sdwan']['path_selection_profile'][0]['sla_class'] = kwargs['sla_class']
                    json_input['sdwan']['path_selection_profile'][0]['backup_interface'] = kwargs['backup_interface']
                    json_input['sdwan']['path_selection_profile'][0]['probe_default_up'] = kwargs['probe_default_up']
                    json_input['sdwan']['path_selection_profile'][0]['reset_connections'] = kwargs['reset_connections']
                    json_input['sdwan']['path_selection_profile'][0]['sla_strategy'] = kwargs['sla_strategy']
                    json_input['sdwan']['path_selection_profile'][0]['load_balancing'] = kwargs['load_balancing']
                    json_input['sdwan']['path_selection_profile'][0]['ingress'] = kwargs['ingress']
                    json_input['sdwan']['path_selection_profile'][0]['egress'] = kwargs['egress']
                elif kwargs['load_balancing'] == 'volume':
                    json_input = copy.deepcopy(self.initial_volume_json)
                    json_input['sdwan']['path_selection_profile'][0]['name'] = kwargs['name']
                    json_input['sdwan']['path_selection_profile'][0]['sdwan_group'] = kwargs['sdwan_group']
                    json_input['sdwan']['path_selection_profile'][0]['sla_probe'] = kwargs['sla_probe']
                    json_input['sdwan']['path_selection_profile'][0]['sla_class'] = kwargs['sla_class']
                    json_input['sdwan']['path_selection_profile'][0]['backup_interface'] = kwargs['backup_interface']
                    json_input['sdwan']['path_selection_profile'][0]['probe_default_up'] = kwargs['probe_default_up']
                    json_input['sdwan']['path_selection_profile'][0]['reset_connections'] = kwargs['reset_connections']
                    json_input['sdwan']['path_selection_profile'][0]['sla_strategy'] = kwargs['sla_strategy']
                    json_input['sdwan']['path_selection_profile'][0]['load_balancing'] = kwargs['load_balancing']
                    json_input['sdwan']['path_selection_profile'][0]['weight'] = kwargs['weight']

            if (not kwargs['sla_probe'].startswith('VPN Probe')):
                json_input['sdwan']['path_selection_profile'][0]['reset_connections'] = kwargs['reset_connections']

        except KeyError:
            logger.info.error('Error: in creating JSON for sdwan probes settings')
            logger.info.info(json_input)
            logger.info('Error: In Creating the Json for sdwan probes')

        return json_input


    def get_sdwan_psp(self):
        get_response = self.fw.api_get(self.url)
        return get_response

    def get_sdwan_psp_name(self,name):
        url = self.url + '/' + 'name' + '/'  + name
        get_response = self.fw.api_get(url)
        return get_response

    def configure_sdwan_psp(self, msg=False, **kwargs):
        self.options = dict(SDWANPathSelectionAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_path_selection(**kwargs)
        logger.info('The json input build is',json_input)
        sdwanpsp_resp = self.fw.api_post(self.url, msg, data=json_input)
        return sdwanpsp_resp

    def delete_sdwan_psp(self, name, msg=False):
        url = self.url + '/' + 'name' + '/'  + name
        sdwanpsp_resp = self.fw.api_delete(url, msg)
        return sdwanpsp_resp

    def delete_all_sdwan_psp(self, msg=False):
        sdwanpsp_resp = self.fw.api_delete(self.url_del, msg)
        return sdwanpsp_resp

    def edit_sdwan_psp(self, msg=False, **kwargs):
        self.options = dict(SDWANPathSelectionAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_path_selection(**kwargs)
        logger.info('The json input build is',json_input)
        sdwanpsp_resp = self.fw.api_put(self.url, msg, data=json_input)
        return sdwanpsp_resp


    def edit_sdwan_psp_name(self, name, msg=False, **kwargs):
        self.options = dict(SDWANPathSelectionAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_sdwan_probes(**kwargs)
        logger.info('The json input build is', json_input)
        url_psp = self.url + '/' + 'name' + '/' + name
        sdwanpsp_resp = self.fw.api_put(url_psp, msg, data=json_input)
        return sdwanpsp_resp


class SdwanRouteApi:
    '''SdwanRouteApi class'''
    default_options = {
        'name': None,
        'source': {'any': True},
        'destination': {'any': True},
        'service': {'any': True},
        'path_selection_profile': None,
        'interface': None,
        'metric': None,
        'comment': "",
        'disable_on_interface_down': True,
        'tcp_acceleration': False
    }

    def __init__(self, fw):
        self.fw = fw
        self.url1 = 'api/sonicos/route-policies/ipv4'  #
        self.url_v6 = 'api/sonicos/route-policies/ipv6'
        self.url2 = 'api/sonicos/reporting/route-policies/ipv4/system'  # auto added rule
        self.url_v6_auto = 'api/sonicos/reporting/route-policies/ipv6/system'  # auto added rule
        self.url_del = 'api/sonicos/route-policies-sdwan/all/'

        self.initial_json_sdwan_route = {
            'route_policies': [{
                'ipv4': {
                    'interface': None,
                    'metric': 1,
                    "source": {"any": True},
                    "destination": {"any": True},
                    "service": {"any": True},
                    "distance": {"auto": True},
                    "path_selection_profile": None,
                    "schedule":{"name": None},
                    "name": 'rr',
                    "type": "sdwan",
                    "comment": "",
                    "disable_on_interface_down": True,
                    "tcp_acceleration": False,
                    "ticket": {
                        "tag1": "",
                        "tag2": "",
                        "tag3": "",
                    }
                }
            }]
}
# Build json for sdwan routes
    def build_json_sdwan_route(self, **kwargs):
        json_input = copy.deepcopy(self.initial_json_sdwan_route)
        try:
            if 'interface' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['interface'] = kwargs['interface']
            if 'name' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['name'] = kwargs['name']
            if 'metric' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['metric'] = kwargs['metric']

            if 'source' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['source'] = kwargs['source']

            if 'destination' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['destination'] = kwargs['destination']

            if 'service' in kwargs.keys():
                if 'app' in json_input['route_policies'][0]['ipv4'].keys():
                    del json_input['route_policies'][0]['ipv4']['app']
                json_input['route_policies'][0]['ipv4']['service'] = kwargs['service']

            if 'app' in kwargs.keys():
                if 'service' in json_input['route_policies'][0]['ipv4'].keys():
                    del json_input['route_policies'][0]['ipv4']['service']
                json_input['route_policies'][0]['ipv4']['app'] = kwargs['app']

            if 'disable_on_interface_down' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['disable_on_interface_down'] = kwargs['disable_on_interface_down']

            if 'comment' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['comment'] = kwargs['comment']

            if 'path_selection_profile' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['path_selection_profile'] = kwargs['path_selection_profile']

            if 'schedule' in kwargs.keys():
                json_input['route_policies'][0]['ipv4']['schedule']['name'] = kwargs['schedule']
                if 'name' in kwargs['schedule']:
                    json_input['schedule'] = {}
                    json_input['route_policies'][0]['ipv4']['schedule']['name'] = kwargs['name']

                if 'always_on' in kwargs['schedule']:
                    del json_input['route_policies'][0]['ipv4']['schedule']['name']
                    json_input['route_policies'][0]['ipv4']['schedule']['always_on'] = kwargs['always_on']
        except KeyError:
            logger.info.error('Error: in creating JSON for sdwan routes settings')
            logger.info.info(json_input)
            logger.info('Error: In Creating the Json for sdwan routes')
        return json_input

    def add_sdwan_route(self, msg=False, **kwargs):
        self.options = dict(SdwanRouteApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        # json_input = kwargs
        json_input = self.build_json_sdwan_route(**kwargs)
        # if 'ipv6' in kwargs['route_policies'][0].keys():
        #     url = self.url_v6
        url = self.url1
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def get_sdwan_route(self, version='v4'):
        if version == 'v4':
            url = self.url1
        else:
            url = self.url_v6
        resp = self.fw.api_get(url)
        return resp

    def get_sdwan_auto_route_policy(self, version='v4'):
        if version == 'v4':
            url = self.url2
        else:
            url = self.url_v6_auto
        resp = self.fw.api_get(url)
        return resp

    def get_sdwan_route_by_name(self, name, version='v4'):
        if version == 'v4':
            url = self.url1
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['route_policies']:
            print(policy)
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                break
        if uuid == None:
            resp = 'No designated sdwan route policy'
            return resp
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_get(url_tmp)
        return resp

    def get_sdwan_route_by_uuid(self, uuid, version='v4'):
        if version == 'v4':
            url = self.url1
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        if uuid == None:
            resp = 'No designated sdwan route policy'
            return resp
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_get(url_tmp)
        return resp

    def del_sdwan_route_by_uuid(self, uuid, version='v4'):
        if version == 'v4':
            url = self.url1

        else:
            url = self.url_v6

        del_url = url + '/uuid/' + uuid
        resp = self.fw.api_delete(del_url)
        return resp

    def del_sdwan_route_by_name(self, name, version='v4'):
        if version == 'v4':
            url = self.url1
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['route_policies']:
            print(policy)
            if policy[version]['name'] == name:
                uuid = policy[version]['uuid']
                break
        del_url = url + '/uuid/' + uuid
        resp = self.fw.api_delete(del_url)
        return resp

    def del_all_sdwan_routes(self):
        resp = self.fw.api_delete(self.url_del)
        return resp

    def edit_sdwan_route_by_uuid(self, uuid, msg=False, version='v4', **kwargs):
        json_input = self.build_json_sdwan_route(**kwargs)
        if version == 'v4':
            url = self.url1

        else:
            url = self.url_v6

        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp

    def edit_sdwan_route(self, rule_name, msg=False, version='v4', **kwargs):
        json_input = self.build_json_sdwan_route(**kwargs)
        if version == 'v4':
            url = self.url1
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        policies = self.fw.api_get(url)
        uuid = None
        for policy in policies['route_policies']:
            if policy[version]['name'] == rule_name:
                uuid = policy[version]['uuid']
                break
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_put(url_tmp, msg, data=json_input)
        return resp
