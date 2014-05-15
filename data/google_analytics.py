#
# Driver for Google Analytics
#

import gdata.analytics.client
import gdata.sample_util
import config.logger as logger
from config.environment import Environment as environment
import datetime

class Google_Analytics:

    #Set date for interval use
    currentdate = datetime.datetime.now()
    yesterday_date = datetime.datetime.now()-datetime.timedelta(days=1)
    my_client = gdata.analytics.client.AnalyticsClient()
    config = environment.data_config 
    authenticated = False
    log = logger.createLogger("Google Analytics",None)
    
    @classmethod
    def _auth_google_analytics(cls):
        " Try to establish a client connection with Google Analytics"
        cls.log.info('Attempting to authenticate with Google Analytics')
        if not cls.authenticated:
            try:
                cls.my_client.client_login(email= cls.config.get('GA')['email'],
                                            password= cls.config.get('GA')['token'],
                                            source= cls.config.get('GA')['source_app_name'],
                                            service= cls.config.get('GA')['service'])
                cls.log.info('Google Analytics authentication successful')
                cls.authenticated=True
            except gdata.client.BadAuthentication:
                cls.log.error('Please check your credentials used for your GA account')
                #exit('Invalid user credentials given.')
            except gdata.client.ClientLoginFailed as e:
                cls.log.error('Login Error %s'%(e))
            except gdata.client.Error as e:
                exit('Login Error %s'%e)

    # Handle GA queries, send and receive data.
    # Return a dict {'lables':'', 'values':''}
    @classmethod
    def _get_ga_data(cls,query):
        " Make our GA query via the analytics api and return the data"

        feed = cls._process_ga_query(query)
        data = cls._print_feed_table(feed)
        cls.log.debug("RAW GA data: %s"% data)
        return data

    # Execute a GA query and return data in feed object
    @classmethod
    def _process_ga_query(cls, query):
        " Execute our query with the api"
        cls.log.info('Attempting to make GA query')
        # Set current date if requested
        if query.has_key("start-date") and query["start-date"]=="today":
            query["start-date"]='%s'% cls.currentdate.strftime("%Y-%m-%d")

        if query.has_key("end-date") and query["end-date"]=="today":
            query["end-date"]='%s'% cls.currentdate.strftime("%Y-%m-%d")

        # Set to today last year
        # datetime.datetime.now() - datetime.timedelta(days=365)
        if query.has_key("start-date") and query["start-date"]=="today-year":
            query["start-date"]='%s'% (cls.currentdate - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

        if query.has_key("end-date") and query["end-date"]=="today-year":
            query["end-date"]='%s'% (cls.currentdate - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

        #self.log.debug("GA query we will run: %s" %query)
        data_query = gdata.analytics.client.DataFeedQuery(query)
        cls.log.debug("Api url we will send: %s" %data_query)
        # Make the GA query and get the feed object
        feed = cls.my_client.GetDataFeed(data_query)
        return feed

    # Iterate through the data and put it in key value pairs. 
    @staticmethod
    def _print_feed_table(feed):

        #Format GA data into json
        dimension_value = []
        metric_value = []
        for index, entry in enumerate(feed.entry):
            for dim in entry.dimension:
                if dim.value:
                    dimension_value.append(dim.value)
                    # self.log.debug('Dimension Name = %s \t Dimension Value = %s'% (dim.name, dim.value))
            for met in entry.metric:
                metric_value.append(met.value);
                # self.log.debug('Metric Name =  %s \t Metric Value =  %s'% (met.name, met.value))

        data = {'labels': dimension_value, 'values': metric_value}
        return data


