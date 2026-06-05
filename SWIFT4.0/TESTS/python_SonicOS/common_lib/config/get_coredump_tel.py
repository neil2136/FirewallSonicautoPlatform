import sys
import os
import re
import argparse
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])

from utm import Firewall
from utm import is_Firewall_up
from util.openstack import Openstack
from lib.modules.CLI.system import StatusCli
from lib.modules.CLI.diag import DiagCli
from runner.settings import Params, logger

class GetCoredumpTel():
    def __init__(self,testbed=''):
        self.testbed = ''
        self.fw = Firewall(ip='192.168.168.168', user='admin', password='password', supported_config_mode='cli-ssh')

    def get_coredump(self):
        # check and get coredump file
        diag = DiagCli(self.fw)
        (rc, output) = diag.show_coredump()
        if not rc:
            logger.error("Failed to show coredump list via cli")
            logger.info(output)
            return rc
        else:
            coredump_list = re.findall('(\S+core\.zst\S*|\S+\.lz4)' ,output, re.M|re.I)
            if len(coredump_list) == 0:
                logger.info(output)
                logger.info('-'*10+'NO coredump generated!'+'-'*10)
                return rc
            else:
                logger.info('coredumplist: {}'.format(coredump_list)) 
                
                # get DUT resource_name
                logger.info('get DUT resource_name')
                if Params.openstack:
                    osstack = Openstack(Params.testbed)
                    dut_res = osstack.get_UTM_dev_obj()
                else:
                    dut_res = ''
                logger.info(dut_res)
                
                # get version code
                logger.info('get version code')
                status = StatusCli(self.fw).show_status()
                ver_code = re.findall('Version.*(\d+\.\d+\.\d+\S+)', status, re.M|re.I)
                if len(ver_code)>0:
                    folder = '/logs/buildtestlogs/{}'.format(ver_code[0])
                else:
                    folder = '/logs/buildtestlogs/Undefine'
                if not (os.path.exists(folder)):
                    os.makedirs(folder) 
                time.sleep(1)
               
                # get ip connected to DUT X0
                logger.info('get ip connected to DUT X0')
                net_info = os.popen('ifconfig').read()
                addr = re.findall('inet\s+addr:(192.168.168.\d+)', net_info, re.M|re.I)
                if len(addr)>0:
                    server_ip = addr[0]
                    logger.info('ip connected to DUT X0: {}'.format(server_ip))
                else:
                    logger.error('can not get Server IP')
                    return False 
        
        tmp_file = os.popen('ls {}'.format(folder)).read()
        for item in coredump_list:
            if (item in tmp_file):
                logger.info('-'*10+'Coredump aleary exists!'+'-'*10)
            else:
                time_res = os.popen('date +%m%d-%k%M%S').read().replace('\n', '').replace(' ', '')
                file_name = '{}-{}-{}'.format(dut_res,time_res,item)
                logger.info(file_name)
                logger.info('-'*15+'saving {} to {}'.format(file_name,folder))
                cmd = ["export core-dump {} scp root@{}:{}/{}".format(item,server_ip,folder,file_name), Params.pc1_password]
                (rc, output) = self.fw.do_cli_commands(cmd, 1)
                if rc:
                    if re.search('Upload Complete', output, re.M|re.I):
                        logger.info('-'*15+'saved {} to {}'.format(file_name,folder))
                    else:
                        logger.error('can not saved {} to {}'.format(file_name,folder))
                else:
                    logger.error('get coredump via cli failed')

        #purge the existed coredump file
        cmd = ["diag purge-coredump"]
        (rc, output) = self.fw.do_cli_commands(cmd, 1)
        if rc:
            if re.search('Will purge the all coredump files', output, re.M|re.I):
                logger.info('purge coredump passed')
            else:
                logger.error('can not saved {} to {}'.format(file_name,folder))
        else:
            logger.error('purge coredump failed')

        return rc

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get testbed.')
    parser.add_argument('-testbed', '--testbed', type=str, dest='testbed', required=True, help='testbed ID, like: VTB518')
    args = parser.parse_args()
    testbed = args.testbed
    res = GetCoredumpTel(testbed)
    res.get_coredump()      
