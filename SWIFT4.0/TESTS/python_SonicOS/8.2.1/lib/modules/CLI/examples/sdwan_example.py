import sys
import os
#sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
#sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append('/DEV_TESTS/python_SonicOS/6.5.4/lib')
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')

import modules.CLI.sdwan
from utm import Firewall
ip = '192.168.168.168'
port = '22'
fw = Firewall(ip,user='admin',password='password',supported_config_mode='cli-ssh')

sdwan_show=modules.CLI.sdwan.show_sdwan_grp(fw)
sdwan_status= sdwan_show.show_sdwan_grp()
print(sdwan_status)

sdwan_grp = modules.CLI.sdwan.SdwanGroupCli(fw)
#dpisslclient = modules.CLI.dpissl.ClientsslCli(fw)
# enable_ssh
sdwan_grp_dict= {
   'group': ['test1'],
   'interface': [['x1']]
}
  
sdwan_grp_add = sdwan_grp.config_sdwan_group(**sdwan_grp_dict, tag=1)
print(sdwan_grp_add)

edit_grp_dict={
    'name': 'test1'
}
#sdwan_grp_edit = sdwan_grp.edit_sdwan_group(**edit_grp_dict, **sdwan_grp_dict, tag=1)
#print(sdwan_grp_edit)

edit_interface_dict={
    'del_interface': ['x1', 'x3']
}
#sdwan_interface_edit = sdwan_grp.edit_sdwan_interface(**edit_interface_dict, **sdwan_grp_dict, tag=1)
#print(sdwan_interface_edit)

del_sdwan_grp_dict={
    'del_group':'test1'
}
#sdwan_grp_del = sdwan_grp.delete_sdwan_group(**edit_interface_dict, **sdwan_grp_dict,tag=1)
#print(sdwan_grp_del)

sdwan_probe= modules.CLI.sdwan.SdwanPerformanceProbeCli(fw)
probe_dict={
    'perf_probe': 'perf1',
    'sdwan-group': 'test1',
    'host': '10.5.14.141',
    'type': 'ping', ##type:ping/tcp(put tcp port no.& rst-miss)
    #'tcp_port' :'',
    #'rst-as-miss':'',
    'probe_interval': '5',
    'probe_down': '4',
    'probe_up': '4',
    'reply-timeout':'3',
    'comment':'perf_probe'
}
probe_add= sdwan_probe.config_perf_probe(**probe_dict, tag=1)
print(probe_add)

edit_probe_dict={
    'probe_name': 'perf2'

}
#probe_edit=sdwan_probe.edit_performance_probe(**edit_grp_dict, tag=1)
#print(probe_edit)
del_probe_dict={
    'probe_del_name':'perf2'
}
#probe_del= sdwan_probe.delete_performance_probe(**del_probe_dict, tag=1)
#print(probe_del)
sdwan_perf_object= modules.CLI.sdwan.SdwanPerformanceClassObjectsCli(fw)
obj_dict={
    'object': 'obj1',
    'jitter': '2',
    'latency': '1',
    'packet-loss':'2',
    'include_jitter':True,
    'include_latency':True,
    'include_packet-loss':True,
    'comment': 'performance-class-obj'
}
#obj_add=sdwan_perf_object.configure_perf_class_objec(**obj_dict, tag=1)
#print(obj_dict)

edit_obj_dict={
    'obj_name': 'obj2'
}
#obj_edit=sdwan_perf_object.edit_perf_obj_name(**edit_obj_dict, tag=1)
#print(obj_edit)

del_obj_dict={
    'del_obj' : 'obj2'
}
#obj_del= sdwan_perf_object.del_perf_obj(**del_probe_dict, tag=1)
#print(obj_dict)

sdwan_path_selection_profile= modules.CLI.sdwan.PathSelectionProfileCli(fw)
profile_dict={
    'path-selection-profile': 'profile1',
    'sdwan-group': 'test1',
    'performance-probe': 'perf1',
    'performance-class':'obj1',
    'backup-interface':'x7',
    'probe-default-up': True,
    'reset-connections': False
}
profile_add=sdwan_path_selection_profile.config_path_selection_profile(**profile_dict, tag=1)
print(profile_add)

profile_edit_dict={
    'name_profile': 'profile2'
}
#profile_edit= sdwan_path_selection_profile.edit_path_selection_profile(**profile_edit_dict, tag=1)
#print(profile_edit)

profile_del_dict={
    'del_profile':'profile2'
}
#profile_del=sdwan_path_selection_profile.del_path_selection_profile(**profile_del_dict, tag=1)
#print(profile_del)
