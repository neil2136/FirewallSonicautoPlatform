import os
import sys
import re
import time
import json
import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from networkdevice import Host
from tools.trafficGen import MyFtp

suite_path = os.environ['PYTHON_SONICOS_HOME'] + \
    '/Log/App_Control_Filename_Logging/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/App_Control_Filename_Logging/testcases")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/App_Control_Filename_Logging")
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/App_Control_Filename_Logging/testplan/testplan.json'
CERT_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Log/App_Control_Filename_Logging/definition/cert/dovecot_1k.p12'
libPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/lib'

from lib.modules.API import log,network,firewallsettings,system,\
    sslvpn,firewall,policy,sslvpn,vpn,users,dpissl,wireless,accesspoint
from lib.modules.CLI.system import LicenseCli, DiagnosticsCli
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall

from tools.send_fetch_email import Email
from definition.send_recv_email import *

os_obj = Openstack(Params.testbed)


PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')
# PC1_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC1', 'eth1')
# PC2_ETH1_IPV6 = os_obj.get_node_interface_ipv6('PC2', 'eth2')
PC1_ETH1_IPV6 = "2000::169"
PC2_ETH1_IPV6 = "2001::169"

PC1_login = Host(PC1_ETH2_IP)
PC2_login = Host(PC2_ETH2_IP)

logger.info("\n" + "-" * 30 + "\n" \
    + "PC1_ETH1_IP(X0 PC) :" + PC1_ETH1_IP + "\n" \
    + "PC1_ETH1_IPV6 :" + PC1_ETH1_IPV6 + "\n" \
    + "PC1_ETH2_IP :" + PC1_ETH2_IP + "\n" \
    + "PC2_ETH1_IP(X1 PC) :" + PC2_ETH1_IP + "\n" \
    + "PC2_ETH1_IPV6 :" + PC2_ETH1_IPV6 + "\n" \
    + "-" * 30
)


mailserver_eth0 = '12.12.1.169'
mail_user = 'sahil'
mail_pwd = 'password'
mail = Email(mailserver_eth0, mail_user, mail_pwd, use_ssl=True)

my_ftp_v4 = MyFtp(host=PC2_ETH1_IP, user='root', password='password')
my_ftp_v6 = MyFtp(host=PC2_ETH1_IPV6, user='root', password='password')

localfile = '/root/Downloads/test.txt'
remotefile = '/var/www/html/virus/test.txt'
MailServerfile = os.environ["PYTHON_SONICOS_HOME"] + '/Log/App_Control_Filename_Logging/definition/confs/mailserver/'
http_confs_path = os.environ["PYTHON_SONICOS_HOME"] + '/Log/App_Control_Filename_Logging/config/httpserver'

# parameters on the openstack
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X2_IP = "13.13.1.168"
    X0_IPV6 = '2000::168'
    X1_IPV6 = '2001::168'
    MASK = '255.255.255.0'
    DNS1 = Params.G_DNS1
    DNS2 = Params.G_DNS2
    platform = os_obj.get_node_platform('UTM')

# settings in TestInitConfig
x0_static_dict = {
    'if': 'X0',
    'zone': 'LAN',
    'mode': 'static',
    'ip': '192.168.168.168',
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_https': True,
}

x2_static_dict = {
    'if': 'X2',
    'zone': "DMZ",
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': Parameter.MASK,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'user_https': True,
}

x1_static_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'netmask': Parameter.MASK,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.DNS1,
    'dns2': Parameter.DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_https': True,
}

x0_opt_ipv6 = {
  "interfaces": [
    {
      "ipv6": {
        "one_arm_mode": False,
        "one_arm_peer": "",
        "management": {
          "https": True,
          "https_source": {
            "any": True
          },
          "ping": True,
          "ping_source": {
            "any": True
          },
          "snmp": True,
          "snmp_source": {
            "any": True
          },
          "ssh": True,
          "ssh_source": {
            "any": True
          }
        },
        "user_login": {
          "http": True,
          "https": True
        },
        "ipv6_traffic": True,
        "listen_router_advertisement": False,
        "duplicate_address_detection_transmits": 1,
        "reachable_time": 30,
        "name": "X0",
        "ip_assignment": {
          "mode": {
            "static": {
              "ip": "2000::168",
              "prefix_length": 64,
              "advertise_subnet_prefix": False,
              "router_advertisement": {
                "enable": False,
                "interval": {
                  "min": 200,
                  "max": 600
                },
                "link_mtu": {},
                "reachable_time": {},
                "retransmit_timer": {},
                "current_hop_limit": {
                  "value": 64
                },
                "router": {
                  "lifetime": {
                    "value": 1800
                  },
                  "preference": "medium"
                },
                "managed": False,
                "other_config": False
              }
            }
          }
        }
      }
    }
  ]
}

