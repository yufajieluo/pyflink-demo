#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2020 WShuai, Inc.
# All Rights Reserved.

# @File: main.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2020/3/2 10:28

import os
import sys
import argparse
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from common.commLog import LogHandler
from common.commFile import FileHandler

from flink import Flink

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='app name', type = str, required = True)
    parser.add_argument('--config', help='config file', type = str, required = True)
    args = parser.parse_args()

    if not os.path.isfile(args.config):
        print('config file {0} not exist.'.format(args.config))
        sys.exit(1)
    else:
        # init config with yaml
        file_handler = FileHandler()
        config = file_handler.loads(type = 'yaml', file = args.config)
        print('read config is {0}'.format(config))

        # init log
        logger_handler = LogHandler(config['logging'])
        logger = logger_handler.register_rotate(args.name)
        logger.info('service config is {0}'.format(config))

        flink = Flink(config = config, logger = logger)
        flink.start()

    sys.exit(0)