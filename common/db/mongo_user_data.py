#------------------------------------------------
#  @brief       Working with Mongo DB for save users data
#  @author      Andrew Simine
#  @copyright   Copyrighted by Andrew Simine
#
#------------------------------------------------
import datetime

from pymongo import MongoClient
#from pymongo.operations import IndexModel
import pymongo
from pymongo.errors import BulkWriteError

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
    def __prepare_category_name(self, category_name):
        return category_name.replace(' ', '_')

    #------------------------------------------------
    ## Check category collection
    # @def prepare_category_collection(self, name)
    # @param category - name of category
    def prepare_category_collection(self, category):
        category_name = self.__prepare_category_name(category)
        if(category_name in self.db.collection_names()):
            print('Category {0} is already created'.format(category_name))
            return self.db.get_collection(category_name)

        print('Creating category {0}...'.format(category_name))
        category_item = self.db.create_collection(category_name)
        category_item.create_index('date')

        return category_item

    #------------------------------------------------
    ## Save any data sent by user in database by category
    # @def save_user_data(self, category, data)
    # @param data - user's data in JSON format
    # @param category_name - category of data for save
    def save_user_data_by_category(self, category_name, data):
        print('Saving user data for category {} ...'.format(category_name))
        retval = True

        category_collection = self.prepare_category_collection(category_name)
        bulk_obj = category_collection.initialize_ordered_bulk_op()
        for param in data:
            bulk_obj.insert(param)

        try:
            bulk_obj.execute()
        except BulkWriteError as bwe:
            print(bwe.details)

        return retval

    #------------------------------------------------
    ## Save any data sent by user in database
    # @def save_user_data(self, data)
    # @param data - user's data in JSON format
    def save_user_data(self, data, ignore_errors=True):
        print('Saving user data...')
        retval = True

        try:
            received_date = data.get('datetime')
        except Exception as e:
            print('Error:\n {}'.format(e.args))
            return False

        # group data by category
        params_by_cetegory = {}
        for param in data.get('params'):
            category_name = param['category']
            if(category_name is  None):
                category_name = 'Unknown'
            else:
                category_name = self.__prepare_category_name(category_name)

            if(category_name not in params_by_cetegory):
                params_by_cetegory[category_name] = []

            param['datetime'] = received_date
            params_by_cetegory[category_name].append(param)

        # save params to database
        for category_name in params_by_cetegory:
            try:
                self.save_user_data_by_category(category_name, params_by_cetegory.get(category_name))
            except Exception as e:
                print('Error: \n{}'.format(e.args))
                if(not ignore_errors):
                    retval = False
                    break

        return retval

    #------------------------------------------------
    ## Get data sent by user from database
    # @def get_user_data(self, to_date=None, limit=None)
    # @param to_date - date when user sent reports
    # @param limit - number of first reports received from user to specified date
    def get_user_data(self, category, to_date=None, records=None):
        retval = []

        if(to_date is None):
            to_date = datetime.datetime.now()
        to_date2 = to_date + datetime.timedelta(days=1)

        date1 = datetime.datetime(to_date.year, to_date.month, to_date.day, 0, 0)
        date2 = datetime.datetime(to_date2.year, to_date2.month, to_date2.day, 0, 0)

        category_collection = self.prepare_category_collection(category)
        query = {'datetime':{'$gte':date1, '$lt':date2}}

        if(records is not None):
            retval = category_collection.find(query).sort([('datetime', pymongo.ASCENDING)]).limit(records)
        else:
            retval = category_collection.find(query).sort([('datetime', pymongo.ASCENDING)])

        return retval

    #------------------------------------------------
