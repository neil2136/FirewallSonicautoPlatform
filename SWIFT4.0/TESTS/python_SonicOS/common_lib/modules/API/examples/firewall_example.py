import sys
import os
#sys.path.append(os.environ["SONICOS_HOME"]+'/6.5.4/python_lib')
sys.path.append('/home/python_lib')
from utm import Firewall
from modules.API.firewall import ConfigModeApi
from modules.API.firewall import EmailObjectApi
from modules.API.firewall import ActionObjectApi
from modules.API.firewall import BandwidthObjectApi
from modules.API.firewall import AppRuleApi
from modules.API.firewall import AppControlApi
from modules.API.firewall import MatchObjectApi
from modules.API.firewall import AccessRuleApi
from modules.API.firewall import CfoObjectApi
from modules.API.firewall import CfoGroupApi

ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

configobject = ConfigModeApi(fw)

emailobject = EmailObjectApi(fw)
emailobject_dict = {
    'name': 'test',
    'match_type': 'partial',  #exact, partial, regex
    'content_entry': ['test123@qq.com']
}

emailobject_dict_edit = {
    'name': 'test',
    'match_type': 'exact',
    'content_entry': ['test123456@qq.com']
}
# rc = emailobject.add_email_object(**emailobject_dict)
# rc = emailobject.edit_email_object(**emailobject_dict_edit)
# rc = emailobject.get_email_object('test')
# rc = emailobject.delete_email_object(**emailobject_dict)


actionobject = ActionObjectApi(fw)
actionobject_dict1 = {
           "name": "test1",
           "action": "block-smtp-error-reply",
           "content": "Blocked by SOnicwall action object",
        }

actionobject_dict2 = {
           "name": "test2",
           "action": "http-block-page",
           "content": "http-block-page action object",
           "color": "white" # white, yellow, bule, red
        }
actionobject_dict2_edit = {
           "name": "test2",
           "action": "http-block-page",
           "content": "http-block-page action object test",
           "color": "red"
        }

actionobject_dict3_global = {
           "name": "test3",
           "action": "bandwidth-management",
           "bw_egress_priority": "realtime",  # realtime,highest,high,medium-high,medium,medium-low,low,lowest
           "bw_ingress_priority": "Highest",
        }
actionobject_dict3_advanced = {
           "name": "test34",
           "action": "bandwidth-management",
           "aggregation_method": "per-action",  # per-policy, per-action
           "usage_tracking": True,
           "bw_egress_object": "test1",
           "bw_ingress_object": "test1",
        }
# rc = actionobject.add_action_object(**actionobject_dict1)
# rc = actionobject.add_action_object(**actionobject_dict2)
# rc = actionobject.add_action_object(**actionobject_dict3)
# rc = actionobject.add_action_object(**actionobject_dict3_advanced)
# rc = actionobject.edit_action_object(**actionobject_dict2_edit)
# rc = actionobject.get_action_object('test2')
# rc = actionobject.delete_action_object(**actionobject_dict2_edit)

bandwidth_object = BandwidthObjectApi(fw)
bandwidthobject_dict ={
        "name": "test delay action",
        "guaranteed": {
            "kbps": { "value": 1000 }
        },
        "maximum": {
            "kbps": 1200
        },
        "priority": "realtime",
        "action": "delay", # delay ,drop
        "comment": "delayed",
        "per_ip_management": {
            "kbps": 1100
        }
    }

bandwidthobject_dict_edit ={
        "name": "test delay action",
        "guaranteed": {
            "mbps": { "value": 1000 }
        },
        "maximum": {
            "mbps": 1200
        },
        "priority": "highest",
        "action": "drop",
        "comment": "test test",
        "per_ip_management": {
            "mbps": 1100
        }
    }
# rc =bandwidth_object.add_bandwidth_object(**bandwidthobject_dict)
# rc=bandwidth_object.edit_bandwidth_object(**bandwidthobject_dict_edit)
# rc = bandwidth_object.get_bandwidth_object("test delay action")

