# This file contains common code that is executed at the beginning and at the end of the each test case.
# Also it contains logic to create {suite_name}.csv

import os
import sys
import csv
import time
import subprocess
import shutil
import platform

from pytest_resources.common_require import *


logger = logging.getLogger('all_logs')

logger.info("opening " + pytest_result_csv + " file for writing test case results")
output_file = open(pytest_result_csv, 'w', newline='')
output_writer = csv.writer(output_file)
output_writer.writerow(['ID', 'RESULT', 'start_time', 'end_time', 'TestRail_UUID'])
output_file.close()
logger.info("Loaded suite")


class PytestRunner():
    def __init__(self, args, path, params, to_users=None, cc_users=None, resultclass=None, pytest=None):
        logger.info(" *****  RUNNING LOCAL PYTESTRUNNER  ***** ")
        self.params = params
        self.path = path

    def run(self):
        try:

            if (str(sys.argv[0]).startswith("C:")) or (platform.system() == 'Windows'):
                sys_path = str(sys.argv[0]).replace("\\", "/")
            else:
                sys_path = str(sys.argv[0])
            current_path = os.path.dirname(sys_path).split("/")
            self.initial_path = ""
            for i in current_path:
                if i == "scripts":
                    break
                if self.initial_path == "":
                    self.initial_path = self.initial_path + i
                else:
                    self.initial_path = self.initial_path + "/" + i
            if (str(sys.argv[0]).startswith("C:")) or (platform.system() == 'Windows'):
                self.initial_path = self.initial_path + "/"
            else:
                self.initial_path = "/" + self.initial_path + "/"

                # self.initial_path = root_dir + "/"

            logger.info("current path " + str(current_path))
            logger.info("Initial path " + str(self.initial_path))

            self.testcasepath = str(self.path).split(".py")

            # if pytest marker is passed
            if PYMARKER != '':
                logger.info(" --- Running testcases with marker value as --- " + str(PYMARKER))
                pytest_cmd = "python3 -m pytest -s " + self.initial_path + self.testcasepath[0] + ".py -k" + " " + \
                             self.testcasepath[1] + " " + self.params
                logger.info(" Pytest command to be called : " + str(pytest_cmd))
                subprocess.call(pytest_cmd, shell=True)

            # if individual testcase needs to be run
            elif PYTCS != '':
                logger.info(" --- Running individual selected testcase with names --- " + str(PYTCS))
                pytest_cmd = "python3 -m pytest -s " + self.initial_path + self.testcasepath[0] + ".py -k" + " " + \
                             self.testcasepath[1] + " " + self.params
                logger.info(" Pytest command to be called : " + str(pytest_cmd))
                subprocess.call(pytest_cmd, shell=True)

            # if entire file needs to run
            else:
                logger.info(" --- Running the full testcase file with path --- " + str(self.path))
                pytest_cmd = "python -m pytest " + self.initial_path + self.testcasepath[0] + ".py" + " " + self.params
                logger.info(" Pytest command to be called : " + str(pytest_cmd))
                subprocess.call(pytest_cmd, shell=True)
            move_log_file()
        except Exception as e:
            logger.info("**** EXCEPTION WHILE RUNNING THE SUITE USING PYTESTRUNNER **** ")
            logger.info("**** EXCEPTION : " + str(e) + " ****")
            move_log_file()


def move_log_file():

    try:
        source_folder = logs_dir_path
        destination_folder = destination_log_path
        logger.info(" Source file path to be copied : " + str(source_folder))
        logger.info(" Destination file path to copy logs :" + str(destination_folder))
        status_copy_files = shutil.copytree(source_folder, destination_folder)
        logger.info(" Log files copied successfully to location : " + str(status_copy_files))
        shutil.rmtree(source_folder, ignore_errors=True)
        logger.info(" *** Successfully deleted Source directory *** ")
    except Exception as e:
        logger.info("Exception while moving local log file and deleting source file : " + str(e))


class Test2(unittest.TestCase):
    def __init__(self, methodName='runTest', param=None, **kwargs):
        super().__init__(methodName)
        self._resultForDoCleanups = None
        self.test_case_name = unittest.TestCase.id(self)
        self.test_case_name_string = str(self.test_case_name)
        self.splitted_name = self.test_case_name_string.split(".")
        self.splitted_name_len = self.splitted_name.__len__()
        self.test_case_id = self.splitted_name[self.splitted_name_len - 2]
        self.test_method_id = self.splitted_name[self.splitted_name_len - 1]
        self.kwargs = kwargs

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
        cls.start_time = str(datetime.datetime.now().replace(microsecond=0))
        cls.test_case_id = cls.__name__
        Test2.test_case_result = 'PASSED'
        logger.info("########## STARTING CASE: " + cls.test_case_id + " ##########")

    @classmethod
    def tearDownClass(cls):
        cls.uuid = Test2.uuid
        # append the result to csv file
        cls.end_time = str(datetime.datetime.now().replace(microsecond=0))
        output_file = open(pytest_result_csv, 'a', newline='')
        a = csv.writer(output_file, delimiter=',')
        a.writerow([Test2.test_case_id, Test2.test_case_result, cls.start_time, cls.end_time, cls.uuid])
        output_file.close()
        logger.info("########## Testcase: " + Test2.test_case_id + ' ' * 3 + Test2.test_case_result + "  ##########" + '\n' * 2)
        print("########## Testcase: " + Test2.test_case_id + ' ' * 3 + Test2.test_case_result + "  ##########" + '\n' * 2)

    def setUp(self):
        Test2.uuid = self.uuid
        Test2.test_case_id = self.test_case_id
        logger.info("\n\n########## STARTING CASE: " + self.test_case_id + " ##########\n")

    def tearDown(self):
        Test2.uuid = self.uuid
        Test2.subTestCount = 0
        # fetch the test result according to
        # http://stackoverflow.com/questions/4414234/getting-pythons-unittest-results-in-a-teardown-method
        if hasattr(self, '_outcome.errors'):
            result = self.defaultTestResult()
            # self._feedErrorsToResult(result, self._outcome.errors)
        else:
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure

        test_result = None
        if not ok:
            typ, text = ('ERROR', error) if error else ('FAIL', failure)

            if str(typ) == "FAIL" or str(typ) == "ERROR":
                logger.info(self.test_method_id + ": Failed")
                test_result = "FAILED"
        else:
            logger.info(self.test_method_id + ": Passed")
            test_result = "PASSED"

        if test_result == 'FAILED':
            Test2.test_case_result = 'FAILED'
        logger.info("#######################################@@@@@@@@: ", test_result)
        Test2.test_case_id = self.test_case_id
        # # calculate the total time taken for test case execution
        # total_time_in_seconds = time.time() - self.start_time
        # total_time1 = str(datetime.timedelta(seconds=total_time_in_seconds))
        # total_time2 = total_time1.split(".")
        # total_time3 = total_time2[0]
        #
        # # append the result to csv file
        # output_file = open(result_csv, 'a', newline='')
        # a = csv.writer(output_file, delimiter=',')
        # logger.info("updating " + result_csv + " file with the test result " + test_result +
        #        " for the test case: " + test_case_id)
        # a.writerow([test_case_id, test_result, total_time3, uuid])
        # output_file.close()

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

