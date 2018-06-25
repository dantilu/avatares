# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Created on Tue Mar 27 18:43:55 2018

@author: Dante
"""

# Este modulo mostrara el menu para que el usuario pueda trabajar con la herramienta
# Import the modules needed to run the script.
import sys
import os
import time
import getpass
import ciberinteligencia.algorithms.utility as utility
import ciberinteligencia.database.databaseConnector as database
import pyautogui
import ciberinteligencia.core.ciberinteligenciaAlgoritmos as ciberInteligencia

# =======================
#     MENUS FUNCTIONS
# =======================1


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_login():
    try:
        # Comprobamos que el usuario introducido por el usuario existe y si la password introducida concide con la que nosotros tenemos
        print "Introduzca los datos de acceso por favor:"
        name = raw_input(" >> User:  ")
        pswd = getpass.getpass("Enter the password: ")
        if database.check_password(name, pswd):
            return name
        else:
            return False
    except Exception as error:
        print('ERROR', error)
    else:
        print('Password entered:', p)


#Login Menu
def print_login_menu():
    pyautogui.hotkey('command', 'i')
    print 10 * "-", "Login", 10 * "-"
    print "1. Login"
    print "2. Register"
    print "3. Exit"
    print 25 * "-"


#Main Menu
def print_main_menu(user_name):  ## Your menu design here
    pyautogui.hotkey('command', 'i')
    print 10 * "-", "Main Menu", 10 * "-"
    print "Bienvenido {}".format(user_name)
    print "1. Cargar Modelo"
    print "2. Generar modelo"
    print "3. Exit"
    print 25 * "-"
    choice = input("Enter your choice [1-3]: ")
    if choice == 1:
        load_model_menu()
    elif choice == 2:
        load_generate_menu()
    elif choice == 3:
         print "See you!"
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Prueba de nuevo!")


def load_generate_menu():
    pyautogui.hotkey('command', 'i')
    print 10 * "-", "Generate a new model", 10 * "-"
    print "Elija el algoritmo para el nuevo modelo"
    print "1. Decision Tree"
    print "2. Random Forest"
    print "3. SVM"
    algoritm_choice = input("Enter your choice [1-3]: ")
    while(algoritm_choice > 3 or algoritm_choice < 1):
        print "Seleccione uno de los algoritmos de la lista"
        algoritm_choice = input("Enter your choice [1-3]: ")
    print "Algoritmo seleccionado, seleccione un dataset para entrenar"
    avaiable_datasets = utility.ls('../Training_Data/')
    i = 1
    for opcion in avaiable_datasets:
        if opcion[len(opcion) - 4:] == '.txt':
            continue
        print str(i) + '. ' + opcion
        i += 1
    dataset_choice = input("Enter you choice [1-" + str(i-1) + ']: ')
    dataset_name = avaiable_datasets[dataset_choice-1]
    while(dataset_choice not in list(range(i)) or dataset_choice == 0):
        print '\n', "¡El dataset seleccionado no es valido!"
        print "Seleccione un dataset de la lista"
        dataset_choice = input("Enter you choice [1-" + str(i - 1) + ']: ')
        dataset_name = avaiable_datasets[dataset_choice]
        print dataset_name
    model, metrics = utility.generateModel(algoritm_choice, dataset_name)
    load_funcional_menu(model, 1, metrics)


#Load model submenu
def load_model_menu():
    pyautogui.hotkey('command', 'i')
    i = 1
    print 10 * "-", "Load Model", 10 * "-"
    print "Elija el menú que desea cargar"
    print "Modelos disponibles: "
    avaiable_models = utility.ls('../models/')
    for opcion in avaiable_models:
        if opcion[len(opcion)-3:] == '.py':
            continue
        print str(i) + '. ' + opcion
        i += 1

    choice = input("Enter you choice [1-" + str(i-1) + ']: ')
    if choice not in  list(range(i)) or choice == 0:
        print '\n',"¡El modelo seleccionado no es valido!"
        load_model_menu()
    else:
        for x in range(i):
            if choice == x:
                print '\n','Cargando el modelo seleccionado... '
                model = utility.loadModel(avaiable_models[x])
                print '\n', 'Modelo:', avaiable_models[x], 'cargado correctamente'
                break
        load_funcional_menu(model, 0, metrics=None)


def load_funcional_menu(model, newModel, metrics):
    pyautogui.hotkey('command', 'i')
    print 10 * "-", "Ciberinteligencia de avatares", 10 * "-"
    print "1. Análizar seguidores de un usuario"
    print "2. Información sobre el modelo"
    if newModel == 1:
        print "3. Guardar el modelo"
        print '\n','Las metricas para el modelo generado son:'
        print metrics
        choice = input("Enter your choice [1-3]: ")

        print metrics
    else:
        choice = input("Enter your choice [1-2]: ")
    if choice == 1:
        print "Introduzca el nombre del usuario a análizar"
        target_user = raw_input(">>")
        print "Ha elegido:", target_user
        user_path = '../datasets/' + target_user + '.csv'
        if os.path.isfile(user_path):
            print 'Ya existe un dataset recopilado para este usuario con fecha:', time.ctime(os.path.getctime(user_path))
            print '¿Desea generar un nuevo dataset?(Esto sobrescribira el documento actual)'
            choice = raw_input('[s/n]:')
            pyautogui.hotkey('command', 'i')
            if choice == 's':
                print "Analizando seguidores de", target_user, '\n', "Esto podría tardar un rato..."
                followers = ciberInteligencia.get_user_followers(target_user, 200)
                ciberInteligencia.filter_profiles(followers, '../datasets/' + target_user + '.csv', 100, True, True, True)
                results = ciberInteligencia.analize_dataset(model, user_path)
                utility.print_results(results, user_path)
            elif choice == 'n':
                print 'Calculando bots.....'
                results = ciberInteligencia.analize_dataset(model, user_path)
                utility.print_results(results, user_path)
        else:
            print "Analizando seguidores de", target_user, '\n', "Esto podría tardar un rato..."
            followers = ciberInteligencia.get_user_followers(target_user, 200)
            ciberInteligencia.filter_profiles(followers, '../datasets/' + target_user + '.csv', 100, True, True, True)
            results = ciberInteligencia.analize_dataset(model, user_path)
            utility.print_results(results, user_path)
    elif choice == 2:
        print "Info sobre el modelo:"
        print utility.calcule_metrics(model)

    elif choice == 3 and newModel == 1:
        print "Intruduzca el nombre con el que se guardará el modelo"
        model_name = raw_input(">>")
        utility.makeItPersistent(model, model_name)
        print "El modelo se ha guardado correctamente"
        load_funcional_menu(model, 0, metrics=None)

# Exit program
def exit():
    sys.exit()


# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    loop = True
    user_name = None
    print_login_menu()  ## Displays menu
    choice = input("Enter your choice [1-3]: ")

    if choice == 1:
        user_name = show_login()
        if user_name is not False:
            # EL usuario ha conseguido hacer login correctamente
            print_main_menu(user_name)
        else:
            print "Datos de acceso incorrectos, hasta pronto!"
    elif choice == 2:
        username = raw_input("Seleccione un nombre de usuario: ")
        password = raw_input("Escriba su contraseña: ")
        database.create_user(username, password)
        print_main_menu(username)
    elif choice == 3:
        print "See you!"
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Prueba de nuevo!")
