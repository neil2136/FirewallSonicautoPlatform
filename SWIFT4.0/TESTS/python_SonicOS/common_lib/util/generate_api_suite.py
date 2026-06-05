import os
import json
import logging
import time
import sys
import argparse
import shutil
from collections import OrderedDict


class Auto_Generate_Testsutie():
    def __init__(self, file=None, log=None, user=''):
        self.file = file
        self.log = log 
        self.user = user
        self.json_output = ''
        LOGGING = logging
        LOGGING.basicConfig(
            format='[%(asctime)s] [%(levelname)s] - %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler(log),
                logging.StreamHandler(stream=sys.stdout)
            ]
        )
        self.logger = LOGGING.getLogger(__name__)        

    def read_template(self):
        global logger
        TESTSUITE = 'Default_API'

        try:
            with open(self.file,'r') as f:
                self.json_output = json.load(f)
        except Exception as e:
            self.logger.error("The template's format has issue: " +e)
        return self.json_output

    def get_testsuite_name(self):
        testsuite_name = 'Default_API'
        try:
            testsuite_name = self.json_output['testsuite']
        except Exception as e:
            self.logger.error('No testsuite specified in template, use default')    
        return testsuite_name

    def get_register_status(self):
        register = 'off'
        try:
            register = self.json_output['register']
        except Exception as e:
            self.logger.error('No register specified in template, will not register firewall.')    
        return register

    def get_testsuite_json(self):
        testsuite_json = {}
        try:
            testsuite_json = self.json_output['json']
        except:
            self.logger.error('No json body in template, finish testing.')
        return testsuite_json

    def get_branch(self):
        branches = ['7.0.1']
        try:
            branches = self.json_output['branch'].replace(" ", "").split(',')
            print('-------')
            print(branches)
        except Exception as e:
            self.logger.error("No branch specified, use default 7.0.1")
        return list(set(branches))

        
    def make_testsuite_dir(self):
        testsuite = self.get_testsuite_name()
        branches = self.get_branch()
        register = self.get_register_status()
        dir_name = '/DEV_TESTS/python_SonicOS/' + branches[0] + '/REST-API/' + testsuite
        sh_dir_name = '/DEV_TESTS_SH/python_SonicOS/' + branches[0] + '/REST-API/'
        if os.path.exists(dir_name):
            self.logger.warning(f'{dir_name} exist, will cover it.')
            shutil.rmtree(dir_name)
        else:
            self.logger.info(f'Make new dir {dir_name}')
        os.makedirs(dir_name)
        os.makedirs(dir_name + '/testsuites')
        os.makedirs(dir_name + '/testcases')
        testsuite_name = testsuite.lower() + '_suite.py'
        abs_testsuite_name = dir_name + '/testsuites/' + testsuite_name
        testcase_name = testsuite.lower() + '.py'
        abs_testcase_name = dir_name + '/testcases/' + testcase_name
        testcase_suffix = testsuite.lower()
        self.logger.info(f'new testsuite file {testsuite_name}')
        f = open(abs_testsuite_name, mode='w')
        f.write(f'import sys\n')
        f.write(f'import os\n')
        f.write(f'import unittest\n')
        f.write(f'from runner.unittest.suite import UnittestSuite\n')
        f.write(f'sys.path.append(os.environ["PYTHON_COMMON_HOME"])\n')
        f.write(f'sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/REST-API")\n')
        f.write(f'sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/REST-API/" + "{testsuite}/testcases")\n\n\n')
        f.write(f'def suite():\n')
        f.write(f'    testcases_list = [\n')
        f.write(f'        "config.init_testbed.TestRestoreDUT",\n')
        f.write(f'        "config.init_testbed.TestUploadFirmware",\n')
        if self.get_register_status() == 'on':
            f.write(f'        "definition.conf_fw.TestConfigFWRegister",\n')
        f.write(f'        "{testcase_suffix}",\n')
        f.write(f'    ]\n')
        f.write(f'    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)\n')
        f.write(f'    return suites\n')
        f.write(f'\n\n')
        f.write(f'if __name__ == "__main__":\n')
        f.write(f'    to_users = "{self.user}"\n')
        f.write(f'    st = UnittestSuite(sys.argv, suite(), to_users=to_users)\n')
        f.write(f'    st.run()\n')
        f.close()
        rc = os.path.exists(abs_testsuite_name)
        if not rc:
            self.logger.error("generate testsuite file failed.")
            return False
        self.logger.info(f'new testcase file {testcase_name}')
        f_case = open(abs_testcase_name, mode='w')
        f_case.write('import sys\n')
        f_case.write('import json\n')
        f_case.write('import os\n')
        f_case.write('import paramunittest\n')
        f_case.write('from collections import OrderedDict\n')
        f_case.write('from nose_parameterized import parameterized\n')
        f_case.write('from runner.unittest.setup import Test\n')
        f_case.write('from runner.settings import Params, logger\n')
        f_case.write('from runner.utils.assertion import Assertion\n')
        f_case.write('sys.path.append(os.environ["PYTHON_COMMON_HOME"])\n')
        f_case.write('from utm import Firewall\n\n')
        f_case.write('FIREWALL="192.168.168.168"\n')
        f_case.write('fw_api = Firewall(FIREWALL, user="admin", password="password", supported_config_mode="api")\n\n\n')
        f_case.write('@paramunittest.parametrized(\n')
        json_data = self.get_testsuite_json()
        for id in json_data:
            value = '{' + '"case_id": "' + id + '", "data":' + json.dumps(json_data[id]["data"]) + ',"url":"' + json_data[id]["url"] + '", "method":"' + json_data[id]["method"] + '"'
            value = value.replace('false','False').replace('true','True')
            if 'header' in json_data[id]:
                header =eval(json.dumps(json_data[id]["header"]))
                value += ', "header":"' + f'OrderedDict({header})' + '"'
            if 'match' in json_data[id]:
                value += ', "match":' + json.dumps(json_data[id]["match"]) 
            value += "}"
            if id != len(json_data):
                value += ','
            value = value.replace('false','False').replace('true','True').replace('null','None')
            f_case.write(f'    {value}\n')
        f_case.write(')\n\n')
        f_case.write('class Test_API_ACTION(Test):\n')
        f_case.write('    def setParameters(self, case_id, data, url, method, match="", header=fw_api.headers1):\n')
        f_case.write('        self.case_id = case_id\n')
        f_case.write('        self.data = data\n')
        f_case.write('        self.url = url\n')
        f_case.write('        self.method = method\n')
        f_case.write('        self.uuid = method\n')
        f_case.write('        self.match = match\n')
        f_case.write('        self.header = header\n\n')
        f_case.write('    def test_post_or_put_or_delete(self):\n')
        f_case.write('        logger.info(f"Try to {self.method}")\n')
        f_case.write('        logger.info("Json data: ")\n')
        f_case.write('        logger.info(f"{self.data}")\n')
        f_case.write('        if self.method.lower() == "put":\n')
        f_case.write(f'           rc=fw_api.api_put(self.url, data=self.data)\n')
        f_case.write('        elif self.method.lower() == "post":\n')
        f_case.write(f'           rc=fw_api.api_post(self.url, data=self.data)\n')
        f_case.write('        elif self.method.lower() == "delete":\n')
        f_case.write(f'           rc=fw_api.api_delete(self.url, data=self.data)\n')
        f_case.write('        elif self.method.lower() == "get":\n')
        f_case.write(f'           rc=json.dumps(fw_api.api_get(self.url))\n')
        f_case.write('        else:\n')
        f_case.write(f'           logger.error("Please specify api method to one of put,post,delete,get.")\n')
        f_case.write('           rc = False\n')
        f_case.write('        if self.method.lower() == "get":\n')
        f_case.write('            Assertion.assert_regular(rc, self.match, f"err:api {self.method} failed.")\n')
        f_case.write('        else:\n')
        f_case.write('            Assertion.assert_equal(rc, True, f"err:api {self.method} failed.")\n')
        f_case.close()

        self.logger.info(f'cp -rf {dir_name} {sh_dir_name}')
        os.popen(f'cp -rf {dir_name} {sh_dir_name}')
        total_suite = abs_testsuite_name
        if len(branches) > 1:
            src= '/DEV_TESTS/python_SonicOS/' + branches[0] + '/REST-API/' + testsuite
            for branch in branches[1:]:
                dst = '/DEV_TESTS/python_SonicOS/' + branch + '/REST-API/'
                sh_dst = '/DEV_TESTS_SH/python_SonicOS/' + branch + '/REST-API/'
                self.logger.info(f'cp -rf {src} {dst}')
                os.popen(f'cp -rf {src} {dst}')
                self.logger.info(f'cp -rf {src} {sh_dst}')
                os.popen(f'cp -rf {src} {sh_dst}')
                total_suite += ',' + abs_testsuite_name.replace(branches[0],branch)
        self.logger.info(f'The suite location:{total_suite}')
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto generate API testsuite.')
    parser.add_argument('-file', '--file', type=str, dest='file', required=False, help='json file path')
    parser.add_argument('-log', '--log', type=str, dest='log', required=False, help='log file path')
    parser.add_argument('-user', '--user', type=str, dest='user', required=False, help='user name')

    known, unknown = parser.parse_known_args(sys.argv[1:])
    val = vars(known)

    auto = Auto_Generate_Testsutie(file=val['file'], log=val['log'], user=val['user'])

    data = auto.read_template()
    if not data:
        exit(1)
    auto.make_testsuite_dir()
    exit(0)
        
