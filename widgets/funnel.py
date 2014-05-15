#
# Funnel Widget
#
import config.logger as logger
from widget import Widget

class Funnel(Widget):

  def __init__(self,items):
    self.name = items['name']
    self.datatype = items['datatype']
    self.type = items['widgettype']
    self.key = items['widgetkey']
    self.pre_data = items['predata']
    self.data2send = {"percentage":"hide","item":[]}
    self.datahandler = Widget.data(self.datatype)
    self.dashboard = items['dashboard'] if items.has_key('dashboard') else None
    self.post_data = {}
    self.log = logger.createLogger(__name__)

  def update(self):
    self.post_data = self.datahandler.get_data(self.pre_data)
    if self.post_data:
      self._set_funnel()
    else:
      self._throwerror("Post data does not exist, no data to update.") 

  def _set_funnel(self):
    self.data2send["item"].append({"value":value,"label":label})
    self.post_data.update({'data': self.data2send})
    self._clean_widget_data()

