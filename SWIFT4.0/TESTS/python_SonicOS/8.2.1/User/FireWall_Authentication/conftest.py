import os
import sys


def pytest_addoption(parser):
    parser.addoption('--g_pytest', action="store", dest="pytest", default='False', required=False)
    parser.addoption('--g_pymarker', action="store", dest="pymarker", default="", required=False)
    parser.addoption('--g_pytcname', action="store", dest="pytcname", default="", required=False)