# if rc:
#     print(rc)
#     print('Config emailobject success')
# else:
#     print('Config emailobject fail')

apprule_smtpclient = {
        "name": "smtptest",
        "type": {
            "smtp_client": True
        },
        "source": {
            "address": {
                "group": "All X0 Management IP"
            },
            "service": {
                "any": True
            }
        },
        "destination": {
            "address": {
                "group": "All WAN IP"
            },
            "service": {
                "name": "SMTP (Send E-Mail)"
            }
        },
        "exclusion": {
            "address": {
                "group": "All WAN IP"
            }
        },
        "match_object": {
            "object": "emailcc"
        },
        "action_object": "Reset/Drop",
        "users": {
            "included": {
                "group": "Everyone"
            },
            "excluded": {
                "guests": True
            }
        },
        "mail_from": {
            "included": "emailao",
            "excluded": "emailao"
        },
        "rcpt_to": {
            "included": "emailao",
            "excluded": "emailao"
        },
        # "schedule": {
        #     "days": {
        #         "days": "M-T-W-TH-F",
        #         "begin": "08:00",
        #         "end": "17:00"
        #     }
        # },dts 221568
        "flow_reporting": True,
        "logging": True,
        "log": {
            "individual": True,
            "redundancy": {
                "global": True
            }
        },
        "connection_side": "client",
        "direction": {
            "advanced": {
                "from": {
                    "zone": "LAN"
                },
                "to": {
                    "zone": "WAN"
                }
            }
        }
    }

apprule_pop3client = {
        "name": "popclienttest",
        "type": {
            "pop3": "client"
        },
        "source": {
            "address": {
                "group": "All Interface IP"
            },
            "service": {
                "any": True
            }
        },
        "destination": {
            "address": {
                "group": "All Interface IP"
            },
            "service": {
                "name": "POP3 (Retrieve E-Mail)"
            }
        },
        "exclusion": {
            "address": {
                "group": "All X4 Management IP"
            }
        },
        "match_object": {
            "object": "custom"
        },
        "action_object": "Reset/Drop",
        "users": {
            "included": {
                "group": "Everyone"
            },
            "excluded": {
                "administrator": True
            }
        },
        "schedule": {
            "always_on": True
        },
        "flow_reporting": False,
        "logging": True,
        "log": {
            "individual": False,
            "redundancy": {
                "global": True
            }
        },
        "connection_side": "client",
        "direction": {
            "advanced": {
                "from": {
                    "zone": "LAN"
                },
                "to": {
                    "zone": "WAN"
                }
            }
        }
    }

apprule_pop3server = {
        "name": "popservertest",
        "type": {
            "pop3": "server"
        },
        "source": {
            "address": {
                "name": "X0 Subnet"
            },
            "service": {
                "name": "POP3 (Retrieve E-Mail)"
            }
        },
        "destination": {
            "address": {
                "name": "X1 Subnet"
            },
            "service": {
                "any": True
            }
        },
        "exclusion": {
            "address": {
                "name": "X1 Subnet"
            }
        },
        "match_object": {
            "object": "emailcc"
        },
        "action_object": "No Action",
        "users": {
            "included": {
                "administrator": True
            },
            "excluded": {
                "group": "Guest Services"
            }
        },
        "schedule": {
            "always_on": True
        },
        "flow_reporting": False,
        "logging": False,
        "log": {
            "individual": False,
            "redundancy": {
                "global": True
            }
        },
        "connection_side": "server",
        "direction": {
            "basic": "incoming"
        }
    }

