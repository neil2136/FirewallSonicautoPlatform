__author__ = "Pachiyappan Velan"

import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Users")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Users/testcases")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Log/Config_Auditing_CLI_Users/definition")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'init_conf_fw',
        'init_conf_pc',
        'Config_Auditing_CLI_Users.TC01_Add_Radius_Server_Via_CLI',
        'Config_Auditing_CLI_Users.TC02_Add_LDAP_Server_Via_CLI',
        'Config_Auditing_CLI_Users.TC03_Add_SSO_Agent_Via_CLI',
        'Config_Auditing_CLI_Users.TC04_Add_Tacacs_server_Via_CLI',
        'Config_Auditing_CLI_Users.TC05_Delete_Radius_server_Via_CLI',
        'Config_Auditing_CLI_Users.TC06_Delete_LDAP_server_Via_CLI',
        'Config_Auditing_CLI_Users.TC07_Delete_SSO_Agent_Via_CLI',
        'Config_Auditing_CLI_Users.TC08_Delete_Tacacs_server_Via_CLI',
        'Config_Auditing_CLI_Users.TC09_Add_SSO_Agent_Terminal_Service_Agents_Via_CLI',
        'Config_Auditing_CLI_Users.TC10_Add_SSO_Agent_Radius_Accounting_Client_Via_CLI',
        'Config_Auditing_CLI_Users.TC11_Add_SSO_Agent_Third_Party_API_Clients_Via_CLI',
        'Config_Auditing_CLI_Users.TC12_Add_Radius_Accounting_Servers_Via_CLI',
        'Config_Auditing_CLI_Users.TC13_Add_Tacacs_Accounting_Servers_Via_CLI',
        'Config_Auditing_CLI_Users.TC14_Add_Authentication_Partitions_Via_CLI',
        'Config_Auditing_CLI_Users.TC15_Add_Partition_Selection_Policies_Via_CLI',
        'Config_Auditing_CLI_Users.TC16_Add_Local_Users_Via_CLI',
        'Config_Auditing_CLI_Users.TC17_Delete_Local_Users_Via_CLI',
        'Config_Auditing_CLI_Users.TC18_Add_Local_Groups_Via_CLI',
        'Config_Auditing_CLI_Users.TC19_Add_Guest_Profiles_Via_CLI',
        'Config_Auditing_CLI_Users.TC20_Add_Guest_Accounts_Via_CLI',
        'Config_Auditing_CLI_Users.TC21_Generate_Guest_Accounts_Via_CLI',
        'Config_Auditing_CLI_Users.TC22_Exports_Guest_Accounts_Via_CLI',
        'Config_Auditing_CLI_Users.TC23_Delete_Guest_Accounts_Via_CLI',
        'Config_Auditing_CLI_Users.TC24_Logout_Users_Via_CLI',
        'Config_Auditing_CLI_Users.TC25_Logout_Guest_Users_Via_CLI',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
