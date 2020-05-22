#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2020 WShuai, Inc.
# All Rights Reserved.

# @File: commLog.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2020/3/2 10:28

import os
import copy
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler

class LogHandler(object):
    def __init__(self, configs):
        self.configs = configs
        self.log_level = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARN': logging.WARNING,
            'ERROR': logging.ERROR,
        }
        return

    def register_default(self, log_file):
        configs = copy.deepcopy(self.configs)
        configs['handlers']['default']['filename'] = \
            configs['handlers']['default']['filename'].replace('FILE', log_file)
        logging.config.dictConfig(configs)
        logger = logging.getLogger('default')
        return logger

    def register_rotate(self, log_file):
        log_level = self.log_level[self.configs['handlers']['default']['level'].upper()]
        log_format = logging.Formatter(self.configs['formatters']['default']['format'])
        log_file_name = self.configs['handlers']['default']['filename'].replace('FILE', log_file)
        if not os.path.isdir(os.path.abspath(os.path.dirname(log_file_name))):
            os.makedirs(os.path.abspath(os.path.dirname(log_file_name)))
        handler = TimedRotatingFileHandler(
            log_file_name,
            when = 'midnight'
        )
        handler.setFormatter(log_format)
        self.logger = logging.getLogger(log_file_name)
        self.logger.addHandler(handler)
        self.logger.setLevel(log_level)
        return self.logger