import os,logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename=f'{os.path.splitext(os.path.basename(__file__))[0]}.log',
                    encoding='utf-8', level=logging.INFO, format='%(asctime)s %(name)s:%(levelname)s:%(message)s')

logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')