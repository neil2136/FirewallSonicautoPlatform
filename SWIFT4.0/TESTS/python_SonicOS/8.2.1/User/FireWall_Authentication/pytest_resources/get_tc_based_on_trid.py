__author__ = 'Syed Maaz'

import os
import sys
import json
import linecache
import re
import platform

# to get root path and differentiate between windows and linux path
if str(sys.argv[0]).startswith("C:") or str(sys.argv[0]).startswith("C:"):
    sys_path = str(sys.argv[0]).replace("\\", "/")
else:
    sys_path = str(sys.argv[0])
current_path = os.path.dirname(sys_path).split("/")
root_dir = ""
for i in current_path:
    if i == "scripts":
        break

root_dir = os.sep.join(str(__file__).split(os.sep)[0:-4]) + os.sep

filename = root_dir + r"User/FireWall_Authentication/pytest_resources/pytest_marker.json"
suite_name_to_tc_path = root_dir + r"User/FireWall_Authentication/pytest_resources/pytest_testcase_path.json"


# Get TC file path using suitename
def get_tc_file_path(suite_name):
    file = open(suite_name_to_tc_path)
    data = json.load(file)
    file.close()
    if suite_name in data:
        return data[suite_name]
    else:
        return None


# Check if tc file has the trid or not
def check_file_for_trid(py_file, trid):
    with open(py_file) as f:
        if trid in f.read():
            return True

    return False


# Get line number of the tc class/function
def get_line_number(phrase, file_name):
    with open(file_name) as f:
        for i, line in enumerate(f, 1):
            if phrase in line:
                return i


# Split and get only the TC name by removing unwanted text
def get_testcase_name(line, file_name):
    line_content = linecache.getline(file_name, line)
    if line_content.startswith("class"):
        tcname = str(line_content).split()
        tc_split = str(tcname[1]).split('(')
        tc = tc_split[0]
        return tc
    else:
        return None


# Formatting TC names based on pytest requirements
def make_tc_name_from_list(tc_list, length):
    sys_platform = platform.system()
    consolidated_tc = ''
    for i in range(length):
        if i < length - 1:
            consolidated_tc += tc_list[i] + ' ' + 'or' + ' '
        else:
            consolidated_tc += tc_list[i]
    if sys_platform == "Windows":
        consolidate = "\"" + consolidated_tc + "\""
    else:
        consolidate = "'" + consolidated_tc + "'"
    return consolidate


# The main function that is used to call for getting TC based on test type/marker
def get_tc_based_on_markers(suite_name, test_type):
    list_tc = []
    py_file = get_tc_file_path(suite_name)
    # py_file = "api/" + py_file
    print(py_file)
    # check if NonTC is present in the TC file
    if check_file_for_nontc(py_file):
        non_tc = get_nontc_name(py_file)
        list_tc += non_tc
    else:
        list_tc = []
    f = open(filename)
    data = json.load(f)
    f.close()
    suite_data = data[test_type][suite_name]
    py_list_tc = get_tc(py_file, suite_data, list_tc)
    # py_list_tc = py_list_tc.strip("api/")
    return py_list_tc


def get_tc(py_file, suite_data, list_tc):
    length_testtype = len(suite_data)

    for trid in range(length_testtype):
        if check_file_for_trid(py_file, suite_data[trid]):
            line = get_line_number(suite_data[trid], py_file)
            line_content = get_testcase_name(line, py_file)
            if line_content:
                list_tc.append(line_content)
    final_tc_list = make_tc_name_from_list(list_tc, len(list_tc))
    py_file += final_tc_list
    return py_file


# Check if TC file has keyword as NonTc
def check_file_for_nontc(py_file):
    phrase = 'NonTC'
    with open(py_file) as f:
        # with open(py_file, encoding='utf-8') as f:
        # with open(py_file, encoding='latin-1') as f:
        if phrase in f.read():
            return True
    return False


# Get nontc name based on class name
def get_nontc_name(file_name):
    list_nontc = []
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("class test_NonTC"):
                m = re.search(r'(class test_NonTC.*)', line)
                if m:
                    full_name = str(m.group(1)).split()
                    non_tc_name = str(full_name[1]).split('(')
                    list_nontc.append(non_tc_name[0])
    return list_nontc


def get_tc_based_on_trid(suite_name, list_trid):
    new_list = []
    for word in list_trid:
        new_list.extend(word.split(","))
    print(new_list)
    list_tc = []
    py_file = get_tc_file_path(suite_name)
    # py_file = "api/" + py_file

    # check if NonTC is present in the TC file
    if check_file_for_nontc(py_file):
        non_tc = get_nontc_name(py_file)
        list_tc += non_tc
    else:
        list_tc = []
    py_tc_list = get_tc(py_file, new_list, list_tc)
    # py_tc_list = py_tc_list.strip("api/")
    return py_tc_list