apprule_httpclient={
    "name": "httpclient",
    "type": {
        "http": "client"
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
            "group": "All Interface IP"
        },
        "service": {
            "name": "HTTP"
        }
    },
    "exclusion": {
        "address": {
            "group": "All Interface IP"
        }
    },
    "match_object": {
        "included": "custom",
        "excluded": ""
    },
    "action_object": "test",
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
        "individual": True,
        "redundancy": {
            "global": True
        }
    },
    "connection_side": "client",
    "direction": {
        "basic": "incoming"
    }
}

apprule_ips = {
    "name": "ips",
    "type": {
        "ips": True
    },
    "address": {
        "any": True
    },
    "exclusion": {
        "address": {}
    },
    "match_object": {
        "object": "ips_match"
    },
    "action_object": "Bypass DPI",
    "users": {
        "included": {
            "all": True
        },
        "excluded": {}
    },
    "ips_message_format": True,
    "zone": {
        "any": True
    }
}

apprule_appcontrol={
    "name": "appcontrol",
    "type": {
        "app_control": True
    },
    "source": {
        "address": {
            "name": "X0 Subnet"
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
            "any": True
        }
    },
    "exclusion": {
        "address": {}
    },
    "match_object": {
        "object": "app"
    },
    "action_object": "test",
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
    "zone": {
        "name": "LAN"
    }
}

apprule_appcontrol_edit={
    "name": "appcontrol",
    "type": {
        "app_control": True
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
            "any": True
        }
    },
    "exclusion": {
        "address": {}
    },
#    "match_object": {
#        "object": "app"
#    },
    "match_object": {
        "included": "app",
        "excluded": ""
    },  # dts 221725
    "action_object": "test",
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
    "zone": {
        "name": "WAN"
    }
}

apprule_object = AppRuleApi(fw)
apprule_setting_dict = {
    "enable": True,
    "log_redundancy":10
}

# apprule_object.config_apprule_setting(**apprule_setting_dict)
# apprule_object.get_apprule_setting()
# apprule_object.add_apprule_object(**apprule_smtpclient)
# apprule_object.add_apprule_object(**apprule_pop3client)
# apprule_object.add_apprule_object(**apprule_pop3server)
# apprule_object.add_apprule_object(**apprule_httpclient)
# apprule_object.add_apprule_object(**apprule_ips)
# apprule_object.add_apprule_object(**apprule_appcontrol)
#
# apprule_object.edit_apprule_object(**apprule_appcontrol_edit)
# apprule_object.delete_apprule_object_byname(**apprule_appcontrol_edit)
# apprule_object.delete_apprule_object_byname('appcontrol')

# apprule_object.get_apprule_object('appcontrol')



appcontrol_object = AppControlApi(fw)
ac_global = {
    "enable": True,
    "log_all": True,
    "log_filename": True,
    "log_redundancy": 10,
}
ac_category= {
    "type": "category",
    "name": "IM",
    "id": 11,
    "block": False,
    "log": {
        "enable": True,   #default:"global": True,
    },
    "included": {
        "ip": {
            "all": True
        },
        "users": {
            "guests": True  #"group": "Everyone" , #"
        }
    },
    "excluded": {
        "ip": {},
        "users": {}
    },
    "schedule": {
        "name": "Work Hours"
    },
    "log_redundancy": {
        "global": True  #"filter": 20
    }
}

ac_application = {
    "type": "application",
    "category": "BAAKUP-APPS",
    "name": "360 Yunpan",
    "id": 1926,
    "block": {
        "enable": True
    },
    "log": {
        "category": True,
    },
    "included": {
        "ip": {
            "all": True
        },
        "users": {
            "group": "Everyone"
        }
    },
    "excluded": {
        "ip": {"group": "All Interface IP"},
        "users": {}
    },
    "schedule": {
        "always_on": True
    },
    "log_redundancy": {
        "filter": 20
    }
}


ac_signature = {
    "type": "signature",
    "category": "BACKUP-APPS",
    "application": "360 Yunpan",
    "name": "DNS Activity",
    "id": 11352,
    "block": {
        "enable": True
    },
    "log": {
    }, #dibable log
}

