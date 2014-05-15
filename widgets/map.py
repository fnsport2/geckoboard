#
# Map Widget
#
import config.logger as logger
from widgets.widget import Widget

class Map(Widget):

  def __init__(self,items):
    self.name = items['name']
    self.datatype = items['datatype']
    self.type = items['widgettype']
    self.key = items['widgetkey']
    self.pre_data = items['predata']
    self.data2send = {"points":{"point":[]}}
    self.datahandler = Widget.data(self.datatype)
    self.dashboard = items['dashboard'] if items.has_key('dashboard') else None
    self.post_data = {}
    self.log = logger.createLogger(__name__)

  def update(self):
    self.post_data = self.datahandler.get_data(self.pre_data)
    if self.post_data:
      self._set_map()
    else:
      self._throwerror("Post data does not exist, no data to update.")
  
  # Lat and Long points for the lat,long are stored in a single array 'labels'.
  # Use xrange to parse the list two at a time. 
  def _set_map(self):
    tempList = self.post_data.get('labels')
    for i in xrange(0,len(self.post_data.get('labels')),2):
          self.data2send['points']['point'].append({"latitude":tempList[i],
                                                    "longitude":tempList[i+1]})
          self.post_data.update({'data': self.data2send})
          self._clean_widget_data()

 
