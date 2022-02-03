#Constructivo (Park, 2001) adaptado a Rostering -> Rotación de personal

#Librerías
import cargaInstancias
import json
import pprint as pp 
import random

#Sección principal
#-----------------

#Carga de la instancia que se va a trabajar
instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example1.json")

#Partir la matriz de requerimientos en pedazos y formar un listado

listadoTurnosPlano = list()
#Arreglo de los tipos de turno
tiposTurno = list(instancia['detalleTurnos'].keys())

#Arreglo con los días
dias = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
for i,tipoTurno in enumerate(instancia['matrizRequerimientos']):
    for j,dia in enumerate(tipoTurno):
        for k in range(dia):
            listadoTurnosPlano.append({
                'dia': dias[j],
                'indiceDia': j,
                'tipoTurno': tiposTurno[i]                        
            })
            
#Salida pedazos (turnos) de la matriz de requerimientos            
for i,turnoK in enumerate(listadoTurnosPlano):
    print(f"Turno {i}: {turnoK}")
    
#Establacer un orden (aleatorio o no) para recorrer esos pedazos
ordenCoberturaTurnos = list(range(len(listadoTurnosPlano)))
random.shuffle(ordenCoberturaTurnos)

# #Salida de diagnóstico
# print(ordenCoberturaTurnos)

#Recorrer los pedazos y acomodarlos entre el personal disponible
cuadroTurnos = list()

#Abrir la programación del primer empleado

#Seccionar la programación del tripulante según los días o el horizonte de tiempo
#Cada tripulante es un elemento de la lista cuadroTurnos, 
# y se representará con un diccionario que contiene la lista de turnos y otros indicadores
#cuadroTurnos.append(listadoTurnosPlano[ordenCoberturaTurnos[0]])

#Acomodar los demás turnos en el cuadro con la estrategia Park, 2001
for i in ordenCoberturaTurnos:
    pass
    


