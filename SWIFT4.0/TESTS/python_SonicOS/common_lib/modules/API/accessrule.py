import json
import copy
import ipaddress
from netaddr import IPAddress
from runner.settings import logger


class Access_Rule():

    def __init__(self, fw):
        self.fw = fw
        self.access_rule_url = 'api/sonicos/access-rules/ipv4'
        self.access_rule_url_ipv6 = 'api/sonicos/access-rules/ipv6'
        self.general_url = 'api/sonicos'

        self.initial_ipv6_access_rule_json = {
            "access_rules": [{
                "ipv6": {
                     "name": ""
                    , "enable": True
                    , "from": ""
                    , "to": ""
                    , "action": ""

                    , "source": {
                        "address": {
                            "any": True
                        }

                        , "port": {
                            "any": True
                        }
                    }

                    , "service": {
                        "any": True
                    }

                    , "destination": {
                        "address": {
                            "any": True
                        }
                    }

                    , "schedule": {
                        "always_on": True
                    }

                    , "users": {
                        "included": {
                            "all": True
                        }

                        , "excluded": {
                            "none": True
                        }
                    }

                    , "comment": ""
                    , "fragments": True
                    , "logging": True
                    , "sip": False
                    , "h323": False
                    , "flow_reporting": False
                    , "botnet_filter": False

                    , "geo_ip_filter": {
                        "enable": False
                        , "global": True
                    }

                    , "block": {
                        "countries": {
                            "unknown": False
                        }
                    }

                    , "packet_monitoring": False
                    , "management": False
                    , "max_connections": 100,

                    # , "priority": {
                    #     "manual": {
                    #         "value": 115
                    #     }
                    # }
                        "priority": {
                            "auto": True
                        }
                    , "tcp": {
                        "timeout": 5
                        , "urgent": False
                    }

                    , "udp": {
                        "timeout": 30
                    }

                    , "connection_limit": {
                        "source": {
                        }

                        , "destination": {
                        }
                    }

                    , "dpi": True

                    , "dpi_ssl": {
                        "client": True
                        , "server": True
                    }

                    , "redirect_unauthenticated_users_to_log_in": True

                    , "quality_of_service": {
                        "class_of_service": {
                        }

                        , "dscp": {
                            "preserve": True
                        }
                    }, 
                    # "bandwidth_management": {
                    #     "egress": {
                    #     }

                    #     , "ingress": {
                    #     }
                    # }
                }
            }]
        }


    def build_ipv6_access_rule_json(self, **kwargs):
        url = self.access_rule_url_ipv6
        logger.info("***                posting JSON to  {}               ***".format(url))
        try:
            json_input = copy.deepcopy(self.initial_ipv6_access_rule_json)
            if "from" not in kwargs.keys() or "to" not in kwargs.keys() or "action" not in kwargs.keys() or "name" not in kwargs.keys():
                logger.info("           importent keys are missing....please input 'from','to','action','name'!      ")
            if 'from' in kwargs.keys() and 'change_from' not in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['from'] = kwargs['from']
            if 'change_from' in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['from'] = kwargs['change_from']
            if 'to' in kwargs.keys() and 'change_to' not in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['to'] = kwargs['to']
            if 'change_to' in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['to'] = kwargs['change_to']
            if 'action' in kwargs.keys():
                if kwargs['action'].lower() in ['allow', 'deny', 'discard']:
                    json_input['access_rules'][0]['ipv6']['action'] = kwargs['action'].lower()
            if 'name' in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['name'] = kwargs['name']
            if 'tcp_timeout' in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['tcp']['timeout'] = kwargs['tcp_timeout']
            if 'udp_timeout' in kwargs.keys():
                if kwargs['udp_timeout'] == 0:
                    logger.info("the udp timeout can not be set under 30!")
                json_input['access_rules'][0]['ipv6']['udp']['timeout'] = kwargs['udp_timeout']
            if 'service' in kwargs.keys():
                dict = {
                    'service':{
                        'name': kwargs['service']
                            },
                        }
                json_input['access_rules'][0]['ipv6'].update(dict)
            if 'schedule' in kwargs.keys():
                dict = {
                    'schedule': {
                        'name': kwargs['schedule']
                    },
                }
                json_input['access_rules'][0]['ipv6'].update(dict)      
            if 'source_addr' in kwargs.keys():
                dict = {
                    'address':{
                        'name': kwargs['source_addr']
                            },
                        }
                json_input['access_rules'][0]['ipv6']['source'].update(dict)
            if 'destination_addr' in kwargs.keys():
                dict = {
                    'address': {
                        'name': kwargs['destination_addr']
                            },
                        }
                json_input['access_rules'][0]['ipv6']['destination'].update(dict)
            if 'priority_mode' in kwargs.keys():
                if kwargs['priority_mode'] == 'manual':
                    if 'priority_value' in kwargs.keys():
                        dict = {
                            "priority": {
                                "manual": {
                                    "value": kwargs['priority_value']
                                }
                            }
                        }
                        json_input['access_rules'][0]['ipv6'].update(dict)
            
            return json_input
                
        except KeyError:
            logger.error('Error: In creating JSON for access rule')

    def delete_ipv6_accessrule(self, **kwargs):
        #to delete a ipv6 access rule must have it's uuid
        if 'name' not in kwargs.keys() or 'from' not in kwargs.keys() or 'to' not in kwargs.keys():
            return False
        uuid = self.get_ipv6_accessrule_uuid(**kwargs)
        logger.info('the custom access-rule {} uuid is: {}'.format(kwargs['name'],uuid))
        url = self.access_rule_url_ipv6  + '/uuid/' + uuid
        logger.info(" URL for delete: {}".format(url))
        delete_response = self.fw.api_delete(url)
        return delete_response

    def config_ipv6_access_rule(self, msg=False, **kwargs):
        if kwargs['option'] == 'add':
            json_input = self.build_ipv6_access_rule_json(**kwargs)
            response = self.fw.api_post(self.access_rule_url_ipv6, msg, data=json_input)
            return response
        if kwargs['option'] == 'delete':
            rc = self.delete_ipv6_accessrule(**kwargs)
            return rc
        if kwargs['option'] == 'modify':
            rc = self.modify_ipv6_access_rule(**kwargs)
            return rc

        logger.info("***********************Configure access rules failed!*********************")
        return False

    def modify_ipv6_access_rule(self, **kwargs):
        #get exist uuid
        if 'name' not in kwargs.keys() or 'from' not in kwargs.keys() or 'to' not in kwargs.keys():
            logger.info("  missing key: 'from' or 'to' or 'name'  ")
            return False
        if 'uuid' in kwargs.keys():
            uuid = kwargs['uuid']
        else:
            uuid = self.get_ipv6_accessrule_uuid(**kwargs)
        url = self.access_rule_url_ipv6 + '/uuid/' + uuid
        logger.info("PUT JSON to URL: {}".format(url))
        json_input = self.build_ipv6_access_rule_json(**kwargs)
        put_response = self.fw.api_put(url, data=json_input)
        return put_response

    #Use it to check management
    def show_ipv6_access_rule(self, access_rule):
        url = self.general_url + '/reporting/access-rules/ipv6'
        logger.info("Get url from: " + url)
        if access_rule == 'https':
            access_rule = 'HTTPS Management'
        elif access_rule == 'http':
            access_rule = 'HTTP Management'
        elif access_rule == 'snmp':
            access_rule = 'SNMP'
        elif access_rule == 'ssh':
            access_rule = 'SSH Management'
        elif access_rule == 'ping':
            access_rule = 'Ping6'
        else:
            logger.info("access rule must be named: https,http,snmp,ssh,ping")
            return False
        json_output = self.fw.api_get(url)
        for item in json_output:
            if item['destination'] == 'X1 Management IPv6 Addresses':
                if item['service'] == access_rule and item['action'] == 'allow':
                    logger.info(item)
                    return True
        logger.info("The access rule {} is not exist".format(access_rule))
        return False

    def get_ipv6_accessrule_uuid(self, **kwargs):
        url = self.general_url + '/reporting/access-rules/ipv6'
        logger.info("Get url from: " + url)
        json_output = self.fw.api_get(url)
        if 'source_addr' in kwargs.keys():
            for item in json_output:
                if item['source'] == kwargs['source_addr']:
                    logger.info(item)
                    #please do not modify this function, I use it to get the priority
                    return item['priority']
        else:    
            for item in json_output:
                if item['from'] == kwargs['from'] and item['to'] == kwargs['to']:
                    logger.info(item)
                    return item['uuid']
            

        logger.info("Get ipv6 accessrule uuid failed!")

    def get_ipv6_accessrule(self, **kwargs):
        uuid = self.get_ipv6_accessrule_uuid(**kwargs)
        url = self.access_rule_url_ipv6 + '/uuid/' + uuid
        logger.info("GET from URL: {}".format(url))
        json_output = self.fw.api_get(url)
        return json_output

    def add_ipv6_accessrule(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url = self.access_rule_url_ipv6
        logger.info(json_input)
        response = self.fw.api_post(url, msg, data=json_input)
        return response


class AccessRuleIPv4Api:
    '''AccessRuleIPv4Api class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_v4 = 'api/sonicos/access-rules/ipv4'
        self.url_v6 = 'api/sonicos/access-rules/ipv6'
        self.url_ipv4 = 'api/sonicos/reporting/access-rules-ipv4/from/'

        self.initial_ipv4_access_rule_json = {
            "access_rules": [
                {
                    "ipv4": {
                        # "name": "default-lan",
                        "comment": "",
                        "action": "allow",
                        "priority": {"auto": True},
                        "enable": True,
                        "from": "LAN",
                        "source": {
                            "address": {},
                            "port": {"any": True}
                        },
                        "to": "WAN",
                        "destination": {
                            "address": {}
                        },
                        "service": {},
                        "users": {
                            "included": {"all": True},
                            "excluded": {"none": True}
                        },
                        "tcp": {"timeout": 15, "urgent": False},
                        "udp": {"timeout": 30},
                        "dpi": True,
                        "dpi_ssl": {"client": True, "server": True},
                        "quality_of_service": {
                            "class_of_service": {},
                            "dscp": {"preserve": True}
                        },
                        "botnet_filter": False,
                        "geo_ip_filter": {"enable": False},
                        "logging": True,
                        "flow_reporting": False,
                        "connection_limit": {
                            "source": {},
                            "destination": {}
                         },
                        "sip": False,
                        "h323": False,
                        "fragments": True,
                        "management": False,
                        "max_connections": 100,
                        "packet_monitoring": False,
#                        "reflexive": False
                        }
                    }
                ]
            }
        
    def build_ipv4_access_rule_json(self, **kwargs):
        '''
        option = {
            'name': 'lan-wan',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {
                'name': 'BGP',
            }
            'source_addr': {
                'name': 'pc1',
            }
            'dst_addr': {
                'host': '10.8.117.1'
            }
        }
        '''
        json_input = copy.deepcopy(self.initial_ipv4_access_rule_json)
        if 'comment' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['comment']=kwargs['comment']
        if 'from' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['from']=kwargs['from']
        if 'to' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['to']=kwargs['to']
        if 'action' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['action']=kwargs['action'].lower()
        if 'name' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['name']=kwargs['name']
        if 'tcp_timeout' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['tcp']['timeout']=kwargs['tcp_timeout']
        if 'udp_timeout' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['udp']['timeout']=kwargs['udp_timeout']
        if 'service' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['service'].update(kwargs['service'])
        if 'schedule' in kwargs.keys():
            dict = {
                'schedule': {
                    'name': kwargs['schedule']
                },
            }
            json_input['access_rules'][0]['ipv4'].update(dict)      
        if 'source_addr' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['source']['address'].update(kwargs['source_addr'])
        if 'dst_addr' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['destination']['address'].update(kwargs['dst_addr'])
        if 'user_included' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['users']['included'] = kwargs['user_included']
        if 'user_excluded' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['users']['excluded'] = kwargs['user_excluded']
        if 'geo_ip_filter' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['geo_ip_filter']['enable'] = kwargs['geo_ip_filter']
        if 'botnet_filter' in kwargs.keys():
            json_input['access_rules'][0]['ipv4']['botnet_filter']= kwargs['botnet_filter']
        if 'priority_mode' in kwargs.keys():
            if kwargs['priority_mode'] == 'manual':
                if 'priority_value' in kwargs.keys():
                    dict = {
                        "priority": {
                            "manual": {
                                "value": kwargs['priority_value']
                            }
                        }
                    }
                    json_input['access_rules'][0]['ipv4'].update(dict)
        
        return json_input

    def del_ipv4_access_rule(self, name):
        #to delete a ipv4 access rule must have it's uuid
        uuid = self.get_ipv4_accessrule_uuid(name)
        logger.info('the custom access-rule {} uuid is: {}'.format(name,uuid))
        url = self.url_v4  + '/uuid/' + uuid
        print(" URL for delete: {}".format(url))
        delete_response = self.fw.api_delete(url)
        return delete_response

    def add_ipv4_access_rule(self, msg=False, **kwargs):
        json_input = self.build_ipv4_access_rule_json(**kwargs)
        response = self.fw.api_post(self.url_v4, msg, data=json_input)
        return response

    def edit_ipv4_access_rule(self, **kwargs):
        uuid = self.get_ipv4_accessrule_uuid(kwargs['name'])
        url = self.url_v4 + '/uuid/' + uuid
        print("PUT JSON to URL: {}".format(url))
        json_input = self.build_ipv4_access_rule_json(**kwargs)
        put_response = self.fw.api_put(url, data=json_input)
        return put_response

    def edit_ipv4_access_rule_uuid(self, uuid, **kwargs):
        url = self.url_v4 + '/uuid/' + uuid
        print("PUT JSON to URL: {}".format(url))
        json_input = self.build_ipv4_access_rule_json(**kwargs)
        put_response = self.fw.api_put(url, data=json_input)
        return put_response

    #Use it to check management
    def show_ipv4_access_rule(self, access_rule):
        url = 'api/sonicos' + '/reporting/access-rules/ipv4'
        print("Get url from: " + url)
        if access_rule == 'https':
            access_rule = 'HTTPS Management'
        elif access_rule == 'http':
            access_rule = 'HTTP Management'
        elif access_rule == 'snmp':
            access_rule = 'SNMP'
        elif access_rule == 'ssh':
            access_rule = 'SSH Management'
        elif access_rule == 'ping':
            access_rule = 'Ping6'
        else:
            logger.info("access rule must be named: https,http,snmp,ssh,ping")
            return False
        json_output = self.fw.api_get(url)
        for item in json_output:
            if item['destination'] == 'X1 Management IPv4 Addresses':
                if item['service'] == access_rule and item['action'] == 'allow':
                    print(item)
                    return True
        print("The access rule {} is not exist".format(access_rule))
        return False

    def get_ipv4_access_rule(self, name):
        uuid = self.get_ipv4_accessrule_uuid(name)
        url = self.url_v4 + '/uuid/' + uuid
        logger.info("GET from URL: {}".format(url))
        json_output = self.fw.api_get(url)
        return json_output

    def get_ipv4_access_rule_by_uuid(self, uuid):
        url = self.url_v4 + '/uuid/' + uuid
        logger.info("GET from URL: {}".format(url))
        json_output = self.fw.api_get(url)
        return json_output

    def get_access_rules(self, version='v4'):
        resp = self.fw.api_get(self.url_v4)
        return resp

    def get_ipv4_accessrule_uuid(self, name):
        policies = self.fw.api_get(self.url_v4)
        for policy in policies['access_rules']:
            if policy['ipv4']['name'] == name:
                uuid = policy['ipv4']['uuid']
        return uuid

    def get_ipv4_access_rule_given_from_to(self, srczone, destzone):
        url = self.url_ipv4 + srczone + '/to/' + destzone
        resp = self.fw.api_get(url)
        return resp

    def del_ipv4_access_rule_uuid(self, uuid, msg=False):
        url = self.url_v4 + '/uuid/' + uuid
        logger.info("URL for delete: {}".format(url))
        delete_response = self.fw.api_delete(url, msg)
        return delete_response


    def add_access_rule_new_block_json(self, uuid, **kwargs):
        url = self.url_v4 + '/uuid/' + uuid
        logger.info("PUT JSON to URL: {}".format(url))
        json_input = copy.deepcopy(kwargs)
        put_response = self.fw.api_put(url, data=json_input)
        return put_response


    def create_access_rule_new_block_json(self,msg=False, **kwargs):
        url = self.url_v4
        logger.info("POST JSON to URL: {}".format(url))
        json_input = copy.deepcopy(kwargs)
        response = self.fw.api_post(url, msg, data=json_input)
        return response

    def edit_ipv4_access_rule_by_uuid(self, uuid, **rule):
        url = self.url_v4 + '/uuid/' + uuid
        print("PUT JSON to URL: {}".format(url))
        put_response = self.fw.api_put(url, data=rule)
        return put_response
