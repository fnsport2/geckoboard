#
# Simple Geckoboard widget factory
#

from map import Map
from meter import Meter
from pie import Pie
from funnel import Funnel
from numbers import Numbers

# Factory Method
def create_widget(init_items):
  if init_items['widgettype'] == 'Map':
      return Map(init_items)
  if init_items['widgettype'] == 'Pie':
      return Pie(init_items)
  if init_items['widgettype'] == 'Funnel':
      return Funnel(init_items)
  if init_items['widgettype'] == 'Numbers':
      return Numbers(init_items)
  if init_items['widgettype'] == 'Meter':
      return Meter(init_items)
