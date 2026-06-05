import os
import sys
import re
import copy
import time
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest

from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion
    
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from lib.modules.CLI.system import AdminCli
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network
from lib.modules.API.system import SettingApi
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DHCP_Server_Options/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DHCP_Server_Options')
os_obj = Openstack(Params.testbed)
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2','eth2')
# PC2_login = Host(PC2_ETH2_IP, user='root', password='password')

FIREWALL = '192.168.168.168'
FW_X2_IP = '172.16.2.168'
MASK = '255.255.255.0'
X1_IP = '172.17.1.168'
X1_GW = '172.17.1.1'
FW_X3_IP = '172.16.3.168'
X1_DNS1 = '10.102.1.60'
X1_DNS2 = '10.190.202.200'
DHCP_Optname = 'DHCP_Opt1'
DHCP_Optname2 = 'DHCP_Opt2'
dynamic_start = '172.16.2.200'
dynamic_end = '172.16.2.210'
call_manager = '222.222.222.222'
DHCP_Grp1 = 'DHCP_Grp1'
Object_ip1 = '111.111.111.111'
Object_ip2 = '222.222.222.222'
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DHCP_Server_Options/testplan/DHCP_Server_Options_Steps.json'
ip = FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
interface_obj = network.InterfaceIPv4Api(fw)
dhcp_obj = network.DHCPServerApi(fw)
FilePath    = '/tmp/dhcpCapture.txt'
setting_obj = SettingApi(fw)


add_dhcp_server_option_object_01 = {
    'dhcp_server': {
		'ipv4': {
			'option': {
				'object': [{
					'name': DHCP_Optname,
					'number': 254,
					'array': False,
					'value': [{
						'ip': Object_ip1
					}]
				}]
			}
		}
	}
}

add_dhcp_server_scope_dynamic_01 = {
    'dhcp_server': {
		'ipv4': {
			'scope': {
				'dynamic': [{
					'from': dynamic_start,
					'to': dynamic_end,
					'enable': True,
					'lease_time': 1440,
					'default_gateway': '0.0.0.0',
					'netmask': '255.255.255.0',
					'comment': '',
					'allow_bootp': False,
					'domain_name': '',
					'dns': {
						'server': {
							'inherit': True
						}
					},
					'wins': {
						'primary': '0.0.0.0',
						'secondary': '0.0.0.0'
					},
					'call_manager': {
						'primary': '',
						'secondary': '',
						'tertiary': ''
					},
					'network_boot': {
						'next_server': '0.0.0.0',
						'boot_file': '',
						'server_name': ''
					},
					'generic_option': {
						'object': DHCP_Optname,
					},
					'always_send_option': True
				}]
			}
		}
	}
}

add_dhcp_server_option_object_02 = {
    'dhcp_server': {
		'ipv4': {
			'option': {
				'object': [{
					'name': DHCP_Optname,
					'number': 70,
					'array': False,
					'value': [{
						'ip': '111.111.111.111'
					}]
				}]
			}
		}
	}
}

add_dhcp_server_scope_dynamic_02 = {
    'dhcp_server': {
		'ipv4': {
			'scope': {
				'dynamic': [{
					'from': dynamic_start,
					'to': dynamic_end,
					'enable': True,
					'lease_time': 1440,
					'default_gateway': '0.0.0.0',
					'netmask': '255.255.255.0',
					'comment': '',
					'allow_bootp': False,
					'domain_name': '',
					'dns': {
						'server': {
							'inherit': True
						}
					},
					'wins': {
						'primary': '0.0.0.0',
						'secondary': '0.0.0.0'
					},
					'call_manager': {
						'primary': '',
						'secondary': '',
						'tertiary': ''
					},
					'network_boot': {
						'next_server': '0.0.0.0',
						'boot_file': '',
						'server_name': ''
					},
					'generic_option': {
						'object': DHCP_Optname,
					},
					'always_send_option': False
				}]
			}
		}
	}
}

add_dhcp_server_option_object_03 = {
    'dhcp_server': {
		'ipv4': {
			'option': {
				'object': [{
					'name': DHCP_Optname,
					'number': 150,
					'array': False,
					'value': [{
						'ip': Object_ip1
					}]
				}]
			}
		}
	}
}

