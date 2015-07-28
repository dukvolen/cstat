#!/bin/python
# -*- coding: utf-8 -*-
#------------------------------------------------
#  @brief       Class for checking json format and saving to specified folder
#  @author      Andrew Simine
#  @copyright   Copyrighted by Andrew Simine
#
#------------------------------------------------
import os
import json
import datetime
import base64
import codecs
import uuid
from common.exceptions.report_format import ReportFormatException

#------------------------------------------------
class ReportDumper():
    '''   Template of JSON report
            test_data = {'datetime':datetime.datetime(2015, 1, 1, 10, 0),
                     'params': [ {'category':'TestCategory',
                                  'tags':['tag1', 'tag2', 'tag3'],
                                  'param':{'name': 'param1',
                                           'type': 'string',
                                           'value': 'string value'}},

    '''

    #--------------------------------------------
    def __init__(self, json_data=None):
        self.json_data = json_data
        self.dump_folder = r'C:\git\github\cstat\tmp\reports_dumps'

    #--------------------------------------------
    def check_format(self, json_data=None):
        print('Checking format...')
        json_obj = self.json_data
        if(json_data is not None):
            json_obj = json_data
        if(json_obj is None):
            raise ReportFormatException("JSON data is None!")

        if('datetime' not in json_obj):
            raise ReportFormatException("Can't find mandatory field <datatime>!")

        if('params' not in json_obj):
            raise ReportFormatException("Can't find mandatory field <params>!")

        if(len(json_obj['params'])>0):
            param = json_obj['params'][0]
            if('category' not in param):
                raise ReportFormatException("Can't find mandatory field <params.category>!")
            if('param' not in param):
                raise ReportFormatException("Can't find mandatory field <params.param>!")
            if('name' not in param['param']):
                raise ReportFormatException("Can't find mandatory field <params.param.name>!")
            if('value' not in param['param']):
                raise ReportFormatException("Can't find mandatory field <params.param.value>!")

        print('Checking format: done.')

    #--------------------------------------------
    def get_guid(self):
        return uuid.uuid4()

    #--------------------------------------------
    def get_dump_file_name(self):
        print('Getting dump file name ...')

        currdate = datetime.datetime.now()
        datestr = currdate.strftime('%Y%m%d%M%H')

        return '{}_{}.rep'.format(self.get_guid(), datestr)

    #--------------------------------------------
    def dump_report(self, json_data=None):
        json_obj = self.json_data
        if(json_data is not None):
            json_obj = json_data

        try:
            self.check_format(json_obj)
        except ReportFormatException as e:
            print(e.message)
            return False
        except Exception as e:
            print(e.args[0])
            return False

        try:
            print('Creating dump folder...')
            if(not os.path.exists(self.dump_folder)):
                os.mkdir(self.dump_folder)
            print('Creating dump folder: done.')

            dump_file_name = self.get_dump_file_name()
            dump_path = os.path.join(self.dump_folder, dump_file_name)

            print('Creating report dump ...')
            date_value = json_obj['datetime']
            json_obj['datetime'] = date_value.strftime("%Y-%m-%d %H:%M:%S")
            with codecs.open(dump_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(json_obj, ensure_ascii=False))
            print('Creating report dump: done.')
        except Exception as e:
            print('Error: \n{}'.format(e.args))
            return False

        return True

    #------------------------------------------------
    def load_report(self, dump_report_file):
        print('Load dump from file ...')
        if(not os.path.exists(dump_report_file)):
            return False

        try:
            with codecs.open(dump_report_file, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)
        except Exception as e:
            print('Error: \n{}'.format(e.args))
            return False

        print('Load dump from file: done.')

        return True

    #------------------------------------------------