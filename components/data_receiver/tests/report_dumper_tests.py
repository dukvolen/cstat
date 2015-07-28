# -*- coding: utf-8 -*-
#------------------------------------------------
# @brief        Tests for report_dumper class
# @author       Andrew Simine
# @copyright    Copyrighted by Andrew Simine
#
#------------------------------------------------
import unittest
import datetime
import json
import os
from common.exceptions.report_format import ReportFormatException
from components.data_receiver.report_dumper import ReportDumper

#------------------------------------------------
class TestReportDumper(unittest.TestCase):
    #--------------------------------------------
    def setUp(self):
        self.rdumper = ReportDumper()
        self.test_data = {}

    #--------------------------------------------
    def testCheckReportFile(self):
        return self.assertIsNotNone(self.rdumper.get_dump_file_name())

    #--------------------------------------------
    def testCheckFormat(self):
        # None test
        try:
            self.rdumper.check_format(None)
            return self.assertTrue(False, "Test for None doesn't work!")
        except ReportFormatException as e:
            print(e.message)

        self.test_data = {}

        # 'datetime' test
        try:
            self.rdumper.check_format(self.test_data)
            return self.assertTrue(False, "Test for 'datetime' doesn't work!")
        except ReportFormatException as e:
            print(e.message)
            self.test_data['datetime'] = datetime.datetime.now()

        # 'params' test
        try:
            self.rdumper.check_format(self.test_data)
            return self.assertTrue(False, "Test for 'params' doesn't work!")
        except ReportFormatException as e:
            print(e.message)
            self.test_data['params'] = []

        # 'params' size test
        param = {}
        self.test_data['params'].append(param)
        # 'params.category' test
        try:
            self.rdumper.check_format(self.test_data)
            return self.assertTrue(False, "Test for 'params.category' doesn't work!")
        except ReportFormatException as e:
            print(e.message)
            param['category'] = 'TestCategory'

        # 'params.param' test
        try:
            self.rdumper.check_format(self.test_data)
            return self.assertTrue(False, "Test for 'params.param' doesn't work!")
        except ReportFormatException as e:
            print(e.message)
            param['param'] = {}

        # 'params.param.name' test
        try:
            self.rdumper.check_format(self.test_data)
            return self.assertTrue(False, "Test for 'params.param.name' doesn't work!")
        except ReportFormatException as e:
            print(e.message)
            param['param']['name'] = 'testParam'

        # 'params.param.value' test
        try:
            self.rdumper.check_format(self.test_data)
            return self.assertTrue(False, "Test for 'params.param.value' doesn't work!")
        except ReportFormatException as e:
            print(e.message)
            param['param']['value'] = 'testValue'

        # final test
        try:
            self.rdumper.check_format(self.test_data)
        except Exception as e:
            return self.assertTrue(False, "Final test for json report doesn't work! \n {}".format(e.args[0]))

        print(self.test_data)

        return self.assertTrue(True, 'Test for checking format is successful!')

    #--------------------------------------------
    def testDumpReport(self):
        self.test_data = {}
        self.test_data['datetime'] = datetime.datetime.now()
        self.test_data['params'] = []
        param = {}
        param['category'] = 'TestCategory'
        param['param'] = {}
        param['param']['name'] = 'testName'
        param['param']['value'] = 'значение1'
        self.test_data['params'].append(param)

        param = {}
        param['param'] = {}
        param['param']['name'] = 'testName2'
        param['param']['value'] = 12
        self.test_data['params'].append(param)

        param = {}
        param['param'] = {}
        param['param']['name'] = 'Параметр1'
        param['param']['value'] = [12, 23, 34]
        self.test_data['params'].append(param)

        param = {}
        param['param'] = {}
        param['param']['name'] = 'testName3'
        param['param']['value'] = ['12', '23', '34']
        self.test_data['params'].append(param)

        json_obj = self.test_data.copy()
        json_obj['datetime'] = self.test_data['datetime'].strftime("%Y-%m-%d %H:%M:%S")
        print('Test JSON:')
        print(json_obj)

        return self.assertTrue(self.rdumper.dump_report(self.test_data))

    #--------------------------------------------
    def testLoadReport(self):
        full_file_name = ''
        for root, folders, files in os.walk(self.rdumper.dump_folder):
            for file in files:
                if(file.find('.rep')>0):
                    full_file_name = os.path.join(root, file)
                    break
                continue
            break

        print('filename: {}'.format(full_file_name))
        if(not os.path.exists(full_file_name)):
            return self.assertTrue(False, "Can't load report for testing ...")

        retval = self.rdumper.load_report(full_file_name)
        print(self.rdumper.json_data)

        return self.assertTrue(retval, "Loading report...")

#------------------------------------------------
def suite():
    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.makeSuite(TestReportDumper))
    return testsuite

#------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
