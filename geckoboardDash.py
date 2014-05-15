#
#
# Class and driver for geckoboard
#
#
# Felix Nance
#

import urllib2
import json
import config.logger as logger
from config.environment import Environment as environment
from widgets import factory

class Geckoboard():
    """
    Manages our geckoboard app. It knows about it's widgets and dashboards.
    """
    def __init__(self,
        push_api = environment.geckoboard_config.get('push_api'),
        api_key = environment.geckoboard_config.get('api_key'),
        log = None
        ):
        self.push_api = push_api
        self.api_key = api_key
        self.num_widgets = 0
        self.widgets = []
        self.log = log or logger.createLogger("Geckoboard",None)
        self.log.info("Initializing")
        
        self._load_widgets()

    # Update Geckoboard with the widget data using push api + key
    def update_dashboard(self):
        self.log.info('updating dashboard')
        self._update_widgets()

    # Create our widgets from our config file.
    def _load_widgets(self):
        for item in environment.widget_config:
            if item['enabled']:
              self.widgets.append(factory.create_widget(item))
              self.num_widgets+=1

    def _update_widgets(self):
        for widget in self.widgets:
            widget.update()
            for key in widget.key: 
                self.log.info(self.push_api+str(widget.key))
                self._push_data(key,widget.post_data)

    # Push data to Geckoboard
    def _push_data(self,key,data):
        request = urllib2.Request(self.push_api+str(key))
        request.add_header("Content-Type", "application/json")
        try:
            finalpackage = '{"api_key":"%s","data":%s}'%(self.api_key,
                                                         json.dumps(data['data']))
            self.log.info('pushing this dump to geckoboard: %s'%finalpackage)
            urllib2.urlopen(request,finalpackage)

        except Exception as e:
            self.log.error('oops: %s'%e) 
     
def main():
  
    ck12geckoboard = Geckoboard()
    ck12geckoboard.update_dashboard()

if __name__ == '__main__':

    main()
