import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('/'))
logger('***************',suite_absolute_path)
script_list= ['modules','DEV_TESTS','API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + '../'
        logger('+++++',root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
logger(sys.path)
sys.path.insert(0, '/DEV_TESTS/')
from PythonRunner.runner.settings import logger

sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')

from utm import Firewall
from modules.API.sdwan import *

ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
logger(fw)
#SSLVPNServerSettingsAPI
#server_url='/api/sonicos/sdwan/groups'
#portal_url='/api/sonicos/ssl-vpn/portal'
sdwangrpobj = SDWANGroupAPI(fw)
sdwanprobes = SDWANProbesAPI(fw)
sdwanperf = SDWANPerfClassAPI(fw)
sdwanpsp = SDWANPathSelectionAPI(fw)
def create_sdwan_groups():
    # {
    #     "sdwan": {
    #         "group": [
    #             {
    #                 "name": "hhh",
    #                 "interface": [
    #                     {
    #                         "name": "X2",
    #                         "priority": 2
    #                     },
    #                     {
    #                         "name": "X1",
    #                         "priority": 1
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # }


    sdwan = {
                'name': 'sdwan_groupt1',
                'interface_name' : ['X2'],
                'priority' : 1

                }


    #put_response1=sdwangrpobj.build_json_sdwan_group(**sdwan)
    post_response  = sdwangrpobj.configure_sdwan_group(**sdwan)

   #logger('The post response is ',post_response)



def get_server_settings():
    get_server_set_resp = sdwangrpobj.get_sdwan_group()
    logger.info(get_server_set_resp)
    # del_new = sdwangrpobj.delete_sdwan_group('sdwan_groupt')
    # logger(del_new)


def edit_sdwan_groups():
    # {
    #     "sdwan": {
    #         "group": [
    #             {
    #                 "name": "hhh",
    #                 "interface": [
    #                     {
    #                         "name": "X2",
    #                         "priority": 2
    #                     },
    #                     {
    #                         "name": "X1",
    #                         "priority": 1
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # }


    sdwan = {
                'name': 'sdwan_groupt',
                'interface_name' : ['X2'],
                'priority' : 2

                }


    #put_response1=sdwangrpobj.build_json_sdwan_group(**sdwan)
    put_response  = sdwangrpobj.edit_sdwan_group(**sdwan)

    #logger('The put update is ',put_response)

def delete_sdwan_groups():
    get_server_set_resp = sdwangrpobj.get_sdwan_group()
    logger.info(get_server_set_resp)
    del_new = sdwangrpobj.delete_sdwan_group('sdwan_groupt')
    logger.info(del_new)

#create_sdwan_groups()
#get_server_settings()
#edit_sdwan_groups()
#delete_sdwan_groups()


def create_sdwan_probes():
    #             {
    #                 'sdwan': {
    #                     'performance_probe': [
    #                         {
    #                             'ipv4': {
    #                                 'name': 'sdwan-perf-probe1',
    #                                 'comment': '',
    #                                 'sdwan_group': 'sdwan-grp2',
    #                                 'probe': {
    #                                     'target': {
    #                                         'name': 'Default Gateway'
    #                                     },
    #                                     'type': {
    #                                         'ping': {
    #                                             'explicit': True
    #                                         }
    #                                     },
    #                                     'interval': 3
    #                                 },
    #                                 'reply_timeout': 1,
    #                                 'interval': {
    #                                     'missed': 3,
    #                                     'successful': 1
    #                                 }
    #                             }
    #                         }
    #                     ]
    #                 }
    #             }
    #         }


    sdwan = {
                'name': 'sdwan_probe',
                'sdwan_group':'sdwan_groupt1',
                'probe_target': 'Default Gateway',
                'probe_type':'tcp',
                'port': 8080,
                'interval': 8,
                'reply_timeout':6,
                'missed' :6,
                'successful':2,
                'rst_as_miss' :True
                # 'probe_type': 'ping',


                }


    #put_response1=sdwanprobes.build_json_sdwan_probes(**sdwan)
    post_response  = sdwanprobes.configure_sdwan_probes(**sdwan)

    #logger('The json obtained is ',put_response1)
    #logger('The post response is ', post_response)


def get_sdwan_probes_settings():
    get_server_set_resp = sdwanprobes.get_sdwan_probes()
    logger(get_server_set_resp)
    # del_new = sdwangrpobj.delete_sdwan_group('sdwan_groupt')
    # logger(del_new)


def edit_sdwan_probes():


    sdwan = {
                'name': 'sdwan_probe',
                'sdwan_group':'sdwan_groupt1',
                'probe_target': 'Default Gateway',
                'probe_type':'ping',
                # 'port': 8080,
                'interval': 10,
                'reply_timeout':6,
                'missed' :8,
                'successful':4,
                # 'rst_as_miss' :True
                # 'probe_type': 'ping',


                }

    # put_response1=sdwanprobes.build_json_sdwan_group(**sdwan)
    put_response  = sdwanprobes.edit_sdwan_probes(**sdwan)

    logger('The put update is ',put_response)

def delete_sdwan_probes():
    get_server_set_resp = sdwanprobes.get_sdwan_probes()
    logger(get_server_set_resp)
    del_new = sdwanprobes.delete_sdwan_probes('sdwan_probe')
    logger(del_new)

#create_sdwan_probes()
#get_sdwan_probes_settings()
#edit_sdwan_probes()
#delete_sdwan_probes()


def create_sdwan_perf_class():
    #             {
    #                'sdwan': {
    #                     'performance_class_object': {
    #                     'name': '',
    #                     'latency': 0,
    #                     'jitter': 0,
    #                     'packet_loss': 0,
    #                     'comment': 'string'
    #                 }
    #             }
    #         }


    sdwan = {
                'name': 'sdwan_perf1',
                'latency': 12,
                'jitter': 2,
                'packet_loss': 10,
                #'comment':'sdwan-perf-commment'
        }

    
    #put_response1 = sdwanperf.build_json_sdwan_perf_class(**sdwan)
    #post_response  = sdwanperf.configure_sdwan_perf_class(**sdwan)
    get_response= sdwanperf.get_sdwan_perf_class()
    #logger('The json obtained is ',put_response1)
    #logger('The post response is ', post_response)


#create_sdwan_perf_class()

def config_sdwan_perf_class():
    sdwan = {
                'name': 'sdwan_perf1',
                'latency': 12,
                'jitter': 15,
                'packet_loss': 10
                # 'comment':'sdwan-perf-commment'
        }


   # put_response1 = sdwanperf.build_json_sdwan_perf_class(**sdwan)
    post_response  = sdwanperf.edit_sdwan_perf_class(**sdwan)
    del_response = sdwanperf.delete_sdwan_perf_class('sdwan_perf1')
    get_response= sdwanperf.get_sdwan_perf_class()

    logger('The json obtained is ',put_response1)
    logger('The post response is ', post_response)
    logger('The delete response is ', del_response)


#config_sdwan_perf_class()


def create_sdwan_path_selection():
    # {
    #     "sdwan": {
    #         "path_selection_profile": [
    #             {
    #                 "name": "psp",
    #                 "sdwan_group": "sdwan_groupt1",
    #                 "performance_probe": "fqdn",
    #                 "performance_class": "",
    #                 "backup_interface": "",
    #                 "probe_default_up": true,
    #                 "reset_connections": true
    #             }
    #         ]
    #     }
    # }


    sdwan = {
                'name': 'psp',
                'sdwan_group': 'grp',
                'performance_probe': 'probe',
                'performance_class': 'aaaa',
                'backup_interface':'X1',
                'probe_default_up':True,
                'reset_connections':True
        }


   # put_response1 = sdwanpsp.build_json_sdwan_path_selection(**sdwan)
    post_response  = sdwanpsp.configure_sdwan_psp(**sdwan)
    #logger('The post response is ', post_response)


def edit_sdwan_path_selection():
    sdwan = {
        'name': 'psp',
        'sdwan_group': 'sdwan_grp',
        'performance_probe': 'probe',
        'performance_class': 'pco',
        'backup_interface': 'X2',
        'probe_default_up': True,
        'reset_connections': True
    }

    #put_response1 = sdwanpsp.build_json_sdwan_path_selection(**sdwan)
    post_response = sdwanpsp.edit_sdwan_psp(**sdwan)

    logger('The post response is ', post_response)

def del_sdwan_path_selection():
    del_rep = sdwanpsp.delete_sdwan_psp('psp')
    logger('The json obtained is ', del_rep)

#create_sdwan_path_selection()
edit_sdwan_path_selection()
del_sdwan_path_selection()
