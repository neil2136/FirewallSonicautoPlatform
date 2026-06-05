import telnetlib  
import time
import re
import sys
import os
import weakref

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.deviceutil import Switchtelnet
from runner.settings import logger


__all__ = [
    "getConf", "configVLAN", "setup_vlan_ports"
]

class S60:
    def __init__(self, **kwargs):
        self.sw_ip = kwargs['ip']
        self.switch = 'openstack switch'
        if 'controllername' in kwargs:
            self.switch = kwargs['controllername']
        self.switchtelnet = Switchtelnet(self.sw_ip,'force10')
        logger.info('New ' + __class__.__name__ + ' object created for ' + self.switch + ' ' + self.sw_ip)
        if not self.switchtelnet.init_session():
            os._exit(0)
        self.ports_status = {}
        show_list = self.switchtelnet.capture('show interface status')
        for line in show_list.split('\n'):
            if re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I) :
                self.ports_status[re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I).group(2)] = re.search(r'(te|gi)\s*(\d\/\d+)', line, re.I).group(1) + ' '        
        self._finalizer = weakref.finalize(self, self.switchtelnet.close_session)
        self.module_name = sys._getframe().f_code.co_filename
        
    def getConf(self):
        vlans = {}
        try:
            vlans_list = self.switchtelnet.capture('show vlan brief').split('\n')            
        except Exception as e:
            logger.error('Unable to get vlan brief.')
            return vlans
        for line in vlans_list:
            if re.search(r'unassigned|\d+\.\d+\.\d+\.\d+', line, re.I):
                output = re.search(r'^(\d+)\s+(.*?)\s+\d+\s+\d+\s+(unassigned|\d+\.\d+\.\d+\.\d+)', line, re.I)
                id = int(output.group(1))
                name = output.group(2)
                name = re.sub(r'\s*$', '', name)
                vlans[id] = {}
                vlans[id]['name'] = name
                vlans[id]['port'] = []
                vlan_lines = self.switchtelnet.capture('show vlan id ' + str(id)).split('\n')
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
                            id = int(result.group(1))
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
                            logger.error('Unrecognized line: ' + vlan_line
                            )
        return vlans

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
                for i in range(int(re.search(r'(\d+)-(\d+)', port_ori).group(1)), int(re.search(r'(\d+)-(\d+)', port_ori).group(2))+1):
                    result.append(slot + str('/')+ str(i) + ':' + type)
            elif re.search(r'(\d+)', port_ori):
                result.append(slot + str('/')+ re.search(r'(\d+)', port_ori).group(1) + ':' + type)
        return result
    _parse_ports = staticmethod(_parse_ports)

    def configVLAN(self, **kwargs):
        mode = kwargs['mode']
        vlans = kwargs['vlans']
        if not self.get_session():
            return None
        self.setup_vlan_ports(mode, vlans)

   
    def setup_vlan_ports(self, mode, vlans):
        # show_inter = self.switchtelnet.capture("show interface status");
        # ports_status = {}
        # for line in show_inter:
        #     result = re.search(r'(te|gi)\s*(\d)\/(\d+)', line, re.I)
        #     if result:
        #         ports_status[result.group(3)] = result.group(1)

        self.switchtelnet.capture("configure")
        for vlan in sorted(vlans.keys()):
            ports_sum = {
                'gi_en_tag_hyb': '',
                'gi_en_tag_unh': '',
                'gi_en_unt_hyb': '',
                'gi_en_unt_unh': '',
                'gi_dis_tag_hyb': '',
                'gi_dis_tag_unh': '',
                'gi_dis_unt_hyb': '',
                'gi_dis_unt_unh': '',
                'te_en_tag_hyb': '',
                'te_en_tag_unh': '',
                'te_en_unt_hyb': '',
                'te_en_unt_unh': '',
                'te_dis_tag_hyb': '',
                'te_dis_tag_unh': '',
                'te_dis_unt_hyb': '',
                'te_dis_unt_unh': '',            
            }
            try:
                vlan_name = vlans[vlan]['name']
            except:
                vlan_name = 'vlan' + vlan
            vlan_name=vlan_name.upper()
            for ports in vlans[vlan]['port']:
                if re.search(r':[!eptuhm]+', ports, re.I):
                    [port_num, flag] = ports.split(':')  # only check [eptu] flags
                else:
                    [port_num] = ports.split(':')  # only check [eptu] flags
                if not re.match(r'(\d+)/(\d+)', str(port_num)):
                    port = port_num
                else:
                    slot = re.match(r'(\d+)/(\d+)', str(port_num)).group(1)
                    port = re.match(r'(\d+)/(\d+)', str(port_num)).group(2)
                if not 'slot' in dir():
                    slot = '0'
                is_en = False
                is_tag = False
                is_hyb = False
                is_te = False
                if (re.search(r'add', mode, re.I) and not re.search(r'!e', flag, re.I)) or\
                    (re.search(r'rem|del', mode, re.I) and re.search(r'^e|[^!]e', flag, re.I)) or\
                    (re.search(r'remu', mode, re.I)):
                    is_en = True
                if re.search(r'^t|[^!]t', flag, re.I):
                    is_tag = True
                if re.search(r'^h|[^!]h', flag, re.I):
                    is_hyb = True
                if re.search(r'gi', self.ports_status[eval('slot + "/" + port')], re.I):
                    is_gi = True
                if re.search(r'te', self.ports_status[eval('slot + "/" + port')], re.I):
                    is_te = True   
                if is_en and is_tag and is_gi and is_hyb:
                    ports_sum['gi_en_tag_hyb'] =  ports_sum['gi_en_tag_hyb'] + "gi " + eval('slot + "/" + port') + ' , '
                if is_en and is_tag and is_gi and not is_hyb:
                    ports_sum['gi_en_tag_unh'] =  ports_sum['gi_en_tag_unh'] + "gi " + eval('slot + "/" + port') + ' , '
                if is_en and not is_tag and is_gi and is_hyb:
                    ports_sum['gi_en_unt_hyb'] =  ports_sum['gi_en_unt_hyb'] + "gi " + eval('slot + "/" + port') + ' , '
                if is_en and not is_tag and is_gi and not is_hyb:
                    ports_sum['gi_en_unt_unh'] =  ports_sum['gi_en_unt_unh'] + "gi " + eval('slot + "/" + port') + ' , '
                if not is_en and is_tag and is_gi and is_hyb:
                    ports_sum['gi_dis_tag_hyb'] =  ports_sum['gi_dis_tag_hyb'] + "gi " + eval('slot + "/" + port') + ' , '
                if not is_en and is_tag and is_gi and not is_hyb:
                    ports_sum['gi_dis_tag_unh'] =  ports_sum['gi_dis_tag_unh'] + "gi " + eval('slot + "/" + port') + ' , '
                if not is_en and not is_tag and is_gi and is_hyb:
                    ports_sum['gi_dis_unt_hyb'] =  ports_sum['gi_dis_unt_hyb'] + "gi " + eval('slot + "/" + port') + ' , '
                if not is_en and not is_tag and is_gi and not is_hyb:
                    ports_sum['gi_dis_unt_unh'] =  ports_sum['gi_dis_unt_unh'] + "gi " + eval('slot + "/" + port') + ' , '

                if is_en and is_tag and is_te and is_hyb:
                    ports_sum['te_en_tag_hyb'] =  ports_sum['te_en_tag_hyb'] + "te " + eval('slot + "/" + port') + ' , '
                if is_en and is_tag and is_te and not is_hyb:
                    ports_sum['te_en_tag_unh'] =  ports_sum['te_en_tag_unh'] + "te " + eval('slot + "/" + port') + ' , '
                if is_en and not is_tag and is_te and is_hyb:
                    ports_sum['te_en_unt_hyb'] =  ports_sum['te_en_unt_hyb'] + "te " + eval('slot + "/" + port') + ' , '
                if is_en and not is_tag and is_te and not is_hyb:
                    ports_sum['te_en_unt_unh'] =  ports_sum['te_en_unt_unh'] + "te " + eval('slot + "/" + port') + ' , '
                if not is_en and is_tag and is_te and is_hyb:
                    ports_sum['te_dis_tag_hyb'] =  ports_sum['te_dis_tag_hyb'] + "te " + eval('slot + "/" + port') + ' , '
                if not is_en and is_tag and is_te and not is_hyb:
                    ports_sum['te_dis_tag_unh'] =  ports_sum['te_dis_tag_unh'] + "te " + eval('slot + "/" + port') + ' , '
                if not is_en and not is_tag and is_te and is_hyb:
                    ports_sum['te_dis_unt_hyb'] =  ports_sum['te_dis_unt_hyb'] + "te " + eval('slot + "/" + port') + ' , '
                if not is_en and not is_tag and is_te and not is_hyb:
                    ports_sum['te_dis_unt_unh'] =  ports_sum['te_dis_unt_unh'] + "te " + eval('slot + "/" + port') + ' , '
            try:
                ports_sum['gi_en_tag_hyb'] = ports_sum['gi_en_tag_hyb'].rstrip(', ')
                ports_sum['gi_en_tag_unh'] = ports_sum['gi_en_tag_unh'].rstrip(', ')
                ports_sum['gi_en_unt_hyb'] = ports_sum['gi_en_unt_hyb'].rstrip(', ')
                ports_sum['gi_en_unt_unh'] = ports_sum['gi_en_unt_unh'].rstrip(', ')
                ports_sum['gi_dis_tag_hyb'] = ports_sum['gi_dis_tag_hyb'].rstrip(', ')
                ports_sum['gi_dis_tag_unh'] = ports_sum['gi_dis_tag_unh'].rstrip(', ')
                ports_sum['gi_dis_unt_hyb'] = ports_sum['gi_dis_unt_hyb'].rstrip(', ')
                ports_sum['gi_dis_unt_unh'] = ports_sum['gi_dis_unt_unh'].rstrip(', ')
                ports_sum['te_en_tag_hyb'] = ports_sum['te_en_tag_hyb'].rstrip(', ')
                ports_sum['te_en_tag_unh'] = ports_sum['te_en_tag_unh'].rstrip(', ')
                ports_sum['te_en_unt_hyb'] = ports_sum['te_en_unt_hyb'].rstrip(', ')
                ports_sum['te_en_unt_unh'] = ports_sum['te_en_unt_unh'].rstrip(', ')
                ports_sum['te_dis_tag_hyb'] = ports_sum['te_dis_tag_hyb'].rstrip(', ')
                ports_sum['te_dis_tag_unh'] = ports_sum['te_dis_tag_unh'].rstrip(', ')
                ports_sum['te_dis_unt_hyb'] = ports_sum['te_dis_unt_hyb'].rstrip(', ')
                ports_sum['te_dis_unt_unh'] = ports_sum['te_dis_unt_unh'].rstrip(', ')
            except:
                pass
            code_en = []
            code_tag = []
            code_hyb = []
            for type in ['gi_en_tag_hyb', 'gi_en_tag_unh', 'gi_en_unt_hyb', 'gi_en_unt_unh',
                         'gi_dis_tag_hyb', 'gi_dis_tag_unh', 'gi_dis_unt_hyb', 'gi_dis_unt_unh',
                         'te_en_tag_hyb', 'te_en_tag_unh', 'te_en_unt_hyb', 'te_en_unt_unh',
                         'te_dis_tag_hyb', 'te_dis_tag_unh', 'te_dis_unt_hyb', 'te_dis_unt_unh']:
                if ports_sum[type]:
                    code_en.append("self.switchtelnet.capture('interface range " + ports_sum[type]  + "')")
                    if 'en' in type:
                        code_en.append("self.switchtelnet.capture('no shutdown')")
                        code_en.append("self.switchtelnet.capture('switchport')")
                        code_en.append("self.switchtelnet.capture('exit')")
                        code_en.append("logger.info('Enable ports " + ports_sum[type] + "')")
                    elif 'dis' in type:
                        code_en.append("self.switchtelnet.capture('shutdown')")
                        code_en.append("self.switchtelnet.capture('no switchport')")
                        code_en.append("self.switchtelnet.capture('exit')")
                        code_en.append("logger.info('Disable ports " + ports_sum[type] + "')")                        
                    if re.search(r'add', mode, re.I) and 'hyb' in type:
                        code_hyb.append("self.switchtelnet.capture('interface range " + ports_sum[type]  + "')")
                        code_hyb.append("self.switchtelnet.capture('no switchport')")
                        code_hyb.append("self.switchtelnet.capture('portmode hybrid')")
                        code_hyb.append("self.switchtelnet.capture('exit')")
                        code_en.append("logger.info('Set ports " + ports_sum[type] + "to hybrid mode." + "')")                        
                    elif re.search(r'rem', mode, re.I) and 'hyb' in type:
                        code_hyb.append("self.switchtelnet.capture('interface range " + ports_sum[type]  + "')")
                        code_hyb.append("self.switchtelnet.capture('no switchport')")
                        code_hyb.append("self.switchtelnet.capture('no portmode hybrid')")
                        code_hyb.append("self.switchtelnet.capture('exit')")
                        code_en.append("logger.info('Remove ports " + ports_sum[type] + "from hybrid mode." + "')") 
                    ports_sum[type] = re.sub(r'\s*,\s*(gi|te)\s*0\/', ',', ports_sum[type])
                    if re.search(r'add', mode, re.I) and 'unt' in type:
                        code_tag.append("self.switchtelnet.capture('untagged " + ports_sum[type]  + "')")
                        code_en.append("logger.info('Added untagged ports " + ports_sum[type] + " into " + str(vlan) + "')") 
                    elif re.search(r'add', mode, re.I) and 'tag' in type:
                        code_tag.append("self.switchtelnet.capture('tagged " + ports_sum[type]  + "')")
                        code_en.append("logger.info('Added tagged ports " + ports_sum[type] + " into " + str(vlan) + "')")
                    elif re.search(r'rem', mode, re.I) and 'unt' in type:
                        code_tag.append("self.switchtelnet.capture('no untagged " + ports_sum[type]  + "')")
                        code_en.append("logger.info('Removed untagged ports " + ports_sum[type] + " from " + str(vlan) + "')")
                    elif re.search(r'rem', mode, re.I) and 'tag' in type:
                        code_tag.append("self.switchtelnet.capture('no tagged " + ports_sum[type]  + "')")
                        code_en.append("logger.info('Removed tagged ports " + ports_sum[type] + " from " + str(vlan) + "')")

