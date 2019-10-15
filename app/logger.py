import logging.config
import yaml
import os

working_dir = os.getcwd()
conf = os.path.join(working_dir, "logging.conf")
logging.config.dictConfig(yaml.load(open(conf)))
logfile = logging.getLogger('file')
logconsole = logging.getLogger('console')


def log(str_log):
    logconsole.debug(str_log)
