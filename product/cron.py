import logging
import datetime



# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def my_scheduled_job():

    print('IN', datetime.datetime.now())

    logger.info('User query', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': '1',
        })

    print(logger)
    logger.warning('User query')

    logger.error('test', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': 'toto',
        })

    print('Hello Cron Job', datetime.datetime.now())
    # a = 1 / 0
    # print(a)

    logger.critical('test exept', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': 'toto',
        })

    print('OUT', datetime.datetime.now())


