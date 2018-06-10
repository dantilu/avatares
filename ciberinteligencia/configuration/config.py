# -*- coding: utf-8 -*-
# !/usr/bin/python
import configparser
import os
import ciberinteligencia.database.databaseConnector as dbCon

CONSUMER_KEY = None
CONSUMER_SECRET = None
ACCESS_TOKEN = None
ACCESS_TOKEN_SECRET = None

SECRET_KEY = None
IV = None
BLOCK_SIZE = None
INTERRUPT = None
PAD = None


try:
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))

    CONSUMER_KEY = dbCon.get_config_param('CONSUMER_KEY')
    CONSUMER_SECRET = dbCon.get_config_param('CONSUMER_SECRET')
    ACCESS_TOKEN = dbCon.get_config_param('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = dbCon.get_config_param('ACCESS_TOKEN_SECRET')

    SECRET_KEY = dbCon.get_config_param('SECRET_KEY')
    IV = dbCon.get_config_param('IV')
    BLOCK_SIZE = dbCon.get_config_param('BLOCK_SIZE')
    INTERRUPT = dbCon.get_config_param('INTERRUPT')
    PAD = dbCon.get_config_param('PAD')
except Exception as e:  # catch all those ugly errors
    print "Error config.py {}".format(e)
