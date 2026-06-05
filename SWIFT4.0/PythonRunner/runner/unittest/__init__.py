import argparse
import os
import re
import sys
import platform
import datetime,pytz
import subprocess,csv
os.environ['PID']=str(os.getpid())
from runner.settings import Params,VARS_DICT, logger,python_logger,SETUPTB,TIMESTAMP,LOG_DIR,SUITE_LOG_FILE_WITH_PATH, FAILED_SUITE_LOG_FILE_WITH_PATH, SUITE_RES_FILE,SUITE_RES_FILE_WITH_PATH, SUITE_PYTHON_FILE_WITH_PATH, SUITE_PYTHON_FILE, SUITE_LOG_FILE,SUITE_LOG_HTML_FILE, FAILED_SUITE_LOG_FILE, SUITE_COMMAND_LINE_FILE, SUITE_COMMAND_LINE_FILE_WITH_PATH, SUITE_STDERR_FILE
from runner.utils.ssdh import SSDH
from runner.utils.sonicauto import SonicAuto

# Set default environment variables if not already set
if 'PYTHON_SONICOS_HOME' not in os.environ:
    os.environ['PYTHON_SONICOS_HOME'] = '/SWIFT4.0/TESTS/python_SonicOS'
if 'SONICOS_HOME' not in os.environ:
    os.environ['SONICOS_HOME'] = '/SWIFT4.0/TESTS/SonicOS'
if 'PYTHON_COMMON_HOME' not in os.environ:
    os.environ['PYTHON_COMMON_HOME'] = '/SWIFT4.0/TESTS/python_SonicOS/common_lib'


def set_local_vars(args_str):
    item_list = args_str.replace('  ', ' ').split(' -')
    item_list = [x for x in item_list if x.strip() != '']
    for item in item_list[::]:  # type: str
        item_work = item.strip()
        if item_work.startswith('var '):
            var_content = item_work.replace('var ', '').strip()
            if '=' in var_content:
                pair = var_content.split('=', 1)
            else:
                parts = var_content.split(' ', 1)
                if len(parts) < 2:
                    continue
                pair = parts
            os.environ[pair[0]] = pair[1]
            VARS_DICT[pair[0]] = pair[1]
            python_logger.write(f'set local vars:\n')
            python_logger.write(f'var [{pair[0]}] , value: {pair[1]}\n')

def _process_args(args):
    args_str = ' ' + ' '.join(args)
    set_local_vars(args_str)
    args_str = args_str.replace('-var ', '').replace('DATABASE_HOST','--DATABASE_HOST').replace('SETUPJOBLOG','--SETUPJOBLOG').replace('SETUPRESULT','--SETUPRESULT').replace('G_', '--g_')
    args_str = args_str.replace('-rv ', '--')
    build_match = re.search(r'(\s*--g_BUILD=[^ ]+)',args_str, re.I)
    switch_build_match = re.search(r'(\s*--g_switch_BUILD=[^ ]+)',args_str, re.I)
    prebuild_match = re.search(r'(\s*--g_PREBUILD=[^ ]+)',args_str, re.I)
    scmlabel_match = re.search(r'(\s*--g_scmlabel=[^ ]+)',args_str, re.I)
    setupjoblog_match = re.search(r'(\s*--setupjoblog=[^ ]+)',args_str, re.I)
    topology_match = re.search(r'(\s*--g_TOPOLOGY=[^ ]+)',args_str, re.I)
    build = ''
    prebuild = ''
    switch_build = ''
    scmlabel = ''
    setupjoblog = ''
    topology = ''
    if build_match:
        build = build_match.group(1)
        args_str = args_str.replace(build, '')
        build =re.sub(r'--g_BUILD','--g_build',build, re.I)
    if switch_build_match:
        switch_build = switch_build_match.group(1)
        args_str = args_str.replace(switch_build, '')
        switch_build =re.sub(r'--g_SWITCH_BUILD','--g_switch_build',switch_build, re.I)
    if scmlabel_match:
        scmlabel = scmlabel_match.group(1)
        args_str = args_str.replace(scmlabel, '')
        scmlabel =re.sub(r'--g_SCMLABEL','--g_scmlabel',scmlabel, re.I)
    if prebuild_match:
        prebuild = prebuild_match.group(1)
        args_str = args_str.replace(prebuild, '')
        prebuild =re.sub(r'--g_PREBUILD','--g_prebuild',prebuild, re.I)
    if topology_match:
        topology = topology_match.group(1)
        args_str = args_str.replace(topology, '')
        topology =re.sub(r'--g_TOPOLOGY','--g_topology',topology, re.I)

    # else:
    if setupjoblog_match:
        setupjoblog = setupjoblog_match.group(1)
        args_str = args_str.replace(setupjoblog, '')
    args_str = args_str.replace(scmlabel, '').lower().replace('-rv ', '--') + build + switch_build + scmlabel + prebuild + setupjoblog + topology
    return args_str.split(' ')

