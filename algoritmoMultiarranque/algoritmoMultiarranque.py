#Constructivo (Park, 2001) adaptado a Rostering -> Rotación de personal
#----------------------------------------------------------------------

#Librerías
#---------
import cargaInstancias #Librería con funcionalidades desarrolladas para gestión de las instancias
import funcionesConstructivoPark as fc
import constructivosRostering as cr
import json
import pprint as pp 
import random
from copy import deepcopy
from time import perf_counter

#Sección principal
#-----------------

#Carga del listado de instancias
nombresInstancias = list()
# nombresInstancias.append("../instancias/versionJSON/Example1.json")
# nombresInstancias.append("../instancias/versionJSON/Example2.json")
# nombresInstancias.append("../instancias/versionJSON/Example3.json")
# nombresInstancias.append("../instancias/versionJSON/Example4.json")
# nombresInstancias.append("../instancias/versionJSON/Example5.json")
# nombresInstancias.append("../instancias/versionJSON/Example6.json")
# nombresInstancias.append("../instancias/versionJSON/Example7.json")
# nombresInstancias.append("../instancias/versionJSON/Example8.json")
# nombresInstancias.append("../instancias/versionJSON/Example9.json")
# nombresInstancias.append("../instancias/versionJSON/Example10.json")
# nombresInstancias.append("../instancias/versionJSON/Example11.json")
# nombresInstancias.append("../instancias/versionJSON/Example12.json")
# nombresInstancias.append("../instancias/versionJSON/Example13.json")
# nombresInstancias.append("../instancias/versionJSON/Example14.json")
# nombresInstancias.append("../instancias/versionJSON/Example15.json") #Revisar 
# nombresInstancias.append("../instancias/versionJSON/Example16.json")
# nombresInstancias.append("../instancias/versionJSON/Example17.json") #Revisar
nombresInstancias.append("../instancias/versionJSON/Example18.json")
# nombresInstancias.append("../instancias/versionJSON/Example19.json")
# nombresInstancias.append("../instancias/versionJSON/Example20.json")

#Recorrer las instancias cargadas en el listado correspondiente
for nombreInstancia in nombresInstancias:
        
    #Carga de la instancia
    instancia = cargaInstancias.cargaVersionJSON(nombreInstancia)

    #Partir la matriz de requerimientos en pedazos y formar un listado
    #-----------------------------------------------------------------
    listadoTurnosPlano = list()
    #Arreglo de los tipos de turno
    tiposTurno = list(instancia['detalleTurnos'].keys())

    #Arreglo con los días (esto puede variar según el horizonte de tiempo)
    dias = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
    for i,tipoTurno in enumerate(instancia['matrizRequerimientos']):
        for j,dia in enumerate(tipoTurno):
            for k in range(dia):
                listadoTurnosPlano.append({
                    'dia': dias[j],
                    'indiceDia': j,
                    'tipoTurno': tiposTurno[i]                        
                })
                
    #Revisar instancia cargada (adición de versión tipo string de las secuencias no permitidas)
    # print("---------------------------")
    # pp.pprint(instancia)
    # print("---------------------------")
    #input()#Detener ejecución para revisión
                
    #Salida pedazos (turnos) de la matriz de requerimientos            
    # print("---------------------------")
    # print("Salida del listado plano de pedazos de turno (base codificación Park 2001): ")
    # for i,turnoK in enumerate(listadoTurnosPlano):
    #     print(f"Turno {i}: {turnoK}")
    # print("---------------------------")
        
    # #Establacer un orden (aleatorio o no) para recorrer esos pedazos (ejemplo único arranque)
    # ordenCoberturaTurnos = list(range(len(listadoTurnosPlano)))
    # random.shuffle(ordenCoberturaTurnos)

    #Generar los arranques (población) según el número de pedazos de programación
    listadoArranques = list()
    while len(listadoArranques) < len(listadoTurnosPlano):
        
        #Establacer un orden (aleatorio o no) para recorrer los pedazos de turno
        ordenCoberturaTurnos = list(range(len(listadoTurnosPlano)))
        random.shuffle(ordenCoberturaTurnos)
        
        #Revisar si está repetido antes de incorporar en el listado de arranques
        if ordenCoberturaTurnos not in listadoArranques:
            listadoArranques.append(ordenCoberturaTurnos)
            
    #Estructura para la incumbente, iniciando en infinito
    incumbente = {
            'cuadroTurnos': dict(),
            'empleadosOcupados' : float("inf"),
            'numeroTotalTurnosCargados' : len(listadoTurnosPlano)
        }
    
    #Inicio de la toma de tiempo
    t1_start = perf_counter()

    #Construir con cada uno de los arranques
    for ordenCoberturaTurnos in listadoArranques:    
        solucionActual = cr.constructivoPark(instancia, ordenCoberturaTurnos)
        if solucionActual['empleadosOcupados'] < incumbente['empleadosOcupados']:
            incumbente = solucionActual.copy()

    #Finalización de la toma de tiempo
    t1_stop = perf_counter()

    #Captura del tiempo transcurrido
    tiempoTranscurrido = t1_stop-t1_start

    #Revisión de factibilidad
    factibilidadAlcanzada = 'Si' if incumbente['empleadosOcupados'] <= instancia['numeroEmpleados'] else 'No'

    #Reportar número de operadores o empleados ocupados con la secuencia aleatoria utilizada
    print('-------------------------------------------------')
    print('Reporte del constructivo multiarranque')
    print('-------------------------------------------------')
    print(f"Nombre Caso: {instancia['nombreCaso']}")
    print(f"Numero Operadores Ocupados: {incumbente['empleadosOcupados']}")
    print(f"Numero Operadores Disponibles: { instancia['numeroEmpleados']}")
    print(f"Tiempo transcurrido en segundos: {tiempoTranscurrido}")
    print(f"Turnos Cubiertos: {incumbente['numeroTotalTurnosCargados']}")
    print(f"Turnos Instancia: {len(listadoTurnosPlano)}")
    print(f"Factibilidad: { factibilidadAlcanzada }")
    print('-------------------------------------------------')
    print()
    # input()#Pausa para revisar el resultado de cada instancia