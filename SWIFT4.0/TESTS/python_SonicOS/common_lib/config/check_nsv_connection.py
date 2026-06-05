import os
import sys
import re
import paramiko
import argparse
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import logger
from config.swconfig import DeviceConfig


class CheckNsvLink():
    def __init__(self, testbed, openstack=True, device='UTM', spec_file=''):
        self.testbed = testbed
        self.openstack = openstack
        self.device = device
        self.spec_file = spec_file if spec_file \
                                   else '/SWIFT4.0/COMMON/data/switches/' + self.testbed.upper() + '.yaml'
        if self.openstack:
            self.osobj = Openstack(self.testbed)
#        else:
#            self.tbobj = DeviceConfig(specfile=self.spec_file)

    def get_esxi_info(self):
        if not self.openstack:
            return True
        logger.info("This is an openstack device.")
        node_info = self.osobj.get_nodes_as_dictionary()
        res_name = node_info['UTM']['topology_resource_name']
        utm_info = self.osobj.get_switch_data('UTM', 'X0')
        if not utm_info:
            logger.info("Can't get the switch info.")
            return False
        self.user = utm_info['user_name']
        self.passwd = utm_info['password']
        self.host = utm_info['ip']
        self.res_name = res_name

        return True

    def check_esxi_link_and_reset(self):
        if not self.openstack:
            return True
        sshobj = paramiko.SSHClient()
        sshobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            sshobj.connect(hostname=self.host, port=22, username=self.user, password=self.passwd)
        except Exception as e:
            logger.info("connect to ESXi server failed.\n" + str(e))

        try:
            try_trans = sshobj.get_transport()
            try_trans.send_ignore()
            logger.info("Login ESXi server passed.")
        except Exception as e:
            logger.info("Exception: " + str(e))
            logger.info("Connect to ESXi server failed.")
            return False

        cmd = 'vim-cmd vmsvc/getallvms'
        stdin, stdout, stderr = sshobj.exec_command(cmd)
        vmid = ''
        for item in stdout.readlines():
            find = re.search(r'(\d+)\s+'+self.res_name+'\s+', item)
            if find:
                vmid = str(find.group(1))
                logger.info("Get VM ID: " + vmid)
                break
        
        if not vmid:
            logger.info("Get VM ID failed.")
            sshobj.close()
            return False

        issue_port_list = []
        cmd = f'vim-cmd vmsvc\/device.getdevices {vmid}'
        stdin, stdout, stderr = sshobj.exec_command(cmd)
        nic_list = ''.join(stdout.readlines()).split('vim.vm.device.VirtualVmxnet3')
        for item in nic_list:
            if 'Network adapter' in item:
                find = re.search(r'key\s+=\s+(\d+).+deviceName\s+=\s+"(\S+)".*connected\s+=\s+(\w+)', item, re.I|re.S)
                if find:
                    nic_key = find.group(1)
                    nic_name = find.group(2)
                    nic_status = find.group(3)
                    if 'soniccore' not in nic_name and 'sonicos' not in nic_name and \
                       not re.search(r'-x\d+', nic_name,re.I):
                        continue
                    if nic_status == 'true':
                        logger.info(f'{nic_name} ID {nic_key} is connected')
                    else:
                        logger.info(f'{nic_name} ID {nic_key} link status: {nic_status}')
                        issue_port_list.append(nic_key)

        for item in issue_port_list:
            logger.info(f"Recover link ID {item}")
            cmd = f'vim-cmd vmsvc\/device.connection {vmid} {item} 1'
            sshobj.exec_command(cmd)

        sshobj.close()
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check and recover NSV device link.')
    parser.add_argument('-testbed', type=str, required=True, help='testbed ID, like: VTB518')
    parser.add_argument('-openstack', type=str, default='1', required=False, help='openstack tag, like: 0|1')
    args = parser.parse_args()

    if args.openstack == '0':
        logger.info("There is no NSV device on static testbed.")
    else:
        obj = CheckNsvLink(testbed=args.testbed)
        obj.get_esxi_info()
        rc = obj.check_esxi_link_and_reset()
        if rc:
            logger.info("Check and recover NSV link passed.")
        else:
            logger.info("Check and recover NSV link failed.")
