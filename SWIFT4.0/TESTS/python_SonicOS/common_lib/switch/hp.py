import telnetlib  
import time
import logging
import re
import sys
import os
import weakref

# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from util.deviceutil import Switchtelnet
from pprint import pprint
from runner.settings import logger

__all__ = ["getConf", "configVLAN", "setup_vlan_ports"]

class ProCurve:
    def __init__(self, **kwargs):
        self.sw_ip = kwargs['ip']
        self.switch = 'openstack switch'
        if 'controllername' in kwargs:
            self.switch = kwargs['controllername']
        self.switchtelnet = Switchtelnet(self.sw_ip,'hp')
        logger.info('New ' + __class__.__name__ + ' object created for ' + self.switch + ' ' + self.sw_ip)
        # if not self.switchtelnet.init_session():
        #     os._exit(0)
        self._finalizer = weakref.finalize(self, self.switchtelnet.close_session)
        self.module_name = sys._getframe().f_code.co_filename

    def getConf(self):
        vlans = {}
        vlans_list = self.switchtelnet.capture('show vlans').split('\n')            
        for line in vlans_list:
            if re.search(r'Port-based', line, re.I):
                output = re.search(r'^\s+(\d+)\s+(.*?)Port-based', line, re.I)
                id = output.group(1)
                name = output.group(2)
                name = re.sub(r'\s*$', '', name)
                vlans[id] = {}
                vlans[id]['name'] = name
                
                vlan_lines = self.switchtelnet.capture('show vlan ' + str(id)).split('\n')
                vlans[id]['port'] = []
                for i in range(0, len(vlan_lines)):
                    vlan_line = vlan_lines[i]
                    
                    match = re.search(r'^\s+(\d+|Trk\d+)\s+(\w+)', vlan_line)
                    if not match:
                        continue
                    else:
                        p = match.group(1)
                        t = match.group(2)
                        if re.search(r'Untagged', t):
                            p = p + ':' + 'U' 
                        if re.search(r'Tagged',t):
                            p = p + ':' + 'T'
                        vlans[id]['port'].append(p)
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
                for i in range(re.search(r'(\d+)-(\d+)', port_ori).group(1), re.search(r'(\d+)-(\d+)', port_ori).group(2)):
                    result.append(slot + str('/')+ i + ':' + type)
            elif re.search(r'(\d+)', port_ori):
                result.append(slot + str('/')+ re.search('(\d+)', port_ori).group(1) + ':' + type)
        return result
    _parse_ports = staticmethod(_parse_ports)

    def configVLAN(self, **kwargs):
        mode = kwargs['mode']
        vlan = kwargs['vlans']
        self.get_session()
        self.setup_vlan_ports(**kwargs)

   
    def setup_vlan_ports(self, mode, vlans):
        self.switchtelnet.capture("configure")
        for vlan in sorted(vlans.keys()):
            ports_sum = {
                'en_tag': '',
                'en_unt': '',
                'dis_tag': '',
                'dis_unt': '',
            }
            try:
                vlan_name = vlans[vlan]['name']
            except:
                vlan_name = 'vlan' + vlan
            for ports in vlans[vlan]['port']:
                if re.search(r':[!eptuhm]+', ports, re.I):
                    [port,flag] = ports.split(':')  # only check [eptu] flags
                else:
                    [port] = ports.split(':')  # only check [eptu] flags
                # if not re.match(r'(\d+)/(\d+)', str(port_num)):
                #     port = port_num
                # else:
                #     slot = re.match(r'(\d+)/(\d+)', str(port_num)).group(1)
                #     port = re.match(r'(\d+)/(\d+)', str(port_num)).group(2)
                # if not 'slot' in dir():
                #     slot = '0'
                is_en = False
                is_tag = False
                # is_hyb = False
                # is_te = False
                if (re.search(r'add', mode, re.I) and not re.search(r'!e', flag, re.I)) or\
                    (re.search(r'rem|del', mode, re.I) and re.search(r'^e|[^!]e', flag, re.I)) or\
                    (re.search(r'remu', mode, re.I)):
                    is_en = True
                if re.search(r'^t|[^!]t', flag, re.I):
                    is_tag = True
                # if re.search(r'^h|[^!]h', flag, re.I):
                #     is_hyb = True
                # if re.search(r'gi', self.ports_status[eval('slot + "/" + port')], re.I):
                #     is_gi = True
                # if re.search(r'te', self.ports_status[eval('slot + "/" + port')], re.I):
                #     is_te = True   
                if is_en and is_tag:
                    ports_sum['en_tag'] =  ports_sum['en_tag'] +  port + ','
                # if is_en and is_tag and is_gi and not is_hyb:
                #     ports_sum['gi_en_tag_unh'] =  ports_sum['gi_en_tag_unh'] + "gi " + eval('slot + "/" + port') + ' , '
                if is_en and not is_tag:
                    ports_sum['en_unt'] =  ports_sum['en_unt'] + port + ','
                # if is_en and not is_tag and is_gi and not is_hyb:
                #     ports_sum['gi_en_unt_unh'] =  ports_sum['gi_en_unt_unh'] + "gi " + eval('slot + "/" + port') + ' , '
                if not is_en and is_tag:
                    ports_sum['dis_tag'] =  ports_sum['dis_tag'] + port + ','
                # if not is_en and is_tag and is_gi and not is_hyb:
                #     ports_sum['gi_dis_tag_unh'] =  ports_sum['gi_dis_tag_unh'] + "gi " + eval('slot + "/" + port') + ' , '
                if not is_en and not is_tag:
                    ports_sum['dis_unt'] =  ports_sum['dis_unt'] + port + ','
                # if not is_en and not is_tag and is_gi and not is_hyb:
                #     ports_sum['gi_dis_unt_unh'] =  ports_sum['gi_dis_unt_unh'] + "gi " + eval('slot + "/" + port') + ' , '

                # if is_en and is_tag and is_te and is_hyb:
                #     ports_sum['te_en_tag_hyb'] =  ports_sum['te_en_tag_hyb'] + "te " + eval('slot + "/" + port') + ' , '
                # if is_en and is_tag and is_te and not is_hyb:
                #     ports_sum['te_en_tag_unh'] =  ports_sum['te_en_tag_unh'] + "te " + eval('slot + "/" + port') + ' , '
                # if is_en and not is_tag and is_te and is_hyb:
                #     ports_sum['te_en_unt_hyb'] =  ports_sum['te_en_unt_hyb'] + "te " + eval('slot + "/" + port') + ' , '
                # if is_en and not is_tag and is_te and not is_hyb:
                #     ports_sum['te_en_unt_unh'] =  ports_sum['te_en_unt_unh'] + "te " + eval('slot + "/" + port') + ' , '
                # if not is_en and is_tag and is_te and is_hyb:
                #     ports_sum['te_dis_tag_hyb'] =  ports_sum['te_dis_tag_hyb'] + "te " + eval('slot + "/" + port') + ' , '
                # if not is_en and is_tag and is_te and not is_hyb:
                #     ports_sum['te_dis_tag_unh'] =  ports_sum['te_dis_tag_unh'] + "te " + eval('slot + "/" + port') + ' , '
                # if not is_en and not is_tag and is_te and is_hyb:
                #     ports_sum['te_dis_unt_hyb'] =  ports_sum['te_dis_unt_hyb'] + "te " + eval('slot + "/" + port') + ' , '
                # if not is_en and not is_tag and is_te and not is_hyb:
                #     ports_sum['te_dis_unt_unh'] =  ports_sum['te_dis_unt_unh'] + "te " + eval('slot + "/" + port') + ' , '
            try:
                ports_sum['en_tag'] = ports_sum['en_tag'].rstrip(',')
                # ports_sum['gi_en_tag_unh'] = ports_sum['gi_en_tag_unh'].rstrip(', ')
                ports_sum['en_unt'] = ports_sum['en_unt'].rstrip(',')
                # ports_sum['gi_en_unt_unh'] = ports_sum['gi_en_unt_unh'].rstrip(', ')
                ports_sum['dis_tag'] = ports_sum['dis_tag'].rstrip(',')
                # ports_sum['gi_dis_tag_unh'] = ports_sum['gi_dis_tag_unh'].rstrip(', ')
                ports_sum['dis_unt'] = ports_sum['dis_unt'].rstrip(',')
                # ports_sum['gi_dis_unt_unh'] = ports_sum['gi_dis_unt_unh'].rstrip(', ')
                # ports_sum['te_en_tag_hyb'] = ports_sum['te_en_tag_hyb'].rstrip(', ')
                # ports_sum['te_en_tag_unh'] = ports_sum['te_en_tag_unh'].rstrip(', ')
                # ports_sum['te_en_unt_hyb'] = ports_sum['te_en_unt_hyb'].rstrip(', ')
                # ports_sum['te_en_unt_unh'] = ports_sum['te_en_unt_unh'].rstrip(', ')
                # ports_sum['te_dis_tag_hyb'] = ports_sum['te_dis_tag_hyb'].rstrip(', ')
                # ports_sum['te_dis_tag_unh'] = ports_sum['te_dis_tag_unh'].rstrip(', ')
                # ports_sum['te_dis_unt_hyb'] = ports_sum['te_dis_unt_hyb'].rstrip(', ')
                # ports_sum['te_dis_unt_unh'] = ports_sum['te_dis_unt_unh'].rstrip(', ')
            except:
                pass
            code_en = []
            code_tag = []
            # code_hyb = []
            for type in ['en_tag', 'en_unt', 'dis_tag', 'dis_unt']:
                if ports_sum[type]:
                    code_en.append("self.switchtelnet.capture('interface " + ports_sum[type]  + "')")
                    if 'en' in type:
                        code_en.append("self.switchtelnet.capture('enable')")
                        # code_en.append("self.switchtelnet.capture('switchport')")
                        code_en.append("self.switchtelnet.capture('exit')")
                        code_en.append("logger.info('Enable ports " + ports_sum[type] + "')")
                    elif 'dis' in type:
                        code_en.append("self.switchtelnet.capture('disable')")
                        # code_en.append("self.switchtelnet.capture('no switchport')")
                        code_en.append("self.switchtelnet.capture('exit')")
                        code_en.append("logger.info('Disable ports " + ports_sum[type] + "')")                        
                    # if re.search(r'add', mode, re.I) and 'hyb' in type:
                    #     code_hyb.append("self.switchtelnet.capture('interface range " + ports_sum[type]  + "')")
                    #     code_hyb.append("self.switchtelnet.capture('no switchport')")
                    #     code_hyb.append("self.switchtelnet.capture('portmode hybrid')")
                    #     code_hyb.append("self.switchtelnet.capture('exit')")
                    #     code_en.append("logger.info('Set ports " + ports_sum[type] + "to hybrid mode." + "')")                        
                    # elif re.search(r'rem', mode, re.I) and 'hyb' in type:
                    #     code_hyb.append("self.switchtelnet.capture('interface range " + ports_sum[type]  + "')")
                    #     code_hyb.append("self.switchtelnet.capture('no switchport')")
                    #     code_hyb.append("self.switchtelnet.capture('no portmode hybrid')")
                    #     code_hyb.append("self.switchtelnet.capture('exit')")
                    #     code_en.append("logger.info('Remove ports " + ports_sum[type] + "from hybrid mode." + "')") 
                    # ports_sum[type] = re.sub(r'\s*,\s*(gi|te)\s*0\/', ',', ports_sum[type])
                    if re.search(r'add', mode, re.I) and 'unt' in type:
                        code_tag.append("self.switchtelnet.capture('vlan " + str(vlan) + " untagged " + ports_sum[type]  + "')")
                        code_tag.append("logger.info('Added untagged ports " + ports_sum[type] + " into " + str(vlan) + "')") 
                    elif re.search(r'add', mode, re.I) and 'tag' in type:
                        code_tag.append("self.switchtelnet.capture('vlan " + str(vlan) + " tagged " + ports_sum[type]  + "')")
                        code_tag.append("logger.info('Added tagged ports " + ports_sum[type] + " into " + str(vlan) + "')")
                    elif re.search(r'rem', mode, re.I) and 'unt' in type:
                        code_tag.append("self.switchtelnet.capture('vlan 2 untagged " + ports_sum[type]  + "')")
                        code_tag.append("logger.info('Removed untagged ports " + ports_sum[type] + " from " + str(vlan) + " into port pool" + "')")
                    elif re.search(r'rem', mode, re.I) and 'tag' in type:
                        code_tag.append("self.switchtelnet.capture('no vlan " + str(vlan) + " tagged " + ports_sum[type]  + "')")
                        code_tag.append("logger.info('Removed tagged ports " + ports_sum[type] + " from " + str(vlan) + "')")

