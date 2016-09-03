import logging
import logging.handlers

def init_logger(level):
    logger = logging.getLogger()

    # send everything DEBUG and higher
    logger.setLevel(level)

    # log via the syslog socket
    handler = logging.handlers.SysLogHandler(address='/dev/log')

    # make sure we send the "python" TAG
    handler.formatter = logging.Formatter('SmartHome: %(message)s')

    # lastly, add the handler
    logger.addHandler(handler)
    return logger

def log_info(log, msg, verbose=0):
    log.info(msg)
    if verbose:
        print(msg)

def log_err(log, msg, verbose=0):
    log.error(" ERROR " + msg)
    if verbose:
        print(msg)
