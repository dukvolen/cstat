#------------------------------------------------
#  @brief       Working with Mongo DB for save users data
#  @author      Andrew Simine
#  @copyright   Copyrighted by Andrew Simine
#
#------------------------------------------------
from pymongo import MongoClient
from pymongo.operations import IndexModel
from pymongo import ASCENDING, DESCENDING

## Data Access Class
# @class DataAccess
class DataAccess(object):

    ## Constructor of the class
    # @def __init__
    # @param username - access DB user
    # @param passwd   - access DB password
    #------------------------------------------------
    def __init__(self, userid='cstat', dbhost='127.0.0.1', dbport=27017,
                 dbuser='statuser', dbpasswd='12345'):
        self.client = MongoClient(dbhost, dbport)
        self.db = self.client.get_database(userid) # userid - userid defines name of database
        self.db.authenticate(dbuser, dbpasswd)

    #------------------------------------------------
    ## Check category collection
    # @def prepare_category_collection(self, name)
    # @param category - name of category
    def prepare_category_collection(self, category):
        if(category in self.db.collection_names()):
            print('Category {0} is already created'.format(category))
            return self.db.get_collection(category)

        print('Creating category {0}...'.format(category))
        category = self.db.create_collection(category)
        category.create_index('date')
        return category

    #------------------------------------------------

