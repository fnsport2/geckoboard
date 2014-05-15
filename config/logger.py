# Logger Module for Geckoboard project
#
#

import logging
from config.environment import Environment as environment


# Configuring for logger done here
def createLogger(name,filehandler=None):
    """Create a logger to log activity."""

    formatter = logging.Formatter('\n%(levelname)s: %(asctime)s - %(name)s -'+
                                 '%(message)s')
    logger = logging.getLogger(name)
    if environment.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    if filehandler != None:
        logger.addHandler(filehandler)
    else:
        fh = logging.FileHandler('defaultgeckoboard.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
