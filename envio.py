import random
from re import X
from traceback import print_tb
from typing import final

class Envio():

    GENERACION_ORIGINAL = []
    ABECEDARIO = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    def enviando(self, dato, generacion_anterior, diccionario_espacios_list):        
        datos = {
            "pI": dato[0],
            "pM": dato[1],
            "numPaquetes": dato[2],
            "tamContenedor": dato[3],
            "decendencia": dato[4], #float
            "mutIndividuo": dato[5], #float
            "mutGen": dato[6], #float
            "generaciones": dato[7],
            "espacios": dato[8],
            "costo": dato[9]
        }

        print( str(datos) )

        #tipo_paquetes_list = self.tipoPaquete()

        #diccionario_espacios_list = self.diccionarioEspacios(tipo_paquetes_list, int(dato[2]) )

        if ( len(generacion_anterior) == 0):            
            individuos = self.crearIndividuos( int(dato[0]), int(dato[2]))
            self.GENERACION_ORIGINAL = individuos
        else:
            individuos = generacion_anterior

        
        print('\nDiccionario espacios')
        for x in diccionario_espacios_list:
            print(x)
        
        print('\nIndividuos paquetes')
        for x in individuos:
            print(x)

        seleccion_TcT_list = self.seleccion( len(individuos) )

        print(seleccion_TcT_list)

        parejas_list = self.combinacion(seleccion_TcT_list, individuos)

        print('\nParejas y decendencia')
        for x in parejas_list:
            print(x)
        
        cruzar_lista = self.verificarDecendencia(parejas_list, int( dato[4] ) )

        print('\nCruzar esta lista')
        for x in cruzar_lista:
            print(x)
        
        #print( len(cruza_cortes_list))

        cruza_cortes_list = self.asignarCortes(cruzar_lista)
        print("\nCorte completa - [ original ] \n")                

        for cruzaDato in cruza_cortes_list:
            print(cruzaDato)


        cruzados_list = self.cruza(cruza_cortes_list)        
        
        print("      ------------ Cruza [Completa] ------------------------ ")
        print("\nCorte completa - [ original ] \n")        
        for orgDato in cruza_cortes_list:
            print(orgDato)

        print("\nCruza Completa - [ Cruzado ]\n")
        for cruzaDato in cruzados_list:
            print(cruzaDato)
        
        print("\n -------------------- Quita Repetidos [Completa] ----------------------------\n") 

        # --------------------------------------------------------------------------------
        cruza_faltantes_list = self.quitarRepetidos(cruzados_list)
        print("\nSin repetidos [lamada]: \n")
        for modificado in cruza_faltantes_list:
            print(modificado)

        # -------------------------------------------------------------------------------
        print("\n -------------------- Agrega Faltantes [ Completa ] ----------------------------\n")
        individuos_completos_list = self.agregarFaltantes(cruza_faltantes_list, cruza_cortes_list)

        print("\nImprimiendo complementados: \n")
        for dato in individuos_completos_list:
            print(dato)
        
        print("\n -------------------- Iniciar Mutacion [ Completa ] ----------------------------\n")
        
        individuoMutado_list = self.mutarIndividuos(individuos_completos_list, float(datos["mutGen"]), float(datos["mutIndividuo"]) )

        print("\nMuestra mutados:\n ")
        for x in individuoMutado_list:
            print(x)
        
        print("\n -------------------- PODA [ incompleta ] ----------------------------\n")

        Poda_list = self.verificar_PODA( int(datos["pM"]), individuoMutado_list , individuos, diccionario_espacios_list, int(datos["tamContenedor"]))

        print("\nMuestra Poda final:\n ")

        # {"Graficar": datos_Graficar, "Individuos_generacion": podado}
        print(Poda_list)

        generacion_actual = []
        print("\n-- Individuos_generacion --")
        for individuo in Poda_list[0]["Individuos_generacion"]:
            #print(individuo["Individuo"])
            print(individuo)
            generacion_actual.append(individuo["Individuo"])
        
        print("\n-- Graficar --")        
        print(Poda_list[0]["Graficar"])

        return [generacion_actual, Poda_list[0]["Graficar"], self.GENERACION_ORIGINAL]


    def crearIndividuos(self, pI, numPaquetes):

        individuos_list = []
        print("creando individuos: "+ str(pI))
        for i in range(pI):
            individuo_paquetes = random.sample(range(1, numPaquetes+1), numPaquetes)
            individuos_list.append(individuo_paquetes)

        return individuos_list

    def tipoPaquete(self, tipo_paquetes):
        print("Tipo paquetes")
        for x in tipo_paquetes:
            x["Espacio"] = int(x["Espacio"])
            x["Costo"] = int(x["Costo"])        
        
        return tipo_paquetes

    def diccionarioEspacios(self, tipo_paquetes_list, numPaquetes):
        diccionario_espacios_list = []

        for indice in range(0, numPaquetes):            
            #print(f"\nindice {indice}")
            tipoRand = random.randint(0, len(tipo_paquetes_list)-1)        
            diccionario_espacios_list.append(tipo_paquetes_list[tipoRand])

        diccionario_espacios_list = sorted(diccionario_espacios_list, key=lambda d: d['Tipo'], reverse=False)
        return diccionario_espacios_list
    
    def contarRepetidosDiccionario(self, diccionario_espacios_list):
        print("Contar repetidos")

        diccionario_espacios_list.sort()
        
        repetidos=[]
        conta=0
        contaSig = 0;
        
        Aux_diccionario_espacios_list=[]        
        
        listaActual =[]
        
        conta=0
        repet =""
        for x in diccionario_espacios_list:
            if repet != x:
                repet = x
                conta=0
                conta+=1
                x = x+ str(conta)
                listaActual.append(x)
            else:                
                x = x+ str(conta)
                listaActual.append(x)
                conta+=1

            #conta+=1
        print(" rep Act: "+str(listaActual)) 

        for dat in Aux_diccionario_espacios_list:
            print(dat)

        print('\n')

    def seleccion(self, pI):
        print('\nSeleccion todos con todos')

        seleccion=[]            

        auxDisminuir=2
        for x in range(1,pI):

            for j in range(auxDisminuir, pI+1):
                print("x: "+str(x)+" J: "+str(j))                                                
                combinacion=[x, j]
                seleccion.append(combinacion)        
            auxDisminuir+=1

        #print("seleccion tct: "+str(seleccion))        
        return seleccion
    
    def combinacion(self, seleccion, individuos):
        parejas = []
        print('\n combinacion')
        print("---->>>   Lista parejas: <<<-----")
        for pareja in seleccion:
            decendencia = ( random.randint(1, 100) ) / 100
            #print("pareja :> ",pareja)
            parejas.append({
                "id1":individuos[ int(pareja[0])-1 ],
                "id2":individuos[ int(pareja[1])-1 ],
                "decendencia": decendencia
                })            
            print(parejas)

        return parejas

    def verificarDecendencia(self, parejas_list,decendencia):
        cruzar = []
        """ print("\nDecendencia")
        print(parejas_list) """
        decendencia = decendencia/100
        print(str(decendencia), "%")

        for pareja in parejas_list:
            print( str(pareja['decendencia']) +" <= "+ str(decendencia))

            if( float( pareja['decendencia'] ) <= decendencia):
                cruzar.append(pareja)

        return cruzar

    def asignarCortes(self, cruzar_list):
        print(f"\nCortes para num list cruza: { len(cruzar_list) }")
        if( len(cruzar_list)==0):
            print('>> Ninguno entro en probabilidad de decendencia')
            return []
        
        print('\n')
        print('>> Entra en probabilidad de decendencia')
        for dato in cruzar_list:
            print(dato)

        punto_corte = 2        
        
        puntos_corte_disponible = len( cruzar_list[0]['id1'] )-1
        print(f'\nPuntos dispobibles: {puntos_corte_disponible}')


        print('\nAgregando corte')

        cruza_con_cortes = []
        for dato in cruzar_list:

            puntos_corte_list = random.sample(range(1, puntos_corte_disponible+1), punto_corte)
            puntos_corte_list.sort()
            dato.update( {'Cortes' : puntos_corte_list } )
            cruza_con_cortes.append(dato)            

        print("\nCortes add")
        for index in cruza_con_cortes:
            print(index)

        return cruza_con_cortes
    
    def cruza(self, cruza_cortes_list):
        print("\nCruzando\n")

        # ----------------------------------------------------------
        if len(cruza_cortes_list)==0:
            print('No hay hay datos para cruzar [def] ')
            return []                    
        # ----------------------------------------------------------
        
        corte_auxiliar =  cruza_cortes_list
        cruzado = []
        for x in corte_auxiliar:
            #print(x)            
            #print("\n Corte: ")
                    
            corte_1 = x['Cortes'][0]
            corte_2 = x['Cortes'][1]
            
            lista1_aux = x['id1']
            lista2_aux = x['id2']

            part1_Par1 = []
            part2_Par1 = []
            part3_Par1 = []

            part1_Par2 = []
            part2_Par2 = []
            part3_Par2 = []

            for index in range( len(lista1_aux) ):
                if(index < corte_1):                    
                    part1_Par1.append(lista1_aux[index])

                if(index < corte_2 and index >= corte_1):                    
                    part2_Par1.append(lista1_aux[index])

                if(index >= corte_2):                    
                    part3_Par1.append(lista1_aux[index])
            #----------------------------------------
            
            for index_2 in range( len(lista2_aux) ):
                if(index_2 < corte_1):                    
                    part1_Par2.append(lista2_aux[index_2])

                if(index_2 < corte_2 and index_2 >= corte_1):                    
                    part2_Par2.append(lista2_aux[index_2])
                    
                if(index_2 >= corte_2):                    
                    part3_Par2.append(lista2_aux[index_2])            

            id1_cruzado = part1_Par1 + part2_Par2 + part3_Par1
            id2_cruzado = part1_Par2 + part2_Par1 + part3_Par2
            
            cruzado.append( {"id1": id1_cruzado, "id2":id2_cruzado, "Corte": [corte_1, corte_2]} )    

        return cruzado
    
    def quitarRepetidos(self, cruzados_list):
        print("\nQuitando repetidos:\n")
 
        print('cruzados')
        for i in cruzados_list:
            print(i)

        print('\n<------- Quitando deuplicados ------>')        

        cruzado_sin_duplicados = []
        
        for i in cruzados_list:
            list_1 = i["id1"]
            list_2 = i["id2"]            
        
            lista_1_sin_repetdo = self.quitaRepetido(list_1)
            lista_2_sin_repetdo = self.quitaRepetido(list_2)
            
            cruzado_sin_duplicados.append( { "id1": lista_1_sin_repetdo, "id2":lista_2_sin_repetdo } ) 

        return cruzado_sin_duplicados
    
    def quitaRepetido(self, lista):        

        resultantList = []        
        for element in lista:
            if element not in resultantList:
                resultantList.append(element)

        return resultantList

    def agregarFaltantes(self,  cruza_faltantes_list,  cruza_cortes_list):
        print("\nAgregando faltantes:\n")

        cruza_completa = []

        print("Faltantes")
        for x in cruza_faltantes_list:
            print(x)
        
        print("original")
        for y in cruza_cortes_list:
            print(y)

        for index in range( len(cruza_cortes_list) ) :
            #print(index)
            datoOrigin = cruza_cortes_list[index]["id2"]
            datoFalta  = cruza_faltantes_list[index]["id1"]

            print("\n>>>>>>>>>>    Ver faltantes y original <<<<<<<<<<<<< \n")
            print(datoOrigin)
            print(datoFalta)
            print(" - - - - - - - - - - - - - -- - - - - -\n")

            for j in datoOrigin:
                existe = False
                for i in datoFalta:
                    if(j == i):
                        existe = True
                        #print("encontrado:", str(j))
                if (existe==False):
                    print("Agregado:", str(j))
                    datoFalta.append(j)
            
            print( "Individuo complementado: " ,str(datoFalta))
            cruza_completa.append(datoFalta)

        return cruza_completa

    def mutarIndividuos(self, individuos_mutar, mutGen, mutIndividuo):
        print("\nIniciando mutacion:\n")

        mutIndividuo = mutIndividuo/100        

        mutados_list = []
        for individuo in individuos_mutar:
            
            probabilidadMutacionIndi = (random.randint(1, 100)) / 100

            if (probabilidadMutacionIndi < mutIndividuo ):
                individuo_mutado = self.agregarMutacionGen(individuo, mutGen)
                mutados_list.append(individuo_mutado)
            else:
                mutados_list.append(individuo)

        return mutados_list

    def agregarMutacionGen(self, individuos_mutar, mutGen):
        print("\nMutar Gen: \n")        
        mutGen = mutGen/100
        print( str(mutGen), "%")

        for x in range(1, len(individuos_mutar) ):
            #print( "\n >> dato mutar: __________________ ",str(individuos_mutar[ x-1 ]))
            probabilidadMutacionGen = (random.randint(1, 100)) / 100
            #print(">> individuo original: ", str(individuos_mutar) )
            
            if (probabilidadMutacionGen < mutGen):                
                lugar = (random.randint(1, len(individuos_mutar)))
                print("\nlugar a: ", str(lugar), " x:", str(x)," \n")
                while lugar == x and lugar > 0:
                    lugar = (random.randint(1, len(individuos_mutar)))
                print("\nlugar b: ", str(lugar), " x:", str(x)," \n")

                inter_1 = individuos_mutar[x-1]
                inter_2 = individuos_mutar[lugar-1]

                individuos_mutar[x-1] = inter_2
                individuos_mutar[lugar-1] = inter_1
                #print("\n>> mutado: ----------------------", str( individuos_mutar ) , " + lugar: ", lugar,"")
            """ else:
                print("\n>> No muto: --------------------- ", str( individuos_mutar ),"") """
        
        return individuos_mutar
            
    def verificar_PODA(self, pM, individuoMutado_list, individuosInicial_list, diccionario_espacios_list, tamContenedor ):

        print("\nIniciando PODA:\n")
        individuos_completos = individuosInicial_list + individuoMutado_list

        podado = []
        if( len(individuos_completos) > pM ):
            print("\nInicia PODA:\n")
            ganacias_list = self.obtenerGanancias(individuos_completos, pM, diccionario_espacios_list, tamContenedor)
            return self.Poda_iniciar(ganacias_list, pM)

        # Graficar = {"maximo": maximo, "minimo": minimo, "promedio": proedio}
        # Individuos_generacion = {"Graficar": datos_Graficar, "Individuos_generacion": podado}

        else:
            print("\nNo hay PODA:\n")
            ganacias_list = self.obtenerGanancias(individuos_completos, pM, diccionario_espacios_list, tamContenedor)
            return self.Poda_iniciar(ganacias_list, pM)
        # Graficar = {"maximo": maximo, "minimo": minimo, "promedio": proedio}
        # Individuos_generacion = {"Graficar": datos_Graficar, "Individuos_generacion": podado}
    
    def obtenerGanancias(self, individuoMutado_list, pM, diccionario_espacios_list, tamContenedor):
        print(f"PODA _ poblacion maxima: {pM}")
        individuo_ganancia = []

        for individuo in individuoMutado_list:
            print("Indivi: " ,individuo)
            peso=0
            costo = 0
            for paquete in individuo:                
                                
                peso = peso + diccionario_espacios_list[paquete-1]["Espacio"]
                if (peso <= tamContenedor):
                    costo += diccionario_espacios_list[paquete-1]["Costo"]

                    print("individuo: ", individuo, " -Costo: ", costo, " -peso: ", peso, " -contenedor:", tamContenedor)
                    #print(f"ultimo: {paquete} - individuo: {individuo}")
                else:
                    peso = peso - diccionario_espacios_list[paquete-1]["Espacio"]
                    break
            print("individuo: ", individuo, " -Costo: ", costo, " -peso: ", peso, " -contenedor:", tamContenedor, "\n----")
            individuo_ganancia.append({
                "Individuo": individuo, 
                "Ganancia": costo, 
                "Espacio": peso, 
                "Contenedor": tamContenedor
                })

        return individuo_ganancia

    def Poda_iniciar(self, podado, pM):
        podado_list = []
        print("\nOrdenar\n")

        podado = sorted(podado, key=lambda individuo: individuo["Ganancia"], reverse=True)

        print("\nAntes de PODA:")
        for x in podado:
            print(x)
        
        datos_Graficar = self.datos_graficar(podado) # {"maximo": maximo, "minimo": minimo, "promedio": proedio}
                
        if ( pM < len(podado) ):
            podado = podado[:pM]
            print("\nPODA completa:")
            for x in podado:
                print(x)
        # Graficar = {"maximo": maximo, "minimo": minimo, "promedio": proedio}
        # Individuos_generacion = {"Graficar": datos_Graficar, "Individuos_generacion": podado}
        podado_list.append( {"Graficar": datos_Graficar, "Individuos_generacion": podado} ) #{"Graficar": datos_Graficar, "Individuos_generacion": podado}
        
        print(" \n>>>>>>>>>>>>>>>>  Max Min Prom    <<<<<<<<<<<<<<<<<<<<<<<<<< \n")
        print(datos_Graficar)
        print(" \n>>>>>>>>>>>>>>>>  ---------    <<<<<<<<<<<<<<<<<<<<<<<<<< \n")

        # datos_Graficar
        return podado_list
    
    def datos_graficar(self, podado):        
        print("Datos graficar")

        maximo = podado[0]["Ganancia"]
        minimo = podado[-1]["Ganancia"]

        suma = 0
        for i in range(0, len(podado) ):
            print(i)
            suma += podado[i]["Ganancia"]
        
        proedio = suma/ (len(podado) )
        print(suma, " / ", len(podado))

        return {"maximo": maximo, "minimo": minimo, "promedio": proedio}



#quede acomodando al PODa
#para graficar con y sin poda