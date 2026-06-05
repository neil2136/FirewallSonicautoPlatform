from examples.skip_jira import TestEmailUtilInit,TestAutomation
from runner.unittest.suite import UnittestSuite
import unittest
import sys

def suite():
    suites = unittest.TestLoader().loadTestsFromNames(['examples.skip_jira.TestEmailUtilInit','examples.skip_jira.TestAutomation'])
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite(), to_users, cc_users)
    st.run()