exclude_list_dict = {
    'ips': True
}
exclude_list_dict_1 = {
    #'object_name': 'X0 Subnet', # object_name,object_name only one can be specified
    'object_group': 'LAN Subnets',

}

appcontrol_object.config_appcontrol_global(**ac_global)
appcontrol_object.get_appcontrol_setting()
appcontrol_object.reset_appcontrol_setting()
appcontrol_object.config_ac_by_category(**ac_category)
appcontrol_object.config_ac_by_application(**ac_application)
appcontrol_object.config_ac_by_signature(**ac_signature)
appcontrol_object.config_ac_exclusion(**exclude_list_dict)
appcontrol_object.config_ac_exclusion(**exclude_list_dict_1)


###############################
##########Match objects 
###################################

matchonj = MatchObjectApi(fw)

def delete_matchobject(name):
    match_object={"object_type":"email-to",
    "name":"email To"}
    get_resp=matchonj.get_matchobject(url)
    if "match_objects" in get_resp.keys():
            list_of_match_obj=get_resp['match_objects']
            for mat_obj in list_of_match_obj:
                if mat_obj["name"]==name:
                    print("in a list")
                    del_url=url+"name"+'/'+name
                    del_response=matchonj.del_matchobject(del_url)
            num_param=1
    elif "match_object" in get_resp.keys():
        match_obj=get_resp['match_object']
        if match_obj["name"]==name:
            num_param=0
            del_url=url+"name"+'/'+name
            del_response=matchonj.del_matchobject(del_url)
            print(del_response)
        else:
            num_param=1
    print(get_resp)

def make_activex():
    match_object = {"object_type":"activex-class-id",
            "name":"activex",
            "match_type":"exact",
            "input_representation":"hexadecimal",
            "content_entry":[{"content_entry": "12345671"},{"content_entry": "1234"}]
            }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)

def delete_activex():
    delete_matchobject("activex")


def make_email_body():
    match_object={"object_type":"email-body",
        "name":"email body2",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "content_entry":[{"content_entry": "112"},{"content_entry": "1234"}]
        }
    # make_and_delete_email_body()
    print("before get")
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)
def delete_email_body():
        delete_matchobject("email body2")

def make_email_CC():
    match_object={"object_type":"email-cc",
        "name":"email cc",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)
def delete_email_CC():
    delete_matchobject("email cc")

