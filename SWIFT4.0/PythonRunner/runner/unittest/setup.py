import unittest
import datetime,pytz
import time
import csv
import os
import re
import sys
import contextlib
import subprocess
import inspect
import functools
import traceback
from runner.settings import LOGGING, SUITE_RES_FILE_WITH_PATH, Descriptions, TestcaseLog, LOG_DIR, Params, logger, python_logger
from runner.utils.myjira import fetch_jira_status
from runner.utils.assertion import Assertion
from runner.utils.sonicauto import SonicAuto
from runner.utils.log import log

FAILED_TESTCASE = []
teardown_flag = False
self_value = None
sa = SonicAuto()
global id2result
id2result={}
def skip_if_fail_method(depend=None):
    import functools
    def wraper_func(test_func):
        @functools.wraps(test_func)
        def inner_func(self):
            if depend == test_func.__name__:
                raise ValueError("{} cannot depend on itself".format(depend))
            failures = str([fail[0] for fail in self._outcome.result.failures])
            errors = str([error[0] for error in self._outcome.result.errors])
            skipped = str([skip[0] for skip in self._outcome.result.skipped])
            flag = (depend in failures) or (depend in errors) or (depend in skipped)
            test = unittest.skipIf(flag, '{} SKIPPED as {} failed or error or skipped'.format(test_func.__name__, depend))(test_func)
            return test(self)
        return inner_func
    return wraper_func

def skip_unless_fail_method(depend=None):
    import functools
    def wraper_func(test_func):
        @functools.wraps(test_func)
        def inner_func(self):
            if depend == test_func.__name__:
                raise ValueError("{} cannot depend on itself".format(depend))
            failures = str([fail[0] for fail in self._outcome.result.failures])
            errors = str([error[0] for error in self._outcome.result.errors])
            skipped = str([skip[0] for skip in self._outcome.result.skipped])
            flag = (depend in failures) or (depend in errors) or (depend in skipped)
            test = unittest.skipUnless(flag, '{} SKIPPED as {} not failed or error or skipped'.format(test_func.__name__, depend))(test_func)
            return test(self)
        return inner_func
    return wraper_func
# def skip(reason):
#     """
#     Unconditionally skip a test.
#     """
#     def decorator(test_item):
#         if not isinstance(test_item, type):
#             @functools.wraps(test_item)
#             def skip_wrapper(*args, **kwargs):
#                 raise SkipTest(reason)
#             test_item = skip_wrapper

#         test_item.__unittest_skip__ = True
#         test_item.__unittest_skip_why__ = reason
#         return test_item
#     return decorator

