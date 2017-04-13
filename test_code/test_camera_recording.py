import logging
import time

logger = logging.getLogger(__name__)
filename = 'logs/' + time.strftime("%Y%m%d-%H%M") + '_camera_app.log'
hdlr = logging.FileHandler(filename)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

logger.error('We have a problem')
logger.info('While this is just chatty')
