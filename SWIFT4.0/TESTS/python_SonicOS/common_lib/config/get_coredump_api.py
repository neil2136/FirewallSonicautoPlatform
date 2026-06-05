import sys
import os
import re
import argparse
import time

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/8.0.1')

from utm import Firewall
from utm import is_Firewall_up
from util.openstack import Openstack
from lib.modules.CLI.system import StatusCli
from lib.modules.API.diag import DiagApi
from runner.settings import Params, logger
from config.rsync_tel import RsyncTel


class GetCoredumpApi():
    def __init__(self,testbed='',product='',qbsjobid='',scmlabel='',ts_display_name='',openstack=1):
        self.testbed = testbed
        self.product = product
        self.qbsjobid= qbsjobid
        self.scmlabel = scmlabel
        self.ts_display_name =ts_display_name
        self.openstack =openstack
        self.fw = Firewall(ip='192.168.168.168', user='admin', password='password', supported_config_mode='cli-ssh')
        self.fw_api = Firewall(ip='192.168.168.168', user='admin', password='password', supported_config_mode='api')
        self.rsync = RsyncTel(self.testbed)

    def get_coredump(self,suffix=None):
        # check and get coredump file
        diag = DiagApi(self.fw_api)
        rc, output = diag.show_coredump_list()
        rc1=True
        if not rc:
            logger.info('-'*10+'Get coredump failed!'+'-'*10)
            cmd = ["show administration sonicos-api","configure","administration","sonicos-api","enable","commit","end","exit"]
            self.fw.do_cli_commands(cmd, 1)
            return rc
        else:
            if len(output) == 0:
                logger.info('-'*10+'NO coredump generated!'+'-'*10)
                return rc
            else:
                logger.info('coredumplist: {}'.format(output))

                # get DUT resource_name
                logger.info('get DUT resource_name')
                
                if self.openstack:
                    osstack = Openstack(self.testbed)
                    dut_res = osstack.get_UTM_dev_obj()
                    dut_res += '-' + str(osstack.get_UTM_resource_id())
                else:
                    dut_res = self.testbed + '-' + self.product
                logger.info(dut_res)

                # get version code
                logger.info('get codump folder on NFS.')
                version = self.scmlabel
                folder = '/logs/buildtestlogs/Undefine'
                if version:
                    folder = '/logs/buildtestlogs/{}'.format(version)
                if not (os.path.exists(folder)):
                    os.makedirs(folder)

                time.sleep(1)

                # get ip connected to DUT X0
                logger.info('get ip connected to DUT X0')
                net_info = os.popen('ifconfig').read()
                addr = re.findall('inet\s+\w*:?(192.168.168.\d+)', net_info, re.M|re.I)
                if len(addr)>0:
                    server_ip = addr[0]
                    logger.info('ip connected to DUT X0: {}'.format(server_ip))
                else:
                    logger.error('can not get Server IP')
                    return False
        purge_flag = True
        tmp_file = os.popen('ls {}'.format(folder)).read()
        for item in output:
            if (item in tmp_file):
                logger.info('-'*10+'Coredump aleary exists!'+'-'*10)
            elif (item != 'latestcoreupload.md5' and item.endswith('core.zst.gpg')):
                time_res = os.popen('date +%Y%m%d-%k%M%S').read().replace('\n', '').replace(' ', '')
                job_id = self.qbsjobid
                file_name = '-{}-{}-{}-{}'.format(dut_res, job_id, time_res, item)
                if suffix:
                    file_name = suffix + '-' + self.ts_display_name + file_name
                elif self.ts_display_name:
                    file_name = self.ts_display_name + file_name
                subfolder=os.path.splitext(os.path.splitext(os.path.splitext(file_name)[0])[0])[0]
                folder = folder+ '/' + subfolder
                os.mkdir(folder)
                logger.info('-'*15+'saving {} to {}'.format(file_name,folder))
                cmd = ["export core-dump {} scp root@{}:{}/{}".format(item,server_ip,folder,file_name), Params.pc1_password,f'export console-logs  scp root@{server_ip}:{folder}/',Params.pc1_password,f'export safe-mode-logs  scp root@{server_ip}:{folder}/',Params.pc1_password]
                (rc, out) = self.fw.do_cli_commands(cmd, 1)
                if rc:
                    if re.search('Upload Complete', out, re.M|re.I):
                        logger.info('-'*15+'saved {} to {}'.format(file_name,folder))
                    else:
                        logger.error('can not saved {} to {}'.format(file_name,folder))
                else:
                    try:
                        os.rmdir(folder)
                    except:
                        logger.error(f'dir {folder} does not exist')
                    logger.error('get coredump via cli failed')
                if not os.path.exists(folder + '/' + file_name):
                    purge_flag &= False
                # --- rsync folder if download success ---
                else:
                    logger.info(f"folder={folder}")
                    logger.info(f"file check={folder}/{file_name}")
                    logger.info(f"exist={os.path.exists(folder + '/' + file_name)}")
                    logger.info('begin sync coredump file to coredump-analyzer server')
                    self.rsync.sync_to_analysis_server(folder, file_name)

            else:
                logger.error(f'Ilegal coredump: {item}')
                continue

        #purge the existed coredump file
        if purge_flag:
            cmd = ["diag purge-coredump"]
            (rc1, out) = self.fw.do_cli_commands(cmd, 1)
            if rc1:
                if re.search('Will purge the all coredump files', out, re.M|re.I):
                    logger.info('purge coredump passed')
                else:
                    logger.error('can not saved {} to {}'.format(file_name,folder))
            else:
                logger.error('purge coredump failed')

        return rc & rc1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get testbed.')
    parser.add_argument('-testbed', '--testbed', type=str, dest='testbed', default='testbed',required=False, help='Example: VTB518')
    parser.add_argument('-qbsjobid', '--qbsjobid', type=str, dest='qbsjobid',default='qbsjobid', required=False, help='Example: 2001234')
    parser.add_argument('-product', '--product', type=str, dest='product', default='product',required=False, help='Example: 2700')
    parser.add_argument('-openstack', '--openstack', type=str, dest='openstack', default=1,required=False, help='Example: 1')
    parser.add_argument('-ts_display_name', '--ts_display_name', type=str, dest='ts_display_name',default='name', required=False, help='Example: Gen7_***')
    parser.add_argument('-scmlabel', '--scmlabel', type=str, dest='scmlabel',default='scmlabel', required=False, help='Example: 8.0.0-R1234')
    args = parser.parse_args()
    res = GetCoredumpApi(args.testbed,args.product,args.qbsjobid,args.scmlabel,args.ts_display_name,args.openstack)
    res.get_coredump()
