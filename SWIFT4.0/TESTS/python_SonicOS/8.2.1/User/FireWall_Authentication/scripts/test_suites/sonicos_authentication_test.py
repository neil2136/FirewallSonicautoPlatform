# Author: Supin Shetty
# Date: 11/04/2024

import sys
import os

root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
suite_absolute_path = (scriptPath.split(os.sep))
for i in range(suite_absolute_path.index('scripts') - 1, len(suite_absolute_path) - 1):
    root = root + "../"
os.chdir(root)
dir = os.path.abspath(os.curdir)
sys.path.append(dir)

from pytest_resources.common_require import *

if __name__ == '__main__':
    to_users = "sshetty@sonicwall.com"
    cc_users = "sshetty@sonicwall.com"
    # Suitename which matches in testcasepath.json and pytest_marker.json files
    suite_name = "sonicos_authentication_test"

    if PYMARKER != '':
        print(PYMARKER)
        tc_path = get_tc_based_on_markers(suite_name, PYMARKER)
        print(tc_path)
        st = PytestRunner(sys.argv, tc_path, pytest_params, to_users, cc_users, pytest=True)
        st.run()
    elif PYTCS != '':
        print(PYTCS)
        tc_path = get_tc_based_on_trid(suite_name, PYTCS)
        st = PytestRunner(sys.argv, tc_path, pytest_params, to_users, cc_users, pytest=True)
        st.run()
    else:
        tc_path = get_tc_file_path(suite_name)
        print(tc_path)
        st = PytestRunner(sys.argv, tc_path, pytest_params, to_users, cc_users, pytest=True)
        st.run()