def make_email_from():
    match_object={"object_type":"email-from",
        "name":"email from",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_email_from():
    delete_matchobject("email from")


def make_email_subject():
    match_object={"object_type":"email-subject",
        "name":"email subject1",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    


def delete_email_subject():
    delete_matchobject("email subject1")

def make_email_to():
    match_object={"object_type":"email-to",
        "name":"email To",
        "match_type":"partial",
        # "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_email_to():
    delete_matchobject("email To")

def make_email_size():
    match_object={"object_type":"email-size",
        "name":"email size",
        "email_size": 20
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_email_size():
    delete_matchobject("email size")

def make_file_extension():
    match_object={"object_type":"file-extension",
        "name":"file extension",
        "match_type":"exact",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_file_extension():
    delete_matchobject("file extension")

def make_file_name():
    match_object={"object_type":"file-name",
        "name":"file name1",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_file_name():
    delete_matchobject("file name1")

def make_ftp_command():
    match_object={"object_type":"ftp-command",
        "name":"ftp command",
        "ftp_command": [{"ftp_command": "allocate"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_ftp_command():
        delete_matchobject("ftp command")

def make_http_cookie():
    match_object={"object_type":"http-cookie",
        "name":"http-cookie123",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_cookie():
        delete_matchobject("http-cookie123")   

def make_http_host():
    match_object={"object_type":"http-host",
        "name":"http-host",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_host():
    delete_matchobject("http-host")   

def make_http_referer():
    match_object={"object_type":"http-referer",
        "name":"http referer",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_referer():
    delete_matchobject("http referer")

def make_set_cookie():
    match_object={"object_type":"http-set-cookie",
        "name":"http set cookie",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_set_cookie():
    delete_matchobject("http set cookie")

def make_uri_content():
    match_object={"object_type":"http-uri-content",
        "name":"http uri content1",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_uri_content():
    delete_matchobject("http uri content1")

def make_http_url():
    match_object={"object_type":"http-url",
        "name":"http url1",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }   
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_url():
    delete_matchobject("http url1")

def make_http_user_agent():
    match_object={"object_type":"http-user-agent",
        "name":"http user agent",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": True,
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_user_agent():
    delete_matchobject("http user agent")

def make_file_content():
    match_object={"object_type":"file-content",
        "name":"file-content",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "content_entry":[{"content_entry": "123456789abcde"},{"content_entry": "1234"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_file_content():
    delete_matchobject("file-content")

def make_file_cmd_val():
    match_object={"object_type":"ftp-command-value",
        "name":"ftp-command-value",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": False,
        "ftp_command": [{"ftp_command": "account"}],
        "argument": [{"argument": "try2"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_file_cmd_val():
    delete_matchobject("ftp-command-value")

def make_mime_cust_header():
    match_object={"object_type":"mime-custom-header",
        "name":"mime-custom-header",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": False,
        "custom_header": "CustomheaderName",
        "content_entry": [{"content_entry": "try3"}]
    }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_mime_cust_header():
    delete_matchobject("mime-custom-header")

def make_http_request_custom_header():
    match_object={"object_type":"http-request-custom-header",
    "name":"http-request-custom-header",
    "match_type":"partial",
    "input_representation":"alphanumeric",
    "negative_matching": False,
    "custom_header": "CustomheaderName",
    "content_entry": [{"content_entry": "try2"}]
    }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_request_custom_header():
    delete_matchobject("http-request-custom-header")

def make_http_response_custom_header():
    match_object={"object_type": "http-response-custom-header",
        "name": "http-response-custom-header",
        "match_type":"partial",
        "input_representation":"alphanumeric",
        "negative_matching": False,
        "custom_header": "CustomheaderName",
         "content_entry": [{"content_entry": "try2"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_http_response_custom_header():
    delete_matchobject("http-request-custom-header")

def make_web_browser():
    match_object={"object_type": "web-browser",
        "name": "web-browser",
        "match_type":"partial",
        "negative_matching": False,
        "browser": [{"browser": "netscape"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_web_browser():
    delete_matchobject("web-browser")

def make_IPS_signature_category_list():
    match_object={"object_type": "ips-signature-category-list",
        "name": "ips-signature-category-list",
        "ips": {"category": [{"id": 61}]}
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_IPS_signature_category_list():
    delete_matchobject("ips-signature-category-list")

def make_IPS_signature_list():
    match_object={"object_type":"ips-signature-list",
        "name":"ips-signature-list",
        "ips": {"policy": [{"category": {"id": 61},"signature": {"id": 5086}}]}
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_IPS_signature_list():
    delete_matchobject("ips-signature-list")

def make_Application_category_list():
    match_object={"object_type": "application-category-list",
        "name": "application-category-list",
        "category": [{"id": 55}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_application_category_list():
    delete_matchobject("application-category-list")

def make_application_list():
    match_object={"object_type": "application-list",
        "name": "application-list",
        "application": [{"category": {"id": 55},"app": {"id": 437}}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_application_list():
    delete_matchobject("application-category-list")

def make_application_signature_list():
    match_object={"object_type": "application-signature-list",
        "name":"application-signature-list",
        "signature": [{"category": {"id": 55},"app": {"id": 437},"sig": {"id": 5600}}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_application_signature_list():
    delete_matchobject("application-signature-list")

def make_log_email_user():
    match_object={
        "object_type": "log-email-user",
        "name":"log-email-user",
     }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)    

def delete_log_email_user():
    delete_matchobject("log-email-user")

def make_custom_nonen():
    match_object={"object_type":"custom",
        "name":"custom default",
        "match_type":"exact",
        "enable": False,
        "input_representation":"alphanumeric",
        "content_entry": [{"content_entry": "try1"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)   

def delete_custom_nonen():
    delete_matchobject("custom default")

def make_custom_en():
    match_object={"object_type":"custom",
        "name":"custom Enable",
        "match_type":"exact",
        "enable": True,
        "input_representation":"alphanumeric",
        "offset": 2,
        "depth": 1500,
        "min_size": 1,
        "max_size": 1500,
        "content_entry": [{"content_entry": "try1"}]
        }
    delete_matchobject(match_object["name"])
    config_matchobject=matchonj.config_matchobject(url=url,**match_object)   

def delete_custom_en():  
    delete_matchobject("custom Enable")

def edit_match_object():
    json_put_match_object={
    "match_objects": [
        {
            "name": "http referer",
            "type": "http-referer",
            "match_type": "partial",
            "negative_matching": True,
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "http set cookie",
            "type": "http-set-cookie",
            "match_type": "partial",
            "negative_matching": True,
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "http uri content1",
            "type": "http-uri-content",
            "match_type": "partial",
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "http url1",
            "type": "http-url",
            "match_type": "partial",
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "http user agent",
            "type": "http-user-agent",
            "match_type": "partial",
            "negative_matching": True,
            "input_representation": "alphanumeric",
            "content_entry": [
                {
                    "content_entry": "123456789abcde"
                },
                {
                    "content_entry": "1234"
                }
            ]
        },
        {
            "name": "ftp-command-value",
            "type": "ftp-command-value",
            "match_type": "partial",
            "negative_matching": False,
            "input_representation": "alphanumeric",
            "ftp_command": [
                {
                    "ftp_command": "account"
                }
            ],
            "argument": [
                {
                    "argument": "try2"
                }
            ]
        },
        {
            "name": "http-response-custom-header",
            "type": "http-response-custom-header",
            "match_type": "partial",
            "negative_matching": False,
            "input_representation": "alphanumeric",
            "custom_header": "CustomheaderName",
            "content_entry": [
                {
                    "content_entry": "try2"
                }
            ]
        },
        {
            "name": "application-list",
            "type": "application-list",
            "application": [
                {
                    "category": {
                        "id": 55
                    },
                    "app": {
                        "id": 437
                    }
                }
            ]
        },
        {
            "name": "activex",
            "type": "application-list",
            "application": [
                {
                    "category": {
                        "id": 55
                    },
                    "app": {
                        "id": 437
                    }
                }
            ]
        }
    ]
}
    # url1=url+"name"+"/"+"activex"
    print("url")
    put_match_resp=matchonj.put_match_object(json_put_match_object,url)
Accessrule=AccessRuleApi(fw)
url='/access-rules/ipv4'
def test_post_access_rule_ipv4():
    access_rule = {
            'name': 'test1',
            'enable': True,
            'from': 'WAN',
            'to': 'LAN',
            'action': 'deny',
            'source': {
                'address': {
                    'any': True},
                'port': {
                    'any': True}},
            'service': {
                    'name': '6over4'},
            'destination': {
                'address': {
                    'any': True}},
            'schedule': {
                'always_on': True},
            'users': {
                'included': {
                    'all': True},
                'excluded': {
                    'none': True}},
            'comment': 'testin from automation framework',
            'fragments': True,
            'logging': True,
            'sip': False,
            'h323': False,
            'flow_reporting': False,
            'botnet_filter': False,
            'geo_ip_filter': False,
            'packet_monitoring': False,
            'management': False,
            'max_connections': 100,
            'priority': {
                'auto': True},
            'tcp': {'timeout': 15,
                    'urgent': False},
            'udp': {'timeout': 30},
            'connection_limit': {
                'source': {},
                'destination': {}},
            'dpi': True,
            'dpi_ssl': {
                'client': True,
                'server': True},
            'quality_of_service': {
                'dscp': {
                    'map': True},
                'class_of_service':
                {'map': True}}}
    #urilist_object = {"content_filter": {"uri_list_object": [{"name": "", "uri": [{"uri":"dd"}], "keyword": [{"uri":"ddd"},{"uri":"dddf"}]}]}}
    response=Accessrule.config_accessrule(**access_rule)
    print (response)
    print("-----------------------------------test_post_access_rule_ipv4 completed---------------------------------------------------------")


def test_delete_accessrule_using_name():
    url="/access-rules/ipv4/name/test1"
    response=Accessrule.delete_accessrule(url)
    print(response)
    print("-----------------------------------test_delete_accessrule_using_name---------------------------------------------------------")
def test_delete_accessrule_using_body():
    access_rule = {
    "access_rules": [
        {
            "ipv4": {
        'name': 'test1',
        'enable': True,
        'from': 'WAN',
        'to': 'LAN',
        'action': 'deny',
        'source': {
                'address': {
                    'any': True},
                'port': {
                    'any': True}},
        'service': {
                'name': '6over4'},
        'destination': {
            'address': {
                'any': True}},
        'schedule': {
            'always_on': True},
        'users': {
            'included': {
                'all': True},
            'excluded': {
                'none': True}},
        'comment': 'testin from automation framework',
            'fragments': True,
            'logging': True,
            'sip': False,
            'h323': False,
            'flow_reporting': False,
            'botnet_filter': False,
            'geo_ip_filter': False,
            'packet_monitoring': False,
            'management': False,
            'max_connections': 100,
            'priority': {
                'auto': True},
            'tcp': {'timeout': 15,
                    'urgent': False},
            'udp': {'timeout': 30},
            'connection_limit': {
                'source': {},
                'destination': {}},
            'dpi': True,
            'dpi_ssl': {
                'client': True,
                'server': True}}}]}
    url = "/access-rules/ipv4"
    response=Accessrule.delete_accessrule(url,data=access_rule)
    print(response)
    print("-----------------------------------test_delete_accessrule_using_body---------------------------------------------------------")

def test_get_accessrule_using_name():
    url="/access-rules/ipv4/name/test1"
    response=Accessrule.get_accessrule(url)
    print("-----------------------------------test_get_accessrule_using_name---------------------------------------------------------")

def test_put_access_rule_ipv4():
    access_rule = {
            'name': 'test1',
            'enable': False,
            'from': 'WAN',
            'to': 'LAN',
            'action': 'deny',
            'source': {
                'address': {
                    'any': True},
                'port': {
                    'any': True}},
            'service': {
                    'name': '6over4'},
            'destination': {
                'address': {
                    'any': True}},
            'schedule': {
                'always_on': True},
            'users': {
                'included': {
                    'all': True},
                'excluded': {
                    'none': True}},
            'comment': 'testin from automation framework',
            'fragments': True,
            'logging': True,
            'sip': False,
            'h323': False,
            'flow_reporting': False,
            'botnet_filter': False,
            'geo_ip_filter': False,
            'packet_monitoring': False,
            'management': False,
            'max_connections': 100,
            'priority': {
                'auto': True},
            'tcp': {'timeout': 15,
                    'urgent': False},
            'udp': {'timeout': 30},
            'connection_limit': {
                'source': {},
                'destination': {}},
            'dpi': True,
            'dpi_ssl': {
                'client': True,
                'server': True},
            'quality_of_service': {
                'dscp': {
                    'map': True},
                'class_of_service':
                {'map': True}}}
    response=Accessrule.put_accessrule(**access_rule)
    print(response)
    print("-----------------------------------test_put_access_rule_ipv4---------------------------------------------------------")










test_post_access_rule_ipv4()
test_get_accessrule_using_name()
test_put_access_rule_ipv4()
test_get_accessrule_using_name()
test_delete_accessrule_using_name()
test_post_access_rule_ipv4()
#time.sleep(10)
test_delete_accessrule_using_body()

# edit_match_object()
# make_email_body()
# make_activex()
delete_activex()
delete_email_body()
# make_email_CC()
# # delete_email_CC()
# make_email_from()
# # # # delete_email_from()
# make_email_subject()
# # # # delete_email_subject()
# make_email_to()
# # # # delete_email_to()
# make_email_size()
# # # # # delete_email_size()
# make_file_extension()
# # # # # delete_file_extension()
# make_file_name()
# make_ftp_command()
# # # # delete_ftp_command()
# make_http_cookie()
# # # # delete_http_cookie()
# make_http_host()
# # # # delete_http_host()
# make_http_host()
# # # delete_http_host()
# make_http_referer()
# # # delete_http_referer()
# make_set_cookie()
# # # # delete_set_cookie()
# make_uri_content()
# # # # delete_uri_content()
# make_http_url()
# # # # delete_http_url()
# make_http_user_agent()
# # # delete_http_user_agent()
# make_file_content()
# # delete_file_content()
# # # # # delete_file_content()
# make_mime_cust_header()
# # delete_mime_cust_header()
# # # make_file_cmd_val()
# make_http_request_custom_header()
# # delete_http_request_custom_header()
# make_http_response_custom_header()
# # delete_http_response_custom_header()
# make_web_browser()
# # delete_web_browser()
# make_IPS_signature_category_list()
# # delete_IPS_signature_category_list()
# make_IPS_signature_list()
# # delete_IPS_signature_list()
# make_Application_category_list()
# # delete_application_category_list()
# make_application_list()
# # delete_application_list()
# make_application_signature_list()
# # delete_application_signature_list()
# make_log_email_user()
# # delete_log_email_user()
# make_custom_nonen()
# # delete_custom_nonen()
# make_custom_en()
# # delete_custom_en()

cfo_obj = CfoObjectApi(fw)
cfg_obj = CfoGroupApi(fw)
grp = {
    'grp_name': 'uri_group',
    'obj_name': ['uri_keyword', 'uri_domain']

}
cfg_obj.configure_cfo_group(**grp)
cfo1 = {
    'object_name': 'uri_uri11',
    'url_name': ['baidu.com', '163.com'],
}
rc = cfo_obj.configure_cfo_object(**cfo1)

cfo2 = {
    'object_name': 'uri_keyword_11',
    'keyword': ['baidu', '163']
}
rc = cfo_obj.configure_cfo_object(**cfo2)

cfo3 = {
    'object_name': 'uri_domain_11',
    'domain': ['baidu.com', '163.com']
}
rc = cfo_obj.configure_cfo_object(**cfo3)



default_acl_dict = {
    "name": "Default Access Rule",
    "enable": True,
    "from": "LAN",
    "to": "WAN",
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
            'all': True
        },
        "excluded": {
            "none": True
        }
    },
    "comment": "",
    "fragments": True,
    "logging": True,
    "sip": False,
    "h323": False,
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
    "priority": {
        "manual": {
            "value": 13
        }
    },
    "tcp": {
        "timeout": 15,
        "urgent": False
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
    "redirect_unauthenticated_users_to_log_in": True,
    "quality_of_service": {
        "class_of_service": {},
        "dscp": {
            "preserve": True
        }
    }
}
getres = accessruleapi.get_accessrule_via_zones(srczone='LAN', dstzone='WAN')
    if 'access_rules' in getres:
        for rule in getres['access_rules']:
            if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                logger.info(f'get target rule successful: {rule}')
                res1 = accessruleapi.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'],
                                                                    acl_json=default_acl_dict)
