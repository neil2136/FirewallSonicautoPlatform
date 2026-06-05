import sys
import os
import re
from types import DynamicClassAttribute
import yaml
import json
import argparse
from runner.settings import logger
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


class DeviceConfig():
    def __init__(self, user='admin', password='password', specformat='yaml',specfile=None):
        self.user = user
        self.password = password
        self.specformat = specformat
        self.specfile = specfile
        self.controller = {}
        self.TOPO = {}
        self.VLAN = {}
        self.NODES = {}
        self.PORTS = {}
        self.load_yaml()

    def spec_format(self):
        return self.specformat

    def default_setting(self, device=None):
        if not device:
            logger.error('Please specify the target device name.')
            return None
        if self.specformat == 'yaml':
            result = self.topo(device)
            if result:
                vlan = result
                return vlan
            return None
        else:
            logger.error('default_setting(): unsupported spec format.')
    
    def device(self, device=None, host=0):
        if self.specformat != 'yaml':
            logger.error('topo(): Unsupported spec format:{}'.format(self.specformat))
            return None 
        if not device:
            devices = sorted(self.conf['device'].keys())
            return devices
        if host:
            device_g = self._smart_find(self.conf['host'], device)
        else:
            device_g = self._smart_find(self.conf['device'], device)       
        if not device_g:
            logger.error('{} is not a valid device name.'.format(device))
            return None
        if host:
            result = self.conf['host'][device]
        else:
            result = self.conf['device'][device]
        return [result, device_g]

    def topo(self, topo=None):
        if self.specformat != 'yaml':
            logger.error('topo(): Unsupported spec format:{}'.format(self.specformat))
            return None            
        if not topo:
            if 'topo' in self.conf['topo']:
                topos = sorted(self.conf['topo'])
            for dev in sorted(self.conf['device']):
                topos.append(dev)
            return topos
        topo_g =self._smart_find(self.conf['topo'], topo)
        if not topo_g:
            topo_g = self._smart_find(self.conf['device'], topo)
            if not topo_g:
                logger.error('{} is not a valid topology name!')
                return None
            elif 'default' not in self.conf['device'][topo_g].keys():
                logger.error('Device {} has no default topo!')
                return None
            else:
                result = self.conf['device'][topo_g]['default']
        elif 'default' in self.conf['topo'][topo_g].keys():
            result = self.conf['topo'][topo_g]['default']
        else:
            result = self.conf['topo'][topo_g]
        return result

    def config_network(self, action, net='', node_list=None):
        TMP_VLAN = {}
        if self.specformat != 'yaml':
            logger.error('Unsupported spec format: {}'.format(self.specformat))
            return None
        switches = self.control('switch')
        for switch in switches:
            self.load_object('switch', switch)
        if re.search(r':\d+$', net):
            net_name, net_id = net.split(':')
            net_id = int(net_id)
        elif re.search(r'^\d+$', net):
            net_name = 'VLAN' + net
            net_id = net
        else:
            net_name = net
        net_name=net_name.upper()
        if action.lower() == 'clear':
            logger.info('Clearing all customized VLAN (id >= 100)')
            for sw in sorted(self.VLAN.keys()):
                TMP_VLAN[sw]={}
                for vlan in sorted(self.VLAN[sw].keys()):
                    if int(vlan) < 100:
                        continue 
                    TMP_VLAN[sw][vlan] = self.VLAN[sw][vlan]
            self.TOPO = self.VLAN = {}
            for n in sorted(self.NODES.keys()):
                changes = 0
                if 'state' not in self.NODES or self.NODES['state'] == 'up':
                    changes += 1
                if not changes and 'uvlan' in self.NODES[n]:
                    if self.NODES[n]['uvlan'] != 'default':
                        changes += 1
                if not changes and 'tvlan' in self.NODES[n]:
                    if self.NODES[n]['tvlan'].len() >0:
                        changes += 1 
                if changes:
                    self.NODES[n]['tvlan'] = []
                    self.NODES[n]['uvlan'] = 'defalut'
                    self.NODES[n]['state'] = 'down'
        elif not node_list:
            if action.lower() == 'add':
                logger.error('nodes are required while adding vlan.')
                return None
            elif action.lower() == 'rem':
                if net_name not in self.TOPO.keys():
                    logger.error('no vlan called {}'.format(net_name))
                    return None
                node_list = self.NODES[net_name]['node'].keys()
                if not node_list:
                    vid = self.TOPO[net_name]['vlan_id']
                    for sw in self.VLAN.keys():
                        for vlan in self.VLAN[sw].keys():
                            if vid == vlan and not self.VLAN[sw][vlan]['port']:
                                TMP_VLAN[sw][vlan] = []
                                self.VLAN[sw].pop(vlan) 
                                self.TOPO.pop(net_name)
                    logger.error('Deleting empty VLAN {}({})'.format(net_name, vid))
                    result = self._dispatch_to_switch('rem', TMP_VLAN)
                    if not result:
                        return None
                    return True
        if action.lower() != 'clear':
            self._unique_list(node_list)
            if net_name in self.TOPO.keys():
                vlan_id = self.TOPO[net_name]['vlan_id']
                restart = ''
                if 'net_id' in locals() and net_id != vlan_id:
                    logger.error('VLAN {} exists already with ID {}'.format(net_name, vlan_id))
                    if action.lower() == 'add':
                        logger.info('Removing {} to avoid network failure.'.format(net_name))
                        if not self.config_network('rem', net_name):
                            return None
                        vlan_id = net_id
                        action = 'add'
                        self.TOPO[net_name]['vlan_id'] = net_id
                        restart = 1
                dedicate_vid = self._get_dedicate_vid(node_list)
                if dedicate_vid and dedicate_vid != int(vlan_id):
                    logger.error('{} conflicts with the predefined ID {}'.format(net_name[vlan_id],dedicate_vid))
                    if re.search('add', action, re.I):
                        logger.info('Removing {} to avoid network failure.'.format(net_name))
                        if not self.config_network('rem', net_name):
                            return None
                        vlan_id = dedicate_vid
                        action = 'add'
                        self.TOPO[net_name]['vlan_id'] = dedicate_vid
                        restart = 1
                if not vlan_id:
                    logger.error('VLAN {} exists without vlan id.'.format(net_name))
                    return None
                if restart and re.search('add', action, re.I):
                    action = 'addp'          
            elif re.search('add', action, re.I):
                dedicate_vid = self._get_dedicate_vid(node_list)
                if 'net_id' in locals().keys():
                    if self._is_vid_used(net_id):
                        logger.error('VLAN ID {} has been used already.')
                        return None
                    min_vid = 1
                    max_vid = 4096
                    testbed = self.conf['testbed']
                    if 'min_vid' in self.conf.keys():
                        min_vid = self.conf['min_vid']
                    if 'max_vid' in self.conf.keys():
                        max_vid = self.conf['max_vid']
                    if type(net_id) is int and (net_id < min_vid or net_id > max_vid):
                        logger.error('VLAN ID {} must be between {} and {}'.format(testbed, min_vid, max_vid))
                        return None
                    vlan_id = net_id
                elif dedicate_vid:
                    vlan_id = dedicate_vid
                # elsif ( my $dedicate_vid =
                #     $self->_get_dedicate_vid($nodes_list_ref) )
                # {
                #     $vlan_id = $dedicate_vid;
                # }
                else:
                    vlan_id = self._get_free_vid()
                    if not vlan_id:
                        return None
                self.TOPO[net_name] = {}
                self.TOPO[net_name]['vlan_id'] = vlan_id
                action = 'add'  
            elif re.search('rem', action, re.I):
                logger.error('{} does not exist, skipping'.format(net_name))           
                return True
            node_info = ''
            for n in node_list:
                if re.search(r'^\s*$', n):
                    continue
                (node_dict, node, flag, mtu) = self.node(n, 'totrunk')
                if not node_dict:
                    logger.error('Cannot determine node name for {}, aborting...'.format(n))
                    return None
                switch = node_dict['switch']
                port = node_dict['port']
                if switch not in TMP_VLAN.keys():
                    TMP_VLAN[switch] = {}
                if vlan_id not in TMP_VLAN[switch].keys():
                    TMP_VLAN[switch][vlan_id] = {}
                if 'name' not in TMP_VLAN[switch][vlan_id]:
                    TMP_VLAN[switch][vlan_id]['name'] = net_name
                if 'vm' in node_dict.keys():
                    vserver = node_dict['vserver']
                    vm = node_dict['vm']
                    # vnic = node_dict['vnic']
                    if not re.search(r'u|t', flag, re.I):
                        flag = "T" + flag
                node_info = node_info + node + '({}:{}),'.format(switch,port)
                if re.search(r'add', action, re.I):
                    flag_g = self._add_node(node, net_name, flag)
                elif re.search(r'rem', action, re.I):
                    flag_g = self._rem_node(node, net_name, action, flag)
                    if not flag_g:
                        logger.warning('{} doesnot belong to {}, skipping'.format(node, net_name))
                        node_info = re.sub(r''+ node + '', '(' + switch + ':' + port + ')', node_info)
                        continue
                port = str(port) + ':' + flag_g
                if mtu:
                    port = str(port) + ':' + mtu
                if 'port' not in TMP_VLAN[switch][vlan_id]:
                    TMP_VLAN[switch][vlan_id]['port'] = []
                self._add_to_list(TMP_VLAN[switch][vlan_id]['port'], port)
                if 'configure_vserver' in self.conf.keys() and 'vm' in node_dict.keys():
                    self._add_to_list(TMP_VNET[vserver][net_name][vm], vnic)
            node_info = re.sub(r',$', '', node_info)
            if re.search(r'rem', action, re.I):
                if net_name in self.TOPO.keys():
                    if not re.search(r'remu', action, re.I):
                        action = 'remp'
                    if re.search(r'remu', action, re.I):
                        action = 'remup'  
                    logger.info('Removing [{}] from {}'.format(node_info, net_name))
                else:
                    logger.info('Removing {}:[{}]'.format(net_name, node_info))
                    if not re.search(r'remu', action, re.I):
                        action = 'rem'
                    if re.search(r'remu', action, re.I):
                        action = 'remu'   
            else:
                logger.info('Adding {}:[{}]'.format(net_name, node_info))               
        if re.search(r'clear', action, re.I):
            action = 'rem'
        result = self._dispatch_to_switch(action, TMP_VLAN)
        if not result:
            return None
        # if TMP_VNET:
        #     result = self._dispatch_to_vserver(action, TMP_VNET)
        #     if not result:
        #         return None
        return True

    def node(self, node, to_trunk='', flag='', mtu=''):
        if self.specformat != 'yaml':
            logger.error('node(): Unsupported spec format: {}'.format(self.specformat))
            return None
        if not node:
            nodes = sorted(self.NODES.keys())
            return nodes
        if re.search(':', node):
            tmp = re.split(r':+', node)
            h = tmp.pop(0)
            m= ''
            if tmp: m = tmp.pop()
            if re.search(r'^\d+$', m):
                mtu = m
            else:
                tmp.append(m)
            if tmp: t = tmp.pop()
            if re.search('^[tuehm!]+$', t, re.I):
                flag = t.upper()
            else:
                tmp.append(t)  
            if re.search(r'TRUNK\d+', h, re.I):
                node = h
            else:
                if re.search(r'(hp|v)?sw\d+$', h, re.I):
                    switch = h + ':'
                else:
                    tmp.insert(0, h)
                if len(tmp) == 1:
                    if re.search('TRUNK', tmp[0], re.I): 
                        node = 'switch' + tmp[0]
                    else:
                        (ct, node) = self.num_to_name(switch + tmp[0])
                else:
                    node = tmp[0] + ':' + tmp[1]
        node_g = self._smart_find(self.NODES, node)
        if not node_g:
            logger.error('{} is not a valid node name.'.format(node))
            return None

        if to_trunk and 'trunk' in self.NODES[node_g].keys():
            node_g = self.NODES[node_g]['trunk']
        result = {}
        result = self.NODES[node_g]
        return (result, node_g, flag, mtu)

    def _get_dedicate_vid(self, node_list):
        vid_node = {}
        for node in node_list:
            (node_dict, n, flag, mtu) = self.node(node)
            if 'vm' in node_dict and 'pvid' in node_dict:
                vid = node_dict['pvid']
                vid_node[vid] = n
        vid = vid_node.keys()
        if len(vid) == 1:
            return tuple(vid)[0]
        elif len(vid) > 1:
            logger.error("Conflict static VLAN ids found:")
            logger.error(vid_node)

            return None
        return None

    def _add_to_list(self, tmp_list, element):
        for i in range(0, int(len(tmp_list))):
            if tmp_list[i] == element:
                return True
        tmp_list.append(element)
        return True

    def _remove_from_list(self, tmp_list, element):
        position = None
        for i in range(0, int(len(tmp_list))):
            if tmp_list[i] == element:
                position = str(i)
                break
        if position:
            del tmp_list[int(position)]
        else:
            return None
            
    def _is_vid_used(self, vid):
        for sw in self.VLAN.keys():
            if vid in self.VLAN[sw]:
                return True
        return False
 
    def _unique_list(self, tmp_list):
        unique = []
        seen = {}
        for elem in tmp_list:
            if elem in seen.keys():
                continue
            else:
                seen[elem] = 1
            unique.append(elem)
        return unique

    def _get_free_vid(self):
        switches = self.VLAN.keys()
        if 'min_vid' in self.conf.keys():
            min_vid = self.conf['min_vid']
        else:
            min_vid = 100
        if 'max_vid' in self.conf.keys():
            max_vid = self.conf['max_vid']
        else:
            max_vid = 4094
        for id in range(min_vid, max_vid):
            for sw in switches:
                if str(id) in self.VLAN[sw].keys() or id in self.VLAN[sw].keys():
                    main_break = False
                    break
                else:
                    main_break = True
            if main_break:
                return id
        logger.error('No free VLAN ID between {} and {}'.format(min_vid, max_vid))
        return None
                
    def _smart_find(self, base, target):
        fully_matched = []
        num_matched = []
        partial_matched = []
        if isinstance(base, dict):
            base_list = base.keys()
        elif isinstance(base, list):
            base_list = base
        else:
            return None
        for obj in base_list:
            if obj.upper() == target:
                fully_matched.append(obj)
            elif re.search(r'' + target + '$', obj, re.I):
                num_matched.append(obj)
            elif re.search(r'' + target + '', obj, re.I):
                partial_matched.append(obj)
        if int(len(fully_matched)) == 1:
            target = fully_matched[0]
        elif int(len(num_matched)) == 1:
            target = num_matched[0]
        elif int(len(partial_matched)) == 1:
            target = partial_matched[0]
        elif int(len(fully_matched)) > 1:
            logger.error('Duplicate targets named {} found: [{}]'.format(target, fully_matched))
            return None
        elif int(len(num_matched)) > 1:
            logger.error('More than one targets surfix-matched {} found:[{}]'.format(target, num_matched))
            return None
        elif int(len(partial_matched)) > 1:
            logger.error('More than one targets partial-matched {} found:[{}]'.format(target, partial_matched))
            return None
        else:
            logger.error('None targets found matched {}'.format(target))
            return None            
        return target

    def num_to_name(self, port=None):
        if not port:
            logger.error('Please supply port number.')
            return None
        tmp_list = re.split(r':+', port)
        switch = ''
        p_num = ''
        if re.search(r'(hp|v)?sw', tmp_list[0], re.I):
            switch = tmp_list[0]
            p_num = tmp_list[1]
        elif re.search(r'^(\d+/)?d+$', tmp_list[0], re.I):
            p_num = tmp_list[0]
        if not p_num:
            logger.error('Port num is null')
            return None
        if p_num not in self.PORTS or switch not in self.PORTS[p_num].keys():
            p_num_2 = p_num
            match = re.search(r'^\d/(\d+)$', p_num)
            if match:
                p_num_2 = match.group(1)
            if p_num_2 in self.PORTS.keys() and (switch in self.PORTS[p_num_2].keys()):
                p_num = p_num_2
            else:
                return(switch, 'Port' + str(p_num))
        #p_num = int(p_num)
        total = len(self.PORTS[p_num])
        if total > 1:
            if not switch:
                logger.error('More than one port with same no.: {}, switch name required.'.format(p_num))
                return None
            for sw in self.PORTS[p_num].keys():
                if re.search(r'^'+ switch +'$', sw, re.I):
                    return(sw, self.PORTS[p_num][sw])
        ct = tuple(self.PORTS[p_num].keys())[0]
        node =self.PORTS[p_num][ct]
        if not switch:
            return (ct, node)
        if re.search(r'^'+ switch +'$', ct, re.I): 
            return (ct, node)
               
        logger.error('The port is only available on {}, not {}'.format(ct, switch))
        return None
        
    def load_yaml(self):
        '''
        Loads the test bed specification yaml file for this controller
        '''
        if re.search(r'URL', self.specformat.upper()):
            raise NotImplementedError
        if not os.path.exists(self.specfile):
            raise FileNotFoundError
        with open(self.specfile) as f:
            try:
                self.conf = json.loads(json.dumps(yaml.load(f,yaml.Loader)))
                self.specformat = 'yaml'
                for dev in sorted(self.conf['device']):
                    self._init_data(self.conf['device'][dev], dev)
                for host in sorted(self.conf['host']):
                    self._init_data(self.conf['host'][host], host) 
                self.specformat = 'yaml'
                return self.conf
            except Exception as e:
                logger.error('Unsupported config file! Only support yaml for now: {}'.format(e))
                self.specformat = 'other'
                return None

