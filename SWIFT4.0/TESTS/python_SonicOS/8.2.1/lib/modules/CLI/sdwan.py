import re
from runner.settings import logger
import time

class SdwanGroupCli:
    '''SdwanGroupCli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_sdwan_grp(self, name=None):
        commands = []
        time.sleep(5)
        if name:
            command = 'show sdwan group ' + name
        else:
            command = 'show sdwan groups'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)
        return output


    def config_sdwan_group(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)

        if 'group' in kwargs and kwargs['group']:
            for i, group_name in enumerate(kwargs['group']):
                commands.append(f'group {group_name}')

                if 'interface' in kwargs and kwargs['interface']:
                    for iface in kwargs['interface'][i]:
                        commands.append(f'interface {iface}')

                        if 'priority' in kwargs:
                            commands.append(f'priority {kwargs["priority"]}')
                        
                        if 'ingress_bandwidth' in kwargs:
                            commands.append(f'ingress-bandwidth {kwargs["ingress_bandwidth"]}')

                        if 'egress_bandwidth' in kwargs:
                            commands.append(f'egress-bandwidth {kwargs["egress_bandwidth"]}')

                        # Set cost if provided
                        if 'cost' in kwargs:
                            commands.append(f'cost {kwargs["cost"]}')

                        commands.append('exit')  # exit interface

                commands.append('exit')  # exit group

        commands.extend(['commit', 'end', 'exit'])
        result_grp = self.fw.do_cli_commands(commands)
        return result_grp


    def edit_sdwan_group(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'name' in kwargs.keys() and kwargs['name']:
            commands.append('group ' + kwargs['group'])
            commands.append('name ' + kwargs['name'])

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_edit_grp = self.fw.do_cli_commands(commands)
        return res_edit_grp

    def edit_sdwan_interface(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'group' in kwargs.keys() and kwargs['group']:
            commands.append('group ' + kwargs['group'])
            if 'del_interface' in kwargs.keys():
                temp = 0
                while temp < len(kwargs['del_interface']):
                    if re.findall(r"^x\d{1,2}", kwargs['del_interface'][temp]):
                        commands.append('no ' + 'interface ' + kwargs['del_interface'][temp])
                        temp += 1
                        print("*******")
                        print(temp)

                    else:
                        commands.append('no ' + 'interface ' + kwargs['del_interface'][temp])
                        temp += 1

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_edit_iface = self.fw.do_cli_commands(commands)
        return res_edit_iface


    def delete_sdwan_group(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'no group' in kwargs.keys():
            commands.append('no group ' + kwargs['no group'])
        self.fw._is_key_exist(commands, kwargs, 'no groups')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


    def change_interface_priority(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'group' in kwargs.keys() and kwargs['group']:
            commands.append('group ' + kwargs['group'])
            if 'interface' in kwargs.keys() and kwargs['interface']:
                commands.append('interface ' + kwargs['interface'])
                if 'priority' in kwargs.keys():
                    commands.append('priority ' + kwargs['priority'])
                else:
                    commands.append('no ' + 'priority ' + kwargs['priority'])


            for command in ['commit', 'end', 'exit']:
                commands.append(command)
            res_edit_iface = self.fw.do_cli_commands(commands)
            return res_edit_iface


    def change_interface_cost(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'group' in kwargs.keys() and kwargs['group']:
            commands.append('group ' + kwargs['group'])
            if 'interface' in kwargs.keys() and kwargs['interface']:
                commands.append('interface ' + kwargs['interface'])
                if 'priority' in kwargs.keys():
                    commands.append('cost ' + kwargs['cost'])
                else:
                    commands.append('no ' + 'cost ' + kwargs['cost'])


            for command in ['commit', 'end', 'exit']:
                commands.append(command)
            res_edit_iface = self.fw.do_cli_commands(commands)
            return res_edit_iface


    def change_interface_ingress(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'group' in kwargs.keys() and kwargs['group']:
            commands.append('group ' + kwargs['group'])
            if 'interface' in kwargs.keys() and kwargs['interface']:
                commands.append('interface ' + kwargs['interface'])
                if 'priority' in kwargs.keys():
                    commands.append('ingress-bandwidth ' + kwargs['ingress-bandwidth'])
                else:
                    commands.append('no ' + 'ingress-bandwidth ' + kwargs['ingress-bandwidth'])


            for command in ['commit', 'end', 'exit']:
                commands.append(command)
            res_edit_iface = self.fw.do_cli_commands(commands)
            return res_edit_iface

    def change_interface_egress(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'group' in kwargs.keys() and kwargs['group']:
            commands.append('group ' + kwargs['group'])
            if 'interface' in kwargs.keys() and kwargs['interface']:
                commands.append('interface ' + kwargs['interface'])
                if 'priority' in kwargs.keys():
                    commands.append('egress-bandwidth ' + kwargs['egress-bandwidth'])
                else:
                    commands.append('no ' + 'egress-bandwidth ' + kwargs['egress-bandwidth'])

            for command in ['commit', 'end', 'exit']:
                commands.append(command)
            res_edit_iface = self.fw.do_cli_commands(commands)
            return res_edit_iface


class SdwanPerformanceProbeCli:
    def __init__(self, fw):
        self.fw = fw


    def show_sdwan_probe(self, name=None):
        commands = []
        time.sleep(5)
        if name:
            command = 'show sdwan sla-probe ' + name
        else:
            command = 'show sdwan sla-probes '
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)
        return output

    def config_perf_probe(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'perf_probe' in kwargs.keys() and kwargs['perf_probe']:
            commands.append('sla-probe ' + kwargs['perf_probe'])
            if 'sdwan-group' in kwargs.keys() and kwargs['sdwan-group']:
                commands.append('sdwan-group ' + kwargs['sdwan-group'])
            try:

                if 'host' in kwargs.keys() and kwargs['host']:
                    commands.append('probe ' + 'target '+ 'host ' + kwargs['host'])
                if 'fqdn' in kwargs.keys() and kwargs['fqdn']:
                    commands.append('probe ' + 'target '+ 'fqdn ' + kwargs['fqdn'])
                if 'name' in kwargs.keys() and kwargs['name']:
                    commands.append('probe ' + 'target ' + 'name ' + kwargs['name'])

                if 'type' in kwargs.keys():
                        if kwargs['type'] == 'ping':
                            commands.append('probe ' + 'type ' + 'ping ' + 'explicit')
                        elif kwargs['type'] == 'tcp':
                            commands.append('probe ' + 'type ' + 'tcp ' + 'explicit ' + 'port ' + kwargs['tcp_port'])
                            self.fw._is_key_exist(commands, kwargs, 'rst-as-miss')
                        elif kwargs['type'] == 'http':
                            commands.append('probe ' + 'type ' + 'http ' + 'explicit ' + 'port ' + kwargs['http_port'])
                        elif kwargs['type'] == 'https':
                            commands.append('probe ' + 'type ' + 'https ' + 'explicit ' + 'port ' + kwargs['https_port'])

                if 'probe_interval' in kwargs.keys() and kwargs['probe_interval']:
                        commands.append('probe ' + 'interval ' + kwargs['probe_interval'])

                if 'probe_down' in kwargs.keys() and kwargs['probe_down']:
                    commands.append('interval ' + 'missed ' + kwargs['probe_down'])
                if 'probe_up' in kwargs.keys() and kwargs['probe_up']:
                    commands.append('interval ' + 'successful ' + kwargs['probe_up'])

                if 'reply-timeout' in kwargs.keys() and kwargs['reply-timeout']:
                    commands.append('reply-timeout ' + kwargs['reply-timeout'])
                if 'comment' in kwargs.keys() and kwargs['comment']:
                    commands.append('comment ' + kwargs['comment'])
                if 'no_comment' in kwargs.keys() and kwargs['no_comment']:
                    commands.append('no comment')
            except KeyError:
                logger.info("Error while adding the performance probe")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_add_probe = self.fw.do_cli_commands(commands)
        return res_add_probe

    def edit_performance_probe(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'probe_name' in kwargs.keys() and kwargs['probe_name']:
            commands.append('sla-probe ' + kwargs['probe_name'])
            if 'edit_name' in kwargs.keys() and kwargs['edit_name']:
                commands.append('name ' + kwargs['edit_name'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_edit_probe = self.fw.do_cli_commands(commands)
        return res_edit_probe

    # def delete_performance_probe(self, **kwargs):
    #     commands = ['configure', 'sdwan']
    #     if 'probe_del_name' in kwargs.keys() and kwargs['probe_del_name']:
    #         commands.append('no ' + 'performance-probe ' + kwargs['probe_del_name'])
    #     for command in ['commit', 'end', 'exit']:
    #         commands.append(command)
    #     res_del_probe = self.fw.do_cli_commands(commands)
    #     return res_del_probe


    def delete_performance_probe(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'no probe' in kwargs.keys():
            commands.append('no sla-probe ' + kwargs['no probe'])

        self.fw._is_key_exist(commands, kwargs, 'no sla-probes')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_del_probe = self.fw.do_cli_commands(commands)
        return res_del_probe

class SdwanPerformanceClassObjectsCli:
    def __init__(self, fw):
        self.fw = fw

    def show_sdwan_class_object(self, name=None):
        commands = []
        time.sleep(5)
        if name:
            command = 'show sdwan sla-class-object ' + name
        else:
            command = 'show sdwan sla-class-objects '
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)
        return output

    def configure_perf_class_objec(self, **kwargs):
        commands= ['configure', 'sdwan']
        time.sleep(5)
        if 'object' in kwargs.keys() and kwargs['object']:
            commands.append('sla-class-object ' + kwargs['object'])
            try:
                try:
                    if 'jitter' in kwargs.keys() and kwargs['jitter']:
                        commands.append('jitter ' + kwargs['jitter'])
                    if 'latency' in kwargs.keys() and kwargs['latency']:
                        commands.append('latency ' + kwargs['latency'])
                    if 'packet-loss' in kwargs.keys() and kwargs['packet-loss']:
                        commands.append('packet-loss ' + kwargs['packet-loss'])
                    else:
                        raise ValueError
                except ValueError:
                    logger.info("(min:0 and max: 1000)for jitter, latency and packet-loss ")
                try:
                    if 'include_jitter' in kwargs.keys():
                        commands.append('include ' + 'jitter ') if kwargs['include_jitter'] else commands.append('no ' +'include ' + 'jitter')
                    if 'include_latency' in kwargs.keys():
                        commands.append('include ' + 'latency') if kwargs['include_latency'] else commands.append('no ' + 'include ' + 'latency')
                    if 'include_packet-loss' in kwargs.keys():
                        commands.append('include ' + 'packet-loss') if kwargs['include_packet-loss'] else commands.append('no ' + 'include ' + 'packet-loss')
                    else:
                        raise KeyError
                except KeyError:
                    print("Error in include key")
                    if 'comment' in kwargs.keys() and kwargs['comment']:
                        commands.append('comment ' + kwargs['comment'])
                    if 'no_comment' in kwargs.keys() and kwargs['no_comment']:
                        commands.append('no comment')
                    if 'no_latency' in kwargs.keys() and kwargs['no_latency']:
                        commands.append('no latency')
                    if 'no_jitter' in kwargs.keys() and kwargs['no_jitter']:
                        commands.append('no jitter')
                    if 'no_packet_loss' in kwargs.keys() and kwargs['no_packet_loss']:
                        commands.append('no packet-loss')
            except KeyError:
                logger.info("Error while creating the performance class object")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_add_obj = self.fw.do_cli_commands(commands)
        return res_add_obj

    def edit_perf_obj_name(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'obj_name' in kwargs.keys() and kwargs['obj_name']:
            commands.append(' sla-class-object ' + kwargs['obj_name'])
            if 'edit_name' in kwargs.keys() and kwargs['edit_name']:
                commands.append('name ' + kwargs['edit_name'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_edit_obj = self.fw.do_cli_commands(commands)
        return res_edit_obj


    def delete_perf_class_obj(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'no performance-class-object' in kwargs.keys():
            commands.append('no sla-class-object ' + kwargs['no performance-class-object'])
        self.fw._is_key_exist(commands, kwargs, 'no sla-class-objects')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_del_obj = self.fw.do_cli_commands(commands)
        return res_del_obj

class PathSelectionProfileCli:
    def __init__(self, fw):
        self.fw = fw

    def config_path_selection_profile(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(10)
        if 'path-selection-profile' in kwargs.keys() and kwargs['path-selection-profile']:
            commands.append('path-selection-profile ' + kwargs['path-selection-profile'])
            try:
                self.fw._is_key_exist(commands, kwargs, 'probe-default-up')
                self.fw._is_key_exist(commands, kwargs, 'reset-connections')
                if 'sdwan-group' in kwargs.keys() and kwargs['sdwan-group']:
                    commands.append('sdwan-group ' + kwargs['sdwan-group'])
                if 'performance-probe' in kwargs.keys() and kwargs['performance-probe']:
                    commands.append('sla-probe ' + kwargs['performance-probe'])
                if 'performance-class' in kwargs.keys() and kwargs['performance-class']:
                    commands.append('sla-class ' + kwargs['performance-class'])
                if 'sla-strategy' in kwargs.keys() and kwargs['sla-strategy']:
                    commands.append('sla-strategy ' + kwargs['sla-strategy'])
                if 'backup-interface' in kwargs.keys() and kwargs['backup-interface']:
                    commands.append('backup-interface ' + kwargs['backup-interface'])
                if 'load-balancing' in kwargs.keys():
                    commands.append('load-balancing ' + kwargs['load-balancing'])
                    if kwargs['load-balancing'] == 'ratio':
                        commands.append('percent' + ' ' +  kwargs['if'] + ' ' +  kwargs['ratio'])
                        commands.append('percent' + ' ' + kwargs['if2'] + ' ' + kwargs['ratio2'])
                    elif kwargs['load-balancing'] == 'volume':
                        commands.append('weight' + ' ' +  kwargs['if'] + ' ' +  kwargs['weight'])
                    elif kwargs['load-balancing'] == 'spillover':
                        if 'ingress' in kwargs.keys():
                            commands.append('ingress' + ' ' +  kwargs['if_1'] + ' ' +  kwargs['ingress'])
                        if 'egress' in kwargs.keys():
                            commands.append('egress' + ' ' +  kwargs['if_2'] + ' ' +  kwargs['egress'])


                if 'no-sdwan-group' in kwargs.keys() and kwargs['no-sdwan-group']:
                    commands.append('no sdwan-group')
                if 'no-performance-probe' in kwargs.keys():
                    commands.append('no sla-probe ' + kwargs['no-performance-probe'])
            except KeyError:
                logger.info("Error while creating path selection profile")


        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_add_profile = self.fw.do_cli_commands(commands)
        return res_add_profile

    def edit_path_selection_profile(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'name_profile' in kwargs.keys() and kwargs['name_profile']:
            commands.append('path-selection-profile ' + kwargs['name_profile'])
            if 'edit_name' in kwargs.keys() and kwargs['edit_name']:
                commands.append('name ' + kwargs['edit_name'])
            if 'sla-strategy' in kwargs.keys() and kwargs['sla-strategy']:
                commands.append('sla-strategy ' + kwargs['sla-strategy'])
            if 'performance-class' in kwargs.keys() and kwargs['performance-class']:
                commands.append('sla-class ' + kwargs['performance-class'])
            if 'performance-probe' in kwargs.keys() and kwargs['performance-probe']:
                commands.append('sla-probe ' + kwargs['performance-probe'])
            if 'backup-interface' in kwargs.keys() and kwargs['backup-interface']:
                commands.append('backup-interface ' + kwargs['backup-interface'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_edit_profile = self.fw.do_cli_commands(commands)
        return res_edit_profile



    def delete_psp(self, **kwargs):
        commands = ['configure', 'sdwan']
        time.sleep(5)
        if 'no_PSP' in kwargs.keys():
            commands.append('no path-selection-profile ' + kwargs['no_PSP'])
        self.fw._is_key_exist(commands, kwargs, 'no path-selection-profiles')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_del_obj = self.fw.do_cli_commands(commands)
        return res_del_obj

    def show_sdwan_PSP(self, name=None):
        commands = []
        time.sleep(5)
        if name:
            command = 'show sdwan path-selection-profile ' + name
        else:
            command = 'show sdwan path-selection-profiles '
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)
        return output























































