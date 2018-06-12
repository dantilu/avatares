# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
Created on Tue Mar 27 18:43:55 2018

@author: Dante
"""
# Import the necessary packages
from consolemenu import *
from consolemenu.items import *

user_name = None

# Create the menu
menu = ConsoleMenu("Ciberinteligencia de Avatares", "Bienvenido!")

# Create some items

# MenuItem is the base class for all items, it doesn't do anything when selected
login_menu_item = MenuItem("Login")

main_menu = MenuItem("Bienvenido ")

# A FunctionItem runs a Python function when selected
function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

# A CommandItem runs a console command
command_item = CommandItem("Run a console command",  "touch hello.txt")

# A SelectionMenu constructs a menu from a list of strings
selection_menu = SelectionMenu(["item1", "item2", "item3"])

# A SubmenuItem lets you add a menu (the selection_menu above, for example)
# as a submenu of another menu
submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

# Once we're done creating them, we just add the items to the menu
menu.append_item(login_menu_item)
menu.append_item(function_item)
menu.append_item(command_item)
menu.append_item(submenu_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()