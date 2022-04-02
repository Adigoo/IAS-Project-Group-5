import logging
import constants

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')

def execute():
    logging.debug('{serviceName} loaded successfully'.format(serviceName = constants.SERVICE_APPLICATION_MANAGER))