####
#mtu
####
            if re.search(r'add', mode):
                # for each in code_hyb:
                #     eval(each)
                if not re.search(r'p$', mode):
                    self.switchtelnet.capture('vlan ' + str(vlan) + ' name ' + vlan_name)
                    eval("logger.info('Added vlan: ' + vlan_name + '(' + str(vlan) + ')')")
                # self.switchtelnet.capture('interface vlan ' + str(vlan))
                for each in code_en:
                    eval(each)
                for each in code_tag:
                    eval(each)
                self.switchtelnet.capture('exit')
            elif re.search(r'rem|del', mode):
                # self.switchtelnet.capture('interface vlan ' + str(vlan))
                for each in code_tag:
                    eval(each)               
                # self.switchtelnet.capture('exit')
                # for each in code_hyb:
                #     eval(each)
                for each in code_en:
                    eval(each)
                if not re.search(r'p$', mode):
                    self.switchtelnet.capture('no vlan ' + str(vlan))
                    logger.info('Removed vlan: ' + vlan_name + '(' + str(vlan) + ')')
                    ###mtu###
                time.sleep(2)
        self.switchtelnet.capture('end')

    def config_vlans(self, **kwargs):
        pass

    def configPort(self, **kwargs):
        port = kwargs['port']
        param = kwargs['param']
        result = ''
        if not self.get_session():
            return None
        self.switchtelnet.capture("configure")
        match_port = re.match(r'^0/(\d+)', port)
        if match_port:
            port = match_port.group(1)
        self.switchtelnet.capture("interface " + str(port))
        prompt = self.switchtelnet.prompt()
        if not re.search(r'\(eth-.*\)#', prompt):
            logging.error('Invalid port {}, current prompt: {}'.format(port, prompt))
            return None
        if 'state' in param.keys():
            if re.search(r'up', param['state'], re.I):
                self.switchtelnet.capture('enable')
                logging.info('Enable port {}'.format(port))
            elif re.search(r'down', param['state'], re.I):
                self.switchtelnet.capture('disable')
                logging.info('Disable port {}'.format(port))
            result = result + ' state'
        if 'speed' in param.keys():
             pass
        if 'duplex' in param.keys():
            pass      

        self.switchtelnet.capture("exit")
        if 'trunk' in param.keys():
            trunk = param['trunk']
            match_trunk=re.search('\+(\d+)',trunk)
            match_trunk_rem=re.search('\-(\d+)',trunk)
            if match_trunk:
                t=match_trunk.group(1)
                logging.info(f'Set port {port} to trunk trk{t}')
                self.switchtelnet.capture(f'trunk {port} trk{t} trunk')
                logging.info(f'Move port trk{t} to vlan 2')
                self.switchtelnet.capture(f'vlan 2 untagged trk{t}')
                logging.info(f'Enable port {port}')
                self.switchtelnet.capture(f'interface {port}')
                self.switchtelnet.capture(f'enable')
                self.switchtelnet.capture("exit")
            elif match_trunk_rem:
                t=match_trunk_rem.group(1)
                self.switchtelnet.capture(f'interface {port}')
                self.switchtelnet.capture(f'disable')
                logging.info(f'Disable port {port}')
                self.switchtelnet.capture("exit")
                self.switchtelnet.capture(f'no trunk {port}')
                logging.info(f'Remove port {port} from trunk')
                self.switchtelnet.capture(f'vlan 2 untagged {port}')
                logging.info(f'Remove port {port} to port pool.')
            self.switchtelnet.capture("exit")
            result = result + ' trunk'
        return result
        
    def get_session(self):
        if self.switchtelnet:
            lines = self.switchtelnet.capture("show ip")
            if lines and re.search(r'Internet', lines, re.I):
                return self.switchtelnet
            else:
                self.switchtelnet.close_session()
        
        result = self.switchtelnet.init_session()
        if not result:
            logger.error('Login to switch failed.')
            return False
        return self.switchtelnet




if __name__ == '__main__':
    import sys
    sys.path.append('/DEV_TESTS/python_SonicOS/common_lib/util')
    hp = ProCurve(ip='10.6.0.250', switch='hp')
    # hp.getConf()

    





