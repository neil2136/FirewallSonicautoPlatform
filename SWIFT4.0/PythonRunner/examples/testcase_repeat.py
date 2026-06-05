from runner.utils.email_util import SendMail
from runner.unittest.setup import Test,repeat_class
from runner.utils.assertion import Assertion
import logging
#from runner.settings import Params
global a 
a=1
@repeat_class(3)
class TestEmailUtilInit(Test):
    uuid = "8A39711E-0464-11DE-860E-445A00F93527"
   # goto_teardown = True# if set, any method fail will cause goto teardown

    def test_1(self):
        print('-----test1----')
        to_users = "wgu@sonicwall.com"
        eu = SendMail(to_users)
        Assertion.assert_equal(eu.to_users, 'wgu@sonicwall.com', "ERR: ToUsers is not correct")

    def test_2(self):
        print('-----test2----')
        global a
        a +=1
        Assertion.assert_equal(a, 3, "ERR: ToUsers is not correct")

class TestAutomation(Test):
    uuid = "8A39711E-0464-11DE-860E-445A00F93527"
    def test_3(self):
        print('-----test3----')
        to_users = "cliu@sonicwall.com"
        Assertion.assert_equal(True, True, "ERR: ToUsers is not correct")
    def test_4(self):
        print('-----test4----')
        to_users = "cliu@sonicwall.com"
        eu = SendMail(to_users)
        Assertion.assert_equal(eu.to_users, 'wgu@sonicwall.com', "ERR: ToUsers is not correct")
