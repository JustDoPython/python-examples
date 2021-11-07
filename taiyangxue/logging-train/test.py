import logging
import m
from foo.foomod import fun as foofun
from foo.bar import barmod

rootlogger = logging.getLogger()
root_hdl = logging.StreamHandler()
root_hdl.setLevel(level=logging.DEBUG)
rootlogger.addHandler(root_hdl)
logging.basicConfig(level=logging.DEBUG, format="%(name)s-%(message)s")
rootlogger.debug("logging debug")
rootlogger.info("logging info")
rootlogger.warning("logging warning")
rootlogger.error("logging error")
rootlogger.critical("logging critical")

logger = logging.getLogger('foo')
logger.warning(logger.hasHandlers())
fmt = logging.Formatter("%(asctime)s-%(filename)s-%(name)s-%(message)s")
hdl = logging.StreamHandler()
hdl.setFormatter(fmt)
logger.addHandler(hdl)
logger.warning(len(logger.handlers))
logger.warning("logger debug")

print(rootlogger.debug == logging.getLogger().debug)

print(m.fun())
m.fun2()
barmod.fun()
foofun() 