import sys
from pprint import pprint
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
from utm import Firewall
from modules.API.log import LogAutomationApi
from modules.API.log import LogSettingsApi

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
log_automation_obj = LogAutomationApi(fw)
log_settings_obj = LogSettingsApi(fw)


################# LogAutomationApi ##################################

# output = log_automation_obj.show_log_automation()

edit_log_automation =  {
    "log": {
        "automation": {
            "email_address": {
                "log": "",
                "alert": "",
                "user": ""
            },
            "send_log": {
                "when_full": True
            },
            "email_format_log": {
                "plain_text": True
            },
            "include_all_log_information": True,
            "health_check_email": {
                "schedule": {}
            },
            "mail_server": "",
            "mail_from": "",
            "authentication_method": "none",
            "mail_server_advanced": {
                "smtp_port": 25,
                "connection_security_method": {},
                "smtp_authentication": False
            },
            "ftp_log": {
                "send_log_to_ftp": False,
                "server": "0.0.0.0",
                "user_name": "admin",
                "password": "6,d1a8ee54400db9d4fb21e52737f48dba06a2fe3ef04171976e87b6bfb3b8927f408a5dd21377ef0ea48d6340b0b2f9a0180fdc67239d84df7e7bc4400a3862a9",
                "directory": "logs",
                "send_log": {
                    "when_full": True
                },
                "file_format": {
                    "plain_text": True
                },
                "include_all_log_information": False
            }
            # "solera": {
            #     "solera_capture_stack_integration": false,
            #     "server": {},
            #     "protocol": "https",
            #     "port": 443,
            #     "deepsee_base_url": "https://$host:$port/deepsee_reports#pathIndex=/timespan/$start_$stop/$ipproto_port/$srcport_and_$dstport/ipv4_address/$srcip_and_$dstip",
            #     "pcap_base_url": "https://$host:$port/ws/pcap?method=deepsee&path=/timespan/$start_$stop/$ipproto_port/$srcport_and_$dstport/ipv4_address/$srcip_and_$dstip",
            #     "link_icon": "data:image/gif;base64,R0lGODlhFAAUAPeYAOXo7+Xo8P7+/vz7/Pv6/Pr5+/39/fz8/eXo8fj4+tHT2ru+yfv7/NPV3MbJ0fHy9L3Ays7Ozv39/tze49/g5cvO2MvO1cvN1d/f4b/CzKWlpvLy8szO1uXm6snL08DDzenq7d3f5MXI0ebn62xsbX59fubp8WhoaXl5er/Aw/f3+MjL1Ofo7OTn7nFxcuHk7OPm7cfJ0o6OjrW1tuTl6tve5r7By9XX3r7Bx8/S2+Tk5MnM0tfZ38rO19rd5by/yYqKitXX3d/i6tbY3peXl3d3ePX2+JOVmczQ2Xx7fFRWWNDS3O/w8vz8/E9QUtvd4pKRknh4eM7Q2erq7o2Njtzf5uLl7M7Q2lZXWY6NjuLj6Hl5eZubm66urvHw8qOjpeDj6nBwcJ2fpPHx8fj4+fj4+Pb2+FNUVvj5+qurrGZnau3u8cnM1LOztMLFzouNkdfY37y/xc7Q2GFiZbi7xvf3+bm8x+/v8mBhZM7R2np6e5mbn9ja4PLx9bS0taqqq1hZXODh5oaFhpGRkbq8wrKyss3NznV3et3f5+Lk6ExNT9/e387P19LU2+Ll7d3f6bq9x3d4fPP09fn6+tbY4ba5vtDS2erq7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJgALAAAAAAUABQAAAj/ADEJFMhghCUHCBuAMDCwoUABgSAoYPGgIg05Hzo4FNiEww1JAkKKFHBHQQMJDQVY4DNyQ4QUMyJsEMCjQcMJQQzoNFCGyxYig6IUGmNAgUZMaBYYOcD0QJsiOpgaCqPhwJoMKCnAGcCVK5AuXQfIKMGVEQhMbC4RWLtWkB+2BKDoWaulEaYPfQro1ashiRe9i05k0TvFAyY7dRIoToAhjQsUf76QoIJBMRM3mH5YAcB5h5ozb45EOiQGDGcAiERgilGFM445TrBUOk0bACUFmEJI4QxIkRJCtWmvGIHJDKQWAPbgiRP8tBAIDAQOQRKguvXr1itQGGhAxBLs4K9wMxDQkIyFHo8QqF+PwFGFC9E3JlqQowYMEy985FnwhPxGgSpM4IENdGRwQQiT/KfgggIFBAA7",
            #     "address_to_link": "lan"
            # }
        }
    }
}
# output = log_automation_obj.edit_log_automation(**edit_log_automation)


################# LogAutomationApi ##################################

# output = log_settings_obj.show_event(event_id='1640')

edit_log_automation = {
    "log": {
        "event": [
            {
                "id": 1640,
                "name": "Policy Matched",
                "category": "Unified Policy Engine",
                "group": "Policy Action",
                "priority_level": "inform",
                "log_monitor": {
                    "redundancy_interval": 0
                },
                "email_alert": {
                    "redundancy_interval": 0
                },
                "syslog": {
                    "redundancy_interval": 0
                },
                "ipfix": {
                    "redundancy_interval": 0
                },
                "event_profile": {
                    "syslog_server_profile": 0
                },
                "log_digest": True,
                "color": {
                    "hex": "0x00000000"
                },
                "alert_email": {}
            }
        ]
    }
}

# output = log_settings_obj.edit_event(event_id='1640', **edit_log_automation)

