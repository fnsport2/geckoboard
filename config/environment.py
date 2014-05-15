# Geckoboard Environment
# Like a global scope (for modules) to have access to config.
#

import yaml
import os

# Get the full path for the file for access from outside modules.
__dir__ = os.path.dirname(os.path.abspath(__file__))
filepath =os.path.join(__dir__,'dashboard.yaml')


# Setting up our environment for some common needs, such as our config file.
class Environment:
    tempyaml=''
    with open(filepath,'r') as f:
        tempyaml = yaml.load(f)

    data_config = tempyaml['Data Config']
    widget_config = tempyaml['Widgets Config']
    geckoboard_config = tempyaml['Geckoboard Config']
    debug = tempyaml['Debug']