x1_opt_ipv6 ={
  "interfaces": [
    {
      "ipv6": {
        "one_arm_mode": False,
        "one_arm_peer": "",
        "management": {
          "https": True,
          "https_source": {
            "any": True
          },
          "ping": True,
          "ping_source": {
            "any": True
          },
          "snmp": True,
          "snmp_source": {
            "any": True
          },
          "ssh": True,
          "ssh_source": {
            "any": True
          }
        },
        "user_login": {
          "http": False,
          "https": True
        },
        "ipv6_traffic": True,
        "listen_router_advertisement": False,
        "duplicate_address_detection_transmits": 1,
        "reachable_time": 30,
        "name": "X1",
        "ip_assignment": {
          "mode": {
            "static": {
              "ip": "2001::168",
              "prefix_length": 64,
              "advertise_subnet_prefix": False,
              "router_advertisement": {
                "enable": False,
                "interval": {
                  "min": 200,
                  "max": 600
                },
                "link_mtu": {},
                "reachable_time": {},
                "retransmit_timer": {},
                "current_hop_limit": {
                  "value": 64
                },
                "router": {
                  "lifetime": {
                    "value": 1800
                  },
                  "preference": "medium"
                },
                "managed": False,
                "other_config": False
              }
            }
          }
        }
      }
    }
  ]
}

x2_opt_ipv6 ={
  "interfaces": [
    {
      "ipv6": {
        # "one_arm_mode": False,
        # "one_arm_peer": "",
        "management": {
          "https": True,
          "https_source": {
            "any": True
          },
          "ping": True,
          "ping_source": {
            "any": True
          },
          "snmp": True,
          "snmp_source": {
            "any": True
          },
          "ssh": True,
          "ssh_source": {
            "any": True
          }
        },
        "user_login": {
          "http": False,
          "https": True
        },
        "ipv6_traffic": True,
        "listen_router_advertisement": False,
        "duplicate_address_detection_transmits": 1,
        "reachable_time": 30,
        "name": "X2",
        "ip_assignment": {
          "mode": {
            "static": {
              "ip": "2002::168",
              "prefix_length": 64,
              "advertise_subnet_prefix": False,
              "router_advertisement": {
                "enable": False,
                "interval": {
                  "min": 200,
                  "max": 600
                },
                "link_mtu": {},
                "reachable_time": {},
                "retransmit_timer": {},
                "current_hop_limit": {
                  "value": 64
                },
                "router": {
                  "lifetime": {
                    "value": 1800
                  },
                  "preference": "medium"
                },
                "managed": False,
                "other_config": False
              }
            }
          }
        }
      }
    }
  ]
}

wan_ao_dict = {
            "object_type": "host",
            "name": PC2_ETH1_IP,
            "zone": "WAN",
            "value": PC2_ETH1_IP,
        }

# sslvpn_ao_dict = {
#             "object_type": "host",
#             "name": "test_09",
#             "zone": "SSLVPN",
#             "value": "2.2.2.100",
#         }

syslog_ao_dict = {
            "object_type": "host",
            "name": 'test_syslog',
            "zone": "LAN",
            "value": '192.168.168.100',
        }

vpn_ao_dict = {
            "object_type": "network",
            "name": "remote_vpn_net",
            "zone": "VPN",
            "value": "22.22.22.0,255.255.255.0"
        }

syslog_param = {
  "log": {
    "syslog": {
      "server": [
        {
          "address": {
            "name": PC2_ETH1_IP
          },
          "port": 514,
          "profile": 0,
          "type": "syslog-server",
          "format": "default",
          "facility": "local-use0",
          "id": "firewall",
          "enabled": True,
          "outbound_interface": ""
        }
      ]
    }
  }
}

audit_setting_dict1 = {
            "log": {
                "event": [{
                    "id": 1382,
                    "name": "Configuration Change Succeeded",
                    "category": "Log",
                    "group": "Configuration Auditing",
                    "priority_level": "alert",
                    "log_monitor": {
                        "redundancy_interval": 0
                    },
                    "email_alert": {
                        "redundancy_interval": 0
                    },
                    "syslog": {
                        "redundancy_interval": 0
                    },
                    "trap": {
                        "redundancy_interval": 0
                    },
                    "event_profile": {
                        "syslog_server_profile": 0
                    },
                    "ipfix": {
                        "redundancy_interval": 60
                    },
                    "log_digest": True,
                    "color": {
                        "hex": "0x00FF0000"
                    },
                    "alert_email": {}
                }]
            }
        }

