# -*- coding: utf-8 -*-
# !/usr/bin/python
import ciberinteligencia.database.databaseConnector as dbCon

#Script para ejecutar diferentes partes del codigo
try:
    #Vaciamos la configuracion
    #dbCon.empty_config_collection()

    #Insertamos la configuracion de nuevo
    #dbCon.load_database()
    print "Main Finalizado"
except Exception as ex:
    print "Error! {}".format(ex)
