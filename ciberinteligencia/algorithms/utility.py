from sklearn.externals import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score, classification_report

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
def calculeMetrics(trueValues, predictedValues):
    #accurancy = accuracy_score(trueValues, predictedValues)
    #recall = recall_score(trueValues, predictedValues)
    #f1 = f1_score(trueValues, predictedValues)
    #precision  = precision_score(trueValues, predictedValues)
    return classification_report(trueValues, predictedValues, target_names=targetNames)

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