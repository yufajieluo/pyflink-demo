#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2020 WShuai, Inc.
# All Rights Reserved.

# @File: flink.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2020/3/2 10:28

import os
import sys
import copy
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

from ddl import DDL
from udf.badboy import badboy
from udf.serialize import get

class Flink(object):
    def __init__(self, **kwargs):
        self.config = kwargs['config']
        self.logger = kwargs['logger']

        self.ddl = DDL()

        self.st_env = None
        self.job_name = self.config['default']['job_name']

        self.source_type = self.config['source']['type']
        self.source_table = self.config['source']['table']
        self.source_config = self.config[self.source_type]

        self.sink_type = self.config['sink']['type']
        self.sink_table = self.config['sink']['table']
        self.sink_config = self.config[self.sink_type]
        return
    
    def init_env(self, **kwargs):
        env = StreamExecutionEnvironment.get_execution_environment()
        self.st_env = StreamTableEnvironment.create(
            env,
            environment_settings = EnvironmentSettings.new_instance().use_blink_planner().build()
        )
        return
    
    def init_connector(self, **kwargs):
        config = copy.deepcopy(kwargs['config'])
        config['table'] = kwargs['table']

        ddl_str = 'self.ddl.ddl_{0}_{1}.format(**config)'.format(
            kwargs['type'],
            config['format_type'],
            ','.join(kwargs['config'].keys())
        )
        self.logger.debug('ddl_str real is {0}'.format(eval(ddl_str)))

        self.st_env.sql_update(eval(ddl_str))
        return

    def init_source(self, **kwargs):
        self.init_connector(type = self.source_type, table = self.source_table, config = self.source_config)
        return

    def init_sink(self, **kwargs):
        self.init_connector(type = self.sink_type, table = self.sink_table, config = self.sink_config)
        return
    
    def init_udf(self, **kwargs):
        self.st_env.register_function('get', get)
        self.st_env.register_function('badboy', badboy)
        return
    
    def transform(self, **kwargs):
        self.st_env.from_path(
            self.source_table
        ).select(
            'get(line, "serialize") as serialize, '
            'get(line, "name") as name, '
            'get(line, "age").cast(INT) as age, '
            'get(line, "wife") as wife, '
            'get(line, "balance").cast(FLOAT) as balance, '
            'get(line, "record_time") as record_time'
        ).filter(
            'serialize = "True"'
        ).select(
            'name, age, wife, badboy(wife) as bad_boy, balance, record_time'
        ).insert_into(
            self.sink_table
        )
        return
    
    def execute(self, **kwargs):
        self.st_env.execute(self.job_name)
        return
    
    def start(self, **kwargs):
        self.init_env()
        self.init_source()
        self.init_sink()
        self.init_udf()
        self.transform()
        self.execute()
        return