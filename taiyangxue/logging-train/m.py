import logging

#logging.warning("m.py info")
logger = logging.getLogger(f'mylog.{__name__}')
def fun():
    logger.warning("fun value 10")
    return 10
    
def fun2():
    logger.info("fun2")