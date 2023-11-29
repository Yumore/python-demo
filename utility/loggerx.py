import logging


def logger(tag, message):
    logging.info('========> {0} - {1}'.format(tag, message))
