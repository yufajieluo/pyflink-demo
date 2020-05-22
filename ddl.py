#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2020 WShuai, Inc.
# All Rights Reserved.

# @File: flink.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2020/3/2 10:28

class DDL(object):
    def __init__(self, **kwargs):
        self.ddl_file_default = '''
            CREATE TABLE {table} (
                name VARCHAR,
                age INT,
                wife VARCHAR,
                bad_boy BOOLEAN,
                balance FLOAT,
                record_time VARCHAR
            ) WITH (
                'connector.type' = 'filesystem',
                'connector.path' = '{path}',
                'format.type' = 'csv',
                'format.field-delimiter' = ';'
            )
        '''

        self.ddl_kafka_csv = '''
            CREATE TABLE {table} (
                line VARCHAR
            ) WITH (
                'connector.type' = 'kafka',
                'connector.version' = 'universal',
                'connector.topic' = '{topic}',
                'connector.properties.zookeeper.connect' = '{zookeeper_connect}',
                'connector.properties.bootstrap.servers' = '{bootstrap_servers}',
                'format.type' = 'csv',
                'format.field-delimiter' = ';'
            )
        '''

        self.ddl_kafka_json = '''
            CREATE TABLE {table} (
            ) WITH (
                'connector.type' = 'kafka',
                'connector.version' = 'universal',
                'connector.topic' = '{topic}',
                'connector.properties.zookeeper.connect' = '{zookeeper_connect}',
                'connector.properties.bootstrap.servers' = '{bootstrap_servers}',
                'format.type' = 'json',
                'format.derive-schema' = 'true',
                'format.fail-on-missing-field' = 'true'
            )
        '''

        self.ddl_mysql_default = '''
            CREATE TABLE {table} (
                name VARCHAR,
                age INT,
                wife VARCHAR,
                bad_boy BOOLEAN,
                balance FLOAT,
                record_time VARCHAR
            ) WITH (
                'connector.type' = '{engine}',
                'connector.url' = '{connstr}',
                'connector.table' = '{intable}',
                'connector.driver' = 'com.mysql.cj.jdbc.Driver',
                'connector.username' = '{user}',
                'connector.password' = '{pswd}',
                'connector.write.flush.interval' = '1s'
            )
        '''

        

        