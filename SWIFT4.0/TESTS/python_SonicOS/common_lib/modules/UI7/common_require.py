import argparse
import base64
import binascii
import copy
import hashlib
import hmac
import json
import pprint
import math
import os
import re
import requests
import socket
import socket
import ssl
import sys
import time
import warnings
import yaml
import traceback
import subprocess
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from pyvirtualdisplay import Display
from os import path
from random import randint
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import unquote
from collections import OrderedDict

warnings.simplefilter("ignore", requests.packages.urllib3.exceptions.InsecureRequestWarning)
warnings.simplefilter("ignore", ResourceWarning)

from runner.settings import Params
global test_type, testbed_id, openstack, FW_MODEL_LEVEL
# parsing command line argument.
browser_type        = str(Params.browser_type)
test_type           = str(Params.test_type)
testbed_id          = str(Params.testbed)
logger_level        = str(Params.log_level)
openstack           = str(Params.openstack)

from runner.settings import logger
from runner.utils.assertion import Assertion
from modules.UI7.common_requirement import *

from modules.UI7.ui_wrapper import *
from modules.UI7.ui_helper import *
from modules.UI7.navigation import *
from modules.UI7.administration import *
from modules.UI7.safemode_ui import *
from modules.UI7.address_objects import *
from modules.UI7.schedule_objects import *
from modules.UI7.diagnostics import *
from modules.UI7.UbootUpgrade_Use_Prebuild import *
#from modules.UI7.network_dns import *
from modules.UI7.system_time import *
from modules.UI7.dhcp_objects import *
#from modules.UI7.highavailability_status import *
#from modules.UI7.highavailability_settings import *
#from modules.UI7.highavailability_monitoring import *
from modules.UI7.client_ssl import *
#from modules.UI7.server_ssl import *
from modules.UI7.l2tp_server import *
# from modules.UI7.dhcp_over_vpn import *

from modules.UI7.firewall_ui import *
