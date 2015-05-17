#------------------------------------------------
# @brief        Tests for mongodb class
# @author       Andrew Simine
# @copyright    Copyrighted by Andrew Simine
#
#------------------------------------------------
from common.db import mongo_user_data
import unittest

#------------------------------------------------
class TestMongoDBDataAccess(unittest.TestCase):

    def setUp(self):
        self.dataobj = mongo_user_data.DataAccess()

    def testPrepareCategoryCollection(self):
        retval = self.dataobj.prepare_category_collection('TestCategory')
        return self.assertIsNotNone(retval, 'Bad test category collection.')

#------------------------------------------------
def suite():
    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.makeSuite(TestMongoDBDataAccess))

    return testsuite

#------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
