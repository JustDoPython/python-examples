import logging
print("__name__", __name__)
logger = logging.getLogger(__name__)

def fun():
    logger.warning("foo fun warning")