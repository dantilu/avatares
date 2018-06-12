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
import msvcrt
import getpass
import ciberinteligencia.database.databaseConnector as Db

# =======================
#     MENUS FUNCTIONS
# =======================


def getpass2(prompt='Password: ', hideChar=' '):
    count = 0
    password = ''

    for char in prompt:
        msvcrt.putch(char)  # cuz password, be trouble

    while True:
        char = msvcrt.getch()

        if char == '\r' or char == '\n':
            break

        if char == '\003':
            raise KeyboardInterrupt  # ctrl + c

        if char == '\b':
            count -= 1
            password = password[:-1]

            if count >= 0:
                msvcrt.putch('\b')
                msvcrt.putch(' ')
                msvcrt.putch('\b')

        else:
            if count < 0:
                count = 0

            count += 1
            password += char
            msvcrt.putch(hideChar)

    msvcrt.putch('\r')
    msvcrt.putch('\n')

    return "'%s'" % password if password != '' else "''"



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
    print 10 * "-", "Main Menu", 10 * "-"
    print "Bienvenido {}".format(user_name)
    print "1. Cargar Modelo"
    print "2. Generar modelo"
    print "3. Exit"
    print 25 * "-"
    choice = input("Enter your choice [1-3]: ")
    if choice == 1:
        print "Cargar el modelo!"
    elif choice == 2:
        print "Generar el modelo nuevo!"
    elif choice == 3:
        print "See you!"
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Prueba de nuevo!")



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
        if user_name is not False or user_name is not None:
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
