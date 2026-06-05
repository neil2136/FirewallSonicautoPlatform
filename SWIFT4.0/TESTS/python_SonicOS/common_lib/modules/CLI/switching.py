from utm import Firewall
import copy
import re


class Vlan:
    '''Vlan class'''

    def __init__(self, fw):
        self.fw = fw

    def add_trunk_ports(self, ports):
        commands = ['configure', 'switch']
        for i in ports:
            commands.append('trunk port ' + i)
            commands.append('exit')
        cmds = ['commit', 'end', 'exit']
        for cmd in cmds:
            commands.append(cmd)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_trunk_ports(self, ports):
        commands = ['configure', 'switch']
        for i in ports:
            commands.append('no trunk port ' + i)
        cmds = ['commit', 'end', 'exit']
        for cmd in cmds:
            commands.append(cmd)
        result = self.fw.do_cli_commands(commands)
        return result

    def add_vlan(self, vlan_dict):
        commands = ['configure', 'switch']
        for interface, vlan_list in vlan_dict.items():
            if not (re.search('x\d{0,2}', interface)):
                return ('invalid interface' + str(interface))
            vlan_list = [x.strip() for x in vlan_list.split(",")]
            for vlan_to_add in vlan_list:
                if not vlan_to_add.isdigit():
                    return ('invalid vlan' + str(vlan_to_add))
                commands.append('trunk port ' + interface)
                commands.append('vlan ' + vlan_to_add)
                commands.append('exit')
        cmds = ['commit', 'end', 'exit']
        for cmd in cmds:
            commands.append(cmd)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_vlan(self, vlan_dict):
        vlan_dict = copy.deepcopy(vlan_dict)
        commands = ['configure', 'switch']
        for interface, vlan_list in vlan_dict.items():
            vlan_list = vlan_list.split(",")
            for vlan_to_add in vlan_list:
                commands.append('trunk port ' + interface)
                commands.append('no vlan ' + vlan_to_add)
                commands.append('exit')
        cmds = ['commit', 'end', 'exit']
        for cmd in cmds:
            commands.append(cmd)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_vlan(self, *ports):
        commands = []
        if not ports:
            commands.append('show switch trunk ports')
        for i in ports:
            commands.append('show switch trunk port ' + i)
        result = self.fw.do_cli_commands(commands)
        return result


class Link_Aggregation:
    '''Link Aggregation Class'''

    def __init__(self, fw):
        self.fw = fw

    def add_link_agg(self, link_dict):
        link_dict = copy.deepcopy(link_dict)
        load_balance = {
            '1': 'source mac',
            '2': 'destination mac',
            '3': 'source destination mac',
            '4': 'source ip',
            '5': 'destination ip',
            '6': 'source destination ip'

        }
        if 'key' not in link_dict or 'port' not in link_dict:
            return "insufficient information key or port missing"
        commands = ['configure', 'switch']
        commands.append('link-aggregation port ' + link_dict['port'])
        commands.append('key id ' + link_dict['key'])
        if 'lacp' in link_dict and link_dict['lacp'] == '1':
            commands.append('lacp')
        if 'lb' in link_dict:
            commands.append('load-balance-type ' + load_balance[link_dict['lb']])
        if 'member' in link_dict:
            member_list = link_dict['member'].split(",")
            for i in member_list:
                commands.append('member ' + i)
        cmds = ['commit', 'end', 'exit']
        for cmd in cmds:
            commands.append(cmd)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_link_agg(self, link_dict):
        link_dict = copy.deepcopy(link_dict)
        if 'port' not in link_dict.keys():
            return "insufficient information  port missing"
        commands = ['configure', 'switch']
        cmds = ['commit', 'end', 'exit']
        member_result = self.edit_member(link_dict, 'del')
        commands.append('no link-aggregation port ' + link_dict['port'])
        for cmd in cmds:
            commands.append(cmd)
        result2 = self.fw.do_cli_commands(commands)
        result = member_result + result2
        return result

    def delete_member(self, link_dict):
        link_dict = copy.deepcopy(link_dict)
        if 'port' not in link_dict.keys():
            return "insufficient information  port missing"
        member_result = self.edit_member(link_dict, 'del')
        return member_result

    def add_member(self, link_dict):
        link_dict = copy.deepcopy(link_dict)
        if 'port' not in link_dict.keys():
            return "insufficient information  port missing"
        member_result = self.edit_member(link_dict, 'add')
        return member_result

    def edit_member(self, link_dict, oper):
        link_dict = copy.deepcopy(link_dict)
        if 'port' not in link_dict or 'member' not in link_dict:
            return "insufficient information  port or member missing"
        member_cmd = ['configure', 'switch']
        member_cmd.append('link-aggregation port ' + link_dict['port'])
        cmds = ['commit', 'end', 'exit']
        member_list = link_dict['member'].split(",")
        for i in member_list:
            if oper == 'add':
                member_cmd.append('member ' + i)
            else:
                member_cmd.append('no member ' + i)
        for cmd in cmds:
            member_cmd.append(cmd)
        member_result = self.fw.do_cli_commands(member_cmd)
        return member_result

    def show_link_agg(self, *ports):
        commands = []
        if not ports:
            commands.append('show switch link-aggregation')
        for i in ports:
            commands.append('show switch link-aggregation port ' + i)
        result = self.fw.do_cli_commands(commands)
        return result


