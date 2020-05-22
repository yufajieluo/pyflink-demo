#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2020 WShuai, Inc.
# All Rights Reserved.

# @File: FileHandler.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2020/3/2 10:28

import os
import yaml
import pickle

class FileHandler(object):
    def __init__(self, **kwargs):
        return

    def dump(self, **kwargs):
        if kwargs['type'] == 'pick':
            with open(file, 'wb') as file_handler:
                pickle.dump(kwargs['content'], file_handler)
        return

    def loads(self, **kwargs):
        content = None
        try:
            if kwargs['type'] == 'pick':
                with open(kwargs['file'], 'rb') as file_handler:
                    content = pickle.load(file_handler)
            elif kwargs['type'] == 'yaml':
                with open(kwargs['file'], 'rb') as file_handler:
                    content = yaml.safe_load(file_handler)
        except Exception as e:
            print('loads from file {0} Exception: {1}'.format(kwargs['file'], e))
        return content