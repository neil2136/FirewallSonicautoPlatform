import copy
import json
import re
from pprint import pprint
import requests
from collections import OrderedDict
from datetime import datetime, timezone
import subprocess
#from util.snwl_logging import logger
#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)
from runner.settings import logger


class EmailObjectApi:
    '''Email Object Api class'''
    default_options = {
            'name': '',
            'match_type': 'exact',
            'content_entry': [],
        }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/email-objects'
        self.initial_email_object_json = {
                    "email_objects": [
                        {
                            "name": "", 
                            "match_type": "", 
                            "content_entry": [
                                {
                                    "content_entry": ""
                                }
                            ]
                        }
                    ]
                }

    def get_all_email_object(self):
        out = self.fw.api_get(self.url)
        return out
    
    def add_email_object(self, msg=False, **kwargs):
        self.options = dict(EmailObjectApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options        
        json_input = self.build_json_email(**kwargs)
        emailobject_resp = self.fw.api_post(self.url, msg, data=json_input)
        return emailobject_resp

    def delete_email_object(self, msg=False, **kwargs):
        self.options = dict(EmailObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_email(**kwargs)
        emailobject_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return emailobject_resp

    def delete_email_object_by_name(self, name):
        url = self.url + '/name/' + name
        emailobject_resp = self.fw.api_delete(url)
        return emailobject_resp

    def get_email_object(self, name):
        url = self.url + '/name/' + name
        emailobject_resp = self.fw.api_get(url)
        return emailobject_resp

    def edit_email_object(self, msg=False, **kwargs):
        self.options = dict(EmailObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_email(**kwargs)
        emailobject_resp = self.fw.api_put(self.url, msg, data=json_input)
        return emailobject_resp

    def build_json_email(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_email_object_json)
            json_input['email_objects'][0]['name'] = kwargs['name']
            json_input['email_objects'][0]['match_type'] = kwargs['match_type']
            content = []
            for entry in kwargs['content_entry']:
                tmp = {'content_entry': entry}
                content.append(tmp)
            json_input['email_objects'][0]['content_entry'] = content
            logger.info('email object json!')
            logger.info(json_input)
        except KeyError as e :
            logger.error('Error: In creating JSON for email object',e)
        return json_input


class ActionObjectApi:
    '''Action Object Api class'''
    default_options = {
           'name': '',
           'action': '',
           'content': '',
           'color': ''
        }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/action-objects'
        self.initial_action_object_json = {
            'action_objects':[ {
                'name': '',
                'action': '',
                'content': ''
            }]
        }


    def add_action_object(self, msg=False, **kwargs):
        self.options = dict(ActionObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_action(**kwargs)
        actionobject_resp = self.fw.api_post(self.url, msg, data=json_input)
        return actionobject_resp

    def delete_action_object(self, msg=False, **kwargs):
        self.options = dict(ActionObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_action(**kwargs)
        actionobject_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return actionobject_resp
        
    def delete_action_object_by_name(self, name):
        url = self.url + '/name/' + name
        actionobject_resp = self.fw.api_delete(url)
        return actionobject_resp

    def get_action_object(self, name):
        url = self.url + '/name/' + name
        actionobject_resp = self.fw.api_get(url)
        return actionobject_resp

    def edit_action_object(self, msg=False, **kwargs):
        self.options = dict(ActionObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_action(**kwargs)
        actionobject_resp = self.fw.api_put(self.url, msg, data=json_input)
        return actionobject_resp

    def build_json_action(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_action_object_json)
            json_input['action_objects'][0]['name'] = kwargs['name']
            json_input['action_objects'][0]['action'] = kwargs['action']
            json_input['action_objects'][0]['content'] = kwargs['content']
            if 'color' in kwargs.keys():
                if kwargs['action'] == 'http-block-page':
                    json_input['action_objects'][0]['color'] = kwargs['color']
                else:
                    logger.error('parameter color can only specified for action http-block-page')
            if kwargs['action'] == 'bandwidth-management':
                del json_input['action_objects'][0]['content']
                json_input['action_objects'][0]['bandwidth_management'] = {}
                json_input['action_objects'][0]['bandwidth_management']['egress'] = {}
                json_input['action_objects'][0]['bandwidth_management']['ingress'] = {}
                if 'aggregation_method' in kwargs.keys():
                    json_input['action_objects'][0]['bandwidth_management']['aggregation_method'] = kwargs['aggregation_method']
                if 'usage_tracking' in kwargs.keys():
                    json_input['action_objects'][0]['bandwidth_management']['usage_tracking'] = kwargs['usage_tracking']
                if 'bw_egress_object' in kwargs.keys():
                    json_input['action_objects'][0]['bandwidth_management']['egress']['bandwidth_object'] = kwargs['bw_egress_object']
                if 'bw_ingress_object' in kwargs.keys():
                    json_input['action_objects'][0]['bandwidth_management']['ingress']['bandwidth_object'] = kwargs['bw_ingress_object']
                if 'bw_egress_priority' in kwargs.keys():
                    json_input['action_objects'][0]['bandwidth_management']['egress']['priority'] = kwargs['bw_egress_priority']
                if 'bw_ingress_priority' in kwargs.keys():
                    json_input['action_objects'][0]['bandwidth_management']['ingress']['priority'] = kwargs['bw_ingress_priority']
            logger.info('action object json!')
            logger.info(json_input)
        except KeyError:
            logger.error('Error: In creating JSON for action object')
        return json_input



class BandwidthObjectApi:
    '''Bandwidth Object Api class'''
    default_options = {
        'name': '',
        'guaranteed': {},
        'maximum': {},
        'priority': 'realtime',
        'action': 'delay',
        'comment': 'delayed',
        'per_ip_management': {}
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/bandwidth-objects'
        self.initial_bandwidth_object_json = {
            'bandwidth_objects': []
        }

    def add_bandwidth_object(self, msg=False, **kwargs):
        self.options = dict(BandwidthObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_bandwidth(**kwargs)
        bandwidthobject_resp = self.fw.api_post(self.url, msg, data=json_input)
        return bandwidthobject_resp

    def delete_bandwidth_object(self, msg=False, **kwargs):
        self.options = dict(BandwidthObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_bandwidth(**kwargs)
        bandwidthobject_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return bandwidthobject_resp

    def get_bandwidth_object(self, name):
        url = self.url + '/name/' + name
        bandwidthobject_resp = self.fw.api_get(url)
        return bandwidthobject_resp

    def edit_bandwidth_object(self, msg=False, **kwargs):
        options = dict(BandwidthObjectApi.default_options)
        options.update(kwargs)
        json_input = self.build_json_bandwidth(**options)
        bandwidthobject_resp = self.fw.api_put(self.url, msg, data=json_input)
        return bandwidthobject_resp

    def build_json_bandwidth(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_bandwidth_object_json)
            json_input['bandwidth_objects'].append(kwargs)
        except KeyError:
            logger.error('Error: In creating JSON for bandwidth object')
        return json_input


class AppRuleApi:
    '''App Rule Object Api class'''
    default_options = {
        'name': '',
        'type': {},
        'source': {
            'address': {},
            'service': {}
        },
        'destination': {
            'address': {},
            'service': {}
        },
        'exclusion': {
            'address': {}
        },
        'match_object': {
            'object': ''
        },
        'users': {
            'included': {},
            'excluded': {}
        },
        'schedule': {
            'always_on': True
        },
        'flow_reporting': False,
        'connection_side': '',
        'logging': False,
        'log': {
            'redundancy': {
                'global': True
            }
        },
        'direction': {
            'basic': 'incoming'
        }

    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/app-rules/policies'
        self.url_base = 'api/sonicos/app-rules/base/'
        self.initial_apprule_object_json = {
            'app_rules': {
                'policy': [{
                    'name': '',
                    'type': {},
                    'source': {
                    },
                    'destination': {
                    },
                    'address': {},
                    'exclusion': {
                        'address': {}  #can be empty
                    },
                    'match_object': {
                        'included': '',
                        'excluded': '',
                    },
                    'users': {
                        'included': {},  #can not be empty
                        'excluded': {}   #can be empty
                    },
                    'mail_from': {},  # only for smtpcliet
                    'rcpt_to': {},  # only for smtpcliet
                    'schedule': {
                        'always_on': True
                    },  # schedule is not must ,default is always_on
                    'connection_side': '',  # connection_side is not must , once type is specified, it is specified
                    'flow_reporting': False,  #flow_reporting is not must
                    'logging': False,
                    'log': {
                        'individual': False,
                        'redundancy': {
                            'global': True
                        }
                    },  # log is not must
                    'direction': {
                        'basic': 'incoming'
                    } # direction
                }]
            }
        }

    def config_apprule_setting(self, msg=False, **kwargs):
        setting_json = {
            'app_rules': {
                'enable': 'True',
                'log_redundancy': ''
            }
        }
        if 'enable' in kwargs.keys():
            setting_json['app_rules']['enable'] = kwargs['enable']
        if 'log_redundancy' in kwargs.keys():
            setting_json['app_rules']['log_redundancy'] = kwargs['log_redundancy']
        app_setting_resp = self.fw.api_put(self.url_base, msg, data=setting_json)
        return app_setting_resp

    def get_apprule_setting(self):
        app_setting_resp = self.fw.api_get(self.url_base)
        return app_setting_resp

    def add_apprule_object(self, msg=False, **kwargs):
        ''' Example:
        apprule_dict ={
            "name": "http",
            "type": {
                "http": 'client',
            },
            "source": {
                "address": {
                    "any": True
                },
                "service": {
                    "any": True
                }
            },
            "destination": {
                "address": {
                    "any": True
                },
                "service": {
                    "name": "HTTP"
                }
            },
            "exclusion": {
                "address": {}
            },
            "match_object": {
                "included": "TC02",
                "excluded": ""
            },
            "action_object": "http_block_page",
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {}
            },
            "schedule": {
                "always_on": True
            },
            "flow_reporting": False,
            "logging": True,
            "log": {
                "redundancy": {
                    "global": True
                }
            },
            "app_control_message_format": True,
            "connection_side": "client",
            "direction": {
                "basic": "both"
            }
        }
        '''
        options = dict(AppRuleApi.default_options)
        options.update(kwargs)
        json_input = self.build_json_apprule(**options)
        bandwidthobject_resp = self.fw.api_post(self.url, msg, data=json_input)
        return bandwidthobject_resp

    def delete_apprule_object(self, msg=False, **kwargs):
        options = dict(AppRuleApi.default_options)
        options.update(kwargs)
        json_input = self.build_json_apprule(**options)
        appruleobject_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return appruleobject_resp

    def delete_apprule_object_byname(self, name):
        url = self.url + '/name/' + name
        appruleobject_resp = self.fw.api_delete(url)
        return appruleobject_resp

    def get_apprule_object(self, name):
        url = self.url + '/name/' + name
        appruleobject_resp = self.fw.api_get(url)
        return appruleobject_resp

    def edit_apprule_object(self, msg=False, **kwargs):
        options = dict(AppRuleApi.default_options)
        options.update(kwargs)
        json_input = self.build_json_apprule(**options)
        appruleobject_resp = self.fw.api_put(self.url, msg, data=json_input)
        return appruleobject_resp

    def build_json_apprule(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_apprule_object_json)
            json_input['app_rules']['policy'][0]['name'] = kwargs['name']
            json_input['app_rules']['policy'][0]['type'] = kwargs['type']
            # source include address and service
            json_input['app_rules']['policy'][0]['source'] = kwargs['source']
            # destination include address and service
            json_input['app_rules']['policy'][0]['destination'] = kwargs['destination']
            json_input['app_rules']['policy'][0]['match_object'] = kwargs['match_object']
            json_input['app_rules']['policy'][0]['action_object'] = kwargs['action_object']
            json_input['app_rules']['policy'][0]['users'] = kwargs['users']

            # not must, have default value
            json_input['app_rules']['policy'][0]['exclusion'] = kwargs['exclusion']
            json_input['app_rules']['policy'][0]['schedule'] = kwargs['schedule']
            json_input['app_rules']['policy'][0]['flow_reporting'] = kwargs['flow_reporting']
            json_input['app_rules']['policy'][0]['logging'] = kwargs['logging']
            json_input['app_rules']['policy'][0]['log'] = kwargs['log']
            json_input['app_rules']['policy'][0]['connection_side'] = kwargs['connection_side']
            json_input['app_rules']['policy'][0]['direction'] = kwargs['direction']

            # set ips_message_format for ips type
            if 'ips' in kwargs['type'].keys():
                if 'ips_message_format' in kwargs.keys():
                    json_input['app_rules']['policy'][0]['ips_message_format'] = kwargs['ips_message_format']

            # set app_control_message_format for app control type
            if 'app_control' in kwargs['type'].keys():
                if 'app_control_message_format' in kwargs.keys():
                    json_input['app_rules']['policy'][0]['app_control_message_format'] = kwargs['app_control_message_format']

            # only smtpclient type have mail_from and rcpt_to parameter
            if 'mail_from' in kwargs.keys() and 'smtp_client' in kwargs['type'].keys():
                json_input['app_rules']['policy'][0]['mail_from'] = kwargs['mail_from']
            else:
                del json_input['app_rules']['policy'][0]['mail_from']
            if 'rcpt_to' in kwargs.keys() and kwargs['type']['smtp_client']:
                json_input['app_rules']['policy'][0]['rcpt_to'] = kwargs['rcpt_to']
            else:
                del json_input['app_rules']['policy'][0]['rcpt_to']

            # delete address paramter for
            if 'ips' not in kwargs['type'].keys():
                del json_input['app_rules']['policy'][0]['address']
            # for ips type
            if 'ips' in kwargs['type'].keys():
                del json_input['app_rules']['policy'][0]['connection_side']
                del json_input['app_rules']['policy'][0]['direction']
                del json_input['app_rules']['policy'][0]['source']
                del json_input['app_rules']['policy'][0]['destination']
                json_input['app_rules']['policy'][0]['address'] = kwargs['address']
                if 'zone' in kwargs.keys():
                    json_input['app_rules']['policy'][0]['zone'] = kwargs['zone']
            # for appcontrol type
            if 'app_control' in kwargs['type'].keys():
                del json_input['app_rules']['policy'][0]['connection_side']
                del json_input['app_rules']['policy'][0]['direction']
                if 'zone' in kwargs.keys():
                    json_input['app_rules']['policy'][0]['zone'] = kwargs['zone']

        except KeyError:
            logger.error('Error: In creating JSON for app rule object')
        return json_input


#edit by cyuan
class AppControlApi:
    '''App control Object Api class'''

    #delete init json
    def __init__(self, fw):
        self.fw = fw

    def config_appcontrol_global(self, msg=False, **kwargs):
        setting_json = {
            "app_control": {
                "enable": False,
                "log_all": False,
                "log_filename": False,
                "log_redundancy": {
                    "filter": {'value': 60}
                }
            }
        }
        url = 'api/sonicos/app-control/base'
        if 'enable' in kwargs.keys():
            setting_json['app_control']['enable'] = kwargs['enable']
        if 'log_all' in kwargs.keys():
            setting_json['app_control']['log_all'] = kwargs['log_all']
        if 'log_filename' in kwargs.keys():
            setting_json['app_control']['log_filename'] = kwargs['log_filename']
        if 'log_redundancy' in kwargs.keys():
            setting_json['app_control']['log_redundancy']['filter']['value'] = kwargs['log_redundancy']
        app_setting_resp = self.fw.api_put(url, msg, data=setting_json)
        return app_setting_resp

    # new add config appcontrol global setting, not build json, from FW get
    def config_appcontrol_global_settings(self, msg=False, **kwargs):
        setting_json = self.get_appcontrol_setting()
        url = 'api/sonicos/app-control/base'
        setting_json['app_control'].update(kwargs)
        app_setting_resp = self.fw.api_put(url, msg, data=setting_json)
        return app_setting_resp

    # change api_put to post, because this not support for put
    def reset_appcontrol_setting(self):
        url = 'api/sonicos/app-control/reset'
        app_setting_resp = self.fw.api_post(url)
        return app_setting_resp

    def get_appcontrol_category_byid(self, id=0):
        url = 'api/sonicos/app-control/categories/id/'+str(id)
        resp = self.fw.api_get(url)
        return resp

    # remove build_json, get json from FW get
    def config_ac_by_category(self, msg=False, **kwargs):
        url = 'api/sonicos/app-control/categories'
        json_input = self.get_appcontrol_category_byid(kwargs['id'])
        json_input['app_control']['category'][0].update(**kwargs)
        appcontrolobject_resp = self.fw.api_put(url, msg, data=json_input)
        return appcontrolobject_resp
    
    #by_application and by_signature no get method, need complete json
    def config_ac_by_application(self, msg=False, **app_json):
        url = 'api/sonicos/app-control/applications'
        appcontrolobject_resp = self.fw.api_put(url, msg, data=app_json)
        return appcontrolobject_resp

    def config_ac_by_signature(self, msg=False, **sig_json):
        url = 'api/sonicos/app-control/signatures'
        appcontrolobject_resp = self.fw.api_put(url, msg, data=sig_json)
        return appcontrolobject_resp

    # change build json to get json from FW
    def config_ac_exclusion(self, msg=False, **kwargs):
        exclusion_json = self.get_appcontrol_exlusion_list()
        url = 'api/sonicos/app-control/exclusion-list'
        if "ips" in kwargs.keys():
            exclusion_json['app_control']['exclusion']['list']['ips'] = True
        elif "object_name" in kwargs.keys():
            exclusion_json['app_control']['exclusion']['list']['object'] = {}
            exclusion_json['app_control']['exclusion']['list']['object']['name'] = kwargs['object_name']
        elif "object_group" in kwargs.keys():
            exclusion_json['app_control']['exclusion']['list']['object'] = {}
            exclusion_json['app_control']['exclusion']['list']['object']['group'] = kwargs['object_group']
        appcontrolobject_resp = self.fw.api_put(url, msg, data=exclusion_json)
        return appcontrolobject_resp
    

    def get_appcontrol_setting(self):
        url = 'api/sonicos/app-control/base'
        app_setting_resp = self.fw.api_get(url)
        return app_setting_resp

    # new add
    def get_appcontrol_category_by_name(self, name):
        url = 'api/sonicos/app-control/categories/name/'+name
        ac_category_resp_by_name = self.fw.api_get(url)
        return ac_category_resp_by_name

    # new add
    def get_appcontrol_category_by_id(self, id):
        url = 'api/sonicos/app-control/categories/id/'+id
        ac_category_resp_by_id = self.fw.api_get(url)
        return ac_category_resp_by_id

    # new add
    def get_appcontrol_exlusion_list(self):
        url = 'api/sonicos/app-control/exclusion-list'
        resp = self.fw.api_get(url)
        return resp

    # new add
    def get_appcontrol_categories(self):
        url = 'api/sonicos/app-control/categories'
        resp = self.fw.api_get(url)
        return resp

    def get_appcontrol_status(self):
        url = "api/sonicos/reporting/app-control"
        resp = self.fw.api_get(url)
        return resp

    def get_ac_application_by_name(self, name):
        if not name:
            logger.error("Please input the correct application name")
            return ""
        url = f"api/sonicos/app-control/applications/name/{name}"
        resp = self.fw.api_get(url)
        return resp

    def get_all_signature_info(self):
        db_time = self.get_appcontrol_status().get("signature_database_timestamp")
        if not db_time:
            logger.error("Get invalid database timestamp in app control status")
            return ""
        dt = datetime.strptime(db_time, "UTC %m/%d/%Y %H:%M:%S.%f")
        ts = round(dt.replace(tzinfo=timezone.utc).timestamp())
        logger.info(f"Get DB timestamp: {ts}")
        url = f"api/sonicos/dynamic-file/getAllSigArray.json?appTs={ts}"
        resp = self.fw.api_get(url)
        return resp


class MatchobjectApi:
    '''Matchobject class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/match-objects'
        self.initial_matchobject_json =  {
            'match_objects': [
                {            
                    'name': '' ,
                }
            ]
        }

    def config_matchobject(self, msg=False, **kwargs):
        json_input = self.build_json_matchobject(**kwargs)
        matchobj_resp = self.fw.api_post(self.url, msg, data=json_input) 
        return matchobj_resp      
       
    def build_json_matchobject(self,**kwargs):
        match_object_type_list1 = ['activex-class-id','email-body','http-uri-content','http-url','file-content']
        match_object_type_list2 = ['email-cc','email-from','email-subject','email-to','file-extension','file-name','http-cookie','http-host','http-referer','http-set-cookie','http-user-agent']
        match_object_type_list3 = ['email-size']
        match_object_type_list4 = ['ftp-command']
        match_object_type_list5 = ['ftp-command-value']
        match_object_type_list6 = ['mime-custom-header','http-request-custom-header', 'http-response-custom-header']
        match_object_type_list7 = ['web-browser']
        match_object_type_list8 = ['ips-signature-category-list','ips-signature-list']
        match_object_type_list9 = ['application-category-list']
        match_object_type_list10 = ['application-list']
        match_object_type_list11 = ['application-signature-list']
        match_object_type_list12 = ['log-email-user']
        match_object_type_list13 = ['custom']
        match_object_all_types = ['activex-class-id','email-body','email-cc','email-from','email-subject','email-to','email-size','file-extension','file-content','file-name','ftp-command','http-cookie','http-host','http-referer','http-set-cookie','http-uri-content','http-url','http-user-agent','file-content','ftp-command-value','mime-custom-header','http-request-custom-header', 'http-response-custom-header','web-browser','ips-signature-category-list','ips-signature-list','application-category-list','application-list','application-signature-list','log-email-user','custom']

        json_input = {}
        object_type = kwargs.get('object_type', '').lower()
        #the match object types which have most of their keys common
        if object_type in  match_object_all_types:
            logger.info('The passed Match Object type is of valid object type')
            json_input = copy.deepcopy(self.initial_matchobject_json)
            try:
                logger.info('Building the JSON')
                json_input['match_objects'][0]['name']=kwargs['name']
                json_input['match_objects'][0]['type']=kwargs['object_type']
            except KeyError as ke:
                logger.error('Key Error Missing the below key in Matchobjects','error')
                logger.error(ke)
            if object_type in match_object_type_list1 or object_type in match_object_type_list2 or object_type in match_object_type_list6 or object_type in match_object_type_list13:
                try:
                    json_input['match_objects'][0]['match_type'] =kwargs['match_type']
                    json_input['match_objects'][0]['input_representation']=kwargs['input_representation']
                    json_input['match_objects'][0]['content_entry']=kwargs['content_entry']
                    if 'pre_defined_regex' in kwargs:
                        json_input['match_objects'][0]['pre_defined_regex']=kwargs['pre_defined_regex']
                    if object_type in match_object_type_list2 or object_type in match_object_type_list6:
                        try:
                            if 'negative_matching' in kwargs.keys():
                                json_input['match_objects'][0]['negative_matching']=kwargs['negative_matching']
                            else:
                                raise KeyError
                        except KeyError as ke:
                            logger.error(ke)
                    if object_type in match_object_type_list6:
                        json_input['match_objects'][0]['custom_header']=kwargs['custom_header']
                    elif object_type in match_object_type_list13:
                        try:
                            if 'enable' in kwargs.keys():
                                json_input['match_objects'][0]['enable']=kwargs['enable']
                            else:
                                raise KeyError
                        except KeyError as ke:
                            logger.error(ke)
                        if kwargs['enable']:
                            try:
                                if kwargs['offset'] and kwargs['depth'] and kwargs['min_size'] and kwargs['max_size']:
                                    json_input['match_objects'][0]['offset']=kwargs['offset']
                                    json_input['match_objects'][0]['depth']=kwargs['depth']
                                    json_input['match_objects'][0]['min_size']=kwargs['min_size']
                                    json_input['match_objects'][0]['max_size']=kwargs['max_size']
                                else:
                                    raise KeyError
                            except KeyError as ke:
                                logger.error(ke)
                except KeyError as ke:
                    logger.error('Key Error missing the below key of Matchobjects','error')
                    logger.error(ke)
            elif object_type in match_object_type_list3:
                try:
                    if 'email_size' in kwargs.keys():
                        json_input['match_objects'][0]['email_size']=kwargs['email_size']   
                    else:
                        raise KeyError('Missing emailsize key')
                except KeyError as ke:
                    logger.error(ke)

            elif object_type in match_object_type_list4:
                try:
                    json_input['match_objects'][0]['ftp_command']=kwargs['ftp_command']
                except KeyError as ke:
                    logger.error('Key error: Missing the below key under Matchobjects','error')
                    logger.error(ke)                
            elif object_type in match_object_type_list5:
                try:
                    json_input['match_objects'][0]['match_type'] =kwargs['match_type']
                    json_input['match_objects'][0]['negative_matching']=kwargs['negative_matching']
                    json_input['match_objects'][0]['input_representation']=kwargs['input_representation']
                    json_input['match_objects'][0]['ftp_command']=kwargs['ftp_command']
                    json_input['match_objects'][0]['argument']=kwargs['argument']
                except KeyError as ke:
                    logger.error('Key error: Missing the below key under Matchobjects','error')
                    logger.error(ke)                
            elif object_type in match_object_type_list7:
                try:
                    json_input['match_objects'][0]['negative_matching']=kwargs['negative_matching']
                    json_input['match_objects'][0]['browser']=kwargs['browser']
                except KeyError as ke:
                    logger.error('Key error: Missing the below key under Matchobjects','error')
                    logger.error(ke)                
            elif object_type in match_object_type_list8:
                try:
                    json_input['match_objects'][0]['ips']=kwargs['ips']
                except KeyError as ke:
                    logger.error('Key error: Missing the below key under Matchobjects','error')
                    logger.error(ke)                
            elif object_type in match_object_type_list9:
                try:
                    json_input['match_objects'][0]['category']=kwargs['category']
                except KeyError as ke:
                    logger.error('Key error: Missing the below key under Matchobjects','error')
                    logger.error(ke)                
            elif object_type in match_object_type_list10:
                try:
                    json_input['match_objects'][0]['application']=kwargs['application']
                except KeyError as ke:
                    logger.error('Key error: Missing the below key under Matchobjects','error')
                    logger.error(ke)                
            elif object_type in match_object_type_list11:
                try:
                    json_input['match_objects'][0]['signature']=kwargs['signature']
                except KeyError as ke:
                    logger.error('Key error: Missing the below key under Matchobjects','error')
                    logger.error(ke)                
            elif object_type in match_object_type_list12:
                pass
            else:
                json_input = {'Error': 'Invalid address object type entered'}
        else:
            logger.info('Not a valid object type')
        return json_input

      
    def edit_match_object(self,json_put_match_object, msg=False):
        put_match_resp = self.fw.api_put(self.url, msg, data=json_put_match_object) 
        return put_match_resp
  
    def get_matchobject(self):
        get_response=self.fw.api_get(self.url)
        return get_response

    def delete_match_object(self, name):
        if name:
            del_url = self.url + '/name/' + name
        else:
            logger.error('name should be specified to delete match_object.')
            return False
        resp = self.fw.api_delete(del_url)
        return resp
        
    def edit_match_object_by_name(self, names=None, **kwargs):
        json_input = self.build_json_matchobject(**kwargs)
        url = self.url + '/name/' + names
        put_match_resp = self.fw.api_put(url, data=json_input)
        return put_match_resp
        
    def del_match_object_by_name(self, name,msg=False):
        url = self.url + '/name/'+ name
        delmatchobj_resp = self.fw.api_delete(url)
        return delmatchobj_resp
    
    #def del_matchobject(self, msg=False):
    #    delmatchobj_resp = self.fw.api_delete(self.url) 
    #    return delmatchobj_resp

    def get_matchobject_by_name(self,name):
        url = self.url + '/name/'+ name
        get_response=self.fw.api_get(url)
        return get_response


class CfoObjectApi():
    '''CfoGroupApi'''
    default_options = {
        'name': None

     }

    def __init__(self, fw):
        self.fw = fw
        self.uri_list_object = 'api/sonicos/content-filter/uri-list-objects'
        self.initial_cfo_object_json ={
             'content_filter': {
                'uri_list_object': [
                    {
                        'name': '',
                        'type':'',
                        "uri": [],
                        "keyword":[],
                        "domain": [],
                    }
                ]
             }

        }


    def build_json_cfo_object(self, **kwargs):
        json_input = {}
        tmp_input = {'uri': ''}
        tmp_inp= {'keyword': ''}
        tmp_domain = {'domain': ''}
        json_input = copy.deepcopy(self.initial_cfo_object_json)
        #temp_obj=0
        if 'object_name' in kwargs.keys():
            json_input['content_filter']['uri_list_object'][0]['name']= kwargs['object_name']
        if 'url_name' in kwargs:
            for val in kwargs['url_name']:
                tmp_input['uri'] = val
                json_input['content_filter']['uri_list_object'][0]['type'] ='uri'
                json_input['content_filter']['uri_list_object'][0]['uri'].append(copy.deepcopy(tmp_input))
        if 'keyword' in kwargs:
            for val_key in kwargs['keyword']:
                tmp_inp['keyword'] = val_key
                json_input['content_filter']['uri_list_object'][0]['type'] = 'keyword'
                json_input['content_filter']['uri_list_object'][0]['keyword'].append(copy.deepcopy(tmp_inp))
                logger.info(json_input)
        if 'domain' in kwargs:
            for val_key in kwargs['domain']:
                tmp_domain['domain'] = val_key
                json_input['content_filter']['uri_list_object'][0]['type'] = 'domain'
                json_input['content_filter']['uri_list_object'][0]['domain'].append(copy.deepcopy(tmp_domain))
                logger.info(json_input)
        # else:
        #     logger.error("Error while configuring object")
        return json_input

    def get_cfo_object(self, name=None):
        if name:
            url = self.uri_list_object + '/name/' + name
        else:
            url = self.uri_list_object
        get_response = self.fw.api_get(url)
        return get_response

    def configure_cfo_object(self, msg=False, **kwargs):
        self.options = dict(CfoObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cfo_object(**kwargs)
        post_resp = self.fw.api_post(self.uri_list_object, msg, data=json_input)
        return post_resp

    def edit_cfo_object(self, msg=False, **kwargs):
        self.options = dict(CfoObjectApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cfo_object(**kwargs)
        post_resp = self.fw.api_put(self.uri_list_object, msg, data=json_input)
        return post_resp
    
    def add_cfo_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        app_setting_resp = self.fw.api_post(self.uri_list_object, msg, data=json_input)
        return app_setting_resp
    

    def import_cfo_object(self, type, name, file, msg=False):
        if type == 'keyword':
            url = 'api/sonicos/import/content-filter/uri-list-object/keywords/name/' + name
        elif type == 'uri':
            url = 'api/sonicos/import/content-filter/uri-list-object/uris/name/' + name
        url = 'https://' + self.fw.ip + '/' + url
        self.fw.api_login()
        curl_command = ['curl', '-k', '-i', '-H', "'Content-Type: application/json' ", '-X', 'PUT', '--data-binary',
                        '@' + file,
                        url]
        logger.info('--------curl command:')
        logger.info(curl_command)
        upload_resp = subprocess.Popen(curl_command, stdout=subprocess.PIPE).communicate()[0]
        rc = self.fw.api_post_pendingchanges()
        logger.info(upload_resp)
        return rc
        
    def delete_cfo_object(self, name):
        url = self.uri_list_object + '/name/' + name
        post_resp = self.fw.api_delete(url)
        return post_resp

class CfoGroupApi():
    '''CfoGroupApi'''
    default_options = {
        'name': None
     }

    def __init__(self, fw):
        self.fw = fw
        self.uri_list_group = 'api/sonicos/content-filter/uri-list-groups'
        self.initial_cfo_group_json ={
             'content_filter': {
                'uri_list_group': [
                    {
                        'name': '',
                        'uri_list_object': []
                    }
                ]
             }

        }

    def build_json_cfo_group(self, **kwargs):
        json_input = {}
        tmp_input = {'name': ''}
        json_input = copy.deepcopy(self.initial_cfo_group_json)
        #temp_obj=0
        if 'grp_name' in kwargs.keys():
            json_input['content_filter']['uri_list_group'][0]['name']= kwargs['grp_name']
        if 'obj_name' in kwargs:
            temp=0
            for val in kwargs['obj_name']:
                tmp_input['name'] = val
                json_input['content_filter']['uri_list_group'][0]['uri_list_object'].append(copy.deepcopy(tmp_input))
                temp +=1
            logger.info("Group added sucessfully")
        else:
            logger.error("Error while configuring the group")
        return json_input

    def get_cfo_group(self, name=None):
        if name:
            url = self.uri_list_group + '/name/' + name
        else:
            url = self.uri_list_group
        get_response = self.fw.api_get(url)
        return get_response

    def configure_cfo_group(self, msg=False, **kwargs):
        self.options = dict(CfoGroupApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cfo_group(**kwargs)
        logger.info(json_input)
        post_resp = self.fw.api_post(self.uri_list_group, msg, data=json_input)
        return post_resp

    def edit_cfo_group(self, msg=False, **kwargs):
        self.options = dict(CfoGroupApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cfo_group(**kwargs)
        put_resp = self.fw.api_put(self.uri_list_group,msg,data=json_input)
        return put_resp

    def delete_cfo_group(self, name):
        url = self.uri_list_group + '/name/' + name
        post_resp = self.fw.api_delete(url)
        return post_resp


class CfoActionApi():
    '''CfoActionApi'''
    default_options = {
        'name': 'CFS Default Action',
        'wipe_cookies': False,
        'flow_reporting': True,
        'block':{'page':{'default':True}},
        'passphrase':{
            'password':None,
            'active_time':60,
            'psge':{'default':True}
        },
        'confirm':{
            "active_time": 60,
            "page": {
                "default": True
            }
        }

     }

    def __init__(self, fw):
        self.fw = fw
        self.uri_list_action = 'api/sonicos/content-filter/actions'
        self.initial_cfo_action_json ={
            'content_filter': {
                'action': [
                {
                    'name': None,
                    'wipe_cookies': False,
                    'flow_reporting': True,
                    'block': {
                        'page': {
                            'default': True
                        }
                    },
                    'passphrase': {
                        'password': None,
                        'active_time': None,
                        'page': {
                            'default': True
                        }
                    },
                    'confirm': {
                        'active_time': None,
                        'page': {
                            'default': True
                        }
                    }
                }
            ]
        }
    }
        
    def build_json_cfo_action(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_cfo_action_json)
        if 'action_name' in kwargs.keys():
            json_input['content_filter']['action'][0]['name']= kwargs['action_name']
        if 'wipe_cookies' in kwargs.keys():
            json_input['content_filter']['action'][0]['wipe_cookies']= kwargs['wipe_cookies']
        if 'flow_reporting' in kwargs.keys():
            json_input['content_filter']['action'][0]['flow_reporting'] = kwargs['flow_reporting']
        if 'default_block' in kwargs.keys():
            json_input['content_filter']['action'][0]['block']['page']['default'] = kwargs['default_block']
        if 'password' in kwargs.keys():
            json_input['content_filter']['action'][0]['passphrase']['password'] = kwargs['password']
        if 'pass_active_time' in kwargs.keys():
            json_input['content_filter']['action'][0]['passphrase']['active_time'] = kwargs['pass_active_time']
        if 'pass_page_custom' in kwargs.keys():
            json_input['content_filter']['action'][0]['passphrase']['page']['custom'] = kwargs['pass_page_custom']
            # default will still exist and cover custom passphrase page if you do not delete it
            del json_input['content_filter']['action'][0]['passphrase']['page']['default']
        if 'confirm_active_time' in kwargs.keys():
            json_input['content_filter']['action'][0]['confirm']['active_time'] = kwargs['confirm_active_time']
        if 'confirm_page_custom' in kwargs.keys():
            json_input['content_filter']['action'][0]['confirm']['page']['custom'] = kwargs['confirm_page_custom']
        if 'pass_pagecustom' in kwargs.keys():
            json_input['content_filter']['action'][0]['passphrase']['page']['custom'] = kwargs['pass_pagecustom']
        logger.info(json_input)
        return json_input

    def get_cfo_action(self, name=None):
        if name:
            url = self.uri_list_action + '/name/' + name
        else:
            url = self.uri_list_action
        get_response = self.fw.api_get(url)
        return get_response

    def configure_cfo_action(self, msg=False, **kwargs):
        self.options = dict(CfoActionApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cfo_action(**kwargs)
        post_resp = self.fw.api_post(self.uri_list_action, msg, data=json_input)
        return post_resp

    def add_cfo_action(self, msg=False, **kwargs):
        url = 'api/sonicos/content-filter/actions'
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        cfo_action = self.fw.api_post(url, msg, data=json_input)
        return cfo_action
    
    def edit_cfo_action_by_name(self, name, msg=False, **kwargs):
        if not name:
            logger.info('pls enter action name...')
            return False
        else:
            url = self.uri_list_action + '/name/' + name
            json_input = copy.deepcopy(kwargs)
            logger.info(json_input)
            edit_cfo_action_resp = self.fw.api_put(url, msg, data=json_input)
            return edit_cfo_action_resp

    def edit_cfo_action(self, msg=False, **kwargs):
        self.options = dict(CfoActionApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cfo_action(**kwargs)
        put_resp = self.fw.api_put(self.uri_list_action,msg,data=json_input)
        return put_resp
    
    def del_cfo_action(self,name,msg=False):
        if not name:
            logger.info('pls enter action name...')
            return False
        else:
            url = self.uri_list_action + '/name/' + name
            resp = self.fw.api_delete(url,msg)
            return resp
    
    
class CfoProfilesApi():
    '''CfoActionApi'''
    default_options = {
        'name': 'CFS Default Profile',
        'search_order': 'allowed-first',
        'forbidden_operation': 'block',
        'categories':'default',
        'smart_filter': False,
        'safe_search': False,
        'google_force_safe_search': False,
        'youtube_restrict_mode': False,
        'bing_force_safe_search': False,
        'required': False,
        'insertuion': False
    }

    def __init__(self, fw):
        self.fw = fw
        self.uri_list_profile = 'api/sonicos/content-filter/profiles'
        self.initial_cfo_profile_json ={
            'content_filter': {
                'profile': [
                    {
                        'name': 'CFS Default Profile',
                        'uri_list': {
                            #'allowed': [
                            #    {
                            #        'name': None
                            #    }
                            #],
                            #"forbidden": [
                            #    {
                            #        'name': None
                            #    }
                            #],
                             'search_order': 'allowed-first',
                             'forbidden_operation': 'block'
                        },
                        'categories': 'default',
                        'smart_filter': False,
                        'safe_search': False,
                        'google_force_safe_search': False,
                        'youtube_restrict_mode': False,
                        'bing_force_safe_search': False,
                        'consent': {
                            'required': False
                        },
                        'custom_header': {
                            'insertion': False
                        }
                    }
                ]
            }
        }
        
    def build_json_cfo_action(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_cfo_profile_json)
        if 'profile_name' in kwargs.keys():
            json_input['content_filter']['profile'][0]['name']= kwargs['profile_name']
        try:
            if 'uri_list_allowed' in kwargs.keys():
                json_input['content_filter']['profile'][0]['uri_list']['allowed'] = []
                json_input['content_filter']['profile'][0]['uri_list']['allowed'].append({'name' : kwargs['uri_list_allowed']})
                json_input['content_filter']['profile'][0]['uri_list']['allowed'][0]['name'] = kwargs['uri_list_allowed']
            if 'uri_list_forbidden' in kwargs.keys():
                json_input['content_filter']['profile'][0]['uri_list']['forbidden'] = []
                json_input['content_filter']['profile'][0]['uri_list']['forbidden'].append({'name' : kwargs['uri_list_forbidden']})
            if 'search_order' in kwargs.keys():
                json_input['content_filter']['profile'][0]['uri_list']['search_order'] = kwargs['search_order']
            if 'forbidden_operation' in kwargs.keys():
                json_input['content_filter']['profile'][0]['uri_list']['forbidden_operation'] = kwargs['forbidden_operation']
                logger.info('URI list configured')
            else:
                raise KeyError
        except KeyError:
            logger.error("Error in the Uri List configuration")
        if 'categories' in kwargs.keys():
            json_input['content_filter']['profile'][0]['categories'] = kwargs['categories']
        if 'https_filtering' in kwargs.keys():
            json_input['content_filter']['profile'][0]['https_filtering'] = kwargs['https_filtering']
        if 'smart_filter' in kwargs.keys():
            json_input['content_filter']['profile'][0]['smart_filter'] = kwargs['smart_filter']
        if 'safe_search' in kwargs.keys():
            json_input['content_filter']['profile'][0]['safe_search'] = kwargs['safe_search']
        if 'google_force_safe_search' in kwargs.keys():
            json_input['content_filter']['profile'][0]['google_force_safe_search'] = kwargs['google_force_safe_search']
        if 'youtube_restrict_mode' in kwargs.keys():
            json_input['content_filter']['profile'][0]['youtube_restrict_mode'] = kwargs['youtube_restrict_mode']
        if 'bing_force_safe_search' in kwargs.keys():
            json_input['content_filter']['profile'][0]['bing_force_safe_search'] = kwargs['bing_force_safe_search']
        try:
            if 'consent_req' in kwargs.keys():
                json_input['content_filter']['profile'][0]['consent']['required'] = kwargs['consent_req']
                try:
                    if kwargs['consent_req']:
                        if 'user_idle_timeout' in kwargs.keys():
                            json_input['content_filter']['profile'][0]['consent']['user_idle_timeout']= kwargs['user_idle_timeout']
                        if 'option_page_url' in kwargs.keys():
                            json_input['content_filter']['profile'][0]['consent']['optional'] ={'page_url':kwargs['option_page_url']}
                        if 'mandatory_page_url' in kwargs.keys():
                            json_input['content_filter']['profile'][0]['consent']['mandatory']={'page_url': kwargs['mandatory_page_url']}
                        if 'mandatory_addr' in kwargs.keys():
                            json_input['content_filter']['profile'][0]['consent']['mandatory'] = {}
                            json_input['content_filter']['profile'][0]['consent']['mandatory']['address']={'any':  kwargs['mandatory_addr']}
                        else:
                            logger.error("Consent request option is not correct")
                    else:
                        logger.info("Consent request is false")
                        raise ValueError
                except ValueError:
                    logger.error("Consent request key is false or some error")
            else:
                raise KeyError
        except KeyError:
            logger.error("Error in consent request key")

        try:
            # tmp_input = {'domain': "",'key':"",'value':""}
            if 'customer_insertion' in kwargs.keys():
                json_input['content_filter']['profile'][0]['custom_header']['insertion'] = kwargs['customer_insertion']
                try:
                    if kwargs['customer_insertion']:
                        for val in kwargs['entry']:
                            json_input['content_filter']['profile'][0]['custom_header']['entry']=[]
                            json_input['content_filter']['profile'][0]['custom_header']['entry'].append(copy.deepcopy(val))
                            logger.info('insertion done sucessfully')
                    else:
                        logger.info('insertion has false value')
                except:
                    logger.error('entry has value error') 
            else:
                raise KeyError
        except KeyError:
            logger.error('Error while configuring customer_insertion')
        logger.info(json_input)
        return json_input

    def get_cfo_profile(self, name=None):
        if name:
            url = self.uri_list_profile + '/name/' + name
        else:
            url = self.uri_list_profile
        get_response = self.fw.api_get(url)
        return get_response

    def configure_cfo_profile(self, msg=False, **kwargs):
        self.options = dict(CfoProfilesApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_cfo_action(**kwargs)
        post_resp = self.fw.api_post(self.uri_list_profile, msg, data=json_input)
        return post_resp

    def add_cfo_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.uri_list_profile, msg, data=json_input)
        return resp

    def edit_cfo_profile_by_name(self, msg=False, name=None, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if name:
            url = self.uri_list_profile + '/name/' + str(name)
        else:
            logger.error('name should be specified for edit the cfs profile.')
            return False
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def edit_cfo_profile(self, msg=False, **kwargs):
        '''
            edit_default_profile = {
                'name': 'CFS Default Action',
                'https_filtering': True,
            }
        '''
        options = dict(CfoProfilesApi.default_options)
        options.update(kwargs)
        logger.info(options)
        json_input = self.build_json_cfo_action(**options)
        logger.info(json_input)
        put_resp = self.fw.api_put(self.uri_list_profile, msg, data=json_input)
        return put_resp

    def delete_cfo_profile(self, msg=False, name=None):
        if name:
            url = self.uri_list_profile + '/name/' + name
        else:
            logger.error('name shoule be specified for delete_cfs_profile.')
            return False
        resp = self.fw.api_delete(url)
        return resp


class AccessRuleApi():

    def __init__(self, fw):
        self.fw = fw
        self.access_rule_url = '/access-rules/ipv4'
        self.access_rule_url_v6 = '/access-rules/ipv6'
        self.general_url = 'api/sonicos'
        self.reporting_url = 'api/sonicos/reporting/access-rules/'
        self.uuid_url = 'api/sonicos/access-rules/ipv4/uuid/'

        # initializing the initial dictionary
        self.initial_access_rule_json = {
            "access_rules": [
                {
                    "ipv4": {
                        "name": "",
                        "enable": True,
                        "from": "None",
                        "to": "None",
                        "action": "allow",
                        "source": {
                            "address": {

                            },
                            "port": {
                                "any": True
                            }
                        },
                        "service": {

                        },
                        "destination": {
                            "address": {

                            }
                        },
                        "schedule": {
                            "always_on": True
                        },
                        "users": {
                            "included": {
                                "all": True
                            },
                            "excluded": {
                                "none": True
                            }
                        },
                        "comment": "None",
                        "fragments": True,
                        "logging": True,
                        "flow_reporting": False,
                        "botnet_filter": False,
                        "geo_ip_filter": False,
                        "packet_monitoring": False,
                        "management": False,
                        "max_connections": 100,
                        "priority": {
                            "auto": True
                        },
                        "tcp": {
                            "timeout": 15
                        },
                        "udp": {
                            "timeout": 30
                        },
                        "connection_limit": {
                            "source": {},
                            "destination": {}
                        },
                        "dpi": True,
                        "dpi_ssl": {
                            "client": True,
                            "server": True
                        },
                        "quality_of_service": {
                            "dscp": {
                                "preserve": True
                            },
                            "class_of_service": {}
                        }
                    }
                }
            ]
        }

    def build_json_access_rule(self, access_rule_ip_version, **access_rule):

        copy_initial_access_rule_json = copy.deepcopy(self.initial_access_rule_json)
        try:
            access_rule_ip_version = access_rule_ip_version.lower()
            copy_initial_access_rule_json["access_rules"][0][access_rule_ip_version] = \
            copy_initial_access_rule_json["access_rules"][0].pop("ipv4")
            if 'bandwidth_management' in access_rule.keys():
                copy_initial_access_rule_json["access_rules"][0][access_rule_ip_version]['bandwidth_management'] = {
                    "egress": {},
                    "ingress": {}
                }
            logger.info(access_rule)
            if "from" not in access_rule.keys() or "to" not in access_rule.keys() or "action" not in access_rule.keys():
                print("importent keys are missing....")
            for keys in access_rule.keys():
                if keys in ["from", "to", "action"]:
                    copy_initial_access_rule_json["access_rules"][0][access_rule_ip_version][keys] = access_rule[keys]
                # for zero level key nested dict
                if keys in ['name', 'enable', 'comment', 'fragments', 'logging', 'sip', 'h323', 'flow_reporting',
                            'botnet_filter', 'geo_ip_filter', 'packet_monitoring', 'management', 'max_connections']:
                    copy_initial_access_rule_json["access_rules"][0][access_rule_ip_version][keys] = access_rule[keys]
                # for one level key nested dict
                if keys in ['schedule', 'priority', "service"]:
                    copy_initial_access_rule_json["access_rules"][0][access_rule_ip_version][keys] = access_rule[keys]
                # for multi level key nested dict
                if keys in ['destination', 'source', 'users', 'tcp', 'udp', 'connection_limit', 'dpi_ssl',
                            'quality_of_service','bandwidth_management']:
                    for nested_keys in access_rule[keys].keys():
                        copy_initial_access_rule_json["access_rules"][0][access_rule_ip_version][keys][nested_keys] = \
                        access_rule[keys][nested_keys]
            if 'pdf' in access_rule.keys():
                copy_initial_access_rule_json["access_rules"][0][access_rule_ip_version]['packet_dissection_filter'] = access_rule['pdf']
            return copy_initial_access_rule_json
        except KeyError:
            logger.error('Error: In creating JSON for access rule')

    def config_accessrule(self, msg=False, url="/access-rules/ipv4", **access_rule):
        url = self.general_url + url
        access_rule_ip_version = url.split("/")[3]
        initial_access_rule_json = self.build_json_access_rule(access_rule_ip_version, **access_rule)
        #url = url.replace('/', '', 1)
        logger.info("URL for posting" + url)
        post_response = self.fw.api_post(url, msg, data=initial_access_rule_json)
        return post_response

    def reset_accessrule_default_setting(self):
        url = 'api/sonicos/access-rules/restore-defaults'
        app_setting_resp = self.fw.api_post(url)
        return app_setting_resp

    # it's using to configure the default acl policy
    def config_accessrule_via_uuid(self, uuid='', msg=False, acl_json=None):
        if not uuid or not acl_json:
            lgger.error('input: uuid or acl json can not empty !')
            return (False, {}) if msg else False
        url = self.uuid_url + uuid
        change_acl_dict = {"access_rules": [{"ipv4": acl_json}]}
        return self.fw.api_put(url, msg, change_acl_dict)

    def add_accessrule(self, msg=False, url="/access-rules/ipv4", **access_rule):
        '''
        opt = {"access_rules": [{
            "ipv4": {
                "name": "lan_to_wan_ping",
                "from": "LAN",
                "to": "WAN",
                "service": {
                    "group": "Ping"
                }
            }
        }]}
        this def is used to add a new ipv4 access rule
        params <name>, <from> and <to> are necessary!  the others will be default for those are not include
        '''
        url = self.general_url + url
        logger.info("URL for posting   " + url)
        init_acl_json = {
            "access_rules": [
                {
                    "ipv4": {
                        "name": "",
                        "enable": True,
                        "from": "",
                        "to": "",
                        "action": "allow",
                        "source": {
                            "address": {
                                "any": True
                            },
                            "port": {
                                "any": True
                            }
                        },
                        "service": {
                            "any": True
                        },
                        "destination": {
                            "address": {
                                "any": True
                            }
                        },
                        "schedule": {
                            "always_on": True
                        },
                        "users": {
                            "included": {
                                "all": True
                            },
                            "excluded": {
                                "none": True
                            }
                        },
                        "comment": "",
                        "fragments": True,
                        "logging": True,
                        # "sip": False,
                        # "h323": False,
                        # "flow_reporting": False,
                        # "botnet_filter": False,
                        # "geo_ip_filter": {
                        #     "enable": False,
                        #     "global": True
                        # },
                        # "packet_monitoring": False,
                        # "management": False,
                        # "max_connections": 100,
                        "priority": {
                            "auto": True
                        },
                        # "tcp": {
                            # "timeout": 15
                        # },
                        # "udp": {
                            # "timeout": 30
                        # },
                        # "connection_limit": {
                        #     "source": {},
                        #     "destination": {}
                        # },
                        # "dpi": True,
                        # "dpi_ssl": {
                        #     "client": True,
                        #     "server": True
                        # },
                        # "quality_of_service": {
                        #     "dscp": {
                        #         "preserve": True
                        #     },
                        #     "class_of_service": {}
                        # }
                    }
                }
            ]
        }  
        json_input = copy.deepcopy(init_acl_json)
        json_input["access_rules"][0]["ipv4"].update(access_rule["access_rules"][0]["ipv4"])
        print(json_input)
        return self.fw.api_post(url, msg, data=json_input)

    def delete_accessrule(self, url="/access-rules/ipv4", msg=False, data=None):
        """
        URL should be given with name or UUID
        exaple:-/access-rules/ipv4/name/testing

        """
        url = self.general_url + url
        # url = url.replace('/', '', 1)
        logger.info("URL for Delete:" + url)
        delete_resp = self.fw.api_delete(url, data=data)
        return delete_resp

    def delete_all_accessrule(self, url="/all-access-rules/ipv4", msg=False, data=None):
        """
        This will delete all custom access rules

        """
        url = self.general_url + url
        # url = url.replace('/', '', 1)
        logger.info("URL for Delete:" + url)
        delete_resp = self.fw.api_delete(url, data=data)
        return delete_resp

    def delete_accessrule_by_name(self, name, version = 'ipv4',msg=False, data=None):
        if version == 'ipv4':
            url = 'api/sonicos/access-rules/ipv4/'
        else:
            url = 'api/sonicos/access-rules/ipv6/'
        ret = self.fw.api_get(url)
        for rule in ret['access_rules']:
            if rule[version]['name'] == name:
                uuid = rule[version]['uuid']
                url_tmp = url + 'uuid/' + uuid
                resp = self.fw.api_delete(url_tmp)
        return resp  
        
    def delete_accessrule_by_json(self, msg=False, **kwd):
        url1 = 'api/sonicos/access-rules/ipv4/'
        version = "ipv4"
        if "version" in kwd.keys():
            if kwd["version"] == "ipv6":
                url1 =  'api/sonicos/access-rules/ipv6/'
                version = "ipv6"
            kwd.remove("version")
        logger.info(url1)
        access_rules = self.fw.api_get(url1)
        kwd_len = len(kwd)
        resp = False
        for access_rule in access_rules['access_rules']:
            flag = 0
            for key in kwd.keys():
                if access_rule[version][key] != kwd[key]:
                    break
                elif access_rule[version][key] == kwd[key]:
                    flag += 1
            if flag == kwd_len:
                logger.info("the access rule will be deleted {}".format(access_rule))
                uuid = access_rule[version]['uuid']
                url_tmp = url1 + 'uuid/' + uuid
                if msg:
                    (resp, msg) = self.fw.api_delete(url_tmp, msg=True)
                    return (resp, msg)
                resp = self.fw.api_delete(url_tmp)
        if not resp:
            logger.error("Not found the access rule")
        return resp  

    def is_accessrule_exists(self,**kwd):
        url1 = 'api/sonicos/access-rules/ipv4/'
        version = "ipv4"
        if "version" in kwd.keys():
            if kwd["version"] == "ipv6":
                url1 =  'api/sonicos/access-rules/ipv6/'
                version = "ipv6"
            kwd.remove("version")
        access_rules = self.fw.api_get(url1)
        kwd_len = len(kwd)
        rc = False
        for access_rule in access_rules['access_rules']:
            flag = 0
            for key in kwd.keys():
                if access_rule[version][key] != kwd[key]:
                    break
                elif access_rule[version][key] == kwd[key]:
                    flag += 1
            if flag == kwd_len:
                logger.info("The access rule is existed")
                logger.info(access_rule)
                logger.info('--**--'*20)
                rc = True
                break
        return rc
        
    def check_accessrule_exists(self, version, **kwd):
        url1 = f'api/sonicos/access-rules/{version}/'
        access_rules = self.fw.api_get(url1)
        kwd_len = len(kwd)
        logger.info(kwd_len)
        rc = False
        for access_rule in access_rules['access_rules']:
            flag = 0
            for key in kwd.keys():
                if access_rule[version][key] != kwd[key]:
                    logger.info('The key is')
                    break
                elif access_rule[version][key] == kwd[key]:
                    flag += 1
            if flag == kwd_len:
                logger.info("The access rule is existed")
                logger.info(access_rule)
                logger.info('--**--'*20)
                rc = True
                break
            
        return rc

    def check_accessrule_v4_status(self, uuid=''):
        status = 'not-get-any'
        url = 'api/sonicos/dynamic-file/getPolicyStats.json?type=1'
        if uuid:
            get_json = self.fw.api_get(url)
            try:
                # data example: |4,2cebdc04-5b19-6e97-0900-2cb8ed4ac9a0,0,0,0,0,0,0,0,0,0.00,1|
                resp = get_json['entries']
                for policy in resp.split('|'):
                    if policy.split(',')[1] == uuid:
                        resp = policy.split(',')[-1]
                        logger.info(f'march a expected entry: {policy}')
                        if resp == "1":
                            status = 'active'
                        elif resp == "0":
                            status = 'inactive'
                        break
            except Exception as e:
                logger.error(f'find active status in json fail: {repr(e)}')
                status = 'get-entry-err'
        else:
            logger.error('acl uuid can not empty.')
        return status

    # Method to GET all the access rule details.
    def get_accessrule(self, url="/access-rules/ipv4"):
        """
        URL should be given with name or UUID
        exaple:-/access-rules/ipv4/name/testing
        """
        url = self.general_url + url
        #url = url.replace('/', '', 1)
        logger.info("URL for Get:- " + url)
        get_response = self.fw.api_get(url)
        return get_response

    def get_accessrule_via_zones(self, srczone='LAN', dstzone='WAN', version='ipv4'):
        url = self.general_url + f'/reporting/access-rules-{version}/from/{srczone}/to/{dstzone}'
        get_response = self.fw.api_get(url)
        return get_response

    def put_accessrule(self, msg=False, url="/access-rules/ipv4", **access_rule):
        """
        URL should be given with name or UUID
        exaple:-/access-rules/ipv4/name/testing

        """
        url = self.general_url + url
        access_rule_ip_version = url.split("/")[3]
        initial_access_rule_json = self.build_json_access_rule(access_rule_ip_version, **access_rule)

        #url = url.replace('/', '', 1)
        logger.info("URL for posting" + url)
        post_response = self.fw.api_put(url, data=initial_access_rule_json)

        return post_response
        
    def disable_accessrule(self, url, msg = False,  **access_rule):
        url = self.general_url + url
        logger.info("URL for posting   " + url)
        post_response = self.fw.api_put(url, data=access_rule)
        return post_response

    def get_access_rule_statistics(self):
        
        report_ipv4 = str(self.reporting_url) + 'ipv4'
        statistics = self.fw.api_get(report_ipv4)
        return statistics

    def delete_access_rule_report_statistics(self, frm_rule, to_rule, version ='v4'):
        if version == 'v4':
            url1 = self.general_url + self.access_rule_url
            url2 = 'api/sonicos/reporting/access-rules/ipv4'
            version = 'ipv4'
        else:
            url1 = self.general_url + self.access_rule_url_v6
            url2 = 'api/sonicos/reporting/access-rules/ipv6'
            version = 'ipv6'
        access_rules = self.fw.api_get(url1)
        statistics = self.fw.api_get(url2)
        uuid = ''
        for access_rule in access_rules['access_rules']:
            if access_rule[version]['from'] == frm_rule and access_rule[version]['to'] == to_rule:
                uuid = access_rule[version]['uuid']
                logger.info('###uuid###')
                logger.info(uuid)
                logger.info('###uuid###')
                break
        else:
            logger.error(f'Error: cannot find rule from {frm_rule} to {to_rule} in access rule lists')
        url = url2  + '/uuid/' + uuid
        logger.info(f"URL for delete operation is: {url}")
        delete_response = self.fw.api_delete(url)
        logger.info(f" Delete response is: {delete_response}")
        return delete_response

    def get_access_rule_report_statistics(self, frm_rule, to_rule, version ='v4'):
        if version == 'v4':
            url1 = self.general_url + self.access_rule_url
            url2 = 'api/sonicos/reporting/access-rules/ipv4'
            version = 'ipv4'
        else:
            url1 = self.general_url + self.access_rule_url_v6
            url2 = 'api/sonicos/reporting/access-rules/ipv6'
            version = 'ipv6'
        access_rules = self.fw.api_get(url1)
        statistics = self.fw.api_get(url2)
        uuid = ''
        for access_rule in access_rules['access_rules']:
            if access_rule[version]['from'] == frm_rule and access_rule[version]['to'] == to_rule:
                uuid = access_rule[version]['uuid']
                logger.info('uuid')
                logger.info(uuid)
                logger.info('uuid')
                break
        for stat in statistics:
            if stat['uuid'] == uuid:
                return stat
        else:
            logger.error('error: cannot find rule that from {} to {} in access rules'.format(frm_rule, to_rule))


    def get_access_rule_uuid(self, frm_rule, to_rule, action_rule, version ='v4'):
        if version == 'v4':
            url1 = self.general_url + self.access_rule_url
            url2 = 'api/sonicos/reporting/access-rules/ipv4'
            version = 'ipv4'
        else:
            url1 = self.general_url + self.access_rule_url_v6
            version = 'ipv6'
        access_rules = self.fw.api_get(url1)
        statistics = self.fw.api_get(url2)
        uuid = ''
        for access_rule in access_rules['access_rules']:
            if access_rule[version]['from'] == frm_rule and access_rule[version]['to'] == to_rule and access_rule[version]['action'] == action_rule:
                uuid = access_rule[version]['uuid']
                logger.info('uuid')
                logger.info(uuid)
                return uuid
            else:
                logger.error('error: cannot find rule that from {} to {} in access rules'.format(frm_rule, to_rule))


    def get_access_rule_by_name(self, name=None):
        '''
        return example:
        {"ipv4": {"uuid": "00000000-0000-0003-0700-2cb8ed691c48", "name": "lan_to_wan_ping", "from": "LAN", "to": "WAN", "action":  "allow", "source": {"address": {"any": true}, "port": {"any": true}}, "service": {"group": "Ping"}, "destination": {"address": {"any": true}}, "schedule": {"always_on": true}, "users": {"included": {"all": true}, "excluded": {"none": true}}, "enable": true, "auto_rule": false, "comment": "", "fragments": true, "logging": true, "sip": false, "h323": false, "flow_reporting": false, "botnet_filter": false, "geo_ip_filter": {"enable": false, "global": true}, "block": {"countries": {"unknown": false}}, "packet_monitoring": false, "management": false, "max_connections": 100, "priority": {"auto": true}, "tcp": {"timeout": 15, "urgent": false}, "udp": {"timeout": 30}, "connection_limit": {"source": {}, "destination": {}}, "dpi": true, "dpi_ssl": {"client": true, "server": true}, "redirect_unauthenticated_users_to_log_in": true, "quality_of_service": {"class_of_service": {}, "dscp": {}}, "bandwidth_management": {"egress": {}, "ingress": {}}}}
        '''
        if 'name' is None:
            logger.error('param <name> is necessary!!!')
            return {}
        resp = self.get_accessrule()
        try:
            for acl in resp["access_rules"]:
                if name == acl['ipv4']["name"]:
                    logger.info(f'find the match access rule:\n{acl}')
                    return acl
            else:
                logger.error(f'not find the name <{name}> access rule')
                return {}
        except Exception as e:
            logger.error(repr(e))
            return False
    
    def edit_access_rule_by_name(self, acl_name=None, msg=False, **kwargs):
        '''
        this def is used to edit a access rule by name, so param acl_name is necessary
        keys <from>, <to> and <action> in kwargs are necessary used to get the acl uuid
        exp:
        opt = {
                'from': 'LAN',
                'to': "WAN",
                "action": "allow",
                "quality_of_service": {"class_of_service": {}, "dscp": {"explicit": {}}}
        }
        '''
        if acl_name is None:
            logger.error('param <acl_name> is necessary!!!')
            return False
        if 'from' not in kwargs or 'to' not in kwargs or 'action' not in kwargs:
            logger.error(f'keys <from>, <to> and <action> in kwargs are necessary!!!')
            return False
        uuid = self.get_access_rule_uuid(frm_rule=kwargs['from'], to_rule=kwargs['to'], action_rule='allow')
        url = self.uuid_url + uuid
        init_json = self.get_access_rule_by_name(acl_name)
        if "quality_of_service" in init_json['ipv4'] and init_json['ipv4']["quality_of_service"]["dscp"] == {"map": True} and \
        "quality_of_service" in kwargs and kwargs["quality_of_service"]["dscp"] != {"map": True}:
            init_json['ipv4'].pop("cos_override", "not found the key <cos_override>")
        if init_json:
            init_json['ipv4'].update(kwargs)
            input_json = {"access_rules": [init_json]}
            return self.fw.api_put(url, msg, data=input_json)
        else:
            return False


#Use it to check management
    def verify_access_rule(self, access_rule, destination):
        url =  self.reporting_url + 'ipv4'
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
            access_rule = 'Ping'
        else:
            logger.info("access rule must be named: https,http,snmp,ssh,ping")
            return False
        json_output = self.fw.api_get(url)
        for item in json_output:
            if item['destination'] == destination:
                if item['service'] == access_rule and item['action'] == 'allow':
                    logger.info(item)
                    return True
        logger.info("The access rule {} is not exist".format(access_rule))
        return False

    def find_access_rules_by_json(self, version='ipv4', **kwargs):
        """
        Parameters:
            version: str, 'ipv4' or 'ipv6', default is 'ipv4'.
            kwargs: dict, kwargs to find matched access rules. 
                - The keys in this dict can refer to self.initial_access_rule_json['access_rules'][0]['ipv4']
                - example: 
                {"comment": "Auto rule for DNS policy",
                "from": "LAN",
                "to": "LAN",
                "service": {"name": "DNS (Name Service) UDP"},
                "destination": {"address": {"group": "LAN Interface IP"}}}.
        Return: list, all access rules matched the kwargs.
        """
        # check api url
        if version == 'ipv4':
            url = 'api/sonicos/access-rules/ipv4/'
        else:
            url = 'api/sonicos/access-rules/ipv6/'
            version = 'ipv6'
        # find rules
        access_rules = self.fw.api_get(url)
        find_list = []
        if 'access_rules' in access_rules.keys():  
            for access_rule in access_rules['access_rules']:
                found = 0
                if version in access_rule.keys():
                    for key in kwargs.keys():
                        if access_rule[version].get(key) != kwargs[key]:
                            break
                        elif access_rule[version].get(key) == kwargs[key]:
                            found += 1
                if found == len(kwargs) and found:
                    logger.info(f"Matched access rule is existed")
                    logger.info(access_rule)
                    logger.info('--**--'*20)
                    find_list.append(access_rule)
        if find_list == []:
            logger.info("No Matched access rules are found !!")
        return find_list
  
    def get_access_rules_uuid_by_json(self, version='ipv4', **kwargs):
        """
        Parameters:
            version: str, 'ipv4' or 'ipv6', default is 'ipv4'.
            kwargs : dict, kwargs to find access rules.
                - The keys in this dict can refer to self.initial_access_rule_json['access_rules'][0]['ipv4']
                - example: 
                {"comment": "Auto rule for DNS policy",
                "from": "LAN",
                "to": "LAN",
                "service": {"name": "DNS (Name Service) UDP"},
                "destination": {"address": {"group": "LAN Interface IP"}}}.
        Return : list, all uuids of access rules matched the kwargs.
        """
        uuids = []
        access_rules = self.find_access_rules_by_json(version=version, **kwargs)
        for access_rule in access_rules:
            if version in access_rule.keys():
                uuid = access_rule[version].get('uuid')
                if uuid:
                    logger.info(f"uuid - {uuid}")
                    logger.info('--**--'*20)
                    uuids.append(uuid)
            else:
                logger.error('Get uuid failed !!')
        return uuids



class AccessRuleIPv6Api():

    def __init__(self,fw):
        self.fw = fw
        self.access_rule_url_ipv6 = 'api/sonicos/access-rules/ipv6'
        self.access_rule_url= '/access-rules/ipv6'
        self.general_url = 'api/sonicos'

        #initializing the initial dictionary
        self.initial_access_rule_json_v6= {
        "access_rules": [
        {
            "ipv6": {
                "name": "",
                "enable": True,
                "from": "None",
                "to": "None",
                "action": "allow",
                "source": {
                    "address": {
                        
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    
                },
                "destination": {
                    "address": {
                    
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "None",
                "fragments": True,
                "logging": True,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": False,
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "auto": True
                },
                "tcp": {
                    "timeout": 15
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "quality_of_service": {
                    "dscp": {
                        "preserve": True
                    },
                    "class_of_service": { }
                }
            }
        }
        ]
        }
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

  
    def build_json_access_rule_ipv6(self,access_rule_ip_version,**access_rule):
        copy_initial_access_rule_json_v6=copy.deepcopy(self.initial_access_rule_json_v6)
        try:
            access_rule_ip_version=access_rule_ip_version.lower()
            copy_initial_access_rule_json_v6["access_rules"][0][access_rule_ip_version]=copy_initial_access_rule_json_v6["access_rules"][0].pop("ipv6")
            if "from" not in access_rule.keys() or "to" not in access_rule.keys() or "action" not in access_rule.keys():
                print("importent keys are missing....")
            for keys in access_rule.keys():
                if keys in ["from","to","action"]:
                    copy_initial_access_rule_json_v6["access_rules"][0][access_rule_ip_version][keys]=access_rule[keys]
                #for zero level key nested dict
                if keys in ['name','enable','comment','fragments','logging','sip','h323','flow_reporting','botnet_filter','geo_ip_filter','packet_monitoring','management','max_connections']:
                    copy_initial_access_rule_json_v6["access_rules"][0][access_rule_ip_version][keys]=access_rule[keys]
                #for one level key nested dict
                if keys in ['schedule','priority',"service"]:
                    copy_initial_access_rule_json_v6["access_rules"][0][access_rule_ip_version][keys]=access_rule[keys]
                #for multi level key nested dict
                if keys in ['destination','source','users','tcp','udp','connection_limit','dpi_ssl','quality_of_service']:
                    for nested_keys in access_rule[keys].keys():
                        copy_initial_access_rule_json_v6["access_rules"][0][access_rule_ip_version][keys][nested_keys]=access_rule[keys][nested_keys]
            if 'pdf' in access_rule.keys():
                copy_initial_access_rule_json_v6["access_rules"][0][access_rule_ip_version]['packet_dissection_filter'] =  access_rule['pdf']
            return copy_initial_access_rule_json_v6
        except KeyError:
            logger.error('Error: In creating JSON for access rule')
     
    def config_accessrule_ipv6(self,msg=False,url="/access-rules/ipv6",**access_rule):
        url=self.general_url+url
        access_rule_ip_version=url.split("/")[3]
        initial_access_rule_json_v6=self.build_json_access_rule_ipv6(access_rule_ip_version,**access_rule)
        logger.info("URL for posting", url)
        post_response=self.fw.api_post(url,data=initial_access_rule_json_v6)
        
        return post_response

    def add_accessrule_ipv6(self, msg=False, url="/access-rules/ipv6", **access_rule):
        url = self.access_rule_url_ipv6
        logger.info("URL for posting   " + url)
        post_response = self.fw.api_post(url, msg, data=access_rule)
        return post_response

    def config_accessrule_via_uuid_ipv6(self, uuid='', msg=False, acl_json=None):
        """
        Example:
        acl_json =  {
        "name": "Default Access Rule",
        "enable": True,
        "from": "LAN",
        "to": "WAN",
        "action": "Allow",
        "priority": {
            "manual": {
                "value": 666
            }
        },
        "source": {
            "address": {
                "any": True
            },
            "port": {
                "any": True
            }
        },
        "service": {
            "any": True
        },
        "destination": {
            "address": {
                "any": True,
            }
        },
        "schedule": {
            "always_on": True
        },
        "users": {
            "included": {
                "all": True
            },
            "excluded": {
                "none": True
            }
        },
        "comment": "Modified",
        "fragments": True,
        "logging": True,
        "sip": True,
        "h323": True,
        "flow_reporting": False,
        "botnet_filter": False,
        "geo_ip_filter": {
            "enable": False,
            "global": True
        },
        "block": {
            "countries": {
                "unknown": False
            }
        },
        "packet_monitoring": False,
        "management": False,
        "max_connections": 100,
        "tcp": {
            "timeout": 15,
            "urgent": False
        },
        "icmp": {
            "timeout": 30
        },
        "connection_limit": {
            "source": {},
            "destination": {}
        },
        "dpi": True,
        "dpi_ssl": {
            "client": True,
            "server": True
        },
        "redirect_unauthenticated_users_to_log_in": True,
        "quality_of_service": {
            "class_of_service": {},
            "dscp": {
                "preserve": True
            }
        },
        }
        """
        if not uuid or not acl_json:
            logger.error('input: uuid or acl json can not empty !')
            return (False, {}) if msg else False
        uuid_url = 'api/sonicos/access-rules/ipv6/uuid/'
        url = uuid_url + uuid
        change_acl_dict = {"access_rules": [{"ipv6": acl_json}]}
        return self.fw.api_put(url, msg, change_acl_dict)

    def delete_accessrule_ipv6(self,url="/access-rules/ipv6",msg=False,data=None):
        """
        URL should be given with name or UUID
        exaple:-/access-rules/ipv6/name/testing

        """
        url=self.general_url+url
        logger.info("URL for Delete:- ",url)
        delete_resp = self.fw.api_delete(url,data=data)
        return delete_resp

    # Method to GET all the access rule details.
    def get_accessrule_ipv6(self, url="/access-rules/ipv6"):
        """
        URL should be given with name or UUID
        exaple:-/access-rules/ipv6/name/testing
        """
        url=self.general_url+url
        logger.info("URL for Get:- ",url)
        get_response = self.fw.api_get(url)
        return get_response

    def get_accessrule_via_zones_ipv6(self, srczone='LAN', dstzone='WAN', version='ipv6'):
        url = self.general_url + f'/reporting/access-rules-{version}/from/{srczone}/to/{dstzone}'
        get_response = self.fw.api_get(url)
        return get_response

    def put_accessrule_ipv6(self,msg=False,url="/access-rules/ipv6",**access_rule):
        """
        URL should be given with name or UUID
        exaple:-/access-rules/ipv6/name/testing

        """
        url=self.general_url+url
        access_rule_ip_version=url.split("/")[3]
        initial_access_rule_json_v6=self.build_json_access_rule_ipv6(access_rule_ip_version,**access_rule)
 
        logger.info("URL for posting",url)
        post_response=self.fw.api_put(url,data=initial_access_rule_json_v6)
        
        return post_response

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
            if 'dpi' in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['dpi'] = kwargs['dpi']
            if 'client_dpi_ssl' in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['dpi_ssl']['client'] = kwargs['client_dpi_ssl']
            if 'server_dpi_ssl' in kwargs.keys():
                json_input['access_rules'][0]['ipv6']['dpi_ssl']['server'] = kwargs['server_dpi_ssl']
                     
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
                if item['from'] == kwargs['from'] and item['to'] == kwargs['to'] :
                    if 'service' in kwargs and item['service'] != kwargs['service']:
                        continue
                    if 'source' in kwargs and item['source'] != kwargs['source']:
                        continue
                    if 'destination' in kwargs and item['destination'] != kwargs['destination']:
                        continue

                    logger.info(item)
                    return item['uuid']


        logger.info("Get ipv6 accessrule uuid failed!")


    def get_ipv6_accessrule(self, **kwargs):
        uuid = self.get_ipv6_accessrule_uuid(**kwargs)
        url = self.access_rule_url_ipv6 + '/uuid/' + uuid
        logger.info("GET from URL: {}".format(url))
        json_output = self.fw.api_get(url)
        return json_output
        

class DNSRuleApi:
    '''DNS Rule Api class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/dns-policies'

    def get_dns_rule(self):
        out = self.fw.api_get(self.url)
        return out
    
    def get_dns_rule_by_name(self, name=''):
        if not name:
            logger.error("Please enter rule's name!!")
            return False
        url = self.url + '/name/' + name
        resp = self.fw.api_get(url)
        return resp
    
    def add_dns_rule(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.url, msg, data=json_input)
        return repu_resp

    def del_dns_rule_by_name(self, name, msg=False):
        if name:
            url = self.url + '/name/' + name
            repu_resp = self.fw.api_delete(url, msg)
            return repu_resp
        else:
            logger.error("Pls enter rule's name")
        return False

    # recommend to use
    def edit_dns_rule(self, msg=False, **kwargs):
        '''
        kwargs: dict, key 'name' is necessary. if you want to change rule's name, use key 'new-name'.
            Example - {'name': 'test', 'new-name': 'edit', 'enable': False}
        '''
        json_input = copy.deepcopy(kwargs)
        if 'name' in json_input.keys():
            name = json_input['name']
            url = self.url + '/name/' + name
            json_final = self.fw.api_get(url)
            if json_final:
                if 'new-name' in json_input.keys():
                    json_input['name'] = json_input.pop('new-name')
                json_final['dns_policies'][0].update(json_input)
                if 'filter_profile' in json_final['dns_policies'][0]['action'].keys():
                    if 'proxy_mode' in json_final['dns_policies'][0].keys():
                        json_final['dns_policies'][0].pop('proxy_mode')             
                repu_resp = self.fw.api_put(url, msg, data=json_final)
                return repu_resp
            else:
                logger.error("Invalid rule's name!")
        else:
            logger.error("Pls enter rule's name")
        return False
    
    # not recommend to use
    def edit_dns_rule_name(self, msg=False, name='', new_name=''):
            if name and new_name:
                url = self.url + '/name/' + name
                json_input = self.fw.api_get(url)
                if json_input and 'dns_policies' in json_input.keys():
                    json_input['dns_policies'][0]['name'] = new_name
                    if msg:
                        (resp, msg) = self.fw.api_put(url, msg=True, data=json_input)
                        return (resp, msg)
                    repu_resp = self.fw.api_put(url, data=json_input)
                    return repu_resp
            else:
                logger.error("Pls enter rule's name and new name!!")
            return False


class CustomMatchApi():
    '''CustomMatchApi class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/custom-matches'
        self.url_groups = 'api/sonicos/custom-match-groups'
        self.initial_custommatch_json =  {
            'custom_matches': [
                {            
                    'name': '' ,
                }
            ]
        }

        self.initial_custommatchgroups_json =  {
            'custom_match_groups': [
                {            
                    'name': '' ,
                }
            ]
        }
        self.delete_custommatchgroups_json = {
            "custom_match_groups": [
                {
                    "name": ''
                }
            ]
        }
        self.delete_custommatches_json = {
            "custom_matches": [
                {
                    "name": ''
                }
            ]
        }

    def config_custommatches(self, msg=False, **kwargs):
        json_input = json_input = copy.deepcopy(kwargs)
        matchobj_resp = self.fw.api_post(self.url, msg, data=json_input) 
        return matchobj_resp  

    def config_custommatchgroups(self, msg=False, **kwargs):
        json_input = json_input = copy.deepcopy(kwargs)
        matchobj_resp = self.fw.api_post(self.url_groups, msg, data=json_input) 
        return matchobj_resp

    def delete_custommatchgroups(self, name = None):
        json_input = copy.deepcopy(self.delete_custommatchgroups_json)
        json_input['custom_match_groups'][0]['name'] = name
        resp = self.fw.api_delete(self.url_groups, data = json_input)
        return resp

    def delete_custommatches(self, name = None):
        json_input = copy.deepcopy(self.delete_custommatches_json)
        json_input['custom_matches'][0]['name'] = name
        resp = self.fw.api_delete(self.url, data = json_input)
        return resp


    
class WebCategoryGroupsApi():
    '''WebCategoryGroupsApi'''
    default_options = {
        'name': 'Default Web Category Object Group',
    }
    
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/web-category-groups'
        self.uri_list_profile = 'api/sonicos/web-category-groups/name'
        self.initial_web_category_groups_json ={
            "web_category_groups": [
                {
                    "name": "Default Web Category Object Group",
                    "web_category_object": [
                        {
                            "name": "Weapons"
                        },
                        {
                            "name": "Violence/Hate/Racism"
                        },
                        {
                            "name": "Sex Education"
                        },
                        {
                            "name": "Radicalization and Extremism"
                        },
                        {
                            "name": "Pornography"
                        },
                        {
                            "name": "Nudism"
                        },
                        {
                            "name": "Malware"
                        },
                        {
                            "name": "Intimate Apparel/Swimsuit"
                        },
                        {
                            "name": "Internet Watch Foundation CAIC"
                        },
                        {
                            "name": "Illegal Skills/Questionable Ski"
                        },
                        {
                            "name": "Hacking/Proxy Avoidance Systems"
                        },
                        {
                            "name": "Gambling"
                        },
                        {
                            "name": "Drugs/Illegal Drugs"
                        },
                        {
                            "name": "Cult/Occult"
                        },
                        {
                            "name": "Alcohol/Tobacco"
                        },
                        {
                            "name": "Adult/Mature Content"
                        }
                    ],
                    "web_category_group": []
                }
            ]
        }

    def get_web_category_groups(self, name = 'Default Web Category Object Group'):
        url = self.uri_list_profile + '/'+ str(name)
        logger.info(url)
        get_response = self.fw.api_get(url)
        return get_response

    def edit_web_category_by_name(self, msg=False, name=None, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if name:
            url = self.uri_list_profile + '/' + str(name)
        else:
            logger.error('name should be specified for edit the web category.')
            return False
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def add_web_category(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp


class SecurityActionProfilesApi():
    '''SecurityActionProfilesApi'''
    def __init__(self, fw):
        self.fw = fw
        self.url_action_profile = 'api/sonicos/security-action-profiles'
        
    def add_security_action_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        post_resp = self.fw.api_post(self.url_action_profile, msg, data=json_input)
        return post_resp

    
    def config_security_action_profile(self, name, msg=False, **kwargs):
        if name :
            url = self.url_action_profile + '/name/' + str(name)
        else:
            logger.error('name should be added.')
            return False
        logger.info(url)
        json_input = copy.deepcopy(kwargs)
        put_resp = self.fw.api_put(url, msg, data=json_input)
        return put_resp

    def delete_security_action_profile_by_name(self, name, msg=False):
        if name:
            url = self.url_action_profile + '/name/' + name
        else:
            logger.error('name should be added.')
            return False
        security_action_profile_resp = self.fw.api_delete(url, msg=msg)
        return security_action_profile_resp
        
        
class FipsApi:
    """FipsApi Class"""

    def __init__(self, fw):
        self.fw = fw
        self.geturl = 'api/sonicos/dynamic-file/getFipsModeSettings.json'

    def get_fips_warning(self):
        logger.info(f'get_fips_warning get url: {self.geturl}')
        return self.fw.api_get(self.geturl)


class CaptureATPApi():
    """CaptureATPApi Class"""

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/capture-atp/base'
        self.scanning_history_url = 'api/sonicos/capture-atp-wrapper'
        self.captureatp_http_exclusion_url = 'api/sonicos/capture-atp/http-exclusions'

    def get_capture_ATP(self):
        return self.fw.api_get(self.base_url)

    def config_capture_ATP(self, msg=False,**kwargs):
        json_input = self.get_capture_ATP()
        logger.info(json_input)
        if 'enable' in kwargs.keys():
            json_input['capture_atp']['enable'] = kwargs['enable']
        resp = self.fw.api_put(self.base_url, msg, data=json_input)
        return resp

    def config_ATP_file_type(self, msg=False, **kwargs):
        # kwargs is {
        #     "exe": True,
        #     "pdf": True,
        #     "office": True,
        #     "officex": True,
        #     "archives": True
        # }
        json_input = self.get_capture_ATP()
        logger.info(f'get current atp configure:\n{json_input}')
        json_input['capture_atp']['enable'] = True
        if 'exe' in kwargs.keys():
            json_input['capture_atp']['file_type']['exe'] = kwargs['exe']
        if 'pdf' in kwargs.keys():
            json_input['capture_atp']['file_type']['pdf'] = kwargs['pdf']
        if 'office' in kwargs.keys():
            json_input['capture_atp']['file_type']['office'] = kwargs['office']
        if 'officex' in kwargs.keys():
            json_input['capture_atp']['file_type']['officex'] = kwargs['officex']
        if 'archives' in kwargs.keys():
            json_input['capture_atp']['file_type']['archives'] = kwargs['archives']

        output = self.fw.api_put(self.base_url, msg, data=json_input)
        return output

    def config_ATP_await_verdict(self, msg=False, **kwargs):
        # kwargs is {
        #     "await_verdict": "block",
        #     "block_until_verdict": {
        #         "http": True,
        #         "smtp": True
        #     }
        # }
        json_input = self.get_capture_ATP()
        logger.info(f'get current atp configure:\n{json_input}')
        json_input['capture_atp']['enable'] = True
        if 'await_verdict' in kwargs.keys():
            if kwargs['await_verdict'] == 'block':
                json_input['capture_atp']['await_verdict'] = 'block'
                if 'block_until_verdict' in kwargs.keys():
                    json_input['capture_atp']['block_until_verdict'] = kwargs['block_until_verdict']
                else:
                    json_input['capture_atp']['block_until_verdict'] = {"http": False, "smtp": False}
            else:
                json_input['capture_atp']['await_verdict'] = 'allow'
        else:
            logger.info('kwargs not await_verdict key !!!')
            return False if not msg else (False, dict)

        output = self.fw.api_put(self.base_url, msg, data=json_input)
        return output

    def get_capture_ATP_Scanning_History(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        post_resp = self.fw.api_post(self.scanning_history_url, msg, data=json_input)
        return post_resp

    def add_capture_atp_http_exclusion(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        post_resp = self.fw.api_post(self.captureatp_http_exclusion_url, msg, data=json_input)
        return post_resp

    def delete_capture_atp_http_exclusion(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        del_resp = self.fw.api_delete(self.captureatp_http_exclusion_url, msg, data=json_input)
        return del_resp

class ConfigModeApi:
    def __init__(self, fw):
        self.fw = fw
        self.configmodeapi = 'api/sonicos/config-mode'
        self.nonconfigmodeapi = 'api/sonicos/non-config-mode'
    def check_config_mode(self, msg=False):
        configmoderesponse = self.fw.api_post(self.configmodeapi, msg, data={})
        return configmoderesponse

    def check_nonconfig_mode(self, msg=False):
        nonconfigmoderesponse = self.fw.api_post(self.nonconfigmodeapi, msg, data={})
        return nonconfigmoderesponse