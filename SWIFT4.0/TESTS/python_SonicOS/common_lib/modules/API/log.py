from runner.settings import logger
import copy
from pprint import pprint
from collections import OrderedDict


class LogMonitorApi:
    '''export log '''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/export/log/'

    def export_log_txt(self, log_switch=False,nologin=False):
        url = self.url + 'txt'
        log = self.fw.api_get(url, log_switch=log_switch,nologin=nologin)
        return log

    def export_log_csv(self):
        url = self.url + 'csv'
        return self.fw.api_get(url)

    def export_log_mail(self):
        url = 'api/sonicos/log/email-log'
        return self.fw.api_post_no_need_pending(url,msg=False) 

    def show_log(self):
        url = 'api/sonicos/reporting/log/view'
        return self.fw.api_get(url)

    def clear_log(self,nologin=False):
        url = 'api/sonicos/log/clear'
        self.fw.api_post(url,nologin=nologin)

    def edit_log_display_time_and_entry(self, msg=False, **kwargs):
        url = 'api/sonicos/log/display'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def get_log_display_settings(self):
        url = 'api/sonicos/log/display'
        return self.fw.api_get(url)

    def get_log(self, id=None):
        if id == None:
            url = "api/sonicos/reporting/log/view"
        else:
            url = "api/sonicos/reporting/log/view" + "/id/" + str(id)
        logger.info("url is: {} ".format(url))
        return self.fw.api_get(url)

    def get_audit_log(self):
        url = 'api/sonicos/export/audit/txt'
        return self.fw.api_get(url)

    def edit_log_time(self, **kwargs):
        url = 'api/sonicos/aar'
        json_input = copy.deepcopy(kwargs)
        return self.fw.api_post(url)

    def reset_default_log_settings(self):
        url = 'api/sonicos/log/import-template/default'
        return self.fw.api_post(url)


class AuditlogMonitorApi:
    '''export audit log '''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/export/audit/'
        self.raw_url = 'api/sonicos/raw'
        self.header = OrderedDict([('Accept', 'application/json'),
                                   ('Content-Type', 'application/json'),
                                   ('Accept-Encoding', 'application/json'),
                                   ('X-SNWL-API-Scope', 'extended'),
                                   ('charset', 'UTF-8')])

    def export_audit_log_txt(self, log_switch=False):
        url = self.url + 'txt'
        log = self.fw.api_get(url, log_switch=False)
        return log

    def export_audit_log_csv(self):
        url = self.url + 'csv'
        return self.fw.api_get(url)

    def configure_audit_log(self, msg=False, **kwargs):
        '''
            {"log":{"audit":{"enable":true,"display_on_console":false,"supplemental_changes":false}}}
        '''
        put_url = 'api/sonicos/log/audit/base'
        input_json = copy.deepcopy(kwargs)
        resp = self.fw.api_put(put_url, msg, data=input_json)
        return resp

    def get_audit_log_config(self):
        get_url = 'api/sonicos/log/audit/base'
        resp = self.fw.api_get(get_url)
        return resp
    
    def show_audit_records(self,log_switch=False):
        get_url = 'api/sonicos/log/audit/view'
        resp = self.fw.api_get(get_url,log_switch=False)
        return resp
        
    def email_audit_records(self, msg=False):
        resp = self.fw.api_post(self.raw_url, msg, data={"stream": "cgiaction=emailAuditRecord"}, headers=self.header)
        return resp