add_dhcp_server_scope_dynamic_03 = {
    'dhcp_server': {
		'ipv4': {
			'scope': {
				'dynamic': [{
					'from': dynamic_start,
					'to': dynamic_end,
					'enable': True,
					'lease_time': 1440,
					'default_gateway': '0.0.0.0',
					'netmask': '255.255.255.0',
					'comment': '',
					'allow_bootp': False,
					'domain_name': '',
					'dns': {
						'server': {
							'inherit': True
						}
					},
					'wins': {
						'primary': '0.0.0.0',
						'secondary': '0.0.0.0'
					},
					'call_manager': {
						'primary': call_manager,
						'secondary': '',
						'tertiary': ''
					},
					'network_boot': {
						'next_server': '0.0.0.0',
						'boot_file': '',
						'server_name': ''
					},
					'generic_option': {
						'object': DHCP_Optname,
					},
					'always_send_option': False
				}]
			}
		}
	}
}

add_dhcp_server_option_object_04 = {
    'dhcp_server': {
		'ipv4': {
			'option': {
				'object': [{
					'name': DHCP_Optname,
					'number': 70,
					'array': False,
					'value': [{
						'ip': Object_ip1
					}]
				}]
			}
		}
	}
}

add_dhcp_server_scope_dynamic_04 = {
    'dhcp_server': {
		'ipv4': {
			'scope': {
				'dynamic': [{
					'from': dynamic_start,
					'to': dynamic_end,
					'enable': True,
					'lease_time': 1440,
					'default_gateway': '0.0.0.0',
					'netmask': '255.255.255.0',
					'comment': '',
					'allow_bootp': False,
					'domain_name': '',
					'dns': {
						'server': {
							'inherit': True
						}
					},
					'wins': {
						'primary': '0.0.0.0',
						'secondary': '0.0.0.0'
					},
					'call_manager': {
						'primary': '',
						'secondary': '',
						'tertiary': ''
					},
					'network_boot': {
						'next_server': '0.0.0.0',
						'boot_file': '',
						'server_name': ''
					},
					'generic_option': {
						'object': DHCP_Optname,
					},
					'always_send_option': True
				}]
			}
		}
	}
}

add_dhcp_server_option_object_0711 = {
    'dhcp_server': {
		'ipv4': {
			'option': {
				'object': [{
					'name': DHCP_Optname,
					'number': 230,
					'array': False,
					'value': [{
						'ip': Object_ip1
					}]
				}]
			}
		}
	}
}

add_dhcp_server_option_object_0722 = {
    'dhcp_server': {
		'ipv4': {
			'option': {
				'object': [{
					'name': DHCP_Optname2,
					'number': 231,
					'array': False,
					'value': [{
						'ip': Object_ip2
					}]
				}]
			}
		}
	}
}

add_dhcp_server_option_group = {
	'dhcp_server': {
		'ipv4': {
			'option': {
				'group': [{
					'name': DHCP_Grp1,
					'option': {
						'object': [{
							'name': DHCP_Optname
						}, {
							'name': DHCP_Optname2
						}]
					}
				}]
			}
		}
	}
}

add_dhcp_server_scope_dynamic_07 = {
    'dhcp_server': {
		'ipv4': {
			'scope': {
				'dynamic': [{
					'from': dynamic_start,
					'to': dynamic_end,
					'enable': True,
					'lease_time': 1440,
					'default_gateway': '0.0.0.0',
					'netmask': '255.255.255.0',
					'comment': '',
					'allow_bootp': False,
					'domain_name': '',
					'dns': {
						'server': {
							'inherit': True
						}
					},
					'wins': {
						'primary': '0.0.0.0',
						'secondary': '0.0.0.0'
					},
					'call_manager': {
						'primary': '',
						'secondary': '',
						'tertiary': ''
					},
					'network_boot': {
						'next_server': '0.0.0.0',
						'boot_file': '',
						'server_name': ''
					},
					'generic_option': {
						'group': DHCP_Grp1,
					},
					'always_send_option': True
				}]
			}
		}
	}
}