audit_setting_dict2 = {
    "log": {
        "event": [{
            "id": 1383,
            "name": "Configuration Change Failed",
            "category": "Log",
            "group": "Configuration Auditing",
            "priority_level": "alert",
            "log_monitor": {
                "redundancy_interval": 0
            },
            "email_alert": {},
            "syslog": {
                "redundancy_interval": 0
            },
            "trap": {
                "redundancy_interval": 0
            },
            "event_profile": {
                "syslog_server_profile": 0
            },
            "ipfix": {
                "redundancy_interval": 60
            },
            "log_digest": False ,
            "color": {
                "hex": "0x00FF0000"
            },
            "alert_email": {}
        }]
    }
}

application_control_detection = {
  "log": {
    "event": [
      {
        "id": 1154,
        "name": "Application Control Detection Alert",
        "category": "Security Services",
        "group": "Application Control",
        "priority_level": "debug",
        "log_monitor": {
          "redundancy_interval": 0
        },
        "email_alert": {
          "redundancy_interval": 0
        },
        "syslog": {
          "redundancy_interval": 0
        },
        "event_profile": {
          "syslog_server_profile": 0
        },
        "trap": {
          "redundancy_interval": 0
        },
        "ipfix": {},
        "log_digest": True,
        "alert_email": {}
      }
    ]
  }
}

application_control_prevention = {
  "log": {
    "event": [
      {
        "id": 1155,
        "name": "Application Control Prevention Alert",
        "category": "Security Services",
        "group": "Application Control",
        "priority_level": "debug",
        "log_monitor": {
          "redundancy_interval": 0
        },
        "email_alert": {
          "redundancy_interval": 0
        },
        "syslog": {
          "redundancy_interval": 0
        },
        "event_profile": {
          "syslog_server_profile": 0
        },
        "trap": {
          "redundancy_interval": 0
        },
        "ipfix": {},
        "log_digest": True,
        "alert_email": {}
      }
    ]
  }
}

filename_logging_log_http = {
  "log": {
    "event": [
      {
        "id": 1574,
        "name": "Filename Logging",
        "priority_level": "debug",
        "log_email": {},
        "log_monitor": {
          "redundancy_interval": 0
        },
        "email_alert": {
          "redundancy_interval": 0
        },
        "syslog": {
          "redundancy_interval": 0
        },
        "trap": {},
        "ipfix": {},
        "event_profile": {
          "syslog_server_profile": 0
        },
        "log_digest": True,
        "color": {
          "hex": "0x001E90FF"
        },
        "alert_email": {}
      }
    ]
  }
}

filename_logging_log_ftp = {
  "log": {
    "event": [
      {
        "id": 1574,
        "name": "Filename Logging",
        "category": "Security Services",
        "group": "Application Control",
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
        "event_profile": {
          "syslog_server_profile": 0
        },
        "trap": {},
        "ipfix": {},
        "log_digest": True,
        "alert_email": {}
      }
    ]
  }
}

snmp_dict = {
            "snmp":{
                "enable": True,
                "system_name": "sonicwall",
                "get_community_name": "public",
                "trap_community_name": "public",
                "host_1": PC2_ETH1_IP,
                "host_2": "",
                "host_3": "",
                "host_4": "",
                "system_contact": "",
                "system_location": "",
            }
        }

#Instantiate objects including API,CLI
console_info = os_obj.get_console_info(dut='UTM')

fw_api = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_console = Firewall(Parameter.FIREWALL, console_ip=console_info[0], console_port=console_info[1], user='admin', password='password', supported_config_mode='cli-console')

interface_api = network.InterfaceIPv4Api(fw_api)
interface_apiv6 = network.InterfaceIPv6Api(fw_api)
fp_api = firewallsettings.FloodprotectionApi(fw_api)
log_api = log.LogMonitorApi(fw_api)
log_cat_api = log.LogCategoryApi(fw_api)
pkg_api = system.PacketmonitorApi(fw_api)
ao_api = network.AddressobjectsApi(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
system_api = system.DiagnosticApi(fw_api)
setting_api = system.SettingApi(fw_api)
restart_obj = system.RestartApi(fw_api)
license_cli = LicenseCli(fw_cli)
tsr_obj = DiagnosticsCli(fw_cli)
log_set = log.LogCategoryApi(fw_api)
snmp_api = system.SNMPApi(fw_api)
# audit_log_api = log.AuditlogMonitorApi(fw_api)
logsetting_api = log.LogSettingsApi(fw_api)
appcontrolapi = firewall.AppControlApi(fw_api)
log_auto_api = log.LogAutomationApi(fw_api)
access_rules_api = firewall.AccessRuleApi(fw_api)
app_rule_api = firewall.AppRuleApi(fw_api)