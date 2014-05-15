#
# Numbers Widget
#
import config.logger as logger
from widget import Widget
import itertools

class Numbers(Widget):

  def __init__(self,items):
    self.name = items['name']
    self.datatype = items['datatype']
    self.type = items['widgettype']
    self.key = items['widgetkey']
    self.pre_data = items['predata']
    self.dashboard = items['dashboard'] if items.has_key('dashboard') else None
    self.post_data = {}
    self.datahandler = Widget.data(self.datatype)
    self.data2send = {"item":[]}
    self.log = logger.createLogger(__name__) 

  def update(self):
    self.post_data = self.datahandler.get_data(self.pre_data)
    if self.post_data:
      self._set_numbers()
    else:
      self._throwerror("Post data does not exist, no data to update.")


  def _set_numbers(self):
    for (value,label) in itertools.izip_longest(self.post_data["values"], self.post_data["labels"],fillvalue=""):
      self.data2send['item'].append({"text":label,"value":value})
      self.post_data.update({'data': self.data2send})
      self._clean_widget_data()
  
