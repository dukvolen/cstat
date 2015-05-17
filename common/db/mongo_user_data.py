#------------------------------------------------
#  @brief       Working with Mongo DB for save users data
#  @author      Andrew Simine
#  @copyright   Copyrighted by Andrew Simine
#
#------------------------------------------------
import pymongo

## Data Access Class
# @class DataAccess
class DataAccess(object):

    ## Constructor of the class
    # @def __init__
    # @param username - access DB user
    # @param passwd - access DB password
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.db = pymongo.MongoClient()