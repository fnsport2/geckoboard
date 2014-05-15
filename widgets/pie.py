#
# Pie Widget
#
import config.logger as logger
from widget import Widget

class Pie(Widget):

  def __init__(self,items):
    self.name = items['name']
    self.datatype = items['datatype']
    self.widgettype = items['widgettype']
    self.widgetkey = items['widgetkey']
    self.pre_data = items['predata']
    self.post_data = {}
    self.dashboard = items['dashboard']
    self.hexcolors = items['hexcolors']
    self.data2send = {"item":[]}
    self.datahandler = Widget.data(self.datatype)
    self.dashboard = items['dashboard'] if items.has_key('dashboard') else None
    self.log = logger.createLogger(__name__)

  def update(self):
    self.post_data = self.datahandler.get_data(self.pre_data)
    if self.post_data:
      self._set_pie()
    else:
      self._throwerror("Post data does not exist, no data to update.")

  def _set_pie(self):
    for i, (value,label) in enumerate(zip(self.post_data["values"], self.post_data["labels"])):

      self.data2send['item'].append({"value":value,"label":label,
                                            "colour":"%s"%self.hexcolors[i]})
      self.post_data.update({'data': self.data2send})
      self._clean_widget_data()
