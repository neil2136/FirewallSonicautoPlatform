import logging
import subprocess
import re
import os
import sys
import datetime,pytz
import time
from pathlib import Path
from urllib import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jinja2 import Environment, FileSystemLoader
# log file and result file

def dirsort(alist):
    try:
        alist.sort(key= lambda x: int(re.findall(r'\d+$', x)[0]))
    except:
        pass
    return alist

def setup_logdir(LOG_DIR):
    pid= os.environ.get('PID')
    if pid:
        pid=int(pid)
    ppid = os.getpid()
    dir_prefix = os.environ['USER'] + '_pythonrunner_'
    new_dirs = []
    for root, dirs, files in os.walk(LOG_DIR):
        if root == LOG_DIR:
            new_dirs = dirs[::]
            for each in dirs:
                if not re.search(r'^' + dir_prefix + r'\d*$', each):
                    new_dirs.remove(each)
            dirsort(new_dirs)
            break
    if not new_dirs:
        index = 0
    elif pid != ppid and pid:
        index = int(re.search(r'' + dir_prefix + r'(\d*)', new_dirs[-1]).group(1))
    else:
        index = int(re.search(r'' + dir_prefix + r'(\d*)', new_dirs[-1]).group(1))+1
    LOG_DIR += '/' + dir_prefix + str(index)
    return LOG_DIR

def get_nfs_ip():
    op_system = sys.platform
    if op_system == 'linux':
        mtab_cmd = ['cat', '/etc/mtab']
    else:
        mtab_cmd = ['/cygdrive/c/WINDOWS/system32/net', 'use']
    mtab_result_string = subprocess.Popen(mtab_cmd, stdout=subprocess.PIPE).communicate()[0]
    mtab_result_string = mtab_result_string.decode('ASCII')
    try:
        result = re.search(r'\b(\d+\.\d+\.\d+\.\d+)(\:/|\\)logs\b', mtab_result_string)
        ip = result.group(1)
    except:
        ip=''
    return ip

SUITE_FILE = os.path.basename(sys.argv[0]).split(".")
TIMESTAMP = str(datetime.datetime.now(pytz.timezone('UTC')).replace(microsecond=0)).replace(" ", "_")
TIMENOW = time.strftime("%s", time.gmtime())
SUITE_LOG_FILE = "commands.log"
FAILED_SUITE_LOG_FILE = 'Failed_testcase' + ".log"
SUITE_RES_FILE = 'summary' + ".csv"
SUITE_COMMAND_LINE_FILE = "command_line.log"
SUITE_LOG_HTML_FILE = "commands.html"
SUITE_PYTHON_FILE = "python_runner.log"
SUITE_STDERR_FILE = "stderr.log"
OPENSTACK_SETUP = {'VTB300': '1','VTB301': '1', 'VTB400': '1','VTB401': '1', 'VTB500': '1', 'VTB501': '1', 'VTB600': '1', 'VTB601': '1','VTB700': '1','VTB701': '1', 'VTB800': '1','VTB801': '1', 'VTB900': '1','VTB901': '1',}
LOG_DIR_F = os.path.join(os.path.expanduser("~"), "Python_Runner_Logs")
SETUPTB=False
if os.popen('hostname').read().split('-')[0] in OPENSTACK_SETUP:
    LOG_DIR_F = os.path.join('/home', "Python_Runner_Logs")
    SETUPTB=True
LOG_DIR = setup_logdir(LOG_DIR_F)
for i in range (0,5):
    try:
        os.makedirs(LOG_DIR)
        break
    except Exception as e:
        print(e)
        LOG_DIR = setup_logdir(LOG_DIR_F)
        time.sleep(0.5)

os.path.exists(LOG_DIR) or os.makedirs(LOG_DIR)
SUITE_LOG_FILE_WITH_PATH = os.path.join(LOG_DIR, SUITE_LOG_FILE)
FAILED_SUITE_LOG_FILE_WITH_PATH = os.path.join(LOG_DIR,FAILED_SUITE_LOG_FILE)
SUITE_RES_FILE_WITH_PATH = os.path.join(LOG_DIR, SUITE_RES_FILE)
SUITE_COMMAND_LINE_FILE_WITH_PATH = os.path.join(LOG_DIR, SUITE_COMMAND_LINE_FILE)
SUITE_PYTHON_FILE_WITH_PATH = os.path.join(LOG_DIR, SUITE_PYTHON_FILE)
# robotframework log files
ROBOT_LOG_FILE = SUITE_FILE[0] + "_" + TIMESTAMP + "_log.html"
ROBOT_REP_FILE = SUITE_FILE[0] + "_" + TIMESTAMP + "_report.html"
ROBOT_OUT_FILE = SUITE_FILE[0] + "_" + TIMESTAMP + "_output.xml"
ROBOT_LOG_FILE_WITH_PATH = os.path.join(LOG_DIR, ROBOT_LOG_FILE)
ROBOT_REP_FILE_WITH_PATH = os.path.join(LOG_DIR, ROBOT_REP_FILE)
ROBOT_OUT_FILE_WITH_PTAH = os.path.join(LOG_DIR, ROBOT_OUT_FILE)

# logging
DEBUG2 = 9
LOGGING = logging
LOGGING.addLevelName(DEBUG2, "DEBUG2")
LOGGING.basicConfig(
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(SUITE_LOG_FILE_WITH_PATH),
        logging.StreamHandler(stream=sys.stdout)
    ]
)
logger = LOGGING.getLogger(__name__)
python_logger = open(SUITE_PYTHON_FILE_WITH_PATH, 'a', newline='',buffering=1)

