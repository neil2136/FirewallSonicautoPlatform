import requests
import xml.etree.ElementTree as ET
from collections import OrderedDict
import json
import smtplib
from email.mime.text import MIMEText
#from email.header import Header
import re
import time
import os

from runner.settings import logger


class Openstack():
    headers1 = OrderedDict([('Accept', 'application/json'),
                        ('Content-Type', 'application/json'),
                        ('Accept-Encoding', 'application/json'),
                        ('charset', 'UTF-8')])

    def __init__(self, testbed):
        #self.oshost = '10.203.26.64'
        self.oshost = 'osservices-sj.eng.sonicwall.com'
        self.testbed = testbed
        self.topo_detail_url = 'http://' + self.oshost + '/topology_details/' + self.testbed + '.json/'
        self.topo_detail_xml = 'http://' + self.oshost + '/topology_details/' + self.testbed + '.xml'
        self.topo_url = 'http://' + self.oshost + '/topologies/' + self.testbed + '/'
        self.switch_url= 'http://' + self.oshost + '/switches/'
        self.switch_token = 'http://' + self.oshost + '/switch_reservations'
        self.topologies_json= 'http://' + self.oshost + '/topologies/' + self.testbed + '.xml'
        self.resource_url = 'http://' + self.oshost + '/topology_resources/'

    def get_oshost(self):
        return self.oshost

    def get_url(self, url):
        for i in range(5):
            time.sleep(1)
            logger.info('trying {} time to get {}'.format(i+1, url))
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response.content.decode('utf-8')
                else:
                    logger.error('Unable to Retrieve {} from OSServices'.format(url))
            except Exception as e:
                logger.error('Unable to Retrieve {} from OSServices: {}'.format(url, e))
            
        return False
            
    def post_url(self, url, msg=False, data=None, headers=headers1, timeout=60):
        logger.info(url)
        if data:
            data = json.dumps(data)
        try:
            logger.info(json.dumps(data))
            response = requests.post(url, headers=headers, data=data, timeout=timeout)
        except Exception as e:
            logger.info(f"ERR:POST request is not successful with expect {e}")
            return False
        logger.info("response:" + str(response))
        status_code = response.status_code
        logger.info("status code:" + str(status_code))
        if status_code == 200:
            return_value = True
        else:
            return_value = False
        resp = response.content.decode('utf-8')
        try:
            return_msg = json.loads(resp)
            logger.info(return_msg)
        except:
            logger.info(resp)
        if msg:
            return return_value, return_msg
        else:
            return return_value

    def delete_url(self, url, msg=False, data=None):
        logger.info(url)
        if data:
            data = json.dumps(data)
            logger.info(json.dumps(data))
        try:
            response = requests.delete(url,data=data, verify=False)
        except:
            logger.error("DELETE request is not successful")
            return False
        status_code = response.status_code
        logger.info("status code:" + str(status_code))
        if status_code == 200:
            return_value = True
        else:
            return_value = False
        resp = response.content.decode('utf-8')
        try:
            return_msg = json.loads(resp)
            logger.info(return_msg)
        except:
            logger.info(resp)
        if msg:
            return return_value, return_msg
        else:
            return return_value
            
    def get_console_info(self, dut='UTM'):
        foundit = None
        url = self.topo_detail_xml
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get {} console info.') 
            return False
        root = ET.fromstring(response)
        for device in root.findall('device'):
            if device.get('name') == dut:
                try:
                    console_ip = device.find('console').find('ip').text
                    console_port = device.find('console').find('port').text
                except Exception as e:
                    logger.error('Fail to get console ip and port due to: {}'.format(e))
                    return False
                foundit = True
                break
        if foundit:
            return console_ip, console_port
        return None
            
    def get_power_info(self, dut='UTM'):
        foundit = None
        #url = self.topo_detail_xml

        url = self.topo_detail_url + 'nodes.' + dut + '.power_controller'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get {} power controller info.')
            return False
        res = json.loads(response)
        logger.info(res)
        power_info = res["data"]
        if power_info :
            power_ip = power_info['ip'] if power_info['ip'] else ''
            power_user= power_info['user_name'] if power_info['user_name'] else ''
            power_port = power_info['port'] if power_info['port'] else ''
            power_model = power_info['model'] if power_info['model'] else ''
            power_type= power_info['type'] if power_info['type'] else ''
            power_pass= power_info['password'] if power_info['password'] else ''
            return power_ip, power_port, power_model, power_type,power_user,power_pass
        else:
            return None

    def get_slave_power_info(self, dut='UTM'):
        foundit = None
        #url = self.topo_detail_xml

        url = self.topo_detail_url + 'nodes.' + dut + '.power_controller_slave'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get {} power controller info.')
            return False
        res = json.loads(response)
        logger.info(res)
        power_info = res["data"]
        if power_info :
            power_ip = power_info['ip'] if power_info['ip'] else ''
            power_user= power_info['user_name'] if power_info['user_name'] else ''
            power_port = power_info['port'] if power_info['port'] else ''
            power_model = power_info['model'] if power_info['model'] else ''
            power_type= power_info['type'] if power_info['type'] else ''
            power_pass= power_info['password'] if power_info['password'] else ''
            return power_ip, power_port, power_model, power_type,power_user,power_pass
        else:
            return None

    def reboot_node(self, node='UTM'):
        url = self.topo_url + 'nodes/' + node + '/reboot'
        response = self.post_url(url)
        time.sleep(7)
        logger.info(response)

        if response == False:
            logger.error('Fail to reboot {}...'.format(node))
            return False
        else:
            return True

    def set_node_interface_state(self, node, iface, st):

        if re.match(r'x\d+', iface, re.I):
            iface = iface.upper()
        elif re.match(r'eth\d+', iface, re.I):
            iface = iface.lower()

        url = self.topo_url + 'nodes/' + node + "/" + "interfaces/" + iface +"/" + st.lower()
        response = self.post_url(url)

        if response == False:
            logger.error('set state={} for interface={} failed...'.format(st,iface))
            return False
        else:
            logger.error('set state={} for interface={} passed...'.format(st,iface))
            return True

    def lock_node(self, node):
        url = self.topo_url + 'nodes/' + node + '/lock'
        response = self.post_url(url)

        if response == True:
            logger.info('Successfully lock node={}...'.format(node))
            nodes = self.get_nodes_as_dictionary()
            resource_name = nodes[node]['topology_resource_name']
            self.lockResourceMail(resource_name)
            return True
        else:
            logger.error('Fail to lock node={}...'.format(node))
            return False
    
    def lockResourceMail(self, resource):

        logger.info('0' * 80)
        for k,v in os.environ.items():
            logger.info("{} = {}".format(k, v))
        logger.info('0' * 80)
        
        receiver = ['shanghai_automation@sonicwall.com']
        if re.search('BLR',resource,re.I):
            receiver +=['blr_openstack_admin@sonicwall.com']
        
        testsuite_name = os.popen('cat /root/Python_Runner_Logs/root_pythonrunner_0/command_line.log').read()
        match = re.search(r'python3 (\/.*?\.py) -var', testsuite_name, re.I)
        if match:
            testsuite_name = match.group(1)
        #commands_last_100= os.popen('tail -n 100 /root/Python_Runner_Logs/root_pythonrunner_0/commands.log').read()
        try:
            QBS_JOBNUM = os.environ['QBS_JOBNUM']
        except:
            QBS_JOBNUM = '1234'
            response = self.get_url(self.topologies_json)
            if response:
                topology = ET.fromstring(response)
                user_name = topology.find("username").text
                QBS_JOBNUM = user_name + '(Manually Local Run)'
                user_email = user_name+'@sonicwall.com'
                if user_email not in receiver:
                    receiver +=[user_email]
    
        html = """<html><body bgcolor="#F4F4F4">
            <p style="color: #555; font-family: Calibri; font-size: 18px;">Hello,<br />
            <br />
            The OpenStack resource {} has been locked when it run python suite.Please have a check.<br />
            <br />
            <h4>Test Execution Summary</h4>
            <table width="1200" style="font-weight:300; font-size:14px;text-align:left">
                    <tr>
                      <td>Product:</td>
                      <td>{}</td>
                    </tr>
                    <tr>
                      <td>Software Version:</td>
                      <td>{}</td>
                    </tr>
                    <tr>
                      <td>Test Bed:</td>
                      <td>{}</td>
                    </tr>
                    <tr>
                      <td>Job ID:</td>
                      <td>{}</td>
                    </tr>
                    <tr>
                      <td>Build:</td>
                      <td>{}</td>
                    </tr>
                    <tr>
                      <td>Test Suite:</td>
                      <td>{}</td>
                    </tr>
                    </table>
            <br />
            Regards,
            <br />
            Automation Team
            </p>
            </body></html>
               """.format(resource, os.environ['G_PRODUCT'], os.environ['G_SCMLABEL'], os.environ['G_TESTBED'], \
                   QBS_JOBNUM, os.environ['G_BUILD'], testsuite_name)
               
        msg = MIMEText(html,'html','utf-8')

        #receiver = ['openstack_admin@sonicwall.com']
        sender = 'auto_email@sonicwall.com'
        subject = 'OpenStack resource {} has been locked'.format(resource)
        
        msg['From'] = sender
        msg['Subject'] = subject
        #platform = self.get_node_platform('UTM')
        #if re.search('TZ\d70|\d700|\d760', platform):
        #    receiver +=['sgao@sonicwall.com', 'mlai@sonicwall.com', 'wegu@sonicwall.com']
        #if re.search('SONICCORE-HYPERV|NSV-VM|SONICCORE-VM', platform):
        #    receiver += ['sgao@sonicwall.com']
        #if re.search('15700', platform):
        #    receiver += ['wgu@sonicwall.com']
        print(msg)
        msg['To'] = ",".join(receiver)
        try:
            smtp = smtplib.SMTP('mail.sonicwall.com')
            smtp.sendmail(sender,receiver,msg.as_string())
            smtp.quit()
        except Exception as e:
            logger.error('Failed to send lock resource email:{}'.format(e))
            
    """
        get network for UTM interface or PC interface.
        node name like UTM , PC1 ..
        interface name like X0 , eth0..
        {"status":"success","message":"Successfully retrieved the testbed topology attributes","data":64}
    """
    def get_node_interface_vlan_id(self, node, interface):
        if re.match(r'x\d+', interface, re.I):
            interface = interface.upper()
        elif re.match(r'eth\d+', interface, re.I):
            interface = interface.lower()

        url = self.topo_detail_url + 'nodes.' + node + '.interfaces.' + interface + '.vlan'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False

        res = json.loads(response)
        vlan_id = res['data']
        if not vlan_id:
            logger.error('Unable to get the vlan id for interface {}!'.format(interface))
        elif isinstance(vlan_id, list):
            # cannot get the specified interface then it will return all interface list
            logger.error('Unable to get the vlan id. Maybe node={} has no interface={}'.format(node, interface))
            vlan_id = 0;
        return vlan_id

    # get ip for UTM interface or PC interface.
    # {"status":"success","message":"Successfully retrieved the testbed topology attributes","data":"192.168.168.168"}
    def get_node_interface_ip(self, node, interface):
        if re.match(r'x\d+', interface, re.I):
            interface = interface.upper()
        elif re.match(r'eth\d+', interface, re.I):
            interface = interface.lower()

        url = self.topo_detail_url + 'nodes.'+ node + '.interfaces.' + interface + '.ip'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False

        res = json.loads(response)
        ip = res["data"]
        if not ip:
            logger.error('Unable to get the ip for interface {}!'.format(interface))
        elif isinstance(ip, list):
            # cannot get the specified interface then it will return all interface list
            logger.error('Unable to get the ip. Maybe node={} has no interface={}'.format(node, interface))
            ip = 0;
        return ip

    def get_node_interface_ipv6(self, node, interface):
        if re.match(r'x\d+', interface, re.I):
            interface = interface.upper()
        elif re.match(r'eth\d+', interface, re.I):
            interface = interface.lower()
        url = self.topo_detail_url + 'nodes.'+ node + '.interfaces.' + interface + '.ipv6'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.').format(url)
            return False
        res = json.loads(response)
        logger.info(res)
        ip = res["data"]
        if not ip:
            logger.error('Unable to get the ip for interface {}!').format(interface)
        elif isinstance(ip, list):
            # cannot get the specified interface then it will return all interface list
            logger.error('Unable to get the ip. Maybe node={} has no interface={}'.format(node, interface))
            ip = 0;
        return ip

    def get_node_floatingip(self,node='PC1'):
        url = self.topo_detail_url + 'nodes.'+ node + '.floatingip'
        response = self.get_url(url)
        ip = response["data"]
        if not ip:
            logger.error('Unable to get the floatingip for node {}!').format(node)
            return False
        else:
            return ip

    # get network for UTM interface or PC interface.
    # {"status":"success","message":"Successfully retrieved the testbed topology attributes","data":"192.168.168.0/24"}
    def get_node_interface_network(self, node, interface):
        if re.match(r'x\d+', interface, re.I):
            interface = interface.upper()
        elif re.match(r'eth\d+', interface, re.I):
            interface = interface.lower()

        url = self.topo_detail_url + 'nodes.' + node + '.interfaces.' + interface + '.network'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False

        res = json.loads(response)
        network = res["data"]
        if not network:
            logger.error('Unable to get the network for interface {}!'.format(interface))
        elif isinstance(network, list):
            # cannot get the specified interface then it will return all interface list
            logger.error('Unable to get the network. Maybe node={} has no interface={}'.format(node, interface))
            return 0;
        return re.sub(r'\/\d+', "", res['data'])

    # get topology_resource_name for UTM
    # {"status":"success","message":"Successfully retrieved the testbed topology attributes","data":"OS-SH-NSA5600-2"}
    def get_UTM_dev_obj(self):
        url = self.topo_detail_url + 'nodes.UTM.topology_resource_name'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False

        res = json.loads(response)
        resource_name = res["data"]
        if not resource_name:
            logger.error('Unable to get the resource name!')
        return resource_name
    
    def get_UTM_serial_number(self):
        url = self.topo_detail_url + 'nodes.UTM.serial_number'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False

        res = json.loads(response)
        serial_number = res["data"]
        if not serial_number	:
            logger.error('Unable to get the serial number!')
        return serial_number	

    # get topology_resource_attributes for UTM
    # {"status":"success","message":"Successfully retrieved the testbed topology attributes","data":"team=UTM,testuse=remote"}
    def get_UTM_resource_attributes(self):
        url = self.topo_detail_url + 'nodes.UTM.attributes'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False

        res = json.loads(response)
        resource_attributes = res["data"]
        if not resource_attributes:
            logger.error('Unable to get the resource attributes!')
        return resource_attributes

    # get topology_resource_name for UTM
    # {"status":"success","message":"Successfully retrieved the testbed topology attributes","data":947}
    def get_UTM_resource_id(self):
        url = self.topo_detail_url + 'nodes.UTM.topology_resource_id'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False

        res = json.loads(response)
        resource_id = res["data"]
        if not resource_id:
            logger.error('Unable to get the resource id!')
        return resource_id
    
    ### get image password from testbed    
    def get_image_pw(self, pcs="PC1"):
        """
        Get image password(s) for PC nodes.
        Usage:
            get_image_pw("PC1")
            get_image_pw(["PC1","PC2","PC3"])
        """
        # convert to list
        if isinstance(pcs, str):
            pcs = [pcs]
        logger.info(f"========== Start get_image_pw for nodes: {pcs} ==========")

        result = {}

        for pc in pcs:
            try:
                # -----------------------------
                # 1. Get platform
                # -----------------------------
                platform_url = f"{self.topo_detail_url}nodes.{pc}.platform"
                logger.info(f"[{pc}] Requesting platform URL: {platform_url}")

                resp = requests.get(platform_url, headers={'Accept': 'application/json'}, timeout=10)
                logger.debug(f"[{pc}] HTTP status: {resp.status_code}")
                resp.raise_for_status()

                platform_data = resp.json()
                logger.info(f"[{pc}] Platform API response: {platform_data}")

                if platform_data.get('status') != 'success':
                    raise Exception(f"[{pc}] Platform API returned error: {platform_data}")

                platform_name = platform_data.get('data')
                logger.info(f"[{pc}] Platform detected: {platform_name}")

                # -----------------------------
                # 2. Get image info
                # -----------------------------
                image_url = f"http://10.203.26.65/images/{platform_name}.json"
                logger.info(f"[{pc}] Requesting image URL: {image_url}")

                resp = requests.get(image_url, headers={'Accept': 'application/json'}, timeout=10)
                logger.debug(f"[{pc}] HTTP status: {resp.status_code}")
                resp.raise_for_status()

                image_data = resp.json()

                logger.info(f"[{pc}] Image API response: {image_data}")

                # -----------------------------
                # 3. Extract password
                # -----------------------------
                pw = image_data.get('image_pw_value', '')
                pw_clean = pw.strip() if pw else None

                logger.info(f"[{pc}] Extracted password: {pw_clean!r}")

                result[pc] = pw_clean

            except requests.RequestException as e:
                logger.error(f"[{pc}] HTTP error: {e}")
                result[pc] = None

            except ValueError as e:
                logger.error(f"[{pc}] JSON parse error: {e}")
                result[pc] = None

            except Exception as e:
                logger.error(f"[{pc}] Unexpected error: {e}")
                result[pc] = None

        logger.info(f"========== Password collection result ==========")
        for pc, pw in result.items():
            logger.info(f"{pc} password is: -> {pw}")

        logger.info(f"========== End get_image_pw ==========")

        return result
    
    # save topology resource build version for UTM
    def save_UTM_resource_version(self, version):
        resource_id = self.get_UTM_resource_id()
        if not resource_id:
            logger.error('Unable to get the resource id!')
            return False
        logger.info('The resource id is {}.'.format(resource_id))
        url = self.resource_url + 'write_resource_build_version'
        data = {
            'resource_id': resource_id,
            'version': version
        }
        response = self.post_url(url, data=data)
        if not response:
            logger.error(f'Failed to save the software version {version}...')
            return False
        if hasattr(response, 'status_code'):
            if response.status_code == 200:
                logger.info(f'Successfully saved software version {version} for resource {resource_id}.')
                return True
            else:
                logger.error(f'HTTP {response.status_code}: {response.text}')
                return False
        else:
            return True
        
    #get default GW for PC
    def get_pc_default_gw_ip(self, node):
        url = self.topo_detail_url + 'nodes.' + node+'.default_gw_ip'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False

        res = json.loads(response)
        default_gw_ip = res["data"]
        if not default_gw_ip:
            logger.error('Unable to get the default gw ip!')
        return default_gw_ip

    def get_nodes(self):
        url = self.topo_detail_url + 'nodes'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False
        res = json.loads(response)
        nodes = res["data"]
        return nodes

    def get_nodes_as_dictionary(self):
        nodes = self.get_nodes()
        nodes = self._convert_to_dictionary(nodes)
        return nodes

    def _convert_to_dictionary(self, nodes):
        if isinstance(nodes, str) or isinstance(nodes, int) or isinstance(nodes, bool):
            return nodes
        elif isinstance(nodes, list):
            nodes_hash = {}
            if isinstance(nodes[0], dict) and 'name' in nodes[0].keys():
                for node in nodes:
                    nodes_hash[node['name']] = self._convert_to_dictionary(node)
                return nodes_hash
            else:
                node_list =[]
                for node in nodes:
                    node_list.append(self._convert_to_dictionary(node))
                return node_list
        elif isinstance(nodes, dict):
            nodes_hash = {}
            for key in nodes:
                nodes_hash[key] = self._convert_to_dictionary(nodes[key])
            return nodes_hash

    def get_node_platform(self, node):
        url = self.topo_detail_url + 'nodes.' + node + '.platform'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False
        res = json.loads(response)
        platform = res["data"]
        if isinstance(platform, list):
            logger.error('Error: Can not find the platform for {}'.format(node))
            return 0
        return platform

    def _get_switch_port(self, node, interface):
        url = self.topo_detail_url + 'nodes.' + node + '.interfaces.'+ interface + '.switch_port'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False
        res = json.loads(response)
        switch_port = res["data"]
        if isinstance(switch_port, list):
            logger.error('Error: Can not find the switch_port for {}'.format(node))
            return 0
        return switch_port

    def _get_switch_id(self, node, interface):
        url = self.topo_detail_url + 'nodes.' + node + '.interfaces.'+ interface + '.switch_id'
        print(url)
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False
        res = json.loads(response)
        switch_id = res["data"]
        if isinstance(switch_id, list):
            logger.error('Error: Can not find the switch_id for {}'.format(node))
            return 0
        return switch_id

    #{"ip":"10.6.1.253","location_id":3,"model":"S60","name":"OS-SH-ASW-4","password":"password","ports":48,"power_controller_port":null,"power_controllerid":null,"switchid":45,"type":"Force10","user_name":"admin"}
    def get_switch_data(self, node, interface):
        interface = interface.upper()
        switch_id = self._get_switch_id(node, interface)
        if switch_id == 0:
            return 0
        switch_port = self._get_switch_port(node, interface)
        if switch_port == 0:
            return 0
        url = self.switch_url + str(switch_id) + '.json'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False
        switch_data = json.loads(response)
        switch_data['switch_port'] = switch_port
        return switch_data

    def set_switch_port(self, node, interface, action):
        data = self.get_switch_data(node, interface)
        print(data)
        port = re.sub(r'\S+ ', "", data['switch_port'])
        # get switch token
        sw_token = self._get_switch_access(data['ip'])
        # import module dynamically
        import_type_name = 'switch.' + data['type'].lower()
        import_type1 = __import__(import_type_name)
        import_type2 = getattr(import_type1, data['type'].lower())
        import_module = getattr(import_type2, data['model'])
        switch = import_module(ip=data['ip'], switch=data['model'])
        rc = '';
        # config switch port
        if re.match(r'up|down', action, re.I):
            kwgs = {'port': port, 'param' : {'state': action}}
            rc = switch.config_port(**kwgs)
        elif re.match(r'auto', action, re.I):
            kwrgs = {'port': port, 'param': {'speed': action}}
            rc = switch.config_port(**kwrgs)
        # release sw_token
        print(rc)
        if sw_token:
            self._release_switch_access(sw_token)
        if rc:
            logger.info('config switch port successfully')
            return True
        else:
            logger.error('Failed to config switch port.')
            return False

    def _get_switch_access(self, ip):
        url = self.switch_token
        fm = {'ip': ip}
        response = self.post_url(url=url, msg=True, data=fm, timeout=1100)
        if not response:
            logger.error('Fail to post url {}.'.format(url))
            return False
        sw_token = response[1]['switch_token']
        return sw_token

    def _release_switch_access(self, sw_token):
        url = self.switch_token + '/' + str(sw_token)
        response = self.delete_url(url=url)
        if not response:
            logger.error('Fail to delete switch token by url {}.'.format(url))
            return False
        return True
    
    def get_tenant_interfaces(self,resource_id):
        #url = self.topo_detail_url + 'nodes.UTM.topology_resource_id'
        #response = self.get_url(url)
        #if not response:
        #    logger.error('Fail to get url {}.'.format(url))
        #    return False

        #res = json.loads(response)
        #resource_id = res["data"]
        #if not resource_id:
        #    logger.error('Unable to get the resource id!')
        #return resource_id
        url = 'http://' +self.oshost + '/get_tenant_interfaces.json'
        response = self.get_url(url)
        if not response:
            logger.error('Fail to get url {}.'.format(url))
            return False
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        requestData = {'topology_resource_id': resource_id}
        ret = requests.get(url, json=requestData, headers=headers)
        if ret.status_code != 200:
            return False, "Call OSservice API failed: status code is " + str(ret.status_code)
        else:
            tmpresult = json.loads(ret.text)
            print(tmpresult)
            return tmpresult