temp_args = _process_args(sys.argv[1:])
parser = argparse.ArgumentParser(description="Parse test suite arguments")
parser.add_argument('--g_cc', action="store", dest="cc", required=False)
parser.add_argument('--g_njs', action="store", dest="njs", required=False)
parser.add_argument('--g_scmlabel', action="store", dest="scmlabel")
parser.add_argument('--g_testbed', action="store", dest="testbed", required=False)
parser.add_argument('--g_avt_mountpoint', action="store", dest="avt_mountpoint", required=False)
parser.add_argument('--g_build', action="store", dest="build", required=False)
parser.add_argument('--g_prebuild', action="store", dest="prebuild", required=False)
parser.add_argument('--g_switch_build', action="store", dest="switch_build", required=False)
parser.add_argument('--g_product', action="store", dest="product")
parser.add_argument('--g_user', action="store", dest="user")
parser.add_argument('--g_requesttime', action="store", dest="requesttime")
parser.add_argument('--mount_point', action="store", dest="mount_point", required=False)
parser.add_argument('--g_qbs', action="store", dest="qbs", required=False)
parser.add_argument('--g_resource', action="store", dest="resource", required=False)
parser.add_argument('-bundle', action="store", dest="bundle", required=False)
parser.add_argument('-rgname', action="store", dest="rgname", required=False)
parser.add_argument('--g_openstack', action="store", dest="openstack", required=False)
parser.add_argument('--setuptestbed', action="store", dest="setuptestbed", required=False)
parser.add_argument('--SETUPJOBLOG', action="store", dest="setupjoblog", required=False)
parser.add_argument('--setupresult', action="store", dest="setupresult", required=False)
parser.add_argument('--g_openstack_tid', action="store", dest="openstack_tid", required=False)
parser.add_argument('--starttime', action="store", dest="starttime", required=False)
parser.add_argument('-log_level', action="store", dest="log_level", default='INFO', required=False)
parser.add_argument('--log_dir', action="store", dest="log_dir", required=False)
parser.add_argument('--g_version', action="store", dest="version", required=False)
parser.add_argument('-sonicos_ver', action="store", dest="sonicos_ver", required=False)
parser.add_argument('-trialrun', action="store_true", default=False, required=False)
parser.add_argument('-nodatabase', action="store_true", default=False, required=False)
parser.add_argument('--g_swvertype', action='store', dest='swvertype', required=False)
parser.add_argument('-skip_dts', action="store_true", default=False, required=False)
parser.add_argument('-dev', action="store_true", default=False, required=False)
parser.add_argument('-noapi', action="store_true", default=False, required=False)
parser.add_argument('-no_security_rule', action="store_true", default=False, required=False)
parser.add_argument('-skip_reg', action="store_true", default=False, required=False)
parser.add_argument('--g_smk', action="store", dest='smk', required=False)
###for ui test
parser.add_argument('-w', "--browser", type=str, dest='browser_type', default='firefox')
parser.add_argument('-t', "--test_type", type=str, dest='test_type', default='ui')
parser.add_argument('--database_host', action="store", dest="database_host", required=False)
###for mt
parser.add_argument('--g_mt_source', action="store", dest="mt_source", required=False)
parser.add_argument('--g_mt_target', action="store", dest="mt_target", required=False)
parser.add_argument('--g_mt_version', action="store", dest="mt_version", required=False)
parser.add_argument('--g_mt_branch', action="store", dest="mt_branch", required=False)
##for topology
parser.add_argument('--g_topology', action="store", dest="topology", required=False)
#for rompack
parser.add_argument('--g_rompack_version', action="store", dest="g_rompack_version", required=False)

