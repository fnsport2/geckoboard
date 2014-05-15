#
#  Widget base class
#

import config.logger as logger
from data.main import Data

defaultLogger = logger.createLogger("Widget")
class Widget():
    """ 
    Manages the internals of the widget, data and state.
    """
    data = Data

    def __init__(self):
      self.error = {'Error': False, 'Msg': None}
    
    def get_my_name(self):
        return{'name':self.name}
    def get_my_key(self):
        return{'key':self.key}
    def get_my_location(self):
        return{'location':self.location}
    def get_my_type(self):
        return{'name':self.type}

    # Update widget with data from source
    def update(self):
        raise NotImplementedError

    # Remove the value and lebel keys.
    def _clean_widget_data(self):
        self.log.info('Removing unwanted key value pairs.')
        try:
            del(self.post_data['values'])
        except KeyError:
            self._throwerror("Key [values] was not found.")
        try:
            del(self.post_data['labels'])
        except KeyError:
            self._throwerror("Key [labels] was not found.")

        self.log.debug("%s post data: %s"%(self.type,self.post_data))

    def _throwerror(self,msg):
        self.error['Error'] = True
        self.error['Msg'] = msg or 'No reason specified, please enable debug.'
        self.log.error("%s"%msg)
