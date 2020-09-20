# import logging
# import datetime


# # Get an instance of a logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# # create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# # add formatter to ch
# ch.setFormatter(formatter)

# logger.addHandler(ch)


def my_scheduled_job_2():

    print('HELLO CRON JOB 2')
    # print('IN', datetime.datetime.now())

    # logger.info('my_scheduled_job info', exc_info=True, extra={
    #     # Optionally pass a request and we'll grab any information we can
    #     'request': 'my_scheduled_job',
    #     })

    # print(logger)
    # logger.warning('my_scheduled_job warning')

    # logger.error('my_scheduled_job error', exc_info=True, extra={
    #     # Optionally pass a request and we'll grab any information we can
    #     'request': 'my_scheduled_job',
    #     })

    # print('Hello Cron Job', datetime.datetime.now())
    # # a = 1 / 0
    # # print(a)

    # logger.critical('my_scheduled_job critical', exc_info=True, extra={
    #     # Optionally pass a request and we'll grab any information we can
    #     'request': 'my_scheduled_job',
    #     })

    # print('OUT', datetime.datetime.now())


if __name__ == '__main__':

    my_scheduled_job_2()
