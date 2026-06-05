import sys
import os
#sys.path.append(os.environ["SONICOS_HOME"]+'/6.5.4/python_lib')
sys.path.append('/home/python_lib')
from utm import Firewall
from modules.API.firewall import EmailObjectApi
from modules.API.firewall import ActionObjectApi
from modules.API.firewall import BandwidthObjectApi
from modules.API.firewall import AppRuleApi
from modules.API.firewall import AppControlApi
ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

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
            "kbps": 1000
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
            "mbps": 1000
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
