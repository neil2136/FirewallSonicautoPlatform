import copy
import json
from runner.settings import logger
from runner.utils.assertion import Assertion

class AwsConnection():
    
    def __init__(self, fw):
        self.fw = fw
        self.aws_connection= 'api/sonicos/amazon-web-services/connection'
        self.initial_json_aws_connection = {
                    "amazon_web_services": {
                        "connection": {
                            "access_key_id": "",
                            "secret": "6,49a0226fbf5c127952722142c503663f5ae3615c30e8c37f36147638f151e3180b12b035218cfbb2b51a971b02b2e3cf530559eeec14d0c0d90ba8b3aee5dfb62b530e16e1878f87a849abf699e7e2fbe0ff54699c0cf49d578b9bdcf01f8db0",
                            "region": "north-virginia"
                        }
                    }
                }

        
    # Build json for aws connection
    def build_json_aws_connection(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_aws_connection)
        if 'access_id' in kwargs.keys():
            json_input['amazon_web_services']['connection']['access_key_id']= kwargs['access_id']
        if 'password' in kwargs.keys():
            json_input['amazon_web_services']['connection']['secret']= kwargs['password']
        if 'region' in kwargs.keys():
            json_input['amazon_web_services']['connection']['region']= kwargs['region']   
        else:
            logger.error('AWS connections not configured')        
        return json_input

    
    def get_aws_connection(self):
        get_response = self.fw.api_get(self.aws_connection)
        return get_response

    
    def edit_aws_connection(self, msg=False, **kwargs):
        json_input = self.build_json_aws_connection(**kwargs)
        logger.info('the json input build is', json_input)
        aws_conn_resp = self.fw.api_put(self.aws_connection, msg, data=json_input)
        logger.info(aws_conn_resp)
        return aws_conn_resp

    
class AwsObjects():
    
    def __init__(self, fw):
        self.fw = fw
        self.aws_objects= 'api/sonicos/amazon-web-services/objects/base'
        self.del_aws_objects= 'api/sonicos/amazon-web-services/address-objects'
        self.aws_force_sync= 'api/sonicos/amazon-web-services/force-sync'
        self.initial_json_aws_obj = {
                    "amazon_web_services": {
                         "objects": {
                            "mapping": True,
                            "syncronization_interval": 180
                        }
                    }
                }

        
    # Build json for aws connection
    def build_json_aws_objects(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_aws_obj)
        if 'mapping' in kwargs.keys():
            json_input['amazon_web_services']['objects']['mapping']= kwargs['mapping']
        if 'sync_interval' in kwargs.keys():
            json_input['amazon_web_services']['objects']['syncronization_interval']= kwargs['sync_interval']
        if 'monitor_region' in kwargs.keys():
            json_input['amazon_web_services']['objects']['monitor_region']=kwargs['monitor_region']             
        else:
            logger.error('AWS connections not configured')        
        return json_input

    
    def get_aws_objects(self):
        get_response = self.fw.api_get(self.aws_objects)
        return get_response

    
    def edit_aws_objects(self, msg=False, **kwargs):
        json_input = self.build_json_aws_objects(**kwargs)
        logger.info('the json input build is', json_input)
        aws_obj_resp = self.fw.api_put(self.aws_objects, msg, data=json_input)
        logger.info(aws_obj_resp)
        return aws_obj_resp
    
    def delete_aws_objects(self, msg=False):
        del_aws_obj_resp = self.fw.api_delete(self.del_aws_objects, msg)
        return del_aws_obj_resp 
    
    def get_force_sync(self):
        get_response = self.fw.api_get(self.aws_force_sync)
        return get_response
        
        
    
class AwsGroupMapping():
    
    def __init__(self, fw):
        self.fw = fw
        self.aws_group_mapping= 'api/sonicos/amazon-web-services/objects/group-mappings'
        self.initial_json_aws_grp_map = {
                    
                    "amazon_web_services": {
                        "objects": {
                            "group_mapping": [
                                    {
                                        "index": 0,
                                        "address_group": None,
                                        "condition": [
                                                # {
                                                #     "custom_key": {
                                                #             "key": None,
                                                #             "value": None
                                                #         }
                                                # },
                                            {
                                                "instance_property": {
                                                        "key": None,
                                                        "value": None
                                                    }
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }

        
    # Build json for aws connection
    def build_json_aws_grp_mapping(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_aws_grp_map)
        if 'index' in kwargs.keys():
            json_input['amazon_web_services']['objects']['group_mapping'][0]['index']= kwargs['index']
        if 'addr_grp' in kwargs.keys():
            json_input['amazon_web_services']['objects']['group_mapping'][0]['address_group']= kwargs['addr_grp']
        # if 'custom_key' in kwargs.keys():
        #     json_input['amazon_web_services']['objects']['group_mapping'][0]['condition'][0]['custom_key']['key']=kwargs['custom_key']
        # if 'custom_value' in kwargs.keys():
        #     json_input['amazon_web_services']['objects']['group_mapping'][0]['condition'][0]['custom_key']['value']=kwargs['custom_value']
        if 'instance_key' in kwargs.keys():
            json_input['amazon_web_services']['objects']['group_mapping'][0]['condition'][0]['instance_property']['key']=kwargs['instance_key'] 
        if 'instance_value' in kwargs.keys():
            json_input['amazon_web_services']['objects']['group_mapping'][0]['condition'][0]['instance_property']['value']=kwargs['instance_value']                     
        else:
            logger.error('AWS group mapping not configured')        
        return json_input

    
    def get_aws_grp_mapping(self):
        get_response = self.fw.api_get(self.aws_group_mapping)
        return get_response
    
    
    def get_aws_grp_mapping_index(self,index):
        url_index = self.aws_group_mapping + '/' + 'index' + '/'  + index
        get_response = self.fw.api_get(url_index)
        return get_response    

    
    def edit_grp_mapping(self, msg=False, **kwargs):
        json_input = self.build_json_aws_grp_mapping(**kwargs)
        logger.info('the json input build is', json_input)
        aws_mapp_resp = self.fw.api_put(self.aws_group_mapping, msg, data=json_input)
        logger.info(aws_mapp_resp)
        return aws_mapp_resp
    
    def config_grp_mapping(self, msg=False, **kwargs):
        json_input = self.build_json_aws_grp_mapping(**kwargs)
        logger.info('the json input build is', json_input)
        aws_mapp_resp = self.fw.api_post(self.aws_group_mapping, msg, data=json_input)
        logger.info(aws_mapp_resp)
        return aws_mapp_resp
    
    def edit_grp_mapping_index(self, index, msg=False, **kwargs):
        json_input = self.build_json_aws_grp_mapping(**kwargs)
        logger.info('the json input build is', json_input)
        url_index = self.aws_group_mapping + '/' + 'index' + '/'  + index
        aws_index_resp = self.fw.api_put(url_index, msg, data=json_input)
        logger.info(aws_index_resp)
        return aws_index_resp
    
    def delete_aws_mapping_index(self,index,msg=False):
        url_index = self.aws_group_mapping + '/' + 'index' + '/'  + index
        del_aws_index_resp = self.fw.api_delete(url_index, msg)
        return del_aws_index_resp 
    
