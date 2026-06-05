# Import required libraries and packages
import sys
import argparse
from platform import system

# Getting client platform information
client_platform = system()
client_platform = 'osx' if client_platform == 'Darwin' else 'win' if client_platform == 'Windows' else \
    client_platform.lower()

# Defining global variables
global logger_level, testbed_id, testbed, release_input, release, openstack, browser_type, to_user_email, cc_user_email, TEST_TYPE, PYTEST, PYMARKER, PYTCS

# Parse the arguments
parser = argparse.ArgumentParser(description="Parse test suite arguments")

parser.add_argument('--g_pytest', action="store", dest="pytest", default='local', required=False)
parser.add_argument('--g_pymarker', action="store", dest="pymarker", default="", required=False)
parser.add_argument('--g_py_tcs', action="store", nargs='+', dest="py_tcs", default="", required=False)

# assign the parsed argument
args_str = ' '.join(sys.argv[1:])
temp_args = args_str.replace('-var ', '').replace('G_', '--g_').lower().replace('-rv ', '--').split(' ')
known, unkown = parser.parse_known_args(temp_args)
val = vars(known)


PYTEST = str(val['pytest']).upper()
PYMARKER = val['pymarker']
PYTCS = val['py_tcs']

# Setting pytest params
pytest_params = " --g_pytest=" + PYTEST

if PYTEST == "TRUE":
    # appending system path of SWIFT4.0 to look for modules
    sys.path.append(r"\\10.5.64.10\SWIFT4.0")
else:
    # Import local pytestrunner
    from pytest_resources.local_pytestrunner.log import *
    from pytest_resources.local_pytestrunner.assertion import *
    from pytest_resources.local_pytestrunner.setup import *
    from pytest_resources.local_pytestrunner.csv import *
    from pytest_resources.get_tc_based_on_trid import *

    # Set logger
    logger = logging.getLogger('all_logs')

