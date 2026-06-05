from examples.wgu_test import TestEmailUtilInit
from examples.wgu_test import TestAutomation
from runner.unittest.suite import UnittestSuite
import unittest
import sys

def suite():
    test_cases = ['TestEmailUtilInit','TestAutomation']
   # test_cases = ['TestEmailUtilInit']
    suites = unittest.TestSuite()
    i = 0
    testcases = []
    while i < test_cases.__len__():
        testcases.extend(['wgu_test.' + test_cases[i]])
        i += 1
    print(testcases)
    suites=unittest.TestLoader().loadTestsFromNames(testcases)
    return suites


if __name__ == '__main__':
#    to_users = 'yaji@sonicwall.com'
    cc_users = 'wgu@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),cc_users=cc_users)
    st.run()
