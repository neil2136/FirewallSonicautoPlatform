import copy
import json
from util.snwl_logging import logger
from util.assertion import *
#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)
from runner.settings import logger
class SettingApi():
    default_options = {
        'assistance_code': None,
        'host': None,
        'net': None,
        'mask': None
    }
    def __init__(self,fw):
        self.fw = fw
        self.virtual_assist_url = '/api/sonicos/virtual-assist/settings'
        self.virtual_assist_json = {
            'virtual_assist': {
                'assistance_code': None,
                 'support_without_invitation': True,
                 'disclaimer': "",
                 'customer_access_link': "",
                 'link_on_portal_login': False,
                 'technician_email_list': None,
                 'invitation_subject': None,
                 'invitation_message': None,
                 'max_requests': None,
                 'limit_message': None,
                 'max_requests_one_ip': 0,
                 'pending_request_expiration': 0,
                 'deny_requests': [{'host': []},
                      {
                         'network': {{'net':[],'mask':[]}}
                     }
                 ]
                 }
        }
    # Method to GET the Virtual Assist page content
    def get_virtual_assist(self):
        get_response = self.fw.api_get_response(self.virtual_assist_url)
        return get_response
	# Build JSON for Virtual Assist
    def build_json_virtual_assist(self, **input_json):
            json_input = {}
            host_list = []
            net_list = []
            json_input = copy.deepcopy(self.virtual_assist_json)
            logger("Virtual Assist json obtained")
            logger(json_input)
            json_input['virtual_assist']['assistance_code'] = input_json['assistance_code']
            json_input['virtual_assist']['support_without_invitation'] = input_json[ 'support_without_invitation']
            json_input['virtual_assist']['disclaimer'] = input_json['disclaimer']
            json_input['virtual_assist']['customer_access_link'] = input_json['customer_access_link']
            json_input['virtual_assist']['link_on_portal_login'] = input_json['link_on_portal_login']
            json_input['virtual_assist']['technician_email_list'] = input_json['technician_email_list']
            json_input['virtual_assist']['invitation_subject'] = input_json['invitation_subject']
            json_input['virtual_assist']['invitation_message'] = input_json['invitation_message']
            json_input['virtual_assist']['max_requests'] = input_json['max_requests']
            json_input['virtual_assist']['limit_message'] = input_json['limit_message']
            json_input['virtual_assist']['max_requests_one_ip'] = input_json['max_requests_one_ip']
            json_input['virtual_assist']['pending_request_expiration'] = input_json['pending_request_expiration']
            try: 
                if 'host' in input_json.keys():
                    while temp < len(input_json['host']):
                         json_input['virtual_assist']['deny_requests'][0]['host'].append(input_json['host'][temp])
                         temp += 1
				else:
					logger("Put the host value")
					raise KeyError
                for val in kwargs['network']: 
                    json_input['virtual_assist']['deny_requests'][1]['network'].append(copy.deepcopy(val))
            except KeyError:
                 logger.error("Error: in adding the ip and netwok")
            return json_input

    def config_virtual_assist(self, msg=False, **kwargs):
        self.options = dict(SettingApi.default_options)
        self.options.update(kwargs)
        input_json= self.options
        logger("options")
        json_input = self.build_json_virtual_assist(**kwargs)
        virtual_assist_resp = self.fw.api_put(self.virtual_assist_url, msg, data=json_input)
        return virtual_assist_resp
