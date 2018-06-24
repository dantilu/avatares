# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Created on Tue Mar 27 18:43:55 2018

@author: Dante
"""
import argparse
import datetime
import tweepy
import re
import time
import pandas as pd     # To handle data
import numpy as np      # For number computing
import math

from ciberinteligencia.cypher.aes import *
from ciberinteligencia.configuration.config import *
from ciberinteligencia.algorithms import utility

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

from datetime import datetime
from collections import defaultdict
from textblob import TextBlob
from textstat.textstat import textstat

class UserRead:
    #Solo se definen campos comunes como variables aqui, lo demas va en los diferentes métodos
    #Inicializamos todas las variables que vayamos a usar en la clase
    def __init__(self):
        self.profile = None
        self.user_timeline = None
        self.name = None
        self.friends_count = 0
        self.followers_count = 0

        # Useful params for training
        self.a_id = None
        self.name_length = None
        self.name_letters_amount = 0
        self.name_numbers_amount = 0
        self.location = None
        self.ratio_friends_followers = 0
        self.verified = None
        self.default_profile_image = False
        self.default_profile = None
        self.creation_date = None
        self.total_number_of_words = 0
        self.total_unique_words = 0
        self.lexical_diversity = 0
        self.average_number_words_per_tweet = 0
        self.smog_index = 0
        self.number_of_tweets = 0
        self.number_of_hashtags = 0
        self.number_of_urls = 0
        self.number_of_mentions = 0
        self.last_24_hours_tweet = 0
        self.average_time_between_tweets = 0
        self.desviacion_tipica_average_tweet_time = 0
        self.creation_content_sources = 0
        self.percent_positive_tweets = 0
        self.percent_negative_tweets = 0
        self.percent_neutral_tweets = 0
        self.average_lenth_from_tweets = 0
        #self.isabot = 0

    def profile_initialize(self, api_profile):
        self.profile = api_profile

    def clean_user(self):
        self.profile = None
        self.user_timeline = None
        self.name = None
        self.friends_count = 0
        self.followers_count = 0

        #Useful params for training
        self.a_id = None
        self.name_length = None
        self.name_letters_amount = 0
        self.name_numbers_amount = 0
        self.location = None
        self.ratio_friends_followers = 0
        self.verified = None
        self.default_profile_image = False
        self.default_profile = None
        self.creation_date = None
        self.total_number_of_words = 0
        self.total_unique_words = 0
        self.lexical_diversity = 0
        self.average_number_words_per_tweet = 0
        self.smog_index = 0
        self.number_of_tweets = 0
        self.number_of_hashtags = 0
        self.number_of_urls = 0
        self.number_of_mentions = 0
        self.last_24_hours_tweet = 0
        self.average_time_between_tweets = 0
        self.desviacion_tipica_average_tweet_time = 0
        self.creation_content_sources = 0
        self.percent_positive_tweets = 0
        self.percent_negative_tweets = 0
        self.percent_neutral_tweets = 0
        self.average_lenth_from_tweets = 0
        #self.isabot = 0

    def paramline(self):
        try:
            params = self.__dict__
            values = ''
            params2 = (param for param in sorted(list(params.keys())) if param not in ['profile', 'user_timeline', 'friends_count', 'followers_count'])
            for param in params2:
                values += str(params[param]) + ','
            values = values[:len(values)-1] + '\n'
            return values
        except Exception as ex:
            print 'Fallo: {}'.format(ex)


    #Generamos la primera linea que contiene el nombre de todas las variables que vamos a utilizar
    def generateFirstLine(self):
        objectparams = self.__dict__
        firstLine = ''
        paramNames = (param for param in sorted(list(objectparams.keys())) if
                   param not in ['profile', 'user_timeline', 'friends_count', 'followers_count'])
        for name in paramNames:
            firstLine += str(name) + ','

        return firstLine[:len(firstLine)-1] + '\n'


def get_followers(user_id, limitador):
    try:
        api_followers = login()
        users = []
        users_count = 0
        page_count = 0
        print "Calculando los followers de {}".format(user_id)
        for page in tweepy.Cursor(api_followers.followers, id=user_id, count=limitador).pages():
            page_count += 1
            for user in page:
                users.append(user.screen_name)
                users_count += 1
                print "Numero {}  nombre {}".format(users_count, user.screen_name)
            print "Pagina {}".format(page_count)
    except tweepy.RateLimitError:
        print "RateLimitError...waiting 1000 seconds to continue "
    print "Numero de followers encontrados : {} ".format(users_count)
    return users


def get_user_followers(user_id, limiter):
    try:
        api_user_followers = login2()
        users = []
        users_count = 0
        print "Calculando los followers de {}".format(user_id)
        for user in tweepy.Cursor(api_user_followers.followers, id=user_id).items(limiter):
            if (datetime.now() - user.created_at).days > 7:
                users.append(user.screen_name)
                users_count += 1
                #print "{}".format(user.screen_name)
    except tweepy.RateLimitError:
        print "RateLimitError...waiting 1000 seconds to continue "
    print "Numero de followers conseguidos : {} ".format(users_count)
    return users


def login():
    #auth = tweepy.OAuthHandler(decrypt_with_aes(cipher_for_decryption, CONSUMER_KEY),
    #                           decrypt_with_aes(cipher_for_decryption, CONSUMER_SECRET))
    #auth.set_access_token(decrypt_with_aes(cipher_for_decryption, ACCESS_TOKEN),
    #                      decrypt_with_aes(cipher_for_decryption, ACCESS_TOKEN_SECRET))
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return tweepy.API(auth)


def login2():
    #auth = tweepy.OAuthHandler(decrypt_with_aes(cipher_for_decryption, CONSUMER_KEY),
    #                           decrypt_with_aes(cipher_for_decryption, CONSUMER_SECRET))
    #auth.set_access_token(decrypt_with_aes(cipher_for_decryption, ACCESS_TOKEN),
    #                      decrypt_with_aes(cipher_for_decryption, ACCESS_TOKEN_SECRET))
    auth = tweepy.OAuthHandler(CONSUMER_KEY2, CONSUMER_SECRET2)
    auth.set_access_token(ACCESS_TOKEN2, ACCESS_TOKEN_SECRET2)

    return tweepy.API(auth)


def check_profile(profile, usuario):
    try:
        api = login2()
        user_name = profile.split('	')
        print user_name
        perfil = api.get_user(user_name[0])

        #isabot = '0'
        #Comprobamos si quedan lineas debajo para no coger el salto de linea
        #if isabot[:len(isabot)] == '1\n' or isabot[:len(isabot)] == '0\n':
        #    isabot = isabot[:len(isabot)-1]
        # Crea un objeto de la clase usuario
        usuario.profile_initialize(perfil)
        return True
    except Exception as ex:  # catch all those ugly errors
        print 'No se ha encontrado el perfil @{} Razon {}'.format(user_name[0], ex.args)
        #Limpiamos el objeto ya que el perfil no existe
        usuario.clean_user()
        return False


def filter_profiles(followers_list, output_filename, limitador,  flag_hashtag, flag_url, flag_mention):
    try:
        f_out = open(output_filename, "w")
        user = UserRead()
        f_out.write(user.generateFirstLine())
        #Procesamos todas las lineas del fichero de entrada, comprobando previamente que el perfil exista, en caso contrario saltaremos al siguiente
        users_proccessed = 0
        for i in followers_list:
            # El perfil analizado no existe
            if check_profile(i, user):
                if profile_based_characteristics(user):
                    if content_based_characteristics(user, limitador,  flag_hashtag, flag_url, flag_mention):
                        if content_based_characteristics_upgraded(user, limitador):
                            f_out.write(user.paramline())
                            print "Parametros del usuario {} : {}".format(user.name, user.paramline())
                            users_proccessed += 1
                            user.clean_user()

        print "Total de usuarios procesados {}".format(users_proccessed)
        f_out.close()
        return
    except Exception as ex:
        return False


def filter_profiles_input_filestream(input_filename, output_filename, limitador,  flag_hashtag, flag_url, flag_mention):
    try:
        f_in = open(input_filename, "r")
        f_out = open(output_filename, "w")
        user = UserRead()
        f_out.write(user.generateFirstLine())
        #Procesamos todas las lineas del fichero de entrada, comprobando previamente que el perfil exista, en caso contrario saltaremos al siguiente
        users_proccessed = 0
        for i in f_in.readlines():
            # El perfil analizado no existe
            if check_profile(i, user):
                if profile_based_characteristics(user):
                    if content_based_characteristics(user, limitador,  flag_hashtag, flag_url, flag_mention):
                        if content_based_characteristics_upgraded(user, limitador):
                            f_out.write(user.paramline())
                            print "Parametros del usuario {} : {}".format(user.name, user.paramline())
                            users_proccessed += 1
                            user.clean_user()

        print "Total de usuarios procesados {}".format(users_proccessed)
        f_in.close()
        f_out.close()
        return
    except Exception as ex:
        return False


def profile_based_characteristics(usuario):
    # Campos a tener en cuenta para filtrar el perfil
    try:
        user = usuario.profile
        usuario.name = user.screen_name
        usuario.name_length = len(str(user.screen_name))
        alphabetical_chars = re.search("[a-zA-Z]+", user.screen_name)
        if alphabetical_chars:
            usuario.name_letters_amount = len(alphabetical_chars.group())
        else:
            usuario.name_letters_amount = 0

        numeric_chars = re.search("[0-9]+", user.screen_name)

        if numeric_chars:
            usuario.name_numbers_amount = len(numeric_chars.group())
        else:
            usuario.name_numbers_amount = 0
        usuario.a_id = user.id_str
        if user.location is not None:
            usuario.location = True
        else:
            usuario.location = False
        usuario.friends_count = user.friends_count
        usuario.followers_count = user.followers_count

        if user.followers_count != 0:
            usuario.ratio_friends_followers = (1.0 * user.friends_count / user.followers_count)

        usuario.verified = user.verified
        if not user.default_profile_image:
            if user.profile_image_url == \
                    "http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png":
                usuario.default_profile_image = True
            else:
                usuario.default_profile_image = False
        else:
            usuario.default_profile_image = False

        # Si el perfil esta por defecto es probable que el usuario sea un candidato a bot
        if user.default_profile:
            usuario.default_profile = True
        else:
            usuario.default_profile = False

        # Si la fecha de creacion es inferior a una semana no podemos discernir si es un bot
        usuario.creation_date = user.created_at
        return True
    except Exception as excep:
        print "Profile Based error from user {}  reason {}".format(usuario.name, excep)
        return False


def content_based_characteristics(usuario, limitador, flag_hashtag, flag_url, flag_mention):
        try:
            api = login2()
            created_at_list = {}
            usuario.user_timeline = api.user_timeline(usuario.name)
            user = usuario.user_timeline
            if user == []:
                return True
            word_count = defaultdict(int)
            number_of_tweets = user[0].user.statuses_count
            total_number_of_hashtags = 0
            total_number_of_urls = 0
            total_number_of_mentions = 0
            last_24_hours_tweet = 0
            flag1 = 0
            flag2 = 0
            flag3 = 0
            tw = 0
            lexical_diversity = 0
            line_counter = 0
            smog_text = ""

            if number_of_tweets > limitador:
                status_size = limitador
            else:
                status_size = number_of_tweets

            lines = tweepy.Cursor(api.user_timeline, screen_name='@' + usuario.name).items(limitador)

            for line in lines:
                if not line:
                    continue
                try:
                    tweet_text = line._json['text'].strip()
                    if not line._json.get('text'):
                        continue
                    words = tweet_text.split()
                    tw += len(words)
                    created_at_list[line_counter] = line.created_at
                    line_counter += 1
                    for word in words:
                        if word[0:1] == '#' and len(word) > 1 and flag1 == 0:
                            total_number_of_hashtags += 1
                            if flag_hashtag:
                                flag1 = 1
                        if "http" in word and flag2 == 0:
                            total_number_of_urls += 1
                            if flag_url:
                                flag2 = 1
                        if word[0:1] == '@' and len(word) > 1 and flag3 == 0:
                            total_number_of_mentions += 1
                            if flag_mention:
                                flag3 = 1
                        word_count[word] += 1

                    flag1 = 0
                    flag2 = 0
                    flag3 = 0

                    if (datetime.now() - line.created_at).days < 1:
                        last_24_hours_tweet += 1

                    if line_counter <= 10:
                        smog_text += tweet_text + ". "
                    if line_counter >= status_size - 10:
                        smog_text += tweet_text + ". "
                    if status_size/2 - 5 <= line_counter <= status_size/2 + 5:
                        smog_text += tweet_text + ". "

                except Exception as e:
                    print "Problem Line: " + line + "" + e

            tuw = len(set(word_count))
            lexical_diversity += 1.0 * tuw / tw
            awpt = 1.0 * tuw / line_counter

            usuario.total_number_of_words = tw
            usuario.total_unique_words = tuw
            usuario.lexical_diversity = lexical_diversity
            usuario.average_number_words_per_tweet = awpt
            usuario.smog_index = textstat.smog_index(smog_text)
            usuario.number_of_tweets = number_of_tweets
            usuario.number_of_hashtags = total_number_of_hashtags
            usuario.number_of_urls = total_number_of_urls
            usuario.number_of_mentions = total_number_of_mentions
            usuario.last_24_hours_tweet = last_24_hours_tweet
            usuario.average_time_between_tweets = calculate_average_time_between_tweets(created_at_list)
            return True
        except Exception as e:
            print "Content Based Characteristics error from user {} reason {}".format(usuario.name, e)
            return False


def calculate_average_time_between_tweets(list):
    try:
        size = list.__len__()
        total_elapsed_ms = 0
        for x in range(0, size-1):
            first = list[x]
            second = list[x+1]
            diff = first - second
            elapsed_ms = (diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000)
            total_elapsed_ms += elapsed_ms
        return total_elapsed_ms / size
    except Exception as e:
        print "Average time problem {}".format(e)


def content_based_characteristics_upgraded(usuario, limitador):
    try:
        tweets = usuario.user_timeline
        data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        #Add the important data that we want to process
        data['len'] = np.array([len(tweet.text) for tweet in tweets])
        data['WordCount'] = np.array([calculate_word_count(tweet) for tweet in tweets])
        data['UniqueWordCount'] = np.array([calculate_unique_word_count(tweet) for tweet in tweets])
        data['ID'] = np.array([tweet.id for tweet in tweets])
        data['Date'] = np.array([tweet.created_at for tweet in tweets])
        data['DateTimestamp'] = np.array([convert_date(tweet.created_at) for tweet in tweets])
        data['Source'] = np.array([tweet.source for tweet in tweets])
        data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
        data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
        data['SA'] = np.array([analize_sentiment(tweet) for tweet in data['Tweets']])

        mean = np.mean(data['len'])

        if not np.isnan(np.std(data['DateTimestamp'])):
            usuario.desviacion_tipica_average_tweet_time = np.std(data['DateTimestamp'])
        else:
            usuario.desviacion_tipica_average_tweet_time = 0

        # We obtain all possible sources:
        usuario.creation_content_sources = 0
        user_sources = []
        for source in data['Source']:
            if source not in user_sources:
                user_sources.append(source)
                usuario.creation_content_sources += 1

        pos_tweets = [tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
        neu_tweets = [tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
        neg_tweets = [tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]
        if len(data['Tweets'] != 0):
            usuario.percent_positive_tweets = len(pos_tweets) * 100 / len(data['Tweets'])
            usuario.percent_negative_tweets = len(neg_tweets) * 100 / len(data['Tweets'])
            usuario.percent_neutral_tweets = len(neu_tweets) * 100 / len(data['Tweets'])
            usuario.average_lenth_from_tweets = mean
        return True
    except Exception as e:
        print "Content Based Upgraded problem for user {} reason {}".format(usuario.name, e)
        return False


def convert_date(fecha):
    string_fecha = fecha.strftime("%d-%m-%Y %H:%M:%S")
    return time.mktime(time.strptime(string_fecha, "%d-%m-%Y %H:%M:%S"))


def calculate_word_count(tweet):
    return len(tweet.text.split())


def calculate_unique_word_count(tweet):
    words = tweet.text.split()
    word_count = defaultdict(int)

    for word in words:
        word_count[word] += 1
    return len(set(word_count))


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analize_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1



def analize_dataset(model, dataset):
    data = utility.prepareDataset(dataset, indexCol='a_id', type="Execution")
    results = model.predict(data)
    return results



try:
    #print
    #parser = argparse.ArgumentParser()
    #parser.add_argument("inputFile", help="inputFile File with the Twitter Profiles")
    #parser.add_argument("outputFile", help="outputFile File where you want to get the output")
    #args = parser.parse_args()

    #print args.inputFile
   #print args.outputFile

    #Hacemos login en la API de Twitter
    #api = login()
    usuario = UserRead()
    #print api.rate_limit_status()
    #get_followers(api, "Ford", 2)
    api = login2()
    #Creamos fichero de salida
    # Si se le pasa true como tercer parametro calcula el numero total de hashtags
    # Por el contrario, si le pasamos false calcula el numero de tweets que tienen algun hashtag
    # Hay que tener en cuenta que las respuestas a un tweet tambien las considera como ULR's porque son enlaces al propio Tweeter
    #filter_profiles(args.inputFile, args.outputFile, 100, True, True, True)
    filter_profiles_input_filestream('../Training_Data/info/Todos.txt', 'salida400_4.txt', 100, True, True, True)

    #data = utility.prepareDataset('../Training_Data/secondDataset.csv', 'a_id')
    #X = data.drop('isabot', axis=1)
    #y = data['isabot']
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    #Modelo de Arbol de decision
    #model = tree.DecisionTreeClassifier()
    #model.fit(X, y)
    #utility.makeItPersistent(model, 'Decision_Tree_Entrenamiento_Bueno')
    #model = utility.loadModel('Random_Forest_Regular')
    #Modelo de Random Forest
    #model = RandomForestClassifier()
    #model.fit(X, y)
    #utility.makeItPersistent(model, 'Random_Forest_Entrenamiento_Bueno')
    #Modelo de SVM
    #model = svm.SVC()
    #model.fit(X_train, y_train)

    # Prueba de funcionamiento y calculo de la precision
    #y_predictExec = model.predict(X)
    #y_predictFit = model.predict(X_train)
    #print utility.howIsTheFit(y_train, y_predictFit, y_test, y_predictExec)
    #print 'Tabla de ejecucion'
    #print utility.calculeClasifficationReport(y, y_predictExec)
    #print 'Tabla de entreno'
    #print utility.calculeClasifficationReport(y_train, y_predictFit)

except Exception as e:  # catch all those ugly errors
    print "Se ha producido un error {}".format(e)
