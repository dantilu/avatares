# -*- coding: utf-8 -*-
# !/usr/bin/python
import configparser
import os

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

    CONSUMER_KEY = config['TWITTER_API']['CONSUMER_KEY']
    CONSUMER_SECRET = config['TWITTER_API']['CONSUMER_SECRET']
    ACCESS_TOKEN = config['TWITTER_API']['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = config['TWITTER_API']['ACCESS_TOKEN_SECRET']

    SECRET_KEY = config['AES']['SECRET_KEY']
    IV = config['AES']['IV']
    BLOCK_SIZE = config['AES']['BLOCK_SIZE']
    INTERRUPT = config['AES']['INTERRUPT']
    PAD = config['AES']['PAD']
except Exception as e:  # catch all those ugly errors
    print "Error config.py {}".format(e)
