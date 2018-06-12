# -*- coding: utf-8 -*-
# !/usr/bin/python
import pymongo
from pymongo import MongoClient
import hashlib


def login_database():
    return MongoClient('localhost', 27017)
    client.test_database


def create_user(username, password):
    try:
        client = login_database()
        user_collection = client.test_database.USERS

        hash_object = hashlib.sha256(password)
        hex_dig = hash_object.hexdigest()

        params = {"_id": collection.count(), "name": username, "password": hex_dig}
        user_collection.insert(params)
        print "Usuario insertado en base de datos"

    except Exception as user_ex:
        print " Error al insertar en USER: " + user_ex


def add_config_param(name, value):
    try:
        client = login_database()
        collection = client.test_database.CONFIGURATION
        collection.count()

        col = {"_id": collection.count(), "param_name": name, "param_value": value}
        collection.insert(col)
        print "Usuario insertado en base de datos"

    except Exception as user_ex:
        print " Error al insertar en CONFIGURATION: " + user_ex


def get_config_param(name):
    try:
        client = login_database()
        collection = client.test_database.CONFIGURATION
        condition = {"param_name": name}
        print "Elemento encontrado: "
        return collection.find_one(condition).values()[1]
    except Exception as user_ex:
        print " Error al insertar en CONFIGURATION: " + user_ex


def load_database():
    add_config_param('CONSUMER_KEY', 'xtXWF1E2tthbAidq1F/uYHMbCtukisOcWcmWBvBQvE+Y6qb8IBvKNcNgqBwnWOQPupecj0DBpWP5fmGDQLdce+qt468Wvsm8+oiTdz3mKxQF8NHmzXuUI5VoPHtpKaAki4DLUVYljdCdf+zFBb5ZaIZjE1sf7ejytwUo2t72LlRH/XjuHGjcns+cv5ioLqMEQG89i+121CmqUY/uYmJgKTW4cjLoetrxrZSN6qptU1cJGOAQZEU6busGNCAVhMDlTaA2Chk5S42nlqWiA1o3SWAXYO5y8pQa1JLRrJFtddV5YPRm5SprovIP371r3jv8plkqEy/QzcTgQBjVY7zxkxgDgFKPWIVOoCgwELbA8vWYPSkU/cGxJ3B7jk8I1duyE5QsHFe1CuIhvWIO5qMvHw==')
    add_config_param('CONSUMER_SECRET', '3bPpvrmBmuazqoj2Q+NtyXvkMbUtIw5111yo4njBfoDL74hT/NUMm3Bk1yxCmgh5HHY4cuCPTnKMPKtc/yrAbvCRGS05kWo0SCMOLp4RHBc=')
    add_config_param('ACCESS_TOKEN', '26MvxTjPoNatyjcN+l49TPDvqO92BVqlpCbtttDMsoDaJZrsgtrud9Nr2HelWbnAxRT9bIpAbaTyXdYJxIO8ahOT2C6JVzJ5XuwjEOjvGXU=')
    add_config_param('ACCESS_TOKEN_SECRET', 'I4FW3OsQvD+ZjQ6aUOqeIuMh0lQJQseux8cVEsxqXjZYxGYTFXZl6u21FMolA9UH5+xquEEs1zLx2Bt2z69u8h42mgo/u0SquPFpvFNOcbqyIBWEJa3cp9EYmRfyJ+oz2l46tiSFqyAY6L5GBmh6Y5a+PYJ7l6XHBNE/RwJEHES9Y9OCClqUJQUqQ6b7GjsV')
    add_config_param('SECRET_KEY', 'c2FiYmF0aCMyMDE4')
    add_config_param('IV', '12345678abcdefgh')
    add_config_param('BLOCK_SIZE', '32')
    add_config_param('INTERRUPT', u'\u0001')
    add_config_param('PAD', u'\u0000')


def empty_config_collection():
    try:
        client = login_database()
        client.test_database.CONFIGURATION.remove({})
    except Exception as ex1:
        print "Error vaciando config"


def check_password(user, pwd):
    try:
        client = login_database()
        pwd_hashed = hashlib.sha256(pwd).hexdigest()
        collection = client.test_database.USERS
        condition = {"name": user, "password": pwd_hashed}
        if collection.find_one(condition) is not None:
            return True
        else:
            return False
    except Exception as login_ex:
        return False


# Main Program
#if __name__ == "__main__":
    # Insertamos usuarios en la base de datos local, antes hay que haber arrancado el server local con mongod.exe
    #client = login_database()
    #collection = client.test_database.USERS
    #create_user("sergio", "ser1234")
