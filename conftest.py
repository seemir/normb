# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import tesults
import os
from _pytest.runner import runtestprotocol

# The data variable holds test results and tesults target information, at the end of test run
# it is uploaded to tesults for reporting.
data = {
    'target': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjMyY2VkNzhjLTI1NmQtNDcwZS04NGYwL'
              'WI2MTRkMzc1NjliYi0xNTU3NjYyODgwNDQyIiwiZXhwIjo0MTAyNDQ0ODAwMDAwLCJ2ZXIiOiIwIiwi'
              'c2VzIjoiODY3MjhlZDEtOGM5Yi00NjFhLThiZTQtOWQzNjU2NDcwMjI1IiwidHlwZSI6InQifQ.tJNY'
              'dBVwgKPjINJTtGqJS0349JtepV7ngAHqZ0KYPZ8',
    'results': {'cases': []}
}


# Converts pytest test outcome to a tesults friendly result (for example pytest uses 'passed',
# tesults uses 'pass')
def tesults_friendly_fesult(outcome):
    if outcome == 'passed':
        return 'pass'
    elif outcome == 'failed':
        return 'fail'
    else:
        return 'unknown'


# Extracts test failure reason
def reason_for_failure(report):
    if report.outcome == 'passed':
        return ''
    else:
        return report.longreprtext


def params_for_test(item):
    param_keys = item.get_marker('parametrize')
    if param_keys:
        param_keys = param_keys.args[0]
        params = {}
        values = item.name.split('[')
        if len(values) > 1:
            values = values[1]
            values = values[:-1]  # removes ']'
            values = values.split("-")  # values now separated
        else:
            return None
        for key in param_keys:
            if len(values) > 0:
                params[key] = values.pop(0)
        return params
    else:
        return None


def files_for_test(item):
    files = []
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        "path-to-test-generated-files", item.name)
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                files.append(os.path.join(path, file))
    return files


# A pytest hook, called by pytest automatically - used to extract test case data and append
# it to the data global variable defined above.
def pytest_runtest_protocol(item, nextitem):
    global data
    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.when == 'call':
            testcase = {
                'name': item.name,
                'result': tesults_friendly_fesult(report.outcome),
                'suite': str(item.parent),
                'desc': item.name,
                'reason': reason_for_failure(report)
            }
            files = files_for_test(item)
            if len(files) > 0:
                testcase['files'] = files
            params = params_for_test(item)
            if params:
                testcase['params'] = params
                testname = item.name.split('[')
                if len(testname) > 1:
                    testcase['name'] = testname[0]
            param_desc = item.get_marker('description')
            if param_desc:
                testcase['desc'] = param_desc.args[0]
            data['results']['cases'].append(testcase)
    return True


# A pytest hook, called by pytest automatically - used to upload test results to tesults.
def pytest_unconfigure(config):
    global data
    print('-----Tesults output-----')
    if len(data['results']['cases']) > 0:
        print('data: ' + str(data))
        ret = tesults.results(data)
        print('success: ' + str(ret['success']))
        print('message: ' + str(ret['message']))
        print('warnings: ' + str(ret['warnings']))
        print('errors: ' + str(ret['errors']))
    else:
        print('No test results.')
