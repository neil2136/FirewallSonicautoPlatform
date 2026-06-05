from runner.utils.email_util import SendMail
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion


class TestEmailUtilInit(Test):
    uuid = "8A39711E-0464-11DE-860E-445A00F93527"
    #uuid = "NonTC"
    jira = 'GEN7-19212'
    def runTest(self):
        to_users = "echen@sonicwall.com"
        eu = SendMail(to_users)
        Assertion.assert_equal(eu.to_users, 'echen@sonicwall.com', "ERR: ToUsers is not correct")
