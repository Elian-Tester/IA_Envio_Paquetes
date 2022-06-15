#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ast import arg
import sys
from turtle import color

#Importar aquí las librerías a utilizar
import matplotlib.pyplot as plt
import random
from math import sin, cos, tan
import math
import cv2

from PyQt5 import uic, QtWidgets
from pymysql import NULL

from envio import Envio
import re
import win32api,win32con
import csv



qtCreatorFile = "vistaPaquete.ui" #Aquí va el nombre de tu archivo


Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    ID_IMAGES=0
    MEJORES_GENERACION = []
    PEORES_GENERACION = []
    PROMEDIO_GENERACIONES = []
    ITERACION_GENERACION = 1
    BANDERA_MAX = True
    BANDERA_FIN_HISTORICO = False

    NUEVA_GENERACION = []
    DATOS_GRAFICAR = []

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #self.boton2.clicked.connect(self.envio)
        
        self.CalcularBoton.clicked.connect(self.obtenerDatos)
        self.autoLlenarBoton.clicked.connect(self.autoLlenar)
        #self.anadirBoton.clicked.connect(self.setTexto)
        
        #self.poblacionInicialText.Text()
        #self.poblacionMaximaText.Text()
        #self.numeroPaquetes.Text()
        #self.tamanoContenedor.Text()
        #self.decendenciaText.Text()
        #self.mutacionIndividuoText.Text()
        #self.mutacionGenText.Text()
        #self.generacionesText.Text()
        #self.espacioText.Text() 
        #self.costoText.Text() 
    
    def autoLlenar(self):
        self.poblacionInicialText.setText('4')
        self.poblacionMaximaText.setText('8')
        self.numeroPaquetes.setText('8')
        self.tamanoContenedor.setText('14')
        self.decendenciaText.setText('90')
        self.mutacionIndividuoText.setText('50')
        self.mutacionGenText.setText('15')
        self.generacionesText.setText('3')
        self.espacioText.setText('2')
        self.costoText.setText('1')

        


    def obtenerDatos(self):
        generaciones = self.generacionesText.text()
        
        poblacion_inicial = self.poblacionInicialText.text()
        poblacion_maxima = self.poblacionMaximaText.text()
        
        numero_paquetes = self.numeroPaquetes.text()
        tamano_contenedor = self.tamanoContenedor.text()
        
        decendencia = self.decendenciaText.text()
        mutacion_individuo = self.mutacionIndividuoText.text()
        mutacion_gen = self.mutacionGenText.text()        
        
        espacios = self.espacioText.text() 
        costo = self.costoText.text()        
        
        datos1 = [
            poblacion_inicial,
            poblacion_maxima,
            numero_paquetes,
            tamano_contenedor,
            decendencia, #float
            mutacion_individuo, #float
            mutacion_gen, #float
            generaciones,
            espacios,
            costo
        ]

        if (self.validarCampos(datos1) == True):
            print("\nbien")
            self.envio(datos1)
        else:
            print("\nError")
        
    def envio(self, datos):
        print('Envio')

        env = Envio()
        todas_generaciones = []
        generacion_original = []
        tipos_paquetes_list = self.leerCsv()
        tipos_paquetes_list = env.tipoPaquete(tipos_paquetes_list)

        diccionario_espacios_list = env.diccionarioEspacios( tipos_paquetes_list, int(datos[2]) )

        for x in range( int(datos[7]) ):
            datos_paquetes = env.enviando(datos, self.NUEVA_GENERACION, diccionario_espacios_list)
            print("\n Entra a for de generaciones \n")

            self.NUEVA_GENERACION = datos_paquetes[0]
            todas_generaciones.append( {"generacion": datos_paquetes[0], "Graficar": datos_paquetes[1] } )
            self.DATOS_GRAFICAR.append( datos_paquetes[1] )

            generacion_original = datos_paquetes[2]
        
        print("\nMostrar en vista: ")
        texto_generaciones = ""
        conta_gen=0
        texto_generaciones += "\n__ Generacion original: \n"+ str(generacion_original) + "\n"
        for x in todas_generaciones:
            conta_gen+=1

            texto_generaciones += f"__ Generacion {conta_gen} \n"
            for y in x["generacion"]:
                texto_generaciones += str(y) +"  "
            grafi = x["Graficar"]
            texto_generaciones += "\n maximo: "+ str(grafi["maximo"]) +"\n minimo: "+str(grafi["minimo"])+"\n promedio: "+ str(grafi["promedio"])+"\n \n"
        
        self.NUEVA_GENERACION.clear()
        self.paquetesFinalLabel.setText(texto_generaciones)
    
    def leerCsv(self):
        print("Leer csv\n")
        
        results = []
        with open('201241.csv') as File:
            reader = csv.DictReader(File)
            for row in reader:
                results.append(row)
                print(row)
            #print (results)        

        return results


    def validarCampos(self, campos):
        print("campos")
        
        for validar in campos:            
            num_format = re.compile(r'^[0-9][0-9]*$')        
            valorA = re.match(num_format, validar)
            if valorA == False:
                #print(f"poblacion incial, correcta {validar}")
                print(f"poblacion incial, incorrecta {validar}")
                self.mensajeAlert(validar)
                return False            
        
        return True

        
    def mensajeAlert(self, mensaje ):
        print(f"Error datos ingresados {mensaje}")




if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_() #evita cerrar la ventana
