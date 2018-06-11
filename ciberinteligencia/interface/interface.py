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
import platform
import getpass
import ciberinteligencia.database.databaseConnector as db

# Main definition - constants
menu_actions = {}

# =======================
#     MENUS FUNCTIONS
# =======================


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def login_menu():
    show_login()


def show_login():
    # Comprobamos que el usuario introducido por el usuario existe y si la password introducida concide con la que nosotros tenemos
    print "Bienvenido, introduzca los datos de acceso por favor:"
    user_name = raw_input(" >> User:  ")
    pswd = getpass.getpass('Password:')
    if db.check_password(user_name, pswd):
        main_menu(user_name)
    else:
        print "Datos de ingreso incorrectos, hasta pronto!"


# Main menu
def main_menu(user_name):
    cls()

    print "Bienvenido {},\n".format(user_name)
    print "Por favor, elija la opcion del menu que desea ejecutar:"
    print "1. Menu 1"
    print "2. Menu 2"
    print "\n0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    cls()
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return


# Menu 1
def menu1():
    print "Hello Menu 1 !\n"
    print "9. Back"
    print "0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 2
def menu2():
    print "Hello Menu 2 !\n"
    print "9. Back"
    print "0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    login_menu()