def skip_if_dts(dts):
    import functools
    def wraper_func(newcls):
        @functools.wraps(newcls)
        def inner_func():
            if newcls.__name__ in dts:
                flag = True
                newcls.start_time_d = datetime.datetime.now(pytz.timezone('UTC'))
                milliseconds = (newcls.start_time_d.microsecond // 1000) * 1000
                newcls.start_time_d= newcls.start_time_d.replace(microsecond=milliseconds)
                
                newcls.start_time=newcls.start_time_d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                output_file = open(SUITE_RES_FILE_WITH_PATH, 'a', newline='')
                a = csv.writer(output_file, delimiter=',')
                a.writerow([newcls.__name__, 'SKIPPED', newcls.start_time, newcls.start_time, '----'])
                output_file.close()
                logger.info("########## Testcase: " + newcls.__name__ + ' '*3 + 'SKIPPED' + "  ##########" + '\n'*2)
            else:
                flag = False
            test = unittest.skipIf(flag, "########## Testcase: {} SKIPPED due to dts ##########\n\n".format(newcls.__name__))(newcls)
            return test()
        return inner_func
    return wraper_func

def skip_if_fail_class(depend=None):
    import functools
    def wraper_func(test_func):
        @functools.wraps(test_func)
        def inner_func(self):
            if depend in FAILED_TESTCASE:
                flag = True
            else:
                flag = False
            test = unittest.skipIf(flag, "########## Teststage: {} SKIPPED due to {} failed ##########\n\n".format(test_func.__name__, depend))(test_func)
            return test()
        return inner_func
    return wraper_func

def repeat_method(repeat, sleep=1):
    import functools
    import traceback
    import sys
    
    def wraper_func(testfunc):
        @functools.wraps(testfunc)
        def wrapper(self):
            global teardown_flag
            last_exception = None
            full_error_info = ""
            
            for i in range(repeat):
                logger.info(f'Run for {i+1}/{repeat} time')
                ori_result = Test.test_case_result
                
                try:
                    re = testfunc(self)
                    return re
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    
                    full_error_info = error_msg
                    last_exception = e
                    
                    logger.error(error_msg)
                    
                    self.failure = True
                    Test.tearDown(self)
                    time.sleep(sleep)
                    Test.test_case_result = ori_result
                    teardown_flag = False
                    
                    if i != repeat-1:
                        if hasattr(Descriptions, 'teststage') and Descriptions.teststage:
                            if Descriptions.teststage[-1]:
                                Descriptions.teststage[-1][self.test_case_id].pop(self.test_method_id, None)
                        Test.setUp(self)
            
            raise last_exception
                
        return wrapper
    return wraper_func

# class repeat_class(repeat):
#     import functools
#     def wraper_cls(test_cls):
#         @functools.wraps(test_cls)
#         def inner_cls():
#             for i in range(repeat):
#                 logger.info(f'Run for {i} time')
#                 try:
#                     re = test_cls()

#                     logger.info('-------------------')
#                     logger.info(Test.test_case_result)
#                     return re
#                 except Exception as e:
#                     # self.failure = True
#                     print('####################')
#                     Test.tearDownClass()
#                     Test.setUpClass()
#             raise Exception
#         return inner_cls
#     return wraper_cls
def repeat_class(repeat,sleep=1,func_prefix="test"):
    """
    :param repeat:repeat time 
    :param func_prefix: when decorator classï¼Œcan be used to determine which methods will be rerun
    :return: wrapped class or wrapped function
    """

    def decorator(func_or_cls):
        if inspect.isfunction(func_or_cls):
            @functools.wraps(func_or_cls)
            def wrapper(*args, **kwargs):
                n =1 
                while n <= repeat:
                    logger.info(f'run for {n} time...')
                    try:
                        n += 1
                        ori_result = Test.test_case_result
                        func_or_cls(*args, **kwargs)
                        return
                    except Exception:  
                        if n <= repeat:
                            trace = sys.exc_info()
                            traceback_info = str()
                            for trace_line in traceback.format_exception(trace[0], trace[1], trace[2], 3):
                                traceback_info += trace_line
                            args[0].failure =True
                            args[0].tearDown()
                            time.sleep(sleep)
                            Test.test_case_result = ori_result
                            if n != repeat:
                                logger.info('ccc')
                                logger.info(Descriptions.teststage)
                                Descriptions.teststage[-1][args[0].test_case_id].pop(args[0].test_method_id)
                            args[0].setUp()
                        else:
                            raise

            return wrapper
        elif inspect.isclass(func_or_cls):
            for name, func in list(func_or_cls.__dict__.items()):
                if inspect.isfunction(func) and name.startswith(func_prefix):
                    setattr(func_or_cls, name, decorator(func))
            return func_or_cls
        else:
            raise AttributeError

    return decorator

#winni
def parse_single_result_file(result):
    if result['type'] == 'TestCase' and result['uuid']:
        result['type_link'] = 'https://testrail.eng.sonicwall.com/testrail/index.php?/cases/view/' + str(result['uuid']) 
        try:
            aio_project=Params.aio_map[result['uuid'].split('-')[0]]
        except Exception as e:
            aio_project=result['uuid'].split('-')[0]
        if '-' in result['uuid']:
            result['type_link'] = f'https://sonicwall.atlassian.net/plugins/servlet/ac/com.kaanha.jira.tcms/aio-tcms-app-browse?ac.project.id={aio_project}&ac.page=case-details&ac.params={{"caseId":"' + str(result['uuid'])+'"}'
    # if result['uuid'] is not None and result['uuid'].lower() != 'nontc':
    #     self.has_uuid = True
    '''
    [{'title': 'Verify Web requests are forwarded to a Proxy Server located on the WAN', 'result': 'FAILED', 'starttime': '201]
    '''
    # for failed_stages in Descriptions.teststage:
    #     if row['ID'] in failed_stages.keys():
    #         for failed_stage in failed_stages[row['ID']]:
    #             result['failed_stage'].append(failed_stage + ': ' + failed_stages[row['ID']][failed_stage])
    #         break
    for description in Descriptions.testcase:
        if result['filename'] in description.keys():
            result['title'] = description[result['filename']]
            break
    my_log = log(Params.resource, Params.product, Params.scmlabel, Params.testbed, Params.user)

    result['log_link']= re.sub(r'\.log','.html',my_log.uploaddir_url + TestcaseLog.log[result['filename']])
    # result['dts_jira_link'] = Params.dts_jira_link[row['ID']]
    if Params.trialrun:
        result['ftype'] = 'TrialRun'
    elif result['dts_jira_link']:
        result['ftype'] = 'Software'
    else:
        result['ftype'] = 'Uncategorized'  
    for i in range(0,5):
        sa = SonicAuto()  
        rc = sa.update_result(Params.job_requestid,result)
        if rc == 'Result got saved successfully':
            python_logger.write(f"Result for {result['filename']} saved to sonicauto successfully.")
            break
        time.sleep(5)
        logger.info('Try again to upload result to sonicauto...')


class NumbersTestResult(unittest.TextTestResult):
    def addSubTest(self, test, subtest, outcome):
        super(NumbersTestResult, self).addSubTest(test, subtest, outcome)
        # add to total number of tests run
        test.subTestteardown(outcome, test.subTestName[test.subTestCount], test.subTestUUID[test.subTestCount])
        self.testsRun += 1
        test.subTestCount += 1

class Test(unittest.TestCase):
    def __init__(self, methodName='runTest', **param):
        super().__init__(methodName)
        self.test_case_name = unittest.TestCase.id(self)
        self.test_case_name_string = str(self.test_case_name)
        self.splitted_name = self.test_case_name_string.split(".")
        self.splitted_name_len = self.splitted_name.__len__()
        self.test_case_id = self.splitted_name[self.splitted_name_len-2]
        self.test_method_id = self.splitted_name[self.splitted_name_len-1]
        self.param = param

    @staticmethod    
    def parametrize(testcase_klass, **kwargs):    
        """ Create a suite containing all tests taken from the given  
            subclass, passing them the parameter 'kwargs'.  
        """    
        testloader = unittest.TestLoader()    
        testnames = testloader.getTestCaseNames(testcase_klass)    
        suite = unittest.TestSuite()    
        for name in testnames:    
            suite.addTest(testcase_klass(name, **kwargs))    
        return suite    
    
    @classmethod
    def setUpClass(cls):
        global id2result
        id2result={}
        global rerun_times
        rerun_times={}
        Test.test_case_result = 'PASSED'
        Test.goto_teardown = False
        Test.is_dts_jira = False
        Test.dts_jira_open = False
        
        cls.start_time_d = datetime.datetime.now(pytz.timezone('UTC'))
        milliseconds = (cls.start_time_d.microsecond // 1000) * 1000
        cls.start_time_d=cls.start_time_d.replace(microsecond=milliseconds)

        cls.start_time = cls.start_time_d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        cls.test_case_id = cls.__name__
        Params.dts_jira_link[cls.test_case_id] = ''
        Descriptions.description = cls.test_case_id
        python_logger.write('Entering Testcase: ' + cls.test_case_id + ' at ' + time.asctime( time.localtime(time.time())) + '\n')
        case_log_dir = LOG_DIR + '/' + cls.test_case_id
        # case_log = case_log_dir + '/' + cls.test_case_id + '.log'
        relative_case_log = cls.test_case_id + '/' + cls.test_case_id + '.log'
        os.path.exists(case_log_dir) or os.makedirs(case_log_dir)
        Descriptions.teststage.append({cls.test_case_id: {}})  
        TestcaseLog.log[cls.test_case_id] = relative_case_log
        cls.handler = LOGGING.FileHandler(case_log_dir + '/' + cls.test_case_id + '.log', mode='w')
        formatter1 = LOGGING.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s')
        if Params.log_level == 'DEBUG2':
            formatter1 = LOGGING.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] - %(message)s')
        cls.handler.setFormatter(formatter1)
        cls.handler.setLevel(Params.log_level)
        logger.addHandler(cls.handler)
        logger.info("########## STARTING CASE: " + cls.test_case_id + " ##########" + "\n")

    @classmethod
    def tearDownClass(cls):
        global teardown_flag
        global self_value
        global id2result
        if hasattr(cls, '_teardown_completed'):
            return
        if 'FAILED' not in id2result.values():
            Test.test_case_result= 'PASSED'
        cls.uuid = Test.uuid
        Descriptions.testcase.append({cls.test_case_id: Descriptions.description})
        if teardown_flag and cls.test_case_id != 'TestGetCoredump' and cls.test_case_id != 'TestRestoreDUTByEnd':
            try:
                logger.debug("teardown_flag set, skipping testcase.")
                if Test.test_case_result != 'FAILED':
                    Test.test_case_result = 'SKIPPED'
                    cls.tearDown(self_value)
            except Exception as e:
                logger.debug("Failed to call tearDown, exception : " + str(e))
        # elif Test.dts_jira_open:
        #     Test.test_case_result = 'SKIPPED'
        #     cls.tearDown(self_value)

            # logger.debug("self.nonTCfailure value in teardown : " + str(teardown_flag))

        # if not cls.uuid or cls.uuid != 'NonTC':
        #     try:
        #         Descriptions.testcase.append({Test.test_case_id: Test.description})
        #     except Exception as e:
        #         logger.warning('description not defined when this is a testcase.')
        # append the result to csv file
        cls.end_time_d = datetime.datetime.now(pytz.timezone('UTC'))
        milliseconds = (cls.end_time_d.microsecond // 1000) * 1000
        cls.end_time_d=cls.end_time_d.replace(microsecond=milliseconds)
        cls.end_time = cls.end_time_d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        output_file = open(SUITE_RES_FILE_WITH_PATH, 'a', newline='')
        a = csv.writer(output_file, delimiter=',')
        a.writerow([cls.test_case_id, Test.test_case_result, cls.start_time, cls.end_time, cls.uuid])
        output_file.close()
        logger.info("########## Testcase: " + cls.test_case_id + ' '*3 + Test.test_case_result + "  ##########" + '\n'*2)
        logger.removeHandler(cls.handler)
        python_logger.write('UUID=' + cls.uuid + '\n')
        python_logger.write('Exiting Testcase: ' + cls.test_case_id + ' at ' + time.asctime( time.localtime(time.time())) + ' ... Result: ' + Test.test_case_result + '\n'*2)
        if Test.test_case_result == 'FAILED':
            FAILED_TESTCASE.append(cls.test_case_id)
        if (Test.test_case_result == "FAILED" or (Test.dts_jira_open and Test.test_case_result == "SKIPPED")) and Test.goto_teardown:
            logger.info("teardown the whole testsuite.\n")
            teardown_flag = True

        #winni
        python_logger.write('Save result to sonicauto...')
        result= {
            # 'title': row['ID'],
            'job_requestid': Params.job_requestid,
            'title': '', #this key is for mouseover testcase name in mail
            'result': Test.test_case_result,
            'starttime': cls.start_time,
            'endtime': cls.end_time,
            'uuid': cls.uuid,
            'matrixid': 0,
            'type': 'NonTC' if cls.uuid.lower() == 'nontc' or None else 'TestCase',
            'ftype': '',
            # 'parameters': '',
            # 'alias': '',
            # 'filename': self.suite_name,
            'filename':  cls.test_case_id,
            'log_link': '',
            'dts_jira_link':Params.dts_jira_link[cls.test_case_id],
            'failed_stage': [], #print these stage when a testcase failed
            # 'scmlabel': Params.scmlabel,
            # 'product':Params.product,
        }
        if cls.test_case_id != 'TestGetCoredump' and cls.test_case_id != 'TestRestoreDUTByEnd' and Params.db_upload != 'No':
            parse_single_result_file(result)
        cls._teardown_completed = True

    def setUp(self):
        global teardown_flag
        global self_value
        global id2result
        if self.test_method_id not in rerun_times:
            rerun_times[self.test_method_id]=1
        else:
            rerun_times[self.test_method_id]+=1
        if self.test_method_id in id2result.keys():
            id2result.pop(self.test_method_id)
        Assertion(self.test_case_id, self.test_method_id)
        self_value = self
        self.failure = False

        try:
            Descriptions.description = self.test_case_id + ' - ' + self.description
        except:
            Descriptions.description = self.test_case_id
                    
        python_logger.write('Entering stage: ' + self.test_method_id + ' at ' + time.asctime( time.localtime(time.time()))+ '\n')
        logger.info("########## STARTING METHOD: " + self.test_method_id + " ##########")
        Test.test_case_id = self.test_case_id
        if teardown_flag and 'get_coredump_by_end' not in self.test_method_id and 'restore_dut_by_end' not in self.test_method_id :
            logger.debug("In setup, testcase with goto_teardown set has failed. Skip all the test cases")
            Test.uuid = self.uuid
            raise unittest.SkipTest("skip test")
        if hasattr(self,'jira') and self.jira:
            Test.uuid = self.uuid
            self.status = fetch_jira_status(self.jira)
            if self.status != 'In Test' and self.status != 'Done' and self.status:
                self.dts_jira_open = True
                Test.dts_jira_open = self.dts_jira_open
                logger.info(f"This testcase has a jira {self.jira}")
                # raise unittest.SkipTest(f"skip test as there is a jira {self.jira}")

    def tearDown(self):
        global teardown_flag
        global id2result
        Test.uuid = self.uuid
        Test.goto_teardown = self.goto_teardown
        Test.subTestCount = 0
        try:
            if re.search(r'^\d+$', self.dts):
                Params.dts_jira_link[self.test_case_id] = 'https://sonicdts.eng.sonicwall.com/update_bug.asp?jobid=' + str(self.dts)  
        except:
            try:
                if re.search(r'^\w*-\d*$', self.jira) and self.status != 'In Test' and self.status != 'Done':
                    Params.dts_jira_link[self.test_case_id] = 'https://sonicwall.atlassian.net/browse/' + str(self.jira).upper()
            except:
                pass
                 
        # fetch the test result according to
        # http://stackoverflow.com/questions/4414234/getting-pythons-unittest-results-in-a-teardown-method
        result = self.defaultTestResult()
        errors = []
        failures = []
        skipped = []

        if hasattr(self, '_outcome') and hasattr(self._outcome, 'errors'):
            try:
                self._feedErrorsToResult(result, self._outcome.errors)
            except Exception as e:
                logger.debug("Failed to call - self._feedErrorsToResult(result, self._outcome.errors) ")
                logger.debug("Exception : " + str(e))
            self.error = self.list2reason(result.errors)
            self.failure = self.list2reason(result.failures) if not self.failure else True
            self.skipped = self.list2reason(result.skipped)
        elif hasattr(self, '_outcome') and hasattr(self._outcome, 'result'):
            result_obj = self._outcome.result
            errors = getattr(result_obj, 'errors', [])
            failures = getattr(result_obj, 'failures', [])
            skipped = getattr(result_obj, 'skipped', [])
            self.error = self.list2reason(errors)
            self.failure = self.list2reason(failures) if not self.failure else True
            self.skipped = self.list2reason(skipped)
            logger.debug("Using _outcome.result")
        elif hasattr(self, '_outcomeForDoCleanups') :
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
            self.error = self.list2reason(result.errors)
            self.failure = self.list2reason(result.failures) if not self.failure else True
            self.skipped = self.list2reason(result.skipped)
        else:
            pass

        ok = not self.error and not self.failure
        test_result = None

##########
        if teardown_flag and 'get_coredump_by_end' not in self.test_method_id and 'restore_dut_by_end' not in self.test_method_id :
            logger.debug("The result is set to skipped")
            logger.info("########## Method: " + str(self.test_method_id) + ' Skipped' + "  ##########" + '\n')
            test_result = "SKIPPED"
            if self.uuid != 'NonTC':
                try:
                    logger.debug("Main test case SKIPPED")
                    if hasattr(self, 'subTestName') and len(self.subTestName) > 0:
                        logger.debug("Main TC SKIPPED : len(self.subTestName) : " + str(len(self.subTestName)))

                    subTestUUID_count2 = 0
                    if hasattr(self, 'subTestName') and len(self.subTestName) > 0:
                        logger.debug("Main test case SKIPPED and subtests are present")
                        logger.debug("So marking them as skipped")
                        self.subTest_skipped_flag = True
                        logger.debug("self.subTest_skipped_flag : " + str(self.subTest_skipped_flag))

                        for n in self.subTestName:
                            logger.debug("subTestUUID_count : " + str(subTestUUID_count2))
                            logger.debug("##################### SKIPPING SUBTEST CASE NAME: " + str(n) +
                                               " ########################")
                            # self.subTest(name=n)
                            # Fetching UUID
                            try:
                                logger.debug("self.subTestUUID : " + str(self.subTestUUID))
                                logger.debug("self.subTestName[subTestUUID_count] : " +
                                                   str(self.subTestName[subTestUUID_count2]))
                                logger.debug("self.subTestUUID.keys() : " + str(self.subTestUUID.keys()))
                                if self.subTestName[subTestUUID_count2] in self.subTestUUID.keys():
                                    uuid = self.subTestUUID[self.subTestName[subTestUUID_count2]]
                                    logger.debug("UUID found : " + str(uuid))
                                else:
                                    uuid = ""
                                    logger.debug("UUID not found, hence UUID is empty")
                            except Exception as e:
                                logger.debug("UUID could not be fetched, hence UUID is empty")
                                logger.debug("Exception : " + str(e))
                                uuid = ""

                            # Fetching JIRA
                            try:
                                logger.debug("self.subTestJIRA : " + str(self.subTestJIRA))
                                if self.subTestName[subTestUUID_count2] in self.subTestJIRA.keys():
                                    JIRA = self.subTestJIRA[self.subTestName[subTestUUID_count2]]
                                    logger.debug("JIRA found : " + str(JIRA))
                                else:
                                    JIRA = ""
                                    logger.debug("JIRA not found, hence JIRA is empty")
                            except Exception as e:
                                logger.debug("JIRA could not be fetched, hence JIRA is empty")
                                logger.debug("Exception : " + str(e))
                                JIRA = ""

                            self.subTestteardown('Skipped', n, uuid, JIRA)

                            TestcaseLog.log[self.subTestName[subTestUUID_count2]] = self.log_link
                            Descriptions.teststage.append({self.subTestName[subTestUUID_count2]: {}})
                            Descriptions.testcase.append(
                                {self.subTestName[subTestUUID_count2]: self.subTestName[subTestUUID_count2]})

                            subTestUUID_count2 += 1

                except Exception as e:
                    logger.debug("Exception raised while marking subtest case as skipped for failed Non TC")
                    logger.debug("This might be because there are no subtest cases for this main test case")
                    logger.debug("Exception is : " + str(e))
####
        # elif hasattr(self, 'dts_jira_open') and self.dts_jira_open:
        #     logger.info("########## Method: " + str(self.test_method_id) + ' Skipped' + "  ##########" + '\n')
        #     test_result = "SKIPPED"
        elif not ok:
            typ, text = ('ERROR', self.error) if self.error else ('FAIL', self.failure)

            if str(typ)== "FAIL" or str(typ)== "ERROR":
                logger.info("########## Method: " + self.test_method_id + ' Failed' + "  ##########" + '\n')
                test_result = "FAILED"
                if self.goto_teardown and rerun_times[self.test_method_id] == Params.repeat_fail_testcase:
                    teardown_flag = True                    
        elif self.skipped:
            logger.info("########## Method: " + self.test_method_id + ' Skipped' + "  ##########" + '\n')
        else:
            logger.info("########## Method: " + self.test_method_id + ' Passed' + "  ##########" + '\n')
            test_result = "PASSED"
    
        id2result[self.test_method_id]= test_result
        if test_result == 'FAILED':
            {self.test_method_id: test_result}
            Test.test_case_result = 'FAILED'
            try:
                if not Descriptions.teststage[-1][self.test_case_id]:
                    Descriptions.teststage[-1][self.test_case_id][self.test_method_id]= 'failed'         
            except Exception as e:
                logger.warning('Warn: {}'.format(e))
        if rerun_times[self.test_method_id] != 1:
            if test_result == 'FAILED': 
                Descriptions.teststage[-1][self.test_case_id][self.test_method_id] += '--> rerun ' + test_result
            elif test_result == 'PASSED': 
                Descriptions.teststage[-1][self.test_case_id][self.test_method_id] = '--> rerun ' + test_result
        Test.test_case_id = self.test_case_id
        python_logger.write('Exiting stage: ' + self.test_method_id + ' at ' + time.asctime( time.localtime(time.time()) ) + '... Result: ' + test_result + '\n')


    def subTest(self, *args, **kwargs):
        python_logger.write('Entering Sub-Testcase: ' + kwargs['name'] + ' at ' + time.asctime( time.localtime(time.time()))+'\n')
        try:
            logger.info("########## STARTING SUBTEST CASE: " + kwargs['name'] + " ##########")
            super().subTest(msg=None, **kwargs)
        except AttributeError:
            super().subTest = contextlib.contextmanager(lambda *a, **kw: (yield))
        return super().subTest(*args, **kwargs)

    def subTestteardown(self, outcome, test_case_id, uuid):
        if outcome is not None:
            logger.error(test_case_id + ": FAILED")
            self.test_case_result = "FAILED"
        else:
            logger.info(test_case_id + ": PASSED")
            self.test_case_result = "PASSED"
        cls.end_time_d = datetime.datetime.now(pytz.timezone('UTC'))
        milliseconds = (cls.end_time_d.microsecond // 1000) * 1000
        cls.end_time_d=cls.end_time_d.replace(microsecond=milliseconds)
        cls.end_time_d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        output_file = open(SUITE_RES_FILE_WITH_PATH, 'a', newline='')
        a = csv.writer(output_file, delimiter=',')
        a.writerow([test_case_id, self.test_case_result, self.start_time, self.end_time, uuid])
        output_file.close()
        logger.info("########## SubTest Case: " + test_case_id + ' ' * 3 + self.test_case_result + "  ##########" + '\n' * 3)
        python_logger.write('Exting Sub-Testcase: ' + test_case_id + ' at ' + time.asctime( time.localtime(time.time())) + ' ... Result: ' + self.test_case_result + '\n')

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]


# class StopTests(Exception):
#     """
# Raise this exception in a test to stop the test run.

#     """
#        pass
