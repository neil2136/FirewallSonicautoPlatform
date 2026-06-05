import unittest
import subprocess
from runner.settings import Params, logger,python_logger,OPENSTACK_SETUP,SETUPTB,QBS_JOBNUM,LOG_DIR
from runner.testrunner import Runner
import sys,os,re
from collections import OrderedDict

class UnittestSuite(Runner):
    def __init__(self, args, suite, to_users = None, cc_users = None, resultclass=None):
        super().__init__(args, suite, to_users, cc_users)
        self.resultclass = resultclass

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

    def run_and_parse_result(self,n):
        if int(Params.repeat_fail_testcase) <1:
            Params.repeat_fail_testcase =1
        elif int(Params.repeat_fail_testcase)>9:
            Params.repeat_fail_testcase=9
        if int(Params.repeat_testcase) <1:
            Params.repeat_testcase =1
        elif int(Params.repeat_testcase)>9:
            Params.repeat_testcase=9
        if int(Params.repeat_fail_testcase) !=1 and not SETUPTB:
            from unittestreport import TestRunner
            re_runner=TestRunner(suite=self.suite)
            results=re_runner.rerun_run(count=int(Params.repeat_fail_testcase)-1,interval=5)
            runner = unittest.TextTestRunner(verbosity=2, resultclass=self.resultclass)
        elif int(Params.repeat_testcase) !=1 and not SETUPTB:
            n=int(Params.repeat_testcase)
            if n !=1:
                new_testcases=self.get_test_names(self.suite)
                new_suite=list(OrderedDict.fromkeys(map(lambda x:'.'.join(x.split('.')[:-1]),new_testcases)))
                repeat_suite=[]
                for testcase in new_suite:
                    if 'TestRestoreDUT' in testcase or 'TestUploadFirmware' in testcase:
                        repeat_suite.append(testcase)
                    else:
                        repeat_suite.extend([testcase]*n)
                self.suite = unittest.TestLoader().loadTestsFromNames(repeat_suite)
            runner = unittest.TextTestRunner(verbosity=2, resultclass=self.resultclass)
            results = runner.run(self.suite)
        else:
            runner = unittest.TextTestRunner(verbosity=2, resultclass=self.resultclass)
            results = runner.run(self.suite)

        if QBS_JOBNUM != '1234' and not SETUPTB:
            python_logger.write(f'cp /tmp/stderr.log to {LOG_DIR}'+ '\n' )
            subprocess.Popen(['cp'] + ['/tmp/stderr.log'] + [LOG_DIR+'/'], stdout=subprocess.PIPE).communicate()[0]

        if re.search('python_SonicOS',Params.rgname,re.I) and Params.openstack and os.popen('hostname').read().split('-')[0] not in OPENSTACK_SETUP:
            sys.path.append(os.environ["PYTHON_COMMON_HOME"])
            sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
            testcases_list=['config.init_testbed.TestGetCoredump']
            if Params.retain==0 and QBS_JOBNUM != '1234':
                testcases_list.append('config.init_testbed.TestRestoreDUTByEnd')
            get_coredump=unittest.TestLoader().loadTestsFromNames(testcases_list)
            runner.run(get_coredump)



        # parse test result
        resultsString = str(results)
        resultArray = resultsString.split(" ")
        # Params.total_run = resultArray[1].split("=")[1]
        # Params.total_errors = resultArray[2].split("=")[1]
        # Params.total_failures = resultArray[3].split('>')[0].split("=")[1]
        # Params.total_pass = int(Params.total_run) - int(Params.total_failures) - int(Params.total_errors)
        #logger.info("<Run Testcase:" + str(Params.total_run) + ", Skipped: " + str(Params.total_skip) + ", Failures: " + str(Params.total_failures) + ">")
        #logger.info("<Run NonTC:" + str(Params.nontc_total_run) + ", Skipped: " + str(Params.nontc_total_skip) + ", Failures: " + str(Params.nontc_total_failures) + ">")
