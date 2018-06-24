from sklearn.externals import joblib
import time
import datetime
import pandas as pd
from sklearn import metrics
from os import listdir
from os.path import isfile, join
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

#Global, con los nombres de las clases en las que clasificamos
targetNames = ['Humano', 'Bot']

#Definimos las funciones comunes de utilidad para los diferentes algoritmos que vamos a utilizar

#Esta funcion parsea y devuelve el dataset de forma que pueda ser utilizado por los diferentes algoritmos
#en este punto, falta serparar el dataset en los diferentes conjuntos de test y entrenamiento

def prepareDataset(csvFile, indexCol, type):
    if type == "Execution":
        # Pasamos el CSV a un dataframe
        data = pd.read_csv(csvFile, index_col=indexCol)
        data = data.drop('name', axis=1)
        print 'Quitando el nombre'
    elif type == "Train":
        # Pasamos el CSV a un dataframe
        data = pd.read_csv(csvFile, index_col=indexCol)
        data = data.drop('name', axis=1)
    #Eliminando las lineas a las que les falta alguno de los valores que utilizamos
    data.dropna(how='any', inplace=True)
    #Pasamos la fecha a formato TimeStamp
    data['creation_date'] = data['creation_date'].apply\
        (lambda x: time.mktime(datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timetuple()))

    return data


def normalizeData(input_data):

    for x in list(input_data) not in ['default_profile', 'default_profile_image', 'location', 'verified']:
        col = input_data[[x]].values.astype(float)
        min_max_scaler = preprocessing.MinMaxScaler()
        # Create an object to transform the data to fit minmax processor
        x_scaled = min_max_scaler.fit_transform(col)
        input_data[x] = x_scaled

    return input_data


#Funcion que genera el fichero donde se almacena el modelo para recuperarlo en caso de que sea necesario
def makeItPersistent(model, fileName):
    #Generamos la ruta donde se almacenara
    path = '../models/' + fileName
    joblib.dump(model, path)
    print 'Model stored in:' + path

#Funcion que carga y devuleve el modelo del alogritmo seleccionado
def loadModel(fileName):
    #Generamos el path
    path = '../models/' + fileName
    model = joblib.load(path)
    return model

#Funcion para el calculo de Fbeta, dependiendo de lo que queramos
def calcFBeta(trueValues, predictedValues,beta):
    Fbeta = metrics.fbeta_score(trueValues, predictedValues, beta)
    return Fbeta


#Funcion que evalua de forma bastante arcaica como esta el modelo en funcion de los errores que se han cometido
#en la clasificacion tanto en la fase de entrenamiento como en la fase de ejecucion
def howIsTheFit(trueValuesFit, predictedValuesFit, predictedValues, trueValues, beta):
    errorOnFit = metrics.fbeta_score(trueValuesFit, predictedValuesFit, beta)
    errorOnExec = metrics.fbeta_score(trueValues, predictedValues, beta)
    if errorOnFit < errorOnExec:
        if errorOnExec-errorOnFit > 0.35:
            return 'The model is overfited: ' + 'Training error: ' + errorOnFit + 'Execution error: ' + errorOnExec
        else:
            return 'The model could be overfited: ' + 'Training error: ' + errorOnFit + 'Execution error: ' \
                   + errorOnExec
    elif (errorOnFit < 0.6) and (errorOnExec < 0.6):
        return 'The model is underfited: ' + 'Training error: ' + errorOnFit + 'Execution error: ' + errorOnExec

    else:
        return 'The model looks OK, check the classification report for more information'

#Calcula las metricas basicas del modelo F1, accurancy y recall
def calcule_metrics(model):
    data = prepareDataset('../Training_Data/set_prueba.csv', indexCol='a_id', type="Train")
    X = data.drop('isabot', axis=1)
    y = data['isabot']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    prediction = model.predict(X_test)
    return metrics.classification_report(y_test, prediction)


#Definimos el comando ls para listar los archivos de un directorio
def ls(ruta = '.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

def print_results(results, user_path):
    data = pd.read_csv(user_path, index_col='a_id')
    data = list(data['name'])
    i = 0
    bots_count = 0
    for result in results:
        if result == 1:
            print 'Usuario detectado como bot:', data[i]
            bots_count += 1
        i += 1
    if bots_count == 0:
        print 'No se ha detectado ningun bot en los seguidores analizados'

def generateModel(model_choice, training_dataset):
    training_dataset = "../Training_Data/" + training_dataset
    dataset = prepareDataset(training_dataset, indexCol='a_id', type="Train")
    X = dataset.drop('isabot', axis=1)
    y = dataset['isabot']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    if model_choice == 1:
        model = tree.DecisionTreeClassifier()
    elif model_choice == 2:
        model = RandomForestClassifier(n_estimators=20)
    elif model_choice == 3:
        model = svm.SVC()
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    print "Nuevo modelo generado!"
    return model, metrics.classification_report(y_test, prediction)