def debug2(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG2):
        self._log(DEBUG2, message, args, **kws)
LOGGING.Logger.debug2 = debug2

# SonicAuto
SONICAUTO_CONN = "postgresql://sonicauto:%s@10.203.15.9:5432/sonicauto" % parse.quote('s0nicw@ll')
SONICAUTO_SESSION = sessionmaker(bind=create_engine(SONICAUTO_CONN))

def get_sonicauto_session():
    return SONICAUTO_SESSION()

# mail server
MAIL_SVR = 'mail.sonicwall.com'
# DEFAULT_FROM_USER = 'auto_email@sonicwall.com'
DEFAULT_FROM_USER = 'automation@sonicwall.com'
DEFAULT_CC_USER = 'automation@sonicwall.com, shanghai_automation@sonicwall.com'

# job related variables
try:
    QBS_JOBNUM = os.environ['QBS_JOBNUM']
except:
    QBS_JOBNUM = '1234'
os.environ['G_TIMESTAMP'] = TIMENOW
python_logger.write(f'set local vars:\n')
python_logger.write(f'var [G_TIMESTAMP] , value: {TIMENOW}\n')

NFS_IP=get_nfs_ip()
VARS_DICT={}
# parameters
class Params:
    console_ip = ''
    console_port = ''
    cc = ''
    njs = ''
    scmlabel = '1.1.1.1'
    testbed = ''
    avt_mountpoint = ''
    build = ''
    prebuild = ''
    switch_build = ''
    product = ''
    user = ''
    requesttime = ''
    mount_point = ''
    qbs = '1'
    resource = ''
    bundle = 'TBD'
    rgname = ''
    openstack = 0
    setuptestbed = ''
    setupjoblog = ''
    openstack_tid = None
    starttime = ''
    log_level = ''
    log_dir = ''
    version = ''
    sonicos_ver = ''
    trialrun = False
    no_database = False
    command = ''
    log_location = SUITE_LOG_FILE_WITH_PATH
    server_log_location = ''
    path = ''
    db_upload = 'Yes'
    job_requestid=''
    qbsjobid = QBS_JOBNUM
    ts_actual_name = ''
    total_aptest = 0
    finishtime = ''
    total_run = 0
    total_errors = 0
    total_skip = 0
    total_failures = 0
    total_pass = 0
    nontc_total_run = 0
    nontc_total_errors = 0
    nontc_total_skip = 0
    nontc_total_failures = 0
    nontc_total_pass = 0
    reg_total_exec = 0
    reg_exec_time = 0
    ts_display_name = ''
    ts_topology_path = ''
    ts_topology_link = ''
    exec_time = ''
    total_exec= 0
    robot = ''
    dts_jira_link = {}
    ##for UI7
    browser_type = 'firefox'
    test_type = 'ui'
    smk = 0
    database_host = ''   
    mt_source = ''
    mt_target = ''
    mt_version = ''
    mt_branch =''
    G_DNS1 = '0.0.0.0'
    G_DNS2 = '0.0.0.0'
    G_DNS3 = '0.0.0.0'
    G_NEW_PASSWORD='S0nic@uto'
    nic_ver = ''
    topology = ''
    g_rompack_version=''
    repeat_testcase=1
    repeat_fail_testcase=2
    retain =0
    rerun_pass=0
    rerun_fail=0
    system_log = ''
    aio_map={}
    pc1_password='password'
###set global dns###
location_dict = {
    '200': 'SC',
    '6': 'SH',
    '5': 'IND'
}
try:
    mount_info = subprocess.Popen('mount -n', shell = True, stdout = subprocess.PIPE).communicate()[0].decode('ASCII')
    location = 'SH'
    match = re.search(r'\d+\.(\d+)\.\d+\.\d+:\/SWIFT4\.0', mount_info,re.I)
    location = location_dict[match.group(1)]
    if match:
        location = location_dict[match.group(1)]
    else:
        logger.error('Get mount info failed, take location as SH')
    dns_info=subprocess.Popen('cat /SWIFT4.0/COMMON/config/DNS_LIST_new', shell = True, stdout = subprocess.PIPE).communicate()[0].decode('ASCII').split('\n')
    flag = 0
    for line in dns_info:
        tmp = line.split('\t')
        if not line:
            continue
        elif tmp[0] == location:
            Params.G_DNS1 = tmp[1]
        elif flag == 0:
            Params.G_DNS3 = tmp[1]
            flag =1
        else:
            Params.G_DNS2 = tmp[1]
except:
    logger.error('Fail to get dns address from /SWIFT4.0/COMMON/config/DNS_LIST_new')
###description for testcase and test stage which show in mail
class Descriptions:
    testcase = []
    teststage = []

class TestcaseLog:
    log = {}

# PythonRunner Home Dir
try:
    PYTHON_RUNNER_HOME = os.environ['PYTHON_RUNNER_HOME']
except:
    PYTHON_RUNNER_HOME = '/SWIFT4.0/PythonRunner'

# Email templates
TEMPLATE_DIR = os.path.join(PYTHON_RUNNER_HOME, "runner/resources/templates/email")
TEMPLATE_ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
TEST_COMPLETED_TEMPLATE = TEMPLATE_ENV.get_template("test_completed.html")
START_TEST_COMPLETED_TEMPLATE = TEMPLATE_ENV.get_template("start_test_completed.html")
CORE_DUMP_FILE_TEMPLATE = TEMPLATE_ENV.get_template("core_dump_file.html")
CORE_DUMP_SUMMARY_TEMPLATE = TEMPLATE_ENV.get_template("core_dump_summary.html")
