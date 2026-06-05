from modules.API.log import LogMonitorApi
from modules.API.log import LogAutomationApi
from modules.API.log import LogSettingsApi
from modules.API.log import LogCategoryApi
from modules.API.log import SyslogSettingsApi
from modules.API.log import AuditlogMonitorApi
from modules.API.log import LogResolutionApi
from modules.API.log import LogAWSApi
from runner.settings import logger
import copy

class LogMonitorApi(LogMonitorApi):
    '''LogApi class'''

        
class LogAutomationApi(LogAutomationApi):
    '''LogAutomationApi class'''
    LogAutomationApi.initial_mail_sever_settings_json = {
            "log": {
                "automation": {
                    "mail_server": "",
                    "mail_from": "",
                    "authentication_method": "none",
                    "mail_server_advanced": {
                        "smtp_port": 25,
                        "connection_security_method": {},
                        "ignore_tls_verify_error": False,
                        "smtp_authentication": False
                    }
                }
            }
        }


    def cfg_mail_server(self, msg=False, **kwargs):
        options = dict(LogAutomationApi.default_mail_sever_settings_options)
        options.update(kwargs)
        kwargs = options
        logger.info(kwargs)

        json_input = copy.deepcopy(self.initial_mail_sever_settings_json)
        try:
            if 'mail_server' in kwargs.keys() and kwargs['mail_server']:
                json_input['log']['automation']['mail_server'] = kwargs['mail_server']
            if 'mail_from' in kwargs.keys() and kwargs['mail_from']:
                json_input['log']['automation']['mail_from'] = kwargs['mail_from']
            if 'smtp_port' in kwargs.keys() and kwargs['smtp_port']:
                json_input['log']['automation']['mail_server_advanced']['smtp_port'] = int(kwargs['smtp_port'])
            if 'smtp_authentication' in kwargs.keys() and kwargs['smtp_authentication']:
                json_input['log']['automation']['mail_server_advanced']['smtp_authentication'] = kwargs['smtp_authentication']
            if 'connection_security_method' in kwargs.keys() and kwargs['connection_security_method']:
                json_input['log']['automation']['mail_server_advanced']['connection_security_method'][kwargs['connection_security_method']] = True
            if 'user_name' in kwargs.keys() and kwargs['user_name']:
                json_input['log']['automation']['mail_server_advanced']['user_name'] = kwargs['user_name']
            if 'password' in kwargs.keys() and kwargs['password']:
                json_input['log']['automation']['mail_server_advanced']['password'] = kwargs['password']
            if 'authentication_method' in kwargs.keys() and kwargs['authentication_method']:
                json_input['log']['automation']['authentication_method'] = kwargs['authentication_method']
            if 'pop3_user_name' in kwargs.keys() and kwargs['pop3_user_name']:
                json_input['log']['automation']['pop3_user_name'] = kwargs['pop3_user_name']
            if 'pop3_password' in kwargs.keys() and kwargs['pop3_password']:
                json_input['log']['automation']['pop3_password'] = kwargs['pop3_password']
            if 'pop3_server' in kwargs.keys() and kwargs['pop3_server']:
                json_input['log']['automation']['pop3_server'] = kwargs['pop3_server']
            if 'ignore_tls_verify_error' in kwargs.keys():
                json_input['log']['automation']['mail_server_advanced']['ignore_tls_verify_error'] = kwargs['ignore_tls_verify_error']
        except KeyError:
            logger.info("Error in creating JSON for config mail server")
        # mail_server_resp = self.fw.api_put(self.url, data=json_input)
        # return mail_server_resp
        return self.fw.api_put(self.url, msg, data=json_input)

        
class LogSettingsApi(LogSettingsApi):
    '''LogSettingsApi class'''

        
class LogCategoryApi(LogCategoryApi):
    '''Enable all log category'''

        
class SyslogSettingsApi(SyslogSettingsApi):
    ''' syslog settings '''

    
    def edit_syslog_server_new(self, msg=False, **kwargs):
        # original syslog server profile and protocol must be specified
        # #e.g. 
        # opt = {
        #      'original_profile': 0,
        #      'original_protocol': 'udp'
        #      'original_syslog_server_name': "syslog_server"
        #      'original_port': 514,
        #      'address': {'name': "syslog_server_4"},
        # }
        # now url is: 
        edit_url = self.url + f'/server/{kwargs["original_syslog_server_name"]}/port/{kwargs["original_port"]}/profile/{kwargs["original_profile"]}/protocol/{kwargs["original_protocol"]}'
        logger.info(f'url is: {edit_url}')
        if 'original_profile' not in kwargs or 'original_protocol' not in kwargs or 'original_syslog_server_name' not in kwargs or 'original_port' not in kwargs:
            logger.error('original_profile or original_protocol not specified')
            return False
        syslog_servers = self.fw.api_get(self.url)
        try:
            get_json = ''
            if not syslog_servers['log']['syslog']:
                logger.error('Error!No syslog server can edit')
                return False
            for logserver in syslog_servers['log']['syslog']['server']:
                if logserver['address']['name'] == kwargs['original_syslog_server_name']:
                    get_json = logserver
                    break
                if get_json == '':
                    logger.error('Error!! The syslog server that needs to be edited does not exist.')
                    return False
                
            logger.info(f"get_json is: \n{get_json}")
            kwargs.pop("original_syslog_server_name")
            kwargs.pop("original_port")
            kwargs.pop("original_profile")
            kwargs.pop("original_protocol")
       
            get_json.update(kwargs)
            input_json = {'log': {'syslog': {'server': [get_json]}}}
            
            return self.fw.api_put(edit_url, msg, input_json)
        except Exception as e:
            logger.error(repr(e))
            if msg:
                return False, repr(e)
            else:
                return False

        
class AuditlogMonitorApi(AuditlogMonitorApi):
    '''AuditlogMonitorApi '''
    
class LogResolutionApi(LogResolutionApi):
    '''LogResolutionApi class'''

class LogAWSApi(LogAWSApi):
    '''LogAWSApi class'''