#powercontrol rpsw5 CDU 10.6.0.15 sentry
    def load_object(self, type, controller, cmodule=None, cip=None, ctype=None):
        '''
        Dynamically loads an object that is capable of connecting to
        and configuring the given controller.
        '''
        if re.search(r'power', type, re.I) and re.search(r'URL', self.specformat.upper()):
            ctrl_type = 'powercontrol' 
            if self.controller[controller]: return self
        elif re.search(r'switch', type) and re.search(r'URL', self.specformat.upper()):
            ctrl_type = 'switch' 
            if self.controller[controller]: return self
        elif re.search(r'switch|power', type):
            if re.search(r'power', type, re.I):
                ctrl_type = 'powercontrol'
            else:
                ctrl_type = 'switch' 
            ctype = self.conf[ctrl_type][controller]['type']
            cmodule = self.conf[ctrl_type][controller]['model']
            if controller in self.controller.keys():
                return self
        else:
            logger.error('Unrecognized object type:{}'.format(type))
            return None
        logger.info('Ready to load {}.{}.{}'.format(ctrl_type, ctype, cmodule))
        try:
            import_type_name = ctrl_type + '.' + ctype
            import_type1 = __import__(import_type_name)
            import_type2 = getattr(import_type1, ctype.lower())
            import_module = getattr(import_type2, cmodule)
        except:
            logger.error('Unable to Load Module defined as {}.{}.{}'.format(ctrl_type, cmodule, ctype))
            return None
        if re.search(r'switch|power', type):
            ctrl_ip = self.conf[type][controller]['ip']
            if 'user' in self.conf[type][controller]:
                self.user = self.conf[type][controller]['user']
            if 'password' in self.conf[type][controller]:
                self.password = self.conf[type][controller]['password']
            if re.search(r'URL', self.specformat.upper()):
                ctrl_ip = controller
            try:
                object_dict = {'ip': ctrl_ip, 'user': self.user, 'password': self.password, 'controllername': controller}
                self.controller[controller] = import_module(**object_dict)
            except Exception as e:
                logger.error('Unable to create object {}.{}.{}: {}'.format(ctrl_type, ctype, cmodule, e))
                return None
        if re.search(r'switch', type) and not re.search(r'URL', self.specformat.upper()):
            self.VLAN[controller] = self.controller[controller].getConf()
            logger.info("Dumping {} VLAN setting before configuration...".format(controller))
            logger.info(self.VLAN[controller])
            self._dump_vlan(self.VLAN[controller], controller)
        return self
    
    def power(self, action, device, host=0):
        if not device:
            logger.error('Please specify the target device name, and the action')
            return None
        if not re.search(r'(power)?(on|off|cycle)', action, re.I):
            logger.error('Unrecognized action: ' + action)
            return None
        if not re.search(r'power', action, re.I):
            action = 'power' + action
        if re.search(r'(v|hp)?sw\d+$', device, re.I):
            [dev_dict, dev] = self.control('switch', device)
        else:
            [dev_dict, dev] = self.device(device, host)
        if not dev_dict:
            logger.error('No such device: ' + device)
            return None
        rpsw = dev_dict['power']['controller']
        port = dev_dict['power']['port']

        self.load_object('powercontrol', rpsw)
        logger.info('Trying to {} {} on {}...'.format(action, dev, rpsw))
        result = self._configure_power(action, rpsw, dev, port)
        return result

    def _configure_power(self, action, powercontroller, device, port_number):
        if self.specformat != 'yaml':
            logger.error('_configure_power(): Unsupported spec format: {}'.format(self.specformat))
            return None
        if not port_number:
            logger.error('The device {} attached to {} has no port defination.'.format(device, powercontroller))
            return None
        logger.info('{} attached to port {} of {}'.format(device, port_number, powercontroller))
        result = self.controller[powercontroller].execute(action, port_number)
        return result

    def _init_data(self, target, device, conf_vs=None):
        switches = {}
        for interface in target['interface']:
            # {'console': {'server': '10.6.0.32', 'sshport': 3007, 'telnetport': 2007}, 'power': 'controller = rpsw32 port = AB4', 'interface': {'X0': {'switch': 'sw32', 'port': 12}, 'X1': {'switch': 'sw32', 'port': 13}, 'X2': {'switch': 'sw32', 'port': 14}, 'X3': {'switch': 'sw32', 'port': 15}}}
            sw = target['interface'][interface]['switch']
            port = str(target['interface'][interface]['port'])
            if 'switch' not in target.keys():
                target['switch'] = [sw]
                switches[sw] = 'y'
            elif sw not in switches.keys():
                target['switch'].append(sw)
                switches[sw] = 'y'
            node = device + ':' + interface
            self.NODES[node] = {}
            self.NODES[node]['switch'] = sw
            self.NODES[node]['port'] = port
            if 'pvid' in target['interface'][interface]:
                self.NODES[node]['pvid'] = target['interface'][interface]['pvid']
            if 'vm' in target.keys():
                if conf_vs == 'yes':
                    if 'vnic' not in target['interface'][interface]:
                        logger.error('"vnic" not defined for {} of VM {}'.format(interface,target['vm']['name']))
                        os._exit() 
                    self.NODES[node]['vnic'] = target['interface'][interface]['vnic']
                self.NODES[node]['vm'] = target['vm']['name']
                self.NODES[node]['vserver'] = target['vm']['server']
                self.NODES[node]['trunk'] = sw + ":TRUNK" + str(port)
                self.PORTS[port] = {}
                self.PORTS[port][sw] = sw + ":TRUNK" + str(port)
                tmp_node = sw + ":TRUNK" + str(port)
                if tmp_node not in self.NODES.keys():
                    self.NODES[tmp_node] = {}
                    self.NODES[tmp_node]['switch'] = sw
                    self.NODES[tmp_node]['port'] = port
                    self.NODES[tmp_node]['vm'] = target['vm']['name']
                    self.NODES[tmp_node]['vserver'] = target['vm']['server']

            else:
                self.PORTS[port] = {}
                self.PORTS[port][sw] = node
            '''
{'NSA5600:X0': {'switch': 'sw_vtb113', 'port': 35}, 'NSA5600:X1': {'switch': 'sw_vtb113', 'port': 36}, 'NSA5600:X2': {'switch': 'sw_vtb113', 'port': 37}, 'NSA5600:X3': {'switch': 'sw_vtb113', 'port': 38}, 'NSA5600:MGMT': {'switch': 'sw_vtb113', 'port': 40}, 'SONICPOINT_ACe:X1': {'switch': 'sw_vtb113', 'port': 29}, 'SONICPOINT_ACi:X1': {'switch': 'sw_vtb113', 'port': 28}, 'SONICPOINT_NDR:X1': {'switch': 'sw_vtb113', 'port': 21}, 'SONICPOINT_NE:X1': {'switch': 'sw_vtb113', 'port': 20}, 'SONICPOINT_W2-ACO:X1': {'switch': 'sw_vtb113', 'port': 39}, 'SONICWAVE_231o_1:X1': {'switch': 'sw_vtb113', 'port': 0}, 'SONICWAVE_231o_2:X1': {'switch': 'sw_vtb113', 'port': 3}, 'SONICWAVE_432i:X1': {'switch': 'sw_vtb113', 'port': 1}, 'TZ470W:X0': {'switch': 'sw_vtb113', 'port': 12}, 'TZ470W:X1': {'switch': 'sw_vtb113', 'port': 13}, 'TZ470W:X2': {'switch': 'sw_vtb113', 'port': 14}, 'TZ470W:X3': {'switch': 'sw_vtb113', 'port': 15}, 'VTB113-GW:X0': {'switch': 'sw_vtb113', 'port': 22}, 'VTB113-NTA1000:eth0': {'switch': 'sw_vtb113', 'port': 16}, 'VTB113-NTA1000:eth1': {'switch': 'sw_vtb113', 'port': 17}, 'VTB113-NTA1000:eth2': {'switch': 'sw_vtb113', 'port': 18}, 'VTB113-NTA1000:eth3': {'switch': 'sw_vtb113', 'port': 19}, 'VTB113-PC1:eth0': {'switch': 'sw_vtb113', 'port': 42, 'pvid': 2096, 'vm': 'VTB113-PC1', 'vserver': 'ESX-SH', 'trunk': 'sw_vtb113:TRUNK42'}, 'sw_vtb113:TRUNK42': {'switch': 'sw_vtb113', 'port': 42, 'vm': 'VTB113-PC1', 'vserver': 'ESX-SH'}, 'VTB113-PC2:eth0': {'switch': 'sw_vtb113', 'port': 27}}
{35: {'sw_vtb113': 'NSA5600:X0'}, 36: {'sw_vtb113': 'NSA5600:X1'}, 37: {'sw_vtb113': 'NSA5600:X2'}, 38: {'sw_vtb113': 'NSA5600:X3'}, 40: {'sw_vtb113': 'NSA5600:MGMT'}, 29: {'sw_vtb113': 'SONICPOINT_ACe:X1'}, 28: {'sw_vtb113': 'SONICPOINT_ACi:X1'}, 21: {'sw_vtb113': 'SONICPOINT_NDR:X1'}, 20: {'sw_vtb113': 'SONICPOINT_NE:X1'}, 39: {'sw_vtb113': 'SONICPOINT_W2-ACO:X1'}, 0: {'sw_vtb113': 'SONICWAVE_231o_1:X1'}, 3: {'sw_vtb113': 'SONICWAVE_231o_2:X1'}, 1: {'sw_vtb113': 'SONICWAVE_432i:X1'}, 12: {'sw_vtb113': 'TZ470W:X0'}, 13: {'sw_vtb113': 'TZ470W:X1'}, 14: {'sw_vtb113': 'TZ470W:X2'}, 15: {'sw_vtb113': 'TZ470W:X3'}, 22: {'sw_vtb113': 'VTB113-GW:X0'}, 16: {'sw_vtb113': 'VTB113-NTA1000:eth0'}, 17: {'sw_vtb113': 'VTB113-NTA1000:eth1'}, 18: {'sw_vtb113': 'VTB113-NTA1000:eth2'}, 19: {'sw_vtb113': 'VTB113-NTA1000:eth3'}, 42: {'sw_vtb113': 'sw_vtb113:TRUNK42'}, 27: {'sw_vtb113': 'VTB113-PC2:eth0'}}

            '''
    def _dispatch_to_switch(self, action, vlan):
        for switch in vlan.keys():
            if not vlan[switch]:
                self.load_object('switch', switch)
            result = self._configure_vlan(action, switch, vlan[switch])
            if not result:
                return None
        return True

    def _add_node(self, node, net_name, flag):
        port = self.NODES[node]['port']
        switch = self.NODES[node]['switch']
        vlan_id = str(self.TOPO[net_name]['vlan_id'])

        if '_UNUSED_' in self.TOPO.keys() and self.TOPO['_UNUSED_']['node'][node]:
            unused_vid = self.TOPO['_UNUSED_']['vlan_id']
            self.TOPO['_UNUSED_']['node'].pop(node)
            self._remove_from_list(self.VLAN[switch][unused_vid]['port'], port)
        if flag and re.search(r'!u|^t|[^!]t', flag, re.I):
            tag_flag = 'T'
        else:
            tag_flag = 'U'
        if flag and re.search(r'^h|[^!]h', flag, re.I):
            tag_flag += 'H'
        if flag and re.search(r'^m|[^!]m', flag, re.I):
            tag_flag += 'M'
        if flag and re.search(r'!e', flag, re.I):
            self.NODES[node]['state'] = 'down'
        else:
            self.NODES[node]['state'] = 'up'

        if tag_flag == 'U':
            if 'uvlan' in self.NODES:
                old_vlan = self.NODES[node]['uvlan']
                if old_vlan == 'default':
                    old_vlan_id = self.TOPO[old_vlan]['vlan_id']
                    self.TOPO[old_vlan]['node'].pop(node)
                    self._remove_from_list(self.VLAN[switch][old_vlan_id]['ports'], port + '' + 'U')
            self.NODES[node]['uvlan'] = net_name
        else:
            self.NODES[node]['tvlan'] = []
            self._add_to_list(self.NODES[node]['tvlan'], net_name)

        if 'node' not in self.TOPO[net_name].keys():
            self.TOPO[net_name]['node'] = {}
        self.TOPO[net_name]['node'][node] = tag_flag
        if vlan_id not in self.VLAN[switch].keys():
            self.VLAN[switch][vlan_id] = {}
        if 'name' in self.VLAN[switch][vlan_id].keys():
            self.VLAN[switch][vlan_id]['name'] = net_name
        if 'port' not in self.VLAN[switch][vlan_id].keys():
            self.VLAN[switch][vlan_id]['port'] = []
        self._add_to_list(self.VLAN[switch][vlan_id]['port'], str(port) + ':' + tag_flag)
        if flag and re.search(r'!e', flag, re.I):
            return '!E' + tag_flag
        return 'E' + tag_flag

    def _rem_node(self, node, net_name, mode, flag):
        tag_flag = None
        port = self.NODES[node]['port']
        switch = self.NODES[node]['switch']
        if self.TOPO.get(net_name):
            vlan_id = self.TOPO[net_name]['vlan_id']
        else:
            return None
        if net_name not in self.TOPO.keys():
            logger.error('no vlan called {} found.'.format(net_name))
            return None
        tag_flag = self.TOPO[net_name]['node'].pop(node)
        if int(len(self.TOPO[net_name]['node'])) == 0 and not re.search(r'p', mode, re.I):
            self.TOPO.pop(net_name)
        if not tag_flag:
            return None
        self._remove_from_list(self.VLAN[switch][vlan_id]['port'], str(port) + ':' + tag_flag)
        is_port_used = False
        if tag_flag == 'U':
            self.NODES[node]['uvlan'] = 'default'
            if 'tvlan' in self.NODES[node].keys() and int(len(self.NODES[node]['tvlan'])) !=0:
                is_port_used = True
        elif tag_flag == 'T':
            self._remove_from_list(self.NODES[node]['tvlan'], net_name)
            if 'uvlan' in self.NODES[node].keys() and not re.search(r'^default|_UNUSED_', self.NODES[node]['uvlan'], re.I):
                is_port_used = True
            if int(len(self.NODES[node]['tvlan'])): 
                is_port_used = True
        if is_port_used:
            if (flag and re.search(r'!e', flag, re.I)) and not re.search(r'remu', mode, re.I):
                if not re.search(r'remall', mode, re.I):
                    logger.warning('Be careful to rem {}, which is a member of other vlans.'.format(node))    
                    self.NODES[node]['state'] == 'down'
                else:
                    self.NODES[node]['state'] == 'up'
        else:
            if not re.search(r'remu', mode, re.I) and (not flag or re.search(r'!e', flag, re.I)):
                self.NODES[node]['state'] = 'down'
            else:
                if '_UNUSED' not in self.TOPO.keys():
                    vid = self._get_free_vid()
                    self.TOPO['_UNUSED_'] = {}
                    self.TOPO['_UNUSED_']['vlan_id'] = vid
                    self.VLAN[switch][vid] = {}
                    self.VLAN[switch][vid]['name'] = '_UNUSED_'
                unused_vid = self.TOPO['_UNUSED_']['vlan_id']
                self.TOPO['_UNUSED_'][node] = 'U'
                self.VLAN[switch][unused_vid]['port'] = []
                self._add_to_list(self.VLAN[switch][unused_vid]['port'], port)
                self.NODES[node]['uvlan'] = '_UNUSED_' 
                self.NODES[node]['state'] = 'up' 
        if int(len(self.VLAN[switch][vlan_id]['port'])) == 0:
            self.VLAN[switch].pop(vlan_id)
        if int(len(self.VLAN[switch])) == 0:
            self.VLAN.pop(switch)
        if re.search(r'remu', mode, re.I) or (is_port_used and (not flag or not re.search(r'!e', flag, re.I))):
            return 'E' + tag_flag
        return '!E' + tag_flag

    def configure_node_trunk(self, action, nodes):
        nodes =nodes.split(',')
        node = nodes[0]
        param = {}
        match_trunk = re.search(r'(add-trunk|rem-trunk)-(\d+)', action)
        if match_trunk:
            trunk = match_trunk.group(2) 
            if re.search('add',action):
                param['trunk'] = '+' + trunk
            if re.search('rem',action):
                param['trunk'] = '-' + trunk

        if re.search(r'((hp|v)?sw\d+):(\d+)$|^\d+$',node):
            p_num = node
            [switch, node] = self.num_to_name(p_num)
            if not node: 
                return None
        else:
            n_tmp = node
            (node_dict, node, flag, mtu) = self.node(n_tmp)
            switch = node_dict['switch']
        self.load_object('switch',switch)
        for node in nodes:
            n_tmp = node
            (node_dict, node, flag, mtu) = self.node(n_tmp)
            switch = node_dict['switch']
            port = node_dict['port']
            if not node_dict:
                logger.error(f"configure_node_trunk: invalid node {n_tmp}")
                return None
            match = re.search(r'^([\w\d-]+):([\w\d]+)$',node)
            if match:
                device = match.group(1)
                interface = match.group(2)
            result = self._configure_port(switch, device, interface,port, param)
            if not result:
                return None
        if re.search(r'trunk',result):
            match_trunk_1 = re.search(r'\+(\d+)',param['trunk'])
            if match_trunk_1:
                self.NODES[node]['trunk'] = match_trunk_1.group(1)
            match_trunk_2 = re.search(r'\-(\d+)',param['trunk'])
            #if match_trunk_2:
             #   self.NODES[node]['trunk'].pop()
        return True

    def configure_node(self, action, nodes):
        nodes =nodes.split(',')
        node = nodes[0]
        param = {
            'speed':'',
            'state':'',
            'duplex':'',
        }
        if re.search(r'(on|off)-mirror-(.*)',action):
            logger.error('Action for mirror not ready yet.')
            return None

        if re.search(r'((hp|v)?sw\d+):(\d+)$|^\d+$',node):
            p_num = node
            [switch, node] = self.num_to_name(p_num)
            if not node:
                return None

        n_tmp = node
        (node_dict, node, flag, mtu) = self.node(n_tmp)
        if not node_dict:
            logger.error(f"configure_node: invalid node {n_tmp}")
            return None
        match = re.search(r'^([\w\d-]+):([\w\d]+)$',node)
        if match:
            device = match.group(1)
            interface = match.group(2)
        port = node_dict['port']
        switch = node_dict['switch']
        self.load_object('switch',switch)
        match_vlan = re.search(r'(add|rem)-vlan-(.*)$',action)
        match_trunk = re.search(r'(add-trunk|rem-trunk)-(\d+)', action)
        if match_vlan:
            act = match_vlan.group(1)
            vlan_flag = match_vlan.group(2).split(':')
            vlan = vlan_flag[0]
            flag = ''
            if len[vlan_flag]>1:
                flag = vlan_flag[1]  
            if 'trunk' in self.NODES[node]:
                trk = self.NODES[node]['trunk']
                vlan_dict= {vlan:{'port':[f'{port}:K{trk}{flag}']}}
            else:
                if not flag:
                    flag = ':' + flag
                vlan_dict= {vlan:{'port':[f'{port}{flag}']}}
            act = act + 'p'
            self.load_object('switch',switch)
            result = self._configure_vlan(act, switch, 'NodeVLAN', vlan_dict)
            if not result:
                return None
            return True
        elif match_trunk:
            trunk = match_trunk.group(2)
            if re.search('add',action):
                param['trunk'] = '+' + trunk
            if re.search('rem',action):
                param['trunk'] = '-' + trunk    
        match_speed = re.search(r'(\d+|auto-speed)',action)
        if match_speed:
            speed = match_speed.group(1)
            if not re.search('auto',speed):
                param['speed'] = speed.upper()
            else:
                param['speed'] = 'auto' 
        duplex_match = re.search(r'(half|full|auto-duplex)',action)
        if duplex_match:
            duplex = duplex_match.group(1)
            if not re.search('auto',duplex):
                param['duplex'] = duplex.lower()
            else:
                param['duplex'] = 'auto'
        state_match = re.search(r'(up|down)',action)
        if state_match:
            state = state_match.group(1)
            param['state'] = state.lower()     
        result = self._configure_port(switch, device, interface,port, param)   
        if not result:
            return None
        if re.search(r'trunk',result):
            match_trunk_1 = re.search(r'\+(\d+)',param['trunk'])
            if match_trunk_1:
                self.NODES[node]['trunk'] = match_trunk_1.group(1)
            match_trunk_2 = re.search(r'\-(\d+)',param['trunk'])
            if match_trunk_2:
                self.NODES[node]['trunk'].pop()
        self.NODES[node]['speed'] = param['speed']
        self.NODES[node]['duplex'] = param['duplex']
        self.NODES[node]['state'] = param['state']
        return True
    
    def _configure_port(self, switch, device, interface, port, param):
        switch_dict={}
        if not port:
            logger.error(f'Port number not defined for {interface} of {device} on {switch}.')
            return None
        logger.info(f'Configuring port {port} on {switch}')
        result = self.controller[switch].configPort(**{'port':port, 'param':param})
        return result

    def control(self, type=None, controller=None):
        switch_g = None
        rpsw_g = None
        if self.specformat != 'yaml':
            logger.error('control(): Unsupported spec format: {}'.format(self.specformat))
            return None
        if not controller:
            ctler = []
            if not type or re.search(r'switch', type, re.I): 
                if 'switch' in self.conf.keys():
                    ctler = sorted(self.conf['switch'].keys())
            if not type or re.search(r'power', type, re.I): 
                if 'powercontrol' in self.conf.keys():
                    ctler = sorted(self.conf['powercontrol'].keys())        
            return ctler
        
        if not type or re.search(r'switch', type, re.I):
            switch_g = self._smart_find(self.conf['switch'], controller)
        if not type or re.search(r'power', type, re.I):
            rpsw_g = self._smart_find(self.conf['powercontrol'], controller)
        if not switch_g and not rpsw_g:
            logger.error('control(): {} is not a valid switch or power controller.'.format(controller))
            return None
        if switch_g:
            result = self.conf['switch'][switch_g]
            controller_g = switch_g
        if rpsw_g:
            result = self.conf['powercontrol'][rpsw_g]
            controller_g = rpsw_g
        return [result, controller_g]

    def _configure_vlan(self, mode, switch, vlan=None):
        if self.specformat != 'yaml':
            logger.error('_configure_vlan(): Unsupported spec format: {}'.format(self.specformat))
            return None        
        if not vlan:
            logger.debug('The DUT attached to {} has no VLAN definition.'.format(switch))
            return None
        vlan_kwargs= {
            'mode': mode,  #add rem clear
            'vlans': vlan
        }
        result = self.controller[switch].configVLAN(**vlan_kwargs)
        return result

    def _dump_vlan(self, vlan, switch, quiet=False, normal=False):
        logger.info('=========================================================================')
        logger.info('ID   NAME         PORTS')
        for id in sorted(vlan.keys()):
            if normal and id<100: continue
            net_name = vlan[id]['name']
            # if not quiet:
            self.TOPO[net_name] = {}
            self.TOPO[net_name]['vlan_id'] = id
            self.TOPO[net_name]['node']= {}
            ports = list(vlan[id]['port'])
            if not ports:
                logger.info('{}'.format(str(id).ljust(5, ' ') + net_name.ljust(13, ' ')))
                continue
            for p in ports:
                if not switch and not (re.search(r'URL', self.specformat, re.I)):
                    (ct, node) = self.num_to_name(p) 
                if switch and not (re.search(r'URL', self.specformat, re.I)):
                    (ct, node) = self.num_to_name(switch + ':' + p) 
                if re.search(r':.*T', p):
                    flag = 'T'
                else: 
                    flag = 'U'
                if p and re.search(r':.*h', p):
                    flag += 'H'
                if not (re.search(r'URL', self.specformat, re.I)):
                    self.TOPO[net_name]['node'][node] = flag
                if re.search(r'U', flag, re.I) and not re.search(r'URL', self.specformat, re.I):
                    if node not in self.NODES.keys():
                        self.NODES[node] = {}
                    self.NODES[node]['uvlan'] = net_name
                if re.search(r'T', flag, re.I) and not re.search(r'URL', self.specformat, re.I):
                    # self.NODES[node] = {}
                    self.NODES[node]['tvlan'] = []
                    self._add_to_list(self.NODES[node]['tvlan'], net_name)
            if quiet: continue
            if int(len(ports)) <= 10:
                logger.info('{}{}'.format(str(id).ljust(5, ' ') + net_name.ljust(13, ' '), ','.join(ports)).ljust(51, ' '))
            else:
                parts = []
                for i in range(0, int(len(ports)/11)):
                    s = i*11
                    if i*11+10 > int(len(ports)):
                        e = int(len(ports))
                    else:
                        e = i*11+10
                    parts.append(','.join(ports[s:e]))
                logger.info('{}{}'.format(str(id).ljust(5, ' ') + net_name.ljust(13, ' '), parts.pop(0).ljust(51, ' ')))
                for part in parts:
                    logger.info(' '*19 + part.ljust(51, ' '))
        logger.info('=========================================================================')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if re.search(r'yaml', self.specformat, re.I):
            for ct in sorted(self.controller.keys()):
                if re.search(r'/switch/', self.controller[ct].module_name, re.I):
                    logger.info('Dumping {} VLAN setting after switch configuration...'.format(ct))
                    vlan_r = self.controller[ct].getConf()
                    self._dump_vlan(vlan_r, ct)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Configure switch and powerswitch.')
    parser.add_argument('-testbed', '--testbed', type=str, dest='testbed', required=False, help='testbed ID, like: VTB518')
    parser.add_argument('-topo', type=str, dest='topo', required=False, help='topo name, like: 5600_default')
    parser.add_argument('-device', type=str, dest='device', required=False, help='topo name, like: 5600_default')
    parser.add_argument('-vlan', type=str, dest='vlan', required=False, help='vlan name, like: DUTX0')
    parser.add_argument('-port', type=str, dest='port', required=False, help='port name, like: TZ300W:DUTX0,PC1:eth0')
    parser.add_argument('-spec', type=str, dest='specification', required=False, help='')
    parser.add_argument('-specformat', type=str, dest='specformat', default='yaml',required=False, help='spec file')
    parser.add_argument('-action', type=str, dest='action', required=True, help='spec file format, default is yaml')

    known, unknown = parser.parse_known_args(sys.argv[1:])
    val = vars(known)
    if re.search(r'http:*\/\/', val['specification']):
        logger.info('Spec file is URL.')
        val['specformat'] = 'URL'
    with DeviceConfig(user='admin', password='password',specfile=val['specification'], specformat=val['specformat']) as dc:
        if dc.specformat == 'yaml':
            if re.search(r'(add|rem)-trunk', val['action'], re.I):
                nodes =val['port']
                dc.configure_node_trunk(val['action'],nodes)
            elif re.search(r'add|rem', val['action'], re.I):
                if val['topo'] or val['device']:
                    if val['topo']:
                        tode = val['topo']
                    elif val['device']:
                        tode = val['device']
                    default = dc.default_setting(tode)
                    if not default:
                        logger.error('{} does not have default settings.'.format(tode))
                        exit(1)
                    for vlan in sorted(default['vlan']):
                        # {'vlan': {'dutx0': 'TZ300W:X0,PC1:eth0', 'dutx1': 'TZ300W:X1,PC1:eth2'}}
                        nodes = default['vlan'][vlan].split(',')
                        dc.config_network(val['action'], vlan, nodes)
                elif val['vlan']:
                    nodes= val['port'].split(',')
                    dc.config_network(val['action'], val['vlan'],nodes)
                else:
                    logger.error('No device name or custom vlan defined')
                    exit(1)
            match_port = re.search(r'port-?(.*)$',val['action'])
            if re.search(r'clear', val['action'], re.I):
                dc.config_network('clear')
            elif re.search(r'power', val['action'], re.I):  
                if val['device'] or val['host']:
                    if val['device']:
                        [node, host] = [val['device'], 0]
                    else:
                        [node, host] = [val['device'], 1]
                    result = dc.power(val['action'], node, host)
                    if not result:
                        exit(1)
                else:
                    logger.error('Please specify the target device for power action.')
                    exit(2)
            elif match_port:
                port_act = match_port.group(1)
                if val['port']:
                    port_act = re.sub(':','', port_act)
                    if re.search(':', val['port']):
                        port_node = val['port']
                    elif val['device']:
                        port_node = val['device'] + ':' + val['port']
                    else:
                        logger.error('Please specify a node name or a device/port pair as the target.')
                        exit(3)

                    dc.configure_node(port_act, port_node)

        elif dc.specformat == 'URL':
            if re.search(r'add|rem|vlan|clear', val['action'],re.I):
                logger.error('openstack does not support VLAN setting')
                exit(1)
        else:
            logger.error('Invalid test bed spec file format:{}'.format(dc.specformat))
            exit(2)
    exit(0)
    '''
    swconfig.py -action add|rem|clear -topo **** -sepc /SWIFT4.0/COMMON/data/swithes/TB32.yaml
    swconfig.py -a add -vlan dutx3 -port NSA5600:X3 -spec /SWIFT4.0/COMMON/data/swithes/TB32.yaml
    '''
