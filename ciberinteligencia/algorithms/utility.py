from sklearn.externals import joblib
import pandas as pd
from sklearn import metrics

#Global, con los nombres de las clases en las que clasificamos
targetNames = ['Humano', 'Bot']

#Definimos las funciones comunes de utilidad para los diferentes algoritmos que vamos a utilizar

#Esta funcion parsea y devuelve el dataset de forma que pueda ser utilizado por los diferentes algoritmos
#en este punto, falta serparar el dataset en los diferentes conjuntos de test y entrenamiento

def prepareDataset(csvFile, indexCol):
    #Pasamos el CSV a un dataframe
    data = pd.read_csv(csvFile, index_col=indexCol)
    #Seleccionamos los campos que vamos a utilizar, Deberia ser estatico, alomejor en el fichero de conf
    data = data[['','','','']]
    #Eliminando las lineas a las que les falta alguno de los valores que utilizamos
    data.dropna(how='any', inplace=True)
    return data

#Esta funcion devuelve una tabla imprimible con los valores de precision, recall y F1 del algoritmo
def calculeClasifficationReport(trueValues, predictedValues):
    #accurancy = accuracy_score(trueValues, predictedValues)
    #recall = recall_score(trueValues, predictedValues)
    #f1 = f1_score(trueValues, predictedValues)
    #precision  = precision_score(trueValues, predictedValues)
    return metrics.classification_report(trueValues, predictedValues, target_names=targetNames)

#Funcion que genera el fichero donde se almacena el modelo para recuperarlo en caso de que sea necesario
def makeItPersistent(model, fileName):
    #Generamos la ruta donde se almacenara
    path = 'models/' + fileName
    joblib.dump(model, path)
    print 'Model stored in:' + path

#Funcion que carga y devuleve el modelo del alogritmo seleccionado
def loadModel(fileName):
    #Generamos el path
    path = 'models/' + fileName
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