####
#mtu
####
            if re.search(r'add', mode):
                for each in code_hyb:
                    eval(each)
                for each in code_en:
                    eval(each)
                if not re.search(r'p$', mode):
                    self.switchtelnet.capture('interface vlan ' + str(vlan))
                    self.switchtelnet.capture('name ' + vlan_name)
                    eval("logger.info('Added vlan: ' + vlan_name + '(' + str(vlan) + ')')")
                self.switchtelnet.capture('interface vlan ' + str(vlan))
                for each in code_tag:
                    eval(each)
                self.switchtelnet.capture('exit')
            elif re.search(r'rem|del', mode):
                self.switchtelnet.capture('interface vlan ' + str(vlan))
                for each in code_tag:
                    eval(each)               
                self.switchtelnet.capture('exit')
                for each in code_hyb:
                    eval(each)
                for each in code_en:
                    eval(each)
                if not re.search(r'p$', mode):
                    self.switchtelnet.capture('no interface vlan ' + str(vlan))
                    logger.info('Removed vlan: ' + vlan_name + '(' + str(vlan) + ')')

                    ###mtu###
                time.sleep(2)
        self.switchtelnet.capture('exit')

    def get_session(self):
        if self.switchtelnet:
            lines = self.switchtelnet.capture("show version")
            if lines and re.search(r'System image', lines, re.I):
                return self.switchtelnet
            else:
                self.switchtelnet.close_session()
        
        result = self.switchtelnet.init_session()
        if not result:
            logger.error('Login to switch failed.')
            return False
        return self.switchtelnet

    def config_vlans(self, **kwargs):
        pass

    def configPort(self, **kwargs):
        port = kwargs['port']
        param = kwargs['param']
        result = ''
        if not re.match(r'\d/', str(port)):
            port = "0/" + str(port) 
        if not self.get_session():
            return None
        self.switchtelnet.capture("configure")
        re.match(r'^0/(\d+)', port)

        self.switchtelnet.capture("interface " + self.ports_status[port] + str(port))
        prompt = self.switchtelnet.prompt()
        if not re.search(r'conf-if-', prompt):
            logger.error('Invalid port {}, current prompt: {}'.format(port, prompt))
            return None
        if 'state' in param.keys():
            if re.search(r'up', param['state'], re.I):
                self.switchtelnet.capture('no shutdown')
                logger.info('Enable port {}'.format(port))
            elif re.search(r'down', param['state'], re.I):
                self.switchtelnet.capture('shutdown')
                logger.info('Disable port {}'.format(port))
            result = result + ' state'
        if 'speed' in param.keys():
            logger.info('Set port {} to speed {}'.format(port, str(param['speed'])))
            if param['speed'] == 'auto':
                output = self.switchtelnet.capture("negotiation auto")
                output += self.switchtelnet.capture("no duplex")
            else:
                output = self.switchtelnet.capture("no negotiation auto")
            output += self.switchtelnet.capture("speed " + str(param['speed']))
            if re.search(r'speed ' + param['speed'] + '', output, re.I):
                result = result + ' speed'
                logger.info('Set port {} to speed {} sucessfully'.format(port, str(param['speed'])))
            else:
                logger.error('Set port {} to speed {} failed'.format(port, str(param['speed'])))
        if 'duplex' in param.keys():
            pass      
        self.switchtelnet.capture("exit")
        return result
    # def remove(self):
    #     if self.switchtelnet:
    #         logger.info('Disconnect from switch ' + self.switch)
    #         self.switchtelnet.close_session()
    #     logger.info('Disconnect from switch ' + self.switch)
    #     self._finalizer()

    # @property
    # def removed(self):
    #     print('removed')
    #     return not self._finalizer.alive       

class S4810(S60):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)
        self.switch = 'S4810'


if __name__ == '__main__':
    s60 = S60(ip='10.6.0.162', switch='s60')
    s60.getConf()
    kwargs = {
        'mode': 'add',  #add rem clear
        'vlans': {
            '200': {
                'name': 'dutx0',
                'ports': ['30:U'],
            },
            '199': {
                'name': 'dutx1',
                'ports': ['31:U'],
            }
        }
    }
    s60.configVLAN(**kwargs)
        