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
#import msvcrt
import getpass
import ciberinteligencia.database.databaseConnector as Db
import ciberinteligencia.algorithms.utility as utility
import ciberinteligencia.core as core
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
        print pswd
        if Db.check_password(name, pswd):
            return name
        else:
            return False
    except Exception as error:
        print('ERROR', error)
    else:
        print('Password entered:', p)


#Login Menu
def print_login_menu():
    print 10 * "-", "Login", 10 * "-"
    print "1. Login"
    print "2. Register"
    print "3. Exit"
    print 25 * "-"


#Main Menu
def print_main_menu(user_name):  ## Your menu design here
    cls()
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
        print "Generar el modelo nuevo!"
    elif choice == 3:
        print "See you!"
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Prueba de nuevo!")


#Load model submenu
def load_model_menu():
    cls()
    i = 1
    print 3 * '\n', 10 * "-", "Load Model", 10 * "-"
    print "Elija el menú que desea cargar"
    print "Modelos disponibles: "
    avaiable_models = utility.ls('../models/')
    for opcion in avaiable_models:
        if opcion[len(opcion)-3:] == '.py':
            continue
        print str(i) + '. ' + opcion
        i += 1

    choice = input("Enter you choice [1-" + str(i-1) + ']: ')
    print choice
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
        load_funcional_menu()


def load_funcional_menu():
    print 3 * '\n', 10 * "-", "Ciberinteligencia de avatares", 10 * "-"
    print "1. Análizar seguidores de un usuario"
    print "2. Info"
    choice = input("Enter your choice [1-3]: ")
    if choice == 1:
        print "Introduzca el nombre del usuario a análizar incluyendo el @"
        target_user = raw_input(">>")
        print "Ha elegido: ", target_user
        print "Analizando seguidores de", target_user, '\n', "Esto podría tardar un rato..."
        followers = ciberInteligencia.get_user_followers(target_user, 200)
        ciberInteligencia.filter_profiles(followers, '../core/salida.txt', 100, True, True, True)
    elif choice == 2:
        print "Ayuda"


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
        print "Under Construction!"
    elif choice == 3:
        print "See you!"
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Prueba de nuevo!")