parser.add_argument('--g_repeat_testcase', action="store", dest="repeat_testcase", required=False)
parser.add_argument('--g_repeat_fail_testcase', action="store", dest="repeat_fail_testcase", required=False)
parser.add_argument('--g_openstack_retain', action="store", dest="retain", required=False)
#for system log saving
parser.add_argument('--g_system_log', action="store", dest="system_log", required=False)


## new add for console info
# parser.add_argument('-cserver', '--con_server', type=str, dest='con_server', required=True, help='console server ip')
# parser.add_argument('-cport', '--con_port', type=str, dest='con_port', required=True, help='console server login user')
parser.add_argument('--console_ip', action="store", dest="console_ip", required=False)
parser.add_argument('--console_port', action="store", dest="console_port", required=False)

known, unknown = parser.parse_known_args(temp_args)
val = vars(known)
try:
    for val_unknown in unknown:
        match= re.search(r'(.*)=(.*)',val_unknown)
        setattr(Params, match.group(1), match.group(2))
except:
    pass
Params.command = sys.argv
Params.path = "//depot/SQA" + sys.argv[0]

if val['cc']: Params.cc = val['cc']
if val['njs']: Params.njs = val['njs']
if val['scmlabel']: 
    Params.scmlabel = val['scmlabel']
    os.environ['G_SCMLABEL'] = val['scmlabel']
# if val['testbed']: 
#     Params.testbed = val['testbed'].upper()
#     os.environ['G_TESTBED'] = Params.testbed
Params.testbed = os.popen('hostname').read().split('-')[0]
os.environ['G_TESTBED'] = Params.testbed
if val['avt_mountpoint']: Params.avt_mountpoint = val['avt_mountpoint']
if val['prebuild']: Params.prebuild = val['prebuild']
if val['switch_build']: Params.switch_build = val['switch_build']
if val['product']: 
    Params.product = val['product'].upper()
    os.environ['G_PRODUCT'] =  Params.product
if val['build'] and not Params.product.startswith('MT-') and 'rompack' not in val['build']:
    Params.build = val['build']
    os.environ['G_BUILD'] = val['build']
    if not SETUPTB:
        ssdh = SSDH(Params.build)
        if ssdh.is_build_sig() and 'NSV' not in Params.product.upper():
            tmp_scmlabel=ssdh.get_version_total_string()
            if int(tmp_scmlabel.split('.')[0]) >=7:
                Params.scmlabel = ssdh.get_version_total_string()
                os.environ['G_SCMLABEL'] = Params.scmlabel
if val['user']: 
    Params.user = val['user']
else:
    logger.warning('Default mail to_user is specified by --g_user or suite owner. And cc_users is automation and shanghai_automation')
    logger.warning('Please specify --g_user if you want to receive mail.')
if val['requesttime']: Params.requesttime = val['requesttime']
if val['mount_point']: Params.mount_point = val['mount_point']
if val['qbs']: Params.qbs = val['qbs']
if val['resource']: Params.resource = val['resource']
if val['bundle']: Params.bundle = val['bundle']
if val['rgname']: Params.rgname = val['rgname'].upper()
if val['openstack']: 
    Params.openstack = val['openstack']
    os.environ['G_OPENSTACK'] = str(val['openstack'])