class LogAutomationApi:
    "Log Automation class"
    default_email_log_options = {
        "send_log": "when_full",
        "email_format_log": "plain_text",
        "include_all_log_information": False
    }

    default_email_audit_options = {
        "send_audit": "when_full",
        "email_format_audit": "plain_text",
    }

    default_mail_sever_settings_options = {
        "authentication_method": "none",
        "smtp_port": 25,
        "smtp_authentication": False,
    }

    default_ftp_log_auto_options = {
        "send_log_to_ftp": False,
        "server": "0.0.0.0",
        "user_name": "admin",
        "password": "6,6e658327aebddcfda97c0226446ac8a18b3364c93b99e48060dee4086e13e7ca5ca0b4a26889a7e61fa688e5a683f8c21f3b2be58b38d9096f95f44dd076b0df",
        "directory": "logs",
        "send_log": {"when_full": True},
        "file_format": {"plain_text": True},
        "include_all_log_information": False
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/log/automation'
        self.test_server_url = 'api/sonicos/log/mail-server/test'

        self.initial_email_log_json = {
            "log": {
                "automation": {
                    "email_address": {
                        "log": "",
                        "alert": "",
                        "user": "",
                    },
                    "send_log": {
                    },
                    "email_format_log": {
                    },
                    "include_all_log_information": False
                }
            }
        }

        self.initial_email_audit_json = {
            "log": {
                "automation": {
                    "email_address": {
                        "audit": ""
                    },
                    "send_audit": {
                    },
                    "email_format_audit": {
                    }
                }
            }
        }

        self.initial_mail_sever_settings_json = {
            "log": {
                "automation": {
                    "mail_server": "",
                    "mail_from": "",
                    "authentication_method": "none",
                    "mail_server_advanced": {
                        "smtp_port": 25,
                        "connection_security_method": {},
                        "smtp_authentication": False
                    }
                }
            }
        }

        self.inital_ftp_log_auto_json = {
            "log": {
                "automation": {
                    "ftp_log": {
                        "send_log_to_ftp": False,
                        "server": "0.0.0.0",
                        "user_name": "admin",
                        "password": "6,6e658327aebddcfda97c0226446ac8a18b3364c93b99e48060dee4086e13e7ca5ca0b4a26889a7e61fa688e5a683f8c21f3b2be58b38d9096f95f44dd076b0df",
                        "directory": "logs",
                        "send_log": {
                            "when_full": True
                        },
                        "file_format": {
                            "plain_text": True
                        },
                        "include_all_log_information": False
                    }
                }
            }
        }

    def show_log_automation(self):
        return self.fw.api_get(self.url)

    def edit_log_automation(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp

    def email_log_settings(self, msg=False, **kwargs):
        options = dict(LogAutomationApi.default_email_log_options)
        options.update(kwargs)
        kwargs = options
        logger.info(kwargs)

        json_input = copy.deepcopy(self.initial_email_log_json)

        try:
            for method in ['log', 'alert', 'user']:
                if method in kwargs.keys() and kwargs[method]:
                    json_input['log']['automation']['email_address'][method] = kwargs[method]
            if 'send_log' in kwargs.keys() and kwargs['send_log']:
                if kwargs['send_log'] == 'when_full':
                    json_input['log']['automation']['send_log'][kwargs['send_log']] = True
                elif kwargs['send_log'] == 'daily':
                    json_input['log']['automation']['send_log'][kwargs['send_log']] = dict()
                    if 'hour' in kwargs.keys() and isinstance(kwargs['hour'],int) \
                            and 'minute' in kwargs.keys() and isinstance(kwargs['minute'], int):
                        json_input['log']['automation']['send_log'][kwargs['send_log']]['hour'] = kwargs['hour']
                        json_input['log']['automation']['send_log'][kwargs['send_log']]['minute'] = kwargs['minute']
                elif kwargs['send_log'] == 'weekly':
                    json_input['log']['automation']['send_log'][kwargs['send_log']] = dict()
                    if 'week' in kwargs.keys() and kwargs['week'] and kwargs['week'] in['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
                        json_input['log']['automation']['send_log'][kwargs['send_log']][kwargs['week']] = dict()
                        if 'hour' in kwargs.keys() and isinstance(kwargs['hour'], int) \
                                and 'minute' in kwargs.keys() and isinstance(kwargs['minute'], int):
                            json_input['log']['automation']['send_log'][kwargs['send_log']][kwargs['week']]['hour'] = kwargs['hour']
                            json_input['log']['automation']['send_log'][kwargs['send_log']][kwargs['week']]['minute'] = kwargs['minute']
            json_input['log']['automation']['email_format_log'][kwargs['email_format_log']] = True
            json_input['log']['automation']['include_all_log_information'] = kwargs['include_all_log_information']
        except KeyError:
            logger.info("Error in creating JSON for email log setting")

        email_log_resp = self.fw.api_put(self.url, msg, data=json_input)
        return email_log_resp

    def email_audit_settings(self, msg=False, **kwargs):
        options = dict(LogAutomationApi.default_email_audit_options)
        options.update(kwargs)
        kwargs = options
        logger.info(kwargs)

        json_input = copy.deepcopy(self.initial_email_audit_json)

        try:
            if 'audit' in kwargs.keys() and kwargs['audit']:
                json_input['log']['automation']['email_address']['audit'] = kwargs['audit']
            if 'send_audit' in kwargs.keys() and kwargs['send_audit']:
                if kwargs['send_audit'] == 'when_full':
                    json_input['log']['automation']['send_audit'][kwargs['send_audit']] = True
                elif kwargs['send_audit'] == 'daily':
                    json_input['log']['automation']['send_audit'][kwargs['send_audit']] = dict()
                    if 'hour' in kwargs.keys() and isinstance(kwargs['hour'], int) and 'minute' in kwargs.keys() and isinstance(kwargs['minute'], int) :
                        json_input['log']['automation']['send_audit'][kwargs['send_audit']]['hour'] = kwargs['hour']
                        json_input['log']['automation']['send_audit'][kwargs['send_audit']]['minute'] = kwargs['minute']
                elif kwargs['send_audit'] == 'weekly':
                    json_input['log']['automation']['send_audit'][kwargs['send_audit']] = dict()
                    if 'week' in kwargs.keys() and kwargs['week'] and kwargs['week'] in ['sun','mon','tues','wed','thrs','fri','sat']:
                        json_input['log']['automation']['send_audit'][kwargs['send_audit']][kwargs['week']] = dict()
                        if 'hour' in kwargs.keys() and isinstance(kwargs['hour'], int) \
                                and 'minute' in kwargs.keys() and isinstance(kwargs['minute'], int):
                            json_input['log']['automation']['send_audit'][kwargs['send_audit']][kwargs['week']]['hour'] = kwargs['hour']
                            json_input['log']['automation']['send_audit'][kwargs['send_audit']][kwargs['week']]['minute'] = kwargs['minute']
            json_input['log']['automation']['email_format_audit'][kwargs['email_format_audit']] = True
        except KeyError:
            logger.info("Error in creating JSON for email audit setting")
        email_audit_resp = self.fw.api_put(self.url, msg, data=json_input)
        return email_audit_resp

    def cfg_health_check(self,**kwargs):
        json_input = copy.deepcopy(self.initial_email_settings_json)

        try:
            if 'address' in kwargs.keys() and kwargs['address']:
                json_input['log']['automation']['health_check_email']['address'] = kwargs['address']
            if 'schedule' in kwargs.keys() and kwargs['schedule']:
                json_input['log']['automation']['health_check_email']['schedule']= kwargs['schedule']
            if 'body' in kwargs.keys() and kwargs['body']:
                json_input['log']['automation']['health_check_email']['body'] = kwargs['body']
            if 'subject' in kwargs.keys() and kwargs['subject']:
                json_input['log']['automation']['health_check_email']['subject'] = kwargs['subject']
        except KeyError:
            logger.info("Error in creating JSON for config mail server")

        health_check_resp = self.fw.api_put(self.url, msg, data=json_input)
        return health_check_resp

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
        except KeyError:
            logger.info("Error in creating JSON for config mail server")
        # mail_server_resp = self.fw.api_put(self.url, data=json_input)
        # return mail_server_resp
        return self.fw.api_put(self.url, msg, data=json_input)

    def mail_server_test(self):
        return self.fw.api_post(self.test_server_url, data=None)


class LogSettingsApi:
    "Log Settings class"

    def __init__(self, fw):
        self.fw = fw
        self.url_events = 'api/sonicos/log/events'

    def show_event(self, event_id=''):
        if event_id == '':
            logger.error('Please pass in event id.')
            return False
        else:
            url_event_id = str(self.url_events) + '/id/' + str(event_id)
        return self.fw.api_get(url_event_id)

    def edit_event(self, msg=False, event_id='', **kwargs):
        if event_id == '' and 'id' not in kwargs.keys():
            logger.error('Please pass in event id.')
            return False
        else:
            url_event_id = str(self.url_events) + '/id/' + str(event_id)
        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(url_event_id, msg, data=json_input)
        return res

    def get_event_log_categories(self):
        return self.fw.api_get(self.url_events)

    def disable_event(self, msg=False, event_id=''):
        if event_id == '':
            logger.error('Please pass in event id.')
            return False
        else:
            url_event_id = 'api/sonicos/log/disable/event-id/' + str(event_id)
        res = self.fw.api_post(url_event_id, msg)
        return res

    def enable_event(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        res = self.fw.api_put(self.url_events, msg, data =json_input )
        return res


class LogCategoryApi:
    "Enable all log category"

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/log/categories'
        self.url_level = 'api/sonicos/log/global-categories'
        self.logginglevel = {
            "log": {
                "categories": {
                    "global_category_attribute": {
                        "log_email": {},
                        "alert_email": {},
                        "priority_level": "mixed",
                        "log_monitor": {"type": "mixed"},
                        "email_alert": {"type": "mixed"},
                        "syslog": {"type": "enabled"},
                        "ipfix": {"type": "mixed"},
                        "event_profile": {"syslog_server_profile": 0},
                        "log_digest": {"mixed": True},
                        "color": {"leave_unchanged": True}
                    },
                    "logging_level": "",
                    "alert_level": "alert",
                    "custom_template_description": "(NULL)"
                }
            }
        }
        self.demo = {
            "email_alert": {
                "type": "mixed"
            },
            "event_profile": {
                "syslog_server_profile": 0
            },
            "id": 1,
            "ipfix": {
                "type": "mixed"
            },
            "log_digest": {
                "mixed": True
            },
            "log_monitor": {
                "type": "mixed"
            },
            "name": "System",
            "priority_level": "mixed",
            "syslog": {
                "type": "enabled"
            }
        }
        self.json_input = {'log': {'category': []}}

    def enable_all_log_category(self, msg=False):
        log_category = self.fw.api_get(self.url)
        for cate in log_category['log']['category']:
            demo = copy.deepcopy(self.demo)
            demo['id'] = cate['id']
            demo['name'] = cate['name']
            self.json_input['log']['category'].append(demo)
        # print(self.json_input)
        res = self.fw.api_put(self.url, msg, data=self.json_input)
        return res

    def edit_all_log_category(self, msg=False, **kwargs):
        log_category = self.fw.api_get(self.url)
        for cate in log_category['log']['category']:
            cate.update(**kwargs)
            self.json_input['log']['category'].append(cate)
        res = self.fw.api_put(self.url, msg, data=self.json_input)
        return res

    def get_all_log_categories(self):
        return self.fw.api_get(self.url)

    def logging_level(self, msg=False, level=''):
        if level == '':
            logger.error('Please choose logging level.')
            return False
        else:
            self.logginglevel['log']['categories']['logging_level'] = level.lower()
            json_input = copy.deepcopy(self.logginglevel)
        res = self.fw.api_put(self.url_level, msg, data=json_input)
        return res

    def logging_monitor_global(self, msg=False, enable_option=True):
        log_monitor_json = {
            "type": "enabled",
            "redundancy_interval": {}
        }
        json_input = copy.deepcopy(self.logginglevel)
        json_input['log']['categories']['global_category_attribute']['log_monitor'] = {}
        if enable_option:
            json_input['log']['categories']['global_category_attribute']['log_monitor'] = log_monitor_json
        res = self.fw.api_put(self.url_level, msg, data=json_input)
        return res

    def log_save_template(self, description, msg=False):
        if description == '':
            logger.error("Description can't be empty for custom template...")
            return False
        url = 'api/sonicos/log/save-template/' + str(description)
        resp = self.fw.api_post(url, msg)

    def import_template(self, template_name, msg=False):
        if template_name == '':
            logger.error("template name can't be empty...")
            return False
        url = 'api/sonicos/log/import-template/' + template_name
        resp = self.fw.api_post(url, msg)
        return resp

    def get_global_categories(self):
        url = 'api/sonicos/log/global-categories'
        return self.fw.api_get(url)

    def config_global_categories(self, msg=False, **kwargs):
        url = 'api/sonicos/log/global-categories'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def get_log_categories_by_name(self, name=''):
        if name == '':
            logger.error("name can't be empty when get log categories...")
            return False
        url = 'api/sonicos/log/categories/name/' + str(name)
        return self.fw.api_get(url)

    def edit_log_categories_by_name(self, name, msg=False, **kwargs):
        if name == '':
            logger.error("name can't be empty when edit log categories...")
            return False
        url = 'api/sonicos/log/categories/name/' + str(name)
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def get_log_categories_statistics_by_name(self, name=''):
        if name == '':
            logger.error("name can't be empty when get log categories...")
            return False
        url = 'api/sonicos/reporting/log/categories/name/' + str(name)
        return self.fw.api_get(url)

    def log_reset_event_count(self, category, msg=False):
        if category == '':
            logger.error("category can't be empty...")
            return False
        url = 'api/sonicos/log/reset/event-count/category/' + category
        resp = self.fw.api_post(url, msg)
        return resp
    
    def get_log_categories_statistics(self):
        url = 'api/sonicos/reporting/log/categories'
        return self.fw.api_get(url)

    def log_reset_all_event_count(self, msg=False):
        url = 'api/sonicos/log/reset/event-count/all'
        resp = self.fw.api_post(url, msg)
        return resp

    def log_reset_event_count_by_event_id(self, eventid, msg=False):
        if eventid == '':
            logger.error("eventid can't be empty...")
            return False
        url = 'api/sonicos/log/reset/event-count/event-id/' + str(eventid)
        resp = self.fw.api_post(url, msg)
        return resp

    def log_reset_event_count_by_group(self, category, group, msg=False):
        if group == '' or category == '':
            logger.error("group can't be empty...")
            return False
        url = 'api/sonicos/log/reset/event-count/category/' + category + '/group/' + group
        resp = self.fw.api_post(url, msg)
        return resp

    def get_log_category_groups_by_id(self, id=''):
        if id == '':
            logger.error("name can't be empty when get log category groups by id...")
            return False
        url = 'api/sonicos/log/groups/id/' + str(id)
        return self.fw.api_get(url)
    
    def get_log_groups_events(self):
        url = 'api/sonicos/log/events'
        return self.fw.api_get(url)
    
    def get_log_group_event_by_id(self, id=''):
        if id == '':
            logger.error("id can't be empty when get log  event by id...")
            return False
        url = 'api/sonicos/log/events/id/' + str(id)
        return self.fw.api_get(url)

    def edit_log_group_event_by_id(self, id, msg=False, **kwargs):
        if id == '':
            logger.error("id can't be empty when edit log category groups by id...")
            return False
        url = 'api/sonicos/log/events/id/' + str(id)
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp


    def edit_log_category_groups_by_id(self, id, msg=False, **kwargs):
        if id == '':
            logger.error("id can't be empty when edit log category groups by id...")
            return False
        url = 'api/sonicos/log/groups/id/' + str(id)
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def log_edit_email_alert(self, msg=False, name=''):
        url = 'api/sonicos/log/categories'
        if name == '':
            logger.error('Please input the name of log-> "System or Network or...".')
            return False
        else:
            log_category = self.fw.api_get(url)
            for cate in log_category['log']['category']:
                if cate.get('name') == name:
                    cate.get('email_alert').update(type='enabled')
            rc = self.fw.api_put(url, msg, data=log_category)
            if rc == False:
                return False
            for typ in log_category['log']['category']:
                if typ.get('name') == name:
                    TYP = typ.get('email_alert').get('type')
                    print("==============emai_alert=======type=============")
                    print(TYP)
                    if TYP == 'enabled':
                        return True
        return False


class SyslogSettingsApi:
    ''' syslog settings '''
    default_options = {
        # Setting portion
        'id'                : 'firewall',  # user defined string
        'name'              : '',  # server name or ip
        'port'              : 514,  # server port
        'facility'          : 'local-use0',  # facility
        'format'            : 'default',  # default, webtrends, enhanced-syslog, arcSight
        'type'              : 'syslog-server',  # syslog-server, analyzer
        'profile'           : 0,
        'enabled'           : True,
        # 'addr_obj'  : '',                  # syslog address object name

        # Switch
        # 'override_s': 'off',                 # on or off
        'en_erl'            : 'off',  # on or off
        'en_drl'            : 'off',  # on or off
        # 'en_ndpp'   : 'off',               # on or off

        'evt_lmt'           : 1000,  # rating limit, events / sec
        'data_lmt'          : 10000000,  # rating limit, bytes / sec

        # Add server portion
        # 'local_interface'   : '-1',  # local interface
        'outbound_interface': '',  # outboundnterface
    }

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/log/syslog/base'
        self.url = 'api/sonicos/log/syslog/syslog-servers'
        self.del_url = 'api/sonicos/log/syslog/servers/delete'

        self.server_json = {
            "log": {
                "syslog": {
                    "server": [{
                        "address": {"name": ""},
                        "port": 514,
                        "profile": 0,
                        "type": "syslog-server",
                        "format": "default",
                        "facility": "local-use0",
                        "id": "firewall",
                        "enabled": True,
                        "event_rate_limiting": {
                            # "enabled": True,
                            # "maximum_events": 1000
                        },
                        "data_rate_limiting": {
                            # "enabled": True,
                            # "maximum_bytes":   0
                        },
                        "outbound_interface": "",
                        # "local_interface": ""
                    }]
                }
            }
        }

    def edit_syslog_settings(self, msg=False, **kwargs):
        json_input = self.fw.api_get(self.base_url)
        path = json_input['log']['syslog']
        try:
            if 'id' in kwargs.keys():
                path['id'] = kwargs['id']
            if 'facility' in kwargs.keys():
                path['facility'] = kwargs['facility']
            if 'format' in kwargs.keys():
                path['format'] = kwargs['format']
            if 'evt_lmt' in kwargs.keys():
                path['event_rate_limiting']['value'] = kwargs['evt_lmt']
            if 'data_lmt' in kwargs.keys():
                path['data_rate_limiting']['value'] = kwargs['data_lmt']
            ### To be developed
            # if 'enhance' in kwargs.keys():
            # if 'arcsight' in kwargs.keys():
            if 'en_ndpp' in kwargs.keys():
                path['ndpp'] = kwargs['en_ndpp']
            if "connection_monitor" in kwargs:
                path["connection_monitor"] = kwargs["connection_monitor"]
        except KeyError:
            logger.error("Error: In creating JSON for syslog settings")
        resp = self.fw.api_put(self.base_url, msg, data=json_input)
        return resp

    def show_syslog_server(self):
        return self.fw.api_get(self.url)

    def add_syslog_server(self, msg=False, **kwargs):
        self.options = dict(SyslogSettingsApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = copy.deepcopy(self.server_json)

        ### add syslog server
        if 'name' not in kwargs.keys() or kwargs['name'] == '':
            logger.error('Log server name cannot be NULL!')
        else:
            json_input = self.build_json_syslog_server(json_input,**kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def add_syslog_server_custom(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def edit_syslog_server_custom_by_servername(self, servername, event_profile, msg=False, **kwargs):
        if servername == '' or event_profile == '':
            logger.error("name can't be empty ...")
            return False
        url = 'api/sonicos/log/syslog/syslog-servers/server/' + str(servername) + '/port/514/profile/' + str(
            event_profile)
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        if not resp:
            url = url+'/protocol/udp'
            resp = self.fw.api_put(url, msg, data=json_input)  
        return resp

    def edit_syslog_server(self, msg=False, **kwargs):
        ## get syslog server info and combine url
        ## use 'new_name' to modify the 'name' you need to edit.

        if 'name' not in kwargs.keys() or kwargs['name'] == '':
            logger.error('Log server name cannot be NULL!')
        else:
            syslog_servers = self.fw.api_get(self.url)
            get_json = ''
            if not syslog_servers['log']['syslog']:
                logger.error('Error!No syslog server can edit')
                return False
            for logserver in syslog_servers['log']['syslog']['server']:
                if logserver['address']['name'] == kwargs['name']:
                    get_json = logserver
                    break
            if get_json == '':
                logger.error('Error!! The syslog server that needs to be edited does not exist.')
                return False

            url = self.url + '/server/{}/port/{}/profile/{}'.format(
                get_json['address']['name'], str(get_json['port']), str(get_json['profile']))

            if 'new_name' in kwargs.keys():
                kwargs['name'] = kwargs['new_name']
                kwargs.pop('new_name')
            
            json_input = {"log": {"syslog": {"server": []}}}
            json_input['log']['syslog']['server'].append(get_json)
            
            json_input = self.build_json_syslog_server(json_input,**kwargs)
            resp = self.fw.api_put(url, msg, data=json_input)
            if not resp:
                url = url+'/protocol/udp'
                resp = self.fw.api_put(url, msg, data=json_input)
            return resp

    def delete_syslog_server(self, **kwargs):
        url = self.url + '/server/{}/port/{}/profile/{}'.format(
            kwargs['name'], kwargs['port'], kwargs['profile'])
        resp = self.fw.api_delete(url)
        if not resp:
            url = url+'/protocol/udp'
            resp = self.fw.api_delete(url)
        return resp

    def delete_all_syslog_servers(self):
        return self.fw.api_post(self.del_url)

    def build_json_syslog_server(self,json_input, **kwargs):
        path = json_input['log']['syslog']['server'][0]
        logger.info(kwargs)
        try:
            path['address']['name'] = kwargs['name']
            kwargs.pop('name')
            if 'port' in kwargs.keys():
                path['port'] = kwargs['port']
                kwargs.pop('port')
            else:
                path['port'] = 514

            path['event_rate_limiting'] = {"enabled": False}
            if 'en_erl' in kwargs.keys():
                if kwargs['en_erl'] == 'on':
                    path['event_rate_limiting'].update({"enabled": True})
                    path['event_rate_limiting'].update({"maximum_events": 1000})
                    if 'evt_lmt' in kwargs.keys():
                        path['event_rate_limiting']["maximum_events"]= kwargs['evt_lmt']
                        kwargs.pop('evt_lmt')
                elif kwargs['en_erl'] == 'off':
                    path['event_rate_limiting'] = {'enabled': False}
                kwargs.pop('en_erl')

            path['data_rate_limiting'] = {"enabled": False}
            if 'en_drl' in kwargs.keys():
                if kwargs['en_drl'] == 'on':
                    path['data_rate_limiting'].update({"enabled": True})
                    path['data_rate_limiting'].update({"maximum_bytes": 1000})
                    if 'data_lmt' in kwargs.keys():
                        path['data_rate_limiting']["maximum_bytes"] = kwargs['data_lmt']
                        kwargs.pop('data_lmt')
                elif kwargs['en_drl'] == 'off':
                    path['data_rate_limiting'] = {'enabled': False}
                kwargs.pop('en_drl')

            for kwd in kwargs.keys():
                if kwd in ['en_erl', 'en_drl', 'evt_lmt', 'data_lmt']:
                    continue
                path[kwd] = kwargs[kwd]

        except KeyError:
            logger.error("Error: In creating JSON for syslog server")
        logger.info("syslog server json obtained")
        logger.info(json_input)
        return json_input
    
    def get_syslog_settings(self):
        return self.fw.api_get(self.base_url)


class LogResolutionApi:
    default_resolution = {
        "log": {
            "name_resolution": {
                "method": "none"
            }
        }
    }

    def __init__(self, fw):
        self.fw = fw
        self.resolution_url = 'api/sonicos/log/name-resolution/base'


    def get_resolution(self):
        resp = self.fw.api_get(self.resolution_url)
        return resp

    def edit_resolution(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.resolution_url, msg, data=json_input)
        return resp
    
    def post_reset_name_cache(self):
        url = 'api/sonicos/log/name-resolution/reset-name-cache'
        response = self.fw.api_post(url)
        return response

class LogAWSApi:
    default_aws = {
        "log": {
            "aws": {
                "enable": False,
                "region": "north-virginia",
                "group_name": "",
                "stream_name": "",
                "synchronization_interval": 60,
                "send_log_when_full": True
            }
        }
    }

    def __init__(self, fw):
        self.fw = fw
        self.aws_url = 'api/sonicos/log/aws'


    def get_aws(self):
        resp = self.fw.api_get(self.aws_url)
        return resp

    def edit_aws(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.aws_url, msg, data=json_input)
        return resp
