import unittest
from examples.testcase_repeat import TestEmailUtilInit

from examples.testcase_repeat import TestAutomation
from runner.unittest.suite import UnittestSuite
import sys

def suite():
    test_cases = ['TestAutomation','TestEmailUtilInit']
   # test_cases = ['TestEmailUtilInit']
    suites = unittest.TestSuite()
    i = 0
    testcases = []
    while i < test_cases.__len__():
        testcases.extend(['testcase_repeat.' + test_cases[i]])
        i += 1
    print(testcases)
    suites=unittest.TestLoader().loadTestsFromNames(testcases)
    return suites


if __name__ == '__main__':
#    to_users = 'yaji@sonicwall.com'
    cc_users = 'wgu@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),cc_users=cc_users)
    st.run(2)
