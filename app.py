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
        self.poblacionInicialText.setText('3')
        self.poblacionMaximaText.setText('6')
        self.numeroPaquetes.setText('8')
        self.tamanoContenedor.setText('7')
        self.decendenciaText.setText('60')
        self.mutacionIndividuoText.setText('5')
        self.mutacionGenText.setText('4')
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
        env.enviando(datos)        
    
    def validarCampos(self, campos):
        print("campos")
        
        for validar in campos:            
            num_format = re.compile(r'^[0-9][0-9]*$')        
            valorA = re.match(num_format, validar)
            if valorA:
                print(f"poblacion incial, correcta {validar}")
            else:
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
