import telnetlib  
import time
import logging
import re
import sys

sys.path.append('/home/python_lib')
from util.deviceutil import Switchtelnet
from pprint import pprint

__all__ = ["getConf", "configVLAN", "setup_vlan_ports"]

class S60:
    def __init__(self, **kwargs):
        self.sw_ip = kwargs['ip']
        self.switchtelnet = Switchtelnet(self.sw_ip,'force10')
        self.switch = kwargs['switch']
        self.ports_status = {}
        show_list = self.switchtelnet.capture('show interface status')
        for line in show_list:
            if re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I) :
                self.ports_status[re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I).group(2)] = re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I).group(1)        

    def getConf(self):
        vlans = {}
        vlans_list = self.switchtelnet.capture('show vlan brief')            
        for line in vlans_list:
            if re.search(r'unassigned|\d+\.\d+\.\d+\.\d+', line, re.I):
                output = re.search(r'^(\d+)\s+(.*?)\s+\d+\s+\d+\s+(unassigned|\d+\.\d+\.\d+\.\d+)', line, re.I)
                id = output.group(1)
                name = output.group(2)
                name = re.sub(r'\s*$', '', name)
                vlans[id] = {}
                vlans[id]['name'] = name
                
                vlan_lines = self.switchtelnet.capture('show vlan id ' + str(id))
                for i in range(0, len(vlan_lines)):
                    vlan_line = vlan_lines[i]

#                    vlan_line = re.sub(r'\cH', '', vlan_line, re.I|re.M)
                    if not re.search(r'[\*\s]*\d*\s*', vlan_line):
                        continue
                    if re.search(r'^\*?\s*(\d+)\s+', vlan_line):
                        while(i < len(vlan_lines)):
                            try:
                                tmp = re.search(r'([A-Za-z0-9,\-\/,\s]+)',vlan_lines[i+1]).group(1)
                                tmp = re.sub(r'^\s+|\s+$', '', tmp)
                                if re.match(r'U\s', tmp):
                                    vlan_line = vlan_line + '.' + tmp               
                                else:
                                    vlan_line = vlan_line + tmp                                   
                            except:
                                pass
                            i += 1
                        vlan_line = re.sub(r'Te', '', vlan_line, re.M)
                        vlan_line = re.sub(r'T\s+', 'T:', vlan_line, re.M)
                        vlan_line = re.sub(r'U\s', 'U:', vlan_line, re.M)
                        result = re.search(r'(\d+)\s+(In)?Active\s+((U|T)+.*$)', vlan_line, re.I)
                        if result:
                            id = result.group(1)
                            portline = result.group(3)
                            if re.search(r'\.',portline):
                                (pg1, pg2) = portline.split('.')
                                ports = S60._parse_ports(pg1)
                                ports.extend(S60._parse_ports(pg2))
                            else:
                                ports = S60._parse_ports(portline)
                            for k in range(0, len(ports) ):
                                port = re.search(r'(\d\/\d+):\w', ports[k]).group(1)
                                self.switchtelnet.capture("configure")                               
                                self.switchtelnet.capture("interface " + self.ports_status[port] + port)
                                port_lines =  self.switchtelnet.capture('show config')
                                if re.search('hybrid', str(port_lines)):
                                    ports[k] = port[k] + 'H'
                                self.switchtelnet.capture('end')                          
                            vlans[id]['port'] = ports
                        elif re.search(r'(\d+)\s+(In)?Active\s*$', vlan_line, re.I):
                            vlans[id]['port'] = []
                        else:
                            logging.error('Unrecognized line: ' + vlan_line
                            )
        pprint(vlans)

    def _parse_ports(line):
        (type, portline) = line.split(":")
        result =[]
        match = re.search(r'(\d+)\/(.*)',portline)
        slot = match.group(1)
        ports = match.group(2)
        ports_ori = [ports]
        if re.search(r'\d+,\d+', ports):
            ports_ori = ports.split(',')
        for port_ori in ports_ori:
            if re.search(r'(\d+)-(\d+)', port_ori):
                for i in range(re.search(r'(\d+)-(\d+)', port_ori).group(1), re.search(r'(\d+)-(\d+)', port_ori).group(2)):
                    result.append(slot + str('/')+ i + ':' + type)
            elif re.search(r'(\d+)', port_ori):
                result.append(slot + str('/')+ re.search('(\d+)', port_ori).group(1) + ':' + type)
        return result
    _parse_ports = staticmethod(_parse_ports)

    def configVLAN(self, **kwargs):
        mode = kwargs['mode']
        vlan = kwargs['vlan']
        self.get_session()
        self.setup_vlan_ports(**kwargs)

   
    def setup_vlan_ports(self, **kwargs):
        # show_inter = self.switchtelnet.capture("show interface status");
        # ports_status = {}
        # for line in show_inter:
        #     result = re.search(r'(te|gi)\s*(\d)\/(\d+)', line, re.I)
        #     if result:
        #         ports_status[result.group(3)] = result.group(1)
        self.switchtelnet.capture("configure")

        pass

    def config_vlans(self, **kwargs):
        pass

    def config_port(self, **kwargs):
        port = kwargs['port']
        param = kwargs['param']
        result = ''
        if not re.match(r'\d/'):
            port = "0/" + str(port) 
        if not self.switchtelnet.get_session():
            return None
        self.switchtelnet.capture("configure")
        result = re.match(r'^0/(\d+)', port)

        self.switchtelnet.capture("interface " + self.ports_status[port] + str(port))
        prompt = self.switchtelnet.prompt()
        if not re.search(r'conf-if-', prompt):
            logging.error('Invalid port {}, current prompt: {}'.format(port, prompt))
            return None
        if 'state' in param.keys():
            if re.search(r'up', param['state'], re.I):
                self.switchtelnet.capture('no shutdown')
                logging.info('Enable port {}'.format(port))
            elif re.search(r'down', param['state'], re.I):
                self.switchtelnet.capture('shutdown')
                logging.info('Disable port {}'.format(port))
            result = result + ' state'
        if 'speed' in param.keys():
             pass
        if 'duplex' in param.keys():
            pass      
        self.switchtelnet.capture("exit")



        pass

    def __del__(self):
        if self.switchtelnet:
            self.switchtelnet.close_session()
            logging.info('Disconnect from switch ' + self.switch)
'''
class S4810(S60):
    def __init__(self):
        super.__init__()
'''


if __name__ == '__main__':
    s60 = S60(ip='10.6.0.162', switch='s60')
    s60.getConf()
    