if val['setuptestbed']: Params.setuptestbed = val['setuptestbed']
if val['setupresult']: os.environ['SETUPRESULT'] = val['setupresult']
if val['setupjoblog']:
    Params.setupjoblog = val['setupjoblog']
    os.environ['G_SETUPLOGDIR'] =val['setupjoblog']
if val['openstack_tid']: 
    Params.openstack_tid = val['openstack_tid']
    os.environ['G_OPENSTACK_TID'] = str(val['openstack_tid'])

if val['starttime']:
    Params.starttime = datetime.datetime.strptime(val['starttime'], '%Y-%m-%d %H:%M:%S')
else:
    Params.starttime = datetime.datetime.now(pytz.timezone('UTC'))
    milliseconds = (Params.starttime.microsecond // 1000) * 1000
    Params.starttime.replace(microsecond=milliseconds)

if val['log_level']: 
    Params.log_level = val['log_level'].upper()
    logger.setLevel(Params.log_level)
if val['log_dir']: Params.log_dir = val['log_dir']
if val['version']: Params.version = val['version']

if val['dev']:
    os.environ["SONICOS_HOME"] = '/DEV_TESTS/SonicOS'
    os.environ["PYTHON_SONICOS_HOME"] = '/DEV_TESTS/python_SonicOS'
    os.environ["PYTHON_COMMON_HOME"] = '/DEV_TESTS/python_SonicOS/common_lib'
if val['sonicos_ver']:
    Params.sonicos_ver = val['sonicos_ver']
    ver_to_remove = val['sonicos_ver'] + "/"
    Params.path = Params.path.replace(ver_to_remove, "")
    os.environ["PYTHON_SONICOS_HOME"] = os.environ["PYTHON_SONICOS_HOME"] + '/' + Params.sonicos_ver
    os.environ["SONICOS_HOME"] = os.environ["SONICOS_HOME"] + '/' + Params.sonicos_ver
elif val['mt_branch']:
    Params.mt_branch = val['mt_branch']
    ver_to_remove = val['mt_branch'] + "/"
    Params.path = Params.path.replace(ver_to_remove, "")
    os.environ["PYTHON_SONICOS_HOME"] = os.environ["PYTHON_SONICOS_HOME"] + '/' + Params.mt_branch
    os.environ["SONICOS_HOME"] = os.environ["SONICOS_HOME"] + '/' + Params.mt_branch
if val['trialrun']: Params.trialrun = val['trialrun']
if val['nodatabase']: Params.no_database = val['nodatabase']
Params.noapi = val['noapi']
Params.no_security_rule = val['no_security_rule']
Params.skip_reg = val['skip_reg']
if val['smk']: Params.smk = val['smk']
if val['database_host']: Params.database_host = val['database_host']
###for UI7 test
if val['browser_type']: Params.browser_type = val['browser_type']
if val['test_type']: Params.test_type = val['test_type']

if val['mt_source']:Params.mt_source = val['mt_source']
if val['mt_target']:Params.mt_target = val['mt_target']
if val['mt_version']:Params.mt_version = val['mt_version']

if val['mt_branch']: Params.mt_branch = val['mt_branch']

if val['topology']: 
    Params.topology = val['topology']

if val['g_rompack_version']: 
    Params.g_rompack_version = val['g_rompack_version']
Params.requesttime = Params.requesttime.replace("_", " ")
if val['repeat_testcase']: Params.repeat_testcase = val['repeat_testcase']
if val['repeat_fail_testcase']: Params.repeat_fail_testcase = val['repeat_fail_testcase']
if val['retain']: Params.retain = val['retain']
if int(Params.openstack) !=1: Params.repeat_fail_testcase=1
if val['system_log']: Params.system_log = val['system_log']

Params.ts_actual_name = sys.argv[0].replace("/SWIFT4.0/TESTS/","")
if Params.no_database or Params.qbsjobid == '1234':
    Params.db_upload = "No"

if Params.testbed == '':
    Params.testbed = os.uname()[1]

if Params.product == '':
    Params.product = 'testProd'

# new add console_ip console_info
Params.console_ip = val['console_ip']
Params.console_port = val['console_port']

# remove "-PC1" from the testbed name
try:
    Params.testbed = re.match('(.*)-PC1', Params.testbed, re.I).group(1)
except:
    pass
centos_ver = ''

sa = SonicAuto()

if Params.db_upload != 'No':
    print('dddd')
    Params.aio_map=sa.get_aio_key_mapping()
def initiate_log():
    cmd_line = 'python3 ' + ' '.join(Params.command)
    _initiate_python_log(cmd_line)
    output_file = open(SUITE_RES_FILE_WITH_PATH, 'w', newline='')
    output_writer = csv.writer(output_file)
    output_writer.writerow(['ID', 'RESULT', 'STARTTIME', 'ENDTIME', 'UUID'])
    output_file.close()
    cmd_line = 'python3 ' + ' '.join(Params.command)
    command_output_file = open(SUITE_COMMAND_LINE_FILE_WITH_PATH, 'w', newline='')
    command_output_file.write(cmd_line)
    command_output_file.close()

    logger.info("Loaded suite")

def _initiate_python_log(cmd_line):
    python_logger.write('Dumping ENV:'+ '\n')
    for env in os.environ:
        python_logger.write(' '*8 +env + '= ' + os.environ[env] + '\n')
    python_logger.write('Start time: ' + TIMESTAMP + '\n')
    python_logger.write('Command line: ' + cmd_line+ '\n')
    python_logger.write('Test log dir: ' + LOG_DIR+ '\n')
    if re.search(r'Linux', platform.system(), re.I):
        python_logger.write('Route table:' + str(subprocess.Popen(['route'] + ['-n'], stdout=subprocess.PIPE).communicate()[0],encoding="utf8")+ '\n')
        python_logger.write('DNS setting:' + str(subprocess.Popen(['cat'] + ['/etc/resolv.conf'], stdout=subprocess.PIPE).communicate()[0],encoding="utf8")+ '\n')
    elif re.search(r'cygwin|mswin32', platform.system(), re.I):
        python_logger.write('Route table:' + str(subprocess.Popen(['/cygdrive/c/WINDOWS/system32/route'] + ['print'], stdout=subprocess.PIPE).communicate()[0],encoding="utf8")+ '\n')
        python_logger.write('DNS setting:' + str(subprocess.Popen(['/cygdrive/c/WINDOWS/system32/ipconfig'] + ['/all'], stdout=subprocess.PIPE).communicate()[0],encoding="utf8")+ '\n')
    if Params.sonicos_ver:
        sys.path.append(os.environ["PYTHON_COMMON_HOME"])
        from util.openstack import Openstack
        try:
            if Params.testbed and Params.openstack and int(Params.openstack) == 1:
                ostack = Openstack(Params.testbed)
                pc1_password=ostack.get_image_pw('PC1')
                if pc1_password['PC1']:
                    Params.pc1_password=pc1_password['PC1']
                nodes = ostack.get_nodes()
                python_logger.write('OpenStack Topology Definition: \n')
            elif 'ubuntu' in platform.version().lower():
                Params.pc1_password='sonicauto'
            for node in nodes:
                python_logger.write(' '*4 + '{\n')
                for node_key in node:
                    python_logger.write(' '*8 + node_key + '=> ' + str(node[node_key]) + '\n')
                python_logger.write(' '*4 + '}\n\n')
        except Exception as e:
            logger.error(e.args)

initiate_log()
