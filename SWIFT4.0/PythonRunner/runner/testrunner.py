import argparse
import csv
import datetime,pytz
import os
import re
import time
import platform
import sys
import subprocess
import psutil
import unittest
import glob
from collections import OrderedDict
import urllib.parse
from runner.utils.log import log
from runner.utils.aptest import ApTest
from runner.utils.email_util import SendMail
from runner.utils.sonicauto import SonicAuto
from runner.settings import Params, logger,python_logger, SUITE_LOG_FILE_WITH_PATH, FAILED_SUITE_LOG_FILE_WITH_PATH, SUITE_RES_FILE,SUITE_RES_FILE_WITH_PATH, SUITE_PYTHON_FILE_WITH_PATH, SUITE_PYTHON_FILE, SUITE_LOG_FILE,SUITE_LOG_HTML_FILE, FAILED_SUITE_LOG_FILE, SUITE_COMMAND_LINE_FILE, SUITE_COMMAND_LINE_FILE_WITH_PATH, SUITE_STDERR_FILE, Descriptions, TestcaseLog, TIMESTAMP, LOG_DIR, DEFAULT_CC_USER,QBS_JOBNUM,VARS_DICT,OPENSTACK_SETUP


class Runner():
    def __init__(self, args, suite, to_users=None, cc_users=None):
        self.suite = suite
        self.suite_name = args[0]

        self.results = []
        self.has_uuid = False
        self.sa = SonicAuto()

        # if no to_users passed in, send email to suite owner and user who submits the test
        tmp_to_users=''
        if to_users is not None:
            tmp_to_users = to_users + ','
        tmp_to_users += Params.user
        suite_owner = self.sa.get_testsuite_owner(Params.path)
        if suite_owner != '' and suite_owner['name'] != Params.user:
            tmp_to_users = tmp_to_users + "," +  suite_owner['name']
        tmp_to_users = 'auto_email' + "," + tmp_to_users
        self.to_users = self._process_users(tmp_to_users)

        # process cc_users
        if cc_users is not None:
            self.cc_users = self._process_users(cc_users)
            self.cc_users = self.cc_users + ',' + DEFAULT_CC_USER
        else:
            self.cc_users = DEFAULT_CC_USER
        if Params.cc:
            self.cc_users = self._process_users(Params.cc) + ',' + self.cc_users
        self.cmd_line = 'python3 ' + ' '.join(Params.command)
        #self._initiate_log()
        self.pid = psutil.Process(os.getpid()).pid
        logger.info(f'Process pid id is: {str(self.pid)}')

    def _process_users(self, users):
        user_list = re.split(r'[;,\s]\s*', users)
        ret_list = []
        for u in user_list:
            if u:
                if u.find('@') > 0:
                    ret_list.append(u)
                else:
                    ret_list.append(u + '@sonicwall.com')

        return ','.join(ret_list)

    # def _initiate_log(self):
    #     self._initiate_python_log()
    #     output_file = open(SUITE_RES_FILE_WITH_PATH, 'w', newline='')
    #     output_writer = csv.writer(output_file)
    #     output_writer.writerow(['ID', 'RESULT', 'STARTTIME', 'ENDTIME', 'UUID'])
    #     output_file.close()
    #     command_output_file = open(SUITE_COMMAND_LINE_FILE_WITH_PATH, 'w', newline='')
    #     command_output_file.write(self.cmd_line)
    #     command_output_file.close()

    #     logger.info("Loaded suite")

    # def _initiate_python_log(self):
    #     python_logger.write('Dumping ENV:'+ '\n')
    #     for env in os.environ:
    #         python_logger.write(' '*8 +env + '= ' + os.environ[env] + '\n')
    #     python_logger.write('Start time: ' + TIMESTAMP + '\n')
    #     python_logger.write('Command line: ' + self.cmd_line+ '\n')
    #     python_logger.write('Test log dir: ' + LOG_DIR+ '\n')
    #     if re.search(r'Linux', platform.system(), re.I):
    #         python_logger.write('Route table:' + str(subprocess.Popen(['route'] + ['-n'], stdout=subprocess.PIPE).communicate()[0],encoding="utf8")+ '\n')
    #         python_logger.write('DNS setting:' + str(subprocess.Popen(['cat'] + ['/etc/resolv.conf'], stdout=subprocess.PIPE).communicate()[0],encoding="utf8")+ '\n')
    #     elif re.search(r'cygwin|mswin32', platform.system(), re.I):
    #         python_logger.write('Route table:' + str(subprocess.Popen(['/cygdrive/c/WINDOWS/system32/route'] + ['print'], stdout=subprocess.PIPE).communicate()[0],encoding="utf8")+ '\n')
    #         python_logger.write('DNS setting:' + str(subprocess.Popen(['/cygdrive/c/WINDOWS/system32/ipconfig'] + ['/all'], stdout=subprocess.PIPE).communicate()[0],encoding="utf8")+ '\n')
    #     if Params.sonicos_ver:
    #         sys.path.append(os.environ["PYTHON_COMMON_HOME"])
    #         from util.openstack import Openstack
    #         try:
    #             if Params.testbed and Params.openstack and int(Params.openstack) == 1:
    #                 ostack = Openstack(Params.testbed)
    #                 nodes = ostack.get_nodes()
    #                 python_logger.write('OpenStack Topology Definition: \n')
    #             for node in nodes:
    #                 python_logger.write(' '*4 + '{\n')
    #                 for node_key in node:
    #                     python_logger.write(' '*8 + node_key + '=> ' + str(node[node_key]) + '\n')
    #                 python_logger.write(' '*4 + '}\n\n')
    #         except Exception as e:
    #             logger.error(e.args)

    def run_and_parse_result(self):
        raise NotImplementedError

    def run(self,n=1):
        if Params.testbed not in OPENSTACK_SETUP:
            self.send_start_email()
        else:
            self.get_dut_log()

        if Params.db_upload != 'No':
            self.save_result_before_run_to_sonicauto()
        self.run_and_parse_result(n)
        self.parse_result_file()
        self.generate_failed_log()
        Params.finishtime = datetime.datetime.now(pytz.timezone('UTC'))
        milliseconds = (Params.finishtime.microsecond // 1000) * 1000
        Params.finishtime=Params.finishtime.replace(microsecond=milliseconds)
        # if Params.db_upload != 'No':
        #     self.upload_result_to_sonicauto()
#use testrail instead of aptest, so skip it
#        if self.has_uuid and Params.qbsjobid != 'None':
#            logger.info("Will upload result to ApTest")
#            Params.total_aptest = self.upload_result_to_aptest()
        self.postrun()
        if Params.testbed not in OPENSTACK_SETUP:
            self.send_email()
        else:
            self.get_logs_info()
        if Params.db_upload != 'No':
             self.upload_jobrequest_after_run()
        self.unset_vars()
#winni
    def get_test_names(self,test_suite):
        test_names = []
        for test in test_suite:
            if isinstance(test, unittest.TestCase):
                # This will get the full name: <module>.<class>.<method>
                test_names.append(test.id())
            elif isinstance(test, unittest.TestSuite):
                # If it's a TestSuite, recurse into it
                test_names.extend(self.get_test_names(test))
        return test_names

    def save_result_before_run_to_sonicauto(self):
        results_before_run=[]
        # testcase= self.get_test_names(self.suite)
        testcases=list(OrderedDict.fromkeys(map(lambda x:'.'.join(x.split('.')[:-1]),self.get_test_names(self.suite))))

        for testcase in testcases:
            title=testcase.split('.')[-1]
            if re.search(r'TestRestoreDUT',title, re.I) or re.search(r'TestUploadFirmware',title,re.I) or re.search('TestAddTopology',title,re.I):
                case_type='NonTC'
            else:
                case_type='TestCase'
            results_before_run.append({
             # 'title': row['ID'],
                    'title': testcase.split('.')[-1], #this key is for mouseover testcase name in mail
                    'result': 'SKIPPED',
                    'starttime': Params.starttime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                    'endtime': Params.starttime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                    'uuid': '',
                    'matrixid': 0,
                    'type': case_type,
                    'ftype': '',
                    'parameters': '',
                    'alias': '',
                    # 'filename': self.suite_name,
                    'filename':  testcase.split('.')[-1],
                    'log_link': 'not generated',
                    'dts_jira_link': '',
                    'failed_stage': [], #print these stage when a testcase failed
                    'scmlabel': Params.scmlabel,
                    'product':Params.product,
            })
            
        for i in range(0,5):
            result = self.sa.save_result_before_run(results=results_before_run)
            if result[1] == 'Result got saved successfully':
                logger.info('Result saved to sonicauto before run successfully.')
                Params.job_requestid =result[0]
                break
            time.sleep(5)
            logger.info('Try again to initial result to sonicauto before run...')
            self.sa = SonicAuto()        

    def unset_vars(self):
        python_logger.write(f'Unsetting local vars:\n')
        for var in VARS_DICT.keys():
            del os.environ[var]
            python_logger.write(f'undefine {var}\n')

    def terminate_child_process(self):
        process_children = psutil.Process(self.pid).children(recursive=True)
        if process_children:
            for child in process_children:
                try:
                    logger.info("Terminating {}".format(child))
                    child.kill()
                except psutil.NoSuchProcess:
                    logger.info(f"{child} no longer exists.")    
            
    def postrun(self):
        python_logger.write('\nExiting Testsuite...\n\n')
        python_logger.flush()
        self.terminate_child_process()

    def send_email(self):
        sm = SendMail(self.to_users, self.cc_users)
        sm.finish_mail(self.get_result_summary(), self.get_execution_summary(), self.get_logs_info(), self.results)

    def send_start_email(self):
        sm = SendMail(self.to_users, self.cc_users)
        sm.start_mail(self.get_start_summary(), self.get_dut_log(), self.sa.get_full_name(Params.user)['full_name'])

    def upload_result_to_sonicauto(self):
        for i in range(0,5):
            result = self.sa.save_result(results=self.results)
            if result == 'Result got saved successfully':
                logger.info('Result saved to sonicauto successfully.')
                break
            time.sleep(5)
            logger.info('Try again to upload result to sonicauto...')
            self.sa = SonicAuto()

    #winni
    def upload_result_to_sonicauto_before_run(self,results):
        for i in range(0,5):
            result = self.sa.save_result(results=results)
            if result == 'Result got saved successfully':
                logger.info('Initial job request and test result to sonicauto before run successfully.')
                break
            time.sleep(5)
            logger.info('Try again toiInitial job request and test result to sonicauto...')
            self.sa = SonicAuto()    

    def upload_jobrequest_after_run(self):
        for i in range(0,5):
            result = self.sa.save_job_request_after_run()
            if result == 'Save job request after run successfully':
                logger.info('Save job request after run successfully.')
                break
            time.sleep(5)
            logger.info('Try again to upload jobrequest to sonicauto...')
            self.sa = SonicAuto()

    def upload_result_to_aptest(self):
        ap = ApTest()
        return ap.upload_aptest(self.results, Params.product, Params.scmlabel)

    def get_dut_log(self):
        data = {
            'Name': 'DUT Console Logs',
            'Link': '',
            'Display': '',           
        }
        try:
            my_log = log(Params.resource, Params.product, Params.scmlabel, Params.testbed, Params.user)
            console_url = my_log.get_dut_console_log_link()
             
            data['Link'] = console_url[0]
            data['Display'] = console_url[0].split('/')[-1]
        except:
            logger.error("Unable to get DUT console info.")
        return data

    def get_logs_info(self):
        data = []
        my_log = log(Params.resource, Params.product, Params.scmlabel, Params.testbed, Params.user)

        my_log.copy_file_to_log_server(LOG_DIR)
        data.append({
            'Name': 'Test Command Log File',
            'Link': Params.server_log_location + SUITE_LOG_HTML_FILE,
            'Display': SUITE_LOG_HTML_FILE
        })

        data.append({
            'Name': 'Failed Cases Log File',
            'Link': Params.server_log_location + FAILED_SUITE_LOG_FILE,
            'Display': FAILED_SUITE_LOG_FILE
        })

        data.append({
            'Name': 'Test Command Line File',
            'Link': Params.server_log_location + SUITE_COMMAND_LINE_FILE,
            'Display': SUITE_COMMAND_LINE_FILE
        })

        data.append({
            'Name': 'PythonRunner File',
            'Link': Params.server_log_location + SUITE_PYTHON_FILE,
            'Display': SUITE_PYTHON_FILE
        })

        try:
            console_url = my_log.get_dut_console_log_link()

            data.append({
                'Name': 'DUT Console Logs',
                'Link': console_url[0],
                'Display': console_url[0].split('/')[-1]
            })
        except:
            data.append({
                'Name': 'DUT Console Logs',
                'Link': '',
                'Display': '',
            })            
        if QBS_JOBNUM != '1234':
            data.append({
                'Name': 'Stderr File',
                'Link': Params.server_log_location + SUITE_STDERR_FILE,
                'Display': SUITE_STDERR_FILE
            })
        if Params.system_log:
            try:
                system_file=glob.glob(f'{LOG_DIR}'+"/scsystemlogs_*")
                system_file=os.path.basename(system_file[0])
                data.append({
                    'Name': 'System Log File',
                    'Link': Params.server_log_location + system_file,
                    'Display': 'systemlogs'
                })
            except Exception as e:
                logger.error(e)

        return data

    def get_start_summary(self):
        self.ts_details = self.sa.get_testsuite_details(Params.path)
        Params.ts_display_name = self.ts_details['display_name']

        data = OrderedDict()
        data['rgname'] = Params.rgname
        # if Params.ts_display_name and Params.ts_actual_name != '': data['Testsuite Display Name'] = Params.ts_actual_name
        if Params.ts_display_name and Params.ts_display_name != '': data['Testsuite Display Name'] = Params.ts_display_name
        if Params.product and Params.product != '' : data['Product'] = Params.product
        if Params.scmlabel and Params.scmlabel != '': data['Software Version'] = Params.scmlabel
        if Params.testbed and Params.testbed != '': data['Test Bed'] = Params.testbed
        if Params.starttime and Params.starttime != '': data['Test Started at'] = Params.starttime
        if Params.qbsjobid and Params.qbsjobid != '': data['QBS Job ID'] = Params.qbsjobid
        if Params.setuptestbed and Params.setuptestbed != '': data['OpenStack Setup Test Bed'] = Params.setuptestbed
        if Params.setupjoblog and Params.setupjoblog != '': data['OpenStack Setup Job Log'] = Params.setupjoblog
        return data

    def get_execution_summary(self):
        # query reg_total_exec, reg_exec_time, and display_name based on path
       # ts_details = self.sa.get_testsuite_details(Params.path)
        Params.reg_total_exec = self.ts_details['testcases']
        Params.reg_exec_time = self.ts_details['exectime']
        Params.ts_display_name = self.ts_details['display_name']
        if 'topology_path' in self.ts_details.keys() and 'topology_link' in self.ts_details.keys():
            Params.ts_topology_path = self.ts_details['topology_path']
            Params.ts_topology_link = self.ts_details['topology_link']

        # calculate exec_time
        Params.exec_time = str(Params.finishtime - Params.starttime).split('.')[0]
        Params.starttime = Params.starttime.strftime('%Y-%m-%d %H:%M:%S')
        Params.finishtime = Params.finishtime.strftime('%Y-%m-%d %H:%M:%S')

        data = OrderedDict()
        
        data['rgname'] = Params.rgname
        if Params.product and Params.product != '' : data['Product'] = Params.product
        if Params.scmlabel and Params.scmlabel != '': data['Software Version'] = Params.scmlabel
        if Params.testbed and Params.testbed != '': data['Test Bed'] = Params.testbed
        if Params.starttime and Params.starttime != '': data['Test Started at'] = Params.starttime
        if Params.finishtime and Params.finishtime != '': data['Test Finished at'] = Params.finishtime
        if Params.reg_exec_time and Params.reg_exec_time != 0: data['Registered Execution Time'] = Params.reg_exec_time
        if Params.exec_time and Params.exec_time != 0: data['Actual Execution Time'] = Params.exec_time
        if Params.reg_total_exec and Params.reg_total_exec != 0: data['Registered Total Testcases'] = Params.reg_total_exec
        if Params.total_exec and Params.total_exec != 0: data['Actual Testcases Executed'] = Params.total_exec
        if Params.total_aptest and Params.total_aptest != 0: data['Results Uploaded to APTEST'] = Params.total_aptest
        if Params.ts_actual_name and Params.ts_actual_name != '': data['Testsuite Actual Name'] = Params.ts_actual_name
        if Params.ts_display_name and Params.ts_display_name != '': data['Testsuite Display Name'] = Params.ts_display_name
        if Params.log_location and Params.log_location != '': data['Local Log Dir'] = Params.log_location
        if Params.qbsjobid and Params.qbsjobid != '': data['QBS Job ID'] = Params.qbsjobid
        if Params.db_upload: data['Database Upload'] = Params.db_upload
        if Params.setuptestbed and Params.setuptestbed != '': data['OpenStack Setup Test Bed'] = Params.setuptestbed
        if Params.setupjoblog and Params.setupjoblog != '': data['OpenStack Setup Job Log'] = Params.setupjoblog
        if Params.ts_topology_path and Params.ts_topology_path != '': data['Testsuite Topology path'] = Params.ts_topology_path
        if Params.ts_topology_link and Params.ts_topology_link != '': data['Testsuite Topology git'] = Params.ts_topology_link
        data['Rerun Pass Count']=0
        data['Rerun Fail Count']=0
        for i in self.results:
            data['Rerun Pass Count'] +=i['rerun_pass_total']
            data['Rerun Fail Count'] += i['rerun_fail_total']
        Params.rerun_pass =data['Rerun Pass Count']
        Params.rerun_fail =data['Rerun Fail Count']    
        return data

    def get_result_summary(self):
        open_jira = 0
        for result in self.results:
            if result['uuid'].lower() == 'nontc':
                if result['result'].upper() == 'PASSED': Params.nontc_total_pass += 1 
                if result['result'].upper() == 'FAILED': Params.nontc_total_failures += 1 
                if result['result'].upper() == 'ERROR': Params.nontc_total_failures += 1 
                if result['result'].upper() == 'SKIPPED': Params.nontc_total_skip += 1 
                Params.nontc_total_run += 1
            else:
                if result['result'].upper() == 'PASSED': Params.total_pass += 1 
                if result['result'].upper() == 'FAILED': Params.total_failures += 1 
                if result['result'].upper() == 'ERROR': Params.nontc_total_failures += 1 
                if result['result'].upper() == 'SKIPPED': Params.total_skip += 1 
                Params.total_run += 1  
                if result['dts_jira_link']: open_jira += 1
        res_summary = [{
            'Name': 'Test Case Result',
            'Pass': str(Params.total_pass),
            'Fail': str(Params.total_failures),
#            'Error': str(Params.total_errors)
            'Skip': str(Params.total_skip)
        },
        {
            'Name': 'Non Test Case Result',
            'Pass': str(Params.nontc_total_pass),
            'Fail': str(Params.nontc_total_failures),
#            'Error': str(Params.nontc_total_errors)
            'Skip': str(Params.nontc_total_skip)
        },
        {
            'open_jira': open_jira,
        }
        ]
        return res_summary

    def parse_result_file(self):
        #aio_map=self.sa.get_aio_key_mapping()
        with open(SUITE_RES_FILE_WITH_PATH,'r') as result_file:
            reader = csv.DictReader(result_file)
            for row in reader:
                type = 'NonTC' if row['UUID'].lower() == 'nontc' or None else 'TestCase'

                self.results.append({
                    # 'title': row['ID'],
                    'title': '', #this key is for mouseover testcase name in mail
                    'result': row['RESULT'],
                    'starttime': row['STARTTIME'],
                    'endtime': row['ENDTIME'],
                    'uuid': row['UUID'],
                    'matrixid': 0,
                    'type': type,
                    'ftype': '',
                    'parameters': '',
                    'alias': '',
                    # 'filename': self.suite_name,
                    'filename':  row['ID'],
                    'log_link': '',
                    'dts_jira_link': '',
                    'failed_stage': [], #print these stage when a testcase failed
                    'scmlabel': Params.scmlabel,
                    'product':Params.product,
                })
                if self.results[-1]['type'] == 'TestCase' and row['UUID']:
                    self.results[-1]['type_link'] = 'https://testrail.eng.sonicwall.com/testrail/index.php?/cases/view/' + str(row['UUID']) 
                    try:
                        aio_project=Params.aio_map[row['UUID'].split('-')[0]]
                    except Exception as e:
                        aio_project=row['UUID'].split('-')[0]
                    if '-' in row['UUID']: 
                        self.results[-1]['type_link'] = f'https://sonicwall.atlassian.net/plugins/servlet/ac/com.kaanha.jira.tcms/aio-tcms-app-browse?ac.project.id={aio_project}&ac.page=case-details&ac.params={{"caseId":"' + str(row['UUID'])+'"}'
                        self.results[-1]['type_link'] = urllib.parse.quote(self.results[-1]['type_link'],safe=':/?&=')
                if not self.has_uuid and (row['UUID'] is not None and row['UUID'].lower() != 'nontc'):
                    self.has_uuid = True
                '''
                [{'title': 'Verify Web requests are forwarded to a Proxy Server located on the WAN', 'result': 'FAILED', 'starttime': '201]
                '''
                for failed_stages in Descriptions.teststage:
                    rerun_pass_total=0
                    rerun_fail_total=0
                    for inner_dict in failed_stages.values():
                        for status in inner_dict.values():
                            if '--> rerun FAILED' in status:
                                rerun_fail_total += 1
                            elif '--> rerun PASSED' in status:
                                rerun_pass_total += 1
                    self.results[-1]['rerun_fail_total']= rerun_fail_total
                    self.results[-1]['rerun_pass_total']= rerun_pass_total
                    if row['ID'] in failed_stages.keys():
                        for failed_stage in failed_stages[row['ID']]:
                            self.results[-1]['failed_stage'].append(failed_stage + ': ' + failed_stages[row['ID']][failed_stage])
                        break
                for description in Descriptions.testcase:
                    if row['ID'] in description.keys():
                        self.results[-1]['title'] = description[row['ID']]
                        break
                my_log = log(Params.resource, Params.product, Params.scmlabel, Params.testbed, Params.user)
                case_logfile=LOG_DIR + '/' +  TestcaseLog.log[row['ID']]
                case_htmlfile=re.sub(r'\.log','.html',case_logfile)
                try:
                    logger.info(case_logfile)
                    my_log.log_to_html(case_logfile,case_htmlfile)
                except Exception as e:
                    logger.error(e.args)
                self.results[-1]['log_link']= re.sub(r'\.log','.html',my_log.uploaddir_url + TestcaseLog.log[row['ID']])
                self.results[-1]['dts_jira_link'] = Params.dts_jira_link[row['ID']]
                if Params.trialrun:
                    self.results[-1]['ftype'] = 'TrialRun'
                elif self.results[-1]['dts_jira_link']:
                    self.results[-1]['ftype'] = 'Software'
                else:
                    self.results[-1]['ftype'] = 'Uncategorized'
                    
    def generate_failed_log(self):
        output_file = open(FAILED_SUITE_LOG_FILE_WITH_PATH, 'a')
        output_file.write(self.csv2log(SUITE_RES_FILE_WITH_PATH))
        output_file.write('\n'*3)
        output_file.write(self.fetch_failed_log())        

    def fetch_failed_log(self):
        failed_log = 'Failed Testcase Detailed Log'.center(108, '*') + '\n'*2
        total_log = open(SUITE_LOG_FILE_WITH_PATH).read()
        start = '########## STARTING CASE:'
        end = '########## Testcase.*?##########'
        pattern = re.compile((r'\[.*?\] \[.*?\] - ' + start+'.*?' + end), re.S)
        results = pattern.findall(total_log)
        for result in results:
            if re.search(r'FAILED  ##########', result):
                failed_log += result + '\n'
        return failed_log + '\n'
                
    def csv2log(self, file):
        csv = open(file)
        width1 = 60
        width2 = 48
        log = 'Complete TestSuite : ' + os.path.basename(self.suite_name) 
        log += '\n' + '='*len(log) + '\n'*2
        log += 'Testcase'.center(width1, ' ') + 'Status'.ljust(width2, ' ') + '\n'
        log += ''.center(width1+width2, '-') + '\n'
        for line in csv:
            (id, result, starttime, endtime, uuid) = line.split(',')
            if id == 'ID':
                continue
            log += id.ljust(width1, '-') + (result + ' ' + starttime + ' ' + endtime).ljust(width2, ' ') + '\n'
        return log

    def __del__(self):
        print('Your Logs are in ' + LOG_DIR)
        python_logger.close()
