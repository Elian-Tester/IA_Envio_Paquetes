import random

class Envio():

    ABECEDARIO = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    def enviando(self, dato):        
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

        tipo_paquetes_list = self.tipoPaquete()

        diccionario_espacios_list = self.diccionarioEspacios(tipo_paquetes_list, int(dato[2]) )

        individuos = self.crearIndividuos( int(dato[0]), int(dato[2]))

        
        print('\nDiccionario espacios')
        for x in diccionario_espacios_list:
            print(x)
        
        print('\nIndividuos paquetes')
        for x in individuos:
            print(x)

        seleccion_TcT_list = self.seleccion( int(dato[0]) )

        print(seleccion_TcT_list)

        parejas_list = self.combinacion(seleccion_TcT_list, individuos)

        print('\nParejas y decendencia')
        for x in parejas_list:
            print(x)
        
        cruzar_lista = self.verificarDecendencia(parejas_list, int( dato[4] ) )

        print('\nCruzar esta lista')
        for x in cruzar_lista:
            print(x)

        cruzado_list = self.cruzar(cruzar_lista)
        #Inciando cruza y acomdo de repetidos al cruzar



    def crearIndividuos(self, pI, numPaquetes):

        individuos_list = []
        print("creando individuos: "+ str(pI))
        for i in range(pI):
            individuo_paquetes = random.sample(range(1, numPaquetes+1), numPaquetes)                    
            individuos_list.append(individuo_paquetes)

        return individuos_list

    def tipoPaquete(self):
        print("Tipo paquetes")

        tipos_paquete_lista = []

        
        for i in range(1, 4):
            espacio = random.randint(1, 10)
            costo = random.randint(1, 20)

            paquete = {"Tipo": self.ABECEDARIO[i-1], "Espacio": espacio, "Costo": costo}
            tipos_paquete_lista.append(paquete)
        
        return tipos_paquete_lista

    def diccionarioEspacios(self, tipo_paquetes_list, numPaquetes):
        diccionario_espacios_list = []

        for indice in range(0, numPaquetes):            
            print(f"\nindice {indice}")
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
        
        for pareja in seleccion:
            decendencia = ( random.randint(1, 100) ) / 100
            parejas.append({
                "id1":individuos[ int(pareja[0])-1 ],
                "id2":individuos[ int(pareja[1])-1 ],
                "decendencia": decendencia
                })

        return parejas

    def verificarDecendencia(self, parejas_list,decendencia):
        cruzar = []
        print("\nDecendencia")
        print(parejas_list)
        decendencia = decendencia/100
        print(decendencia)

        for pareja in parejas_list:
            print( str(pareja['decendencia']) +" <= "+ str(decendencia))

            if( float( pareja['decendencia'] ) <= decendencia):
                cruzar.append(pareja)

        return cruzar

    def cruzar(self, cruzar_list):
        print("\nCruzando")
        print(cruzar_list)