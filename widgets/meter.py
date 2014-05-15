#
# Meter Widget
#
import config.logger as logger
from widget import Widget

class Meter(Widget):

  def __init__(self,items):
    self.name = items['name']
    self.datatype = items['datatype']
    self.type = items['widgettype']
    self.key = items['widgetkey']
    self.pre_data = items['predata']
    self.post_data = {}
    self.dashboard = items['dashboard']
    self.data2send = {"item":""}
    self.datahandler = Widget.data(self.datatype)
    self.dashboard = items['dashboard'] if items.has_key('dashboard') else None
    self.log = logger.createLogger(__name__)

  def update(self):
    self.post_data = self.datahandler.get_data(self.pre_data)
    if self.post_data:
      self._set_meter()
    else:
      self._throwerror("Post data does not exist, no data to update.")

  def _set_meter(self):
    self.data2send.update({"item":value,
                            "max":{"text":widget["max_text"],"value":widget["max_number"]},
                            "min":{"text":widget["min_text"],"value":widget["min_number"]}})
    self.post_data.update({'data': self.data2send})
    self._clean_widget_data()
