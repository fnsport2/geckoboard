#
#
#

import urllib2
import json
import datetime
from google_analytics import Google_Analytics as ga
import config.logger as logger
from config.environment import Environment as environment

defaultlog = logger.createLogger("Data")

class Data():
    """
    Processes all data, and manages the database
    """
    #log = logger.createLogger("Data",None)

    def __init__(self,
        data_type=None,
        config=environment.data_config,
        database=None,
        log=None
        ):
        self.datatype=data_type
        self.config = config
        self.db_name = database or config.get('DB')['database']
        self.db_cursor = None
        self.log = log or defaultlog
        self.log.info("Initializing")
        self.currentdate = datetime.datetime.now()
        self.my_client = None
        self.authenticate()

    # Authenticate to necessary thrid parties.
    def authenticate(self):
        self.log.info("Authenticating with 3rd party data clients")
        #self._auth_database()
        ga._auth_google_analytics()

    # Determine the type of data we need to process.
    def get_data(self,raw):
        processed=None

        if self.datatype:
            if self.datatype.lower() == 'google analytics': processed = ga._get_ga_data(raw)
            elif self.datatype.lower() == 'api': processed = self._get_apiurl_data(raw)
            else: self.log.error("Config Error: dataType ' %s' is unknown. Check config file."%self.datatype)
        else:
            self.log.error("Config Error: dataType missing for widget. Check config file.")

        return processed

    # Make api calls using urllib2
    # Returns a dict: 
    #   {'lables':'', 'values':''}
    def _get_apiurl_data(self,api):

        self.log.info('making a request to this url %s'%api['request'])
        url = urllib2.Request(url= api['request'])
        f = urllib2.urlopen(url)
        temp_data = json.loads(f.read())
        if temp_data.has_key('response'):
          temp_data= temp_data['response']
        data = {'labels': [api['text']], 'values': [temp_data[api['value']]]}
        self.log.debug('data received for key [ %s ]  was %s'%(api['value'],temp_data[api['value']]))
        return data

    def _auth_database(self):
        " Connect to the database"
        raise NotImplementedError