class Port_Mirroring:
    '''Port Mirroring Class'''

    def __init__(self, fw):
        self.fw = fw

    def add_port_mirror(self, mirr_dict):
        mirr_dict = copy.deepcopy(mirr_dict)
        if 'name' not in mirr_dict or 'mirror' not in mirr_dict or 'mirrored' not in mirr_dict:
            return "insufficient information "
        commands = ['configure', 'switch']
        commands.append('port mirror ' + mirr_dict['name'])
        commands.append('mirror-port ' + mirr_dict['mirror'])
        if 'mirrored' in mirr_dict:
            mirrored_list = mirr_dict['mirrored'].split(",")
            for i in mirrored_list:
                commands.append('mirrored-port ' + i)
        if 'direction' in mirr_dict:
            commands.append('direction ' + mirr_dict['direction'])
        else:
            commands.append('direction ingress')
        if 'enable' in mirr_dict:
            if mirr_dict['enable'] == 0:
                print("not enabling port mirror")
            else:
                commands.append('enable')
        else:
            commands.append('enable')
        cmds = ['commit', 'end', 'exit']
        for cmd in cmds:
            commands.append(cmd)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_port_mirror(self, mirr_dict):
        mirr_dict = copy.deepcopy(mirr_dict)
        if 'name' not in mirr_dict:
            return "insufficient information "
        commands = ['configure', 'switch']
        commands.append('no port mirror ' + mirr_dict['name'])
        cmds = ['commit', 'end', 'exit']
        for cmd in cmds:
            commands.append(cmd)
        result = self.fw.do_cli_commands(commands)
        return result

    def modify_settings(self, mirr_dict):
        mirr_dict = copy.deepcopy(mirr_dict)
        if 'name' not in mirr_dict:
            return "insufficient information "
        commands = ['configure', 'switch']
        commands.append('port mirror ' + mirr_dict['name'])
        if 'new_name' in mirr_dict:
            commands.append('name ' + mirr_dict['new_name'])
        if 'enable' in mirr_dict:
             if mirr_dict['enable'] == '0' or mirr_dict['enable'] == 0:
                 commands.append('no enable')
             elif mirr_dict['enable'] == '1' or mirr_dict['enable'] == 1:
                 commands.append('enable')
        if 'add_mirrored' in mirr_dict:
            mirrored_list = mirr_dict['add_mirrored'].split(",")
            for i in mirrored_list:
                commands.append('mirrored-port ' + i)
        if 'del_mirrored' in mirr_dict:
            mirrored_list = mirr_dict['del_mirrored'].split(",")
            for i in mirrored_list:
                commands.append('no mirrored-port ' + i)
        if 'direction' in mirr_dict:
            commands.append('direction ' + mirr_dict['direction'])
        cmds = ['commit', 'end', 'exit']
        for cmd in cmds:
            commands.append(cmd)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_port_mirror(self, *names):
        commands = []
        if not names:
            commands.append('show switch port mirrors')
        for i in names:
            commands.append('show switch port mirror ' + i)
        result = self.fw.do_cli_commands(commands)
        return result
