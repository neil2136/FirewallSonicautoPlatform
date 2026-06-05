import sys
import requests
sys.path.append('/DEV_TESTS/PythonRunner')
import argparse
from sqlalchemy import create_engine
from sqlalchemy import or_,and_
from sqlalchemy.orm import sessionmaker
from runner.utils.models import TestSuiteDetail, User, Platform, TestSuite, TestBed, JobRequest, TestResult, ApTestSessionGroup, TestFailure, FailureType
from urllib import parse


class FetchTestcaseNum:

    def __init__(self,suite_name, job_id):
        self.suite_name = suite_name
        self.job_id = job_id
        SONICAUTO_CONN = "postgres://sonicauto:%s@10.203.15.9:5432/sonicauto" % parse.unquote('s0nicw@ll')
        self.session = sessionmaker(create_engine(SONICAUTO_CONN))()

    def get_testsuite_case_info(self):
        self.get_test_result()

    def get_job_request_id(self):
        try:
            job_request = self.session.query(JobRequest).filter(JobRequest.qbsjobid == self.job_id)
        except Exception as e:
            print(f'not able to get job request id for {self.job_id}')
            print(e)
            return False
        return job_request[0].job_requestid

    def get_test_result(self):
        self.job_request_id = self.get_job_request_id()
        if self.job_request_id:
            try:
                test_result = self.session.query(TestResult).filter(TestResult.job_requestid == self.job_request_id)
            except Exception as e:
                print(f'not able to get test result for {self.job_request_id}' )
                return False
            total = 0
            testcase_num = 0
            for i in test_result:
                if test_result[total].type == 'TestCase':
                    print(test_result[total].title)
                    testcase_num += 1
                total += 1
            return test_result
            # for index in test_result:
        return False

    # def __del__(self):
    #     self.session.close()

class FetchTestcase:
    def __init__(self, suite_path,  summary_log_url='',action=''):
        self.suite_path = suite_path
        self.action = action
        self.summary_log = summary_log_url
        SONICAUTO_CONN = "postgres://sonicauto:%s@10.203.15.12:5432/sonicauto" % parse.unquote('s0nicw@ll')
        self.session = sessionmaker(create_engine(SONICAUTO_CONN))()

    def get_testcase_detail(self):
        if self.summary_log.endswith('csv'):
            response = requests.get(self.summary_log)
            logs = response.content.decode('utf-8').split('\r\n')
            suite_id = self.get_suite_id()
            if (self.action.lower() == 'add'):
                for result in logs[1:-1]:
                    result_seg = result.split(',')
                    if result_seg[-1] != 'NonTC' and not None:
                        testsuite_detail = TestSuiteDetail()
                        testsuite_detail.tc_name = result_seg[0]
                        testsuite_detail.suiteid = suite_id
                        testsuite_detail.uuid = result_seg[-1]
                        testsuite_detail.tc_status = True
                        self.session.add(testsuite_detail)
                        self.session.commit()
                        self.session.refresh(testsuite_detail)
            elif (self.action.lower() == 'edit'):
                testsuite_detail = TestSuiteDetail()
                ori_testcase_db = self.session.query(TestSuiteDetail).filter(TestSuiteDetail.suiteid == self.get_suite_id())
                ori_testcase_num = 0
                ori_testcase = []
                for i in ori_testcase_db:
                    ori_testcase.append(ori_testcase_db[ori_testcase_num].tc_name)
                    ori_testcase_num += 1
                new_testcase = []  
                uuid_map = {}
                for result in logs[1:-1]:
                    result_seg = result.split(',')
                    if result_seg[-1] != 'NonTC' and not None:
                        new_testcase.append(result_seg[0])
                        uuid_map[result_seg[0]]= result_seg[-1]
                for new_testcase_single in set(new_testcase)-set(ori_testcase):
                    testsuite_detail = TestSuiteDetail()
                    testsuite_detail.tc_name = new_testcase_single
                    testsuite_detail.suiteid = suite_id
                    testsuite_detail.uuid = uuid_map[new_testcase_single]
                    testsuite_detail.tc_status = True
                    self.session.add(testsuite_detail)
                    self.session.commit()
                    self.session.refresh(testsuite_detail)     
                for testcase in set(ori_testcase)-set(new_testcase):
                    ori_testcase_single = ori_testcase_db.filter(and_(TestSuiteDetail.tc_name == testcase))
                    ori_testcase_single[0].tc_status = False         
                    self.session.commit()
            return True
        else:
            print('Only support csv file.')
            return False
            
    def get_suite_id(self):
        try:
            suites = self.session.query(TestSuite).filter(TestSuite.path == self.suite_path)
            return suites[0].testsuiteid
        except Exception as e:
            print(f"Not able to get suite id with error {e.args}")
            return ''

    def __del__(self):
        self.session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch testsuite testcase name and add to test_suite_detail table.')
    parser.add_argument('-suitepath', '--suitepath', type=str, dest='suitepath', required=True, help='suite path, like: //depot/SQA/SWIFT4.0/TESTS/Application/GMS')
    parser.add_argument('-log', '--log', type=str, dest='log', required=True, help='result summary log url, like: http://10.5.64.10/buildtestlogs/TZ570-PROTOTYPE/7.0.0-P354/VTB912/kskarkera/kskarkera_VTB912_1596062820/root_pythonrunner_0/summary.csv')
    parser.add_argument('-action', '--action', type=str, dest='action', required=True, help='add or edit. add for first time')
     
    known, unknown = parser.parse_known_args(sys.argv[1:])
    val = vars(known)
    ft = FetchTestcase(val['suitepath'], val['log'], val['action'])
    ft.get_testcase_detail()

