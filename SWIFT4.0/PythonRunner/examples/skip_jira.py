from runner.utils.email import SendMail
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
import logging
#from runner.settings import Params
class TestEmailUtilInit(Test):
    uuid = "8A39711E-0464-11DE-860E-445A00F93527"
    jira = 'GEN7-19212'
    def test_1(self):
        print('-----test1----')
        to_users = "wgu@sonicwall.com"
        eu = SendMail(to_users)
        Assertion.assert_equal(eu.to_users, 'wgu@sonicwall.com', "ERR: ToUsers is not correct")

    def test_2(self):
        # self.goto_teardown=True#if set, this method fail will cause go to teardown
        print('-----test2----')
        Assertion.assert_equal(1, 2, "ERR: ToUsers is not correct")


class TestAutomation(Test):
    uuid = "8A39711E-0464-11DE-860E-445A00F93527"
    def test_3(self):
        print('-----test3----')
        Assertion.assert_equal(True, True, "ERR: ToUsers is not correct")
        
    def test_4(self):
        print('-----test4----')
        to_users = "wgu@sonicwall.com"
        eu = SendMail(to_users)
        Assertion.assert_equal(eu.to_users, 'wgu@sonicwall.com', "ERR: ToUsers is not correct")