#if __name__ == '__main__':
    #os = Openstack("VTB510")
    # vlan = os.get_node_interface_vlan_id('UTM', 'X11')
    # print(vlan)
    # vlan = os.get_node_interface_vlan_id('PC1', 'eth0')
    # print(vlan)

    # ip = os.get_node_interface_ip('UTM', 'X11')
    # print(ip)
    # ip = os.get_node_interface_ip('PC1', 'eth0')
    # print(ip)
    # ip = os.get_node_interface_ip('UTM', 'X0')
    # print(ip)
    #
    # network = os.get_node_interface_network('UTM', 'X0')
    # print(network)
    # network = os.get_node_interface_network('PC1', 'eth0')
    # print(network)
    #
    # resource_name = os.get_UTM_dev_obj()
    # print(resource_name)
    #
    # defalut_gw_ip = os.get_pc_default_gw_ip('PC1')
    # print(defalut_gw_ip)
    #
    # node_platform = os.get_node_platform('PC1')
    # print(node_platform)
    # node_platform = os.get_node_platform('UTM')
    # print(node_platform)
    #
    #node_hash = os.get_nodes_as_dictionary()
    #print(node_hash)
    #print(node_hash['UTM'])
    #print(node_hash['UTM']['interfaces']['X0'])

    # switch_data = os.get_switch_data('UTM','X0')
    # print(switch_data)

    # os.set_switch_port('UTM','X0','down')
    # os.set_switch_port('UTM','X0','up')
    # os.set_switch_port('UTM','X0','auto')        
