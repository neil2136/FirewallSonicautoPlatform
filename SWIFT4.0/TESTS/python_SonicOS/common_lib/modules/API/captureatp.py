import re
import copy
from pprint import pprint

from utm import is_Firewall_up
#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)
from runner.settings import logger

class CaptureAtpApi:
    '''CaptureAtpApi Class'''
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/capture-atp'

    def show_capatp(self):
        url = 'api/sonicos/reporting/capture-atp'
        return self.fw.api_get(url)

    def show_atp_setting(self):
        url = self.url + '/base'
        return self.fw.api_get(url)

    def conf_atp(self, msg=False, **kwargs):
        url = self.url + '/base'
        init_json = {
            'capture_atp': {}
        }
        logger.info("The initial json is ")
        logger.info(init_json)
        init_json['capture_atp'].update(kwargs)
        # logger.info("Updated json")
        # logger.info(init_json)
        return self.fw.api_put(url, msg, data=init_json)

    def show_md5_ex(self):
        url = self.url + '/md5-exclusions'
        return self.fw.api_get(url)

    def conf_md5_ex(self, msg=False, **kwargs):
        url = self.url + '/md5-exclusions'
        init_json = { 'capture_atp': { 'exclude': {} } }
        init_json['capture_atp'] = { 'exclude': kwargs }
        return self.fw.api_put(url, msg, data=init_json)

    def add_md5_ex(self, msg=False, **kwargs):
        url = self.url + '/md5-exclusions'
        json_input = copy.deepcopy(kwargs)
        post_resp = self.fw.api_post(url, msg, data=json_input)
        return post_resp

    def delete_md5_ex(self, msg=False, **kwargs):
        url = self.url + '/md5-exclusions'
        json_input = copy.deepcopy(kwargs)
        del_resp = self.fw.api_delete(url, msg, data=json_input)
        return del_resp

