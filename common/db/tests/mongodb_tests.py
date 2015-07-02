#------------------------------------------------
# @brief        Tests for mongodb class
# @author       Andrew Simine
# @copyright    Copyrighted by Andrew Simine
#
#------------------------------------------------
from common.db import mongo_user_data
import unittest
import datetime

#------------------------------------------------
class TestMongoDBDataAccess(unittest.TestCase):

    def setUp(self):
        self.dataobj = mongo_user_data.DataAccess()

    #--------------------------------------------
    def testPrepareCategoryCollection(self):
        retval = self.dataobj.prepare_category_collection('TestCategory')
        return self.assertIsNotNone(retval, 'Bad test category collection.')

    #--------------------------------------------
    def testSaveData(self):
        test_data = {'datetime':datetime.datetime(2015, 1, 1, 10, 0),
                     'params': [ {'category':'TestCategory',
                                  'tags':['tag1', 'tag2', 'tag3'],
                                  'param':{'name': 'param1',
                                           'type': 'string',
                                           'value': 'string value'}},
                                 {'category':'TestCategory',
                                  'tags':['tag1', 'tag2', 'tag3'],
                                  'param':{'name': 'param2',
                                           'type': 'numeric',
                                           'value': 12}},
                                 {'category':'TestCategory',
                                  'tags':['tag1', 'tag2', 'tag3'],
                                  'param':{'name': 'param3',
                                           'type': 'string',
                                           'value': 'string value'}},
                                 {'category':'TestCategory',
                                  'tags':['tag1', 'tag2', 'tag3'],
                                  'param':{'name': 'param4',
                                           'type': 'string_array',
                                           'value': ['str1', 'str2', 'str3']}},
                                 {'category':'TestCategory',
                                  'tags':['tag1', 'tag2', 'tag3'],
                                  'param':{'name': 'param5',
                                           'type': 'numeric_array',
                                           'value': [12, 6, 9]}}]
                     }
        retval = self.dataobj.save_user_data(test_data)
        return self.assertTrue(retval, 'Tested data is saved successfully.')

    #--------------------------------------------
    def testGetData(self):
        test_date = datetime.datetime(2015, 1, 1, 12, 0)
        retval1 = self.dataobj.get_user_data(to_date=test_date, limit=2)
        retval2 = self.dataobj.get_user_data(limit=2)
        retval3 = self.dataobj.get_user_data(to_date=test_date)
        retval4 = self.dataobj.get_user_data()
        return self.assertTrue((retval1 and retval2 and retval3 and retval4), 'Test getting is successfully.')

#------------------------------------------------
def suite():
    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.makeSuite(TestMongoDBDataAccess))
    return testsuite

#------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
