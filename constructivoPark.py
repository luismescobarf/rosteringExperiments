#Constructivo (Park, 2001) adaptado a Rostering -> Rotación de personal
#----------------------------------------------------------------------

#Librerías
#---------
import cargaInstancias #Librería con funcionalidades desarrolladas para gestión de las instancias
import json
import pprint as pp 
import random

#Definición de funciones específicas del constructivo
#----------------------------------------------------

#Función para inicializar la programación del empleado dependiendo de la instancia
def generarProgramacionEmpleado(horizonteTiempo, tiposTurno):
    
    #Inicializar el diccionario contenedor
    programacionEmpleado = dict()
    
    #Inicializar valores
    programacionEmpleado['cerrada'] = False
                
    #Forma resumida -> genera problemas por enlazado o referencia de las listas
    #programacionEmpleado['itinerario'] = [ [ ] ] * len(horizonteTiempo)
    
    #Forma explícita de agregar diccionarios vacíos de turnos en el listado de días del cuadro de turnos del empleado
    programacionEmpleado['itinerario'] = list()
    [programacionEmpleado['itinerario'].append(dict()) for _ in range(len(horizonteTiempo))]
    
    programacionEmpleado['totalDiasLibre'] = len(horizonteTiempo)    
    programacionEmpleado['diasTrabajo'] = 0    
    programacionEmpleado['conteoTiposTurno'] = dict()
    for tipoTurno in tiposTurno:
        programacionEmpleado['conteoTiposTurno'][tipoTurno] = 0            
    programacionEmpleado['diasLibreConsecutivos'] = len(horizonteTiempo)    
    
    #Retornar una copia (evitar paso por referencia por defecto de Python)
    return programacionEmpleado.copy()

#Función para obtener el número de días consecutivos libres de un itinerario
def numeroDiasLibresConsecutivos(programacionEnRevision, horizonteTiempo):
    #Inicializar bandera que controla la revisión
    revision = True    
    longitudSecuencia = 0 #Ninguna secuencia detectada aún    
    i = 0 #Aumento del alcance de la variable        
    #Bucle que detecta la mayor secuencia con días libres
    while revision:
        #Inicializar la longitud de la secuencia actual (para comparar con la burbuja)
        longitudSecuenciaActual = 0
        #Realizar el conteo de cada secuencia
        #while i < len(horizonteTiempo):            
        while i < horizonteTiempo:            
            #Si el día actual está libre
            #if programacionEnRevision['itinerario'][i] == list():
            if programacionEnRevision['itinerario'][i] == dict():
                longitudSecuenciaActual += 1
                i += 1
            else:#El día no está libre, se rompe la secuencia
                #Revisar si la mayor longitud se supera
                if longitudSecuenciaActual > longitudSecuencia:
                    longitudSecuencia = longitudSecuenciaActual                
                #Mover el día para la búsqueda de la siguiente secuencia
                i += 1                
                break #Terminación de la secuencia actual       
        #Si la revisión ha llegado al final romper el bucle general
        #if i == len(horizonteTiempo)-1:
        if i == horizonteTiempo-1:
            break
    #Al finalizar todo el proceso, retornar la longitud mayor
    return longitudSecuencia

#Función para incorporar turno en el itinerario de un empleado (actualización de indicadores)
#--------------------------------------------------------------------------------------------
def incorporarTurno(programacionEnActualizacion, turnoEntrante):
    
    # #Salida de diagnóstico
    # print("Valores recibidos:")    
    # print("ProgramacionEnActualizacion")
    # pp.pprint(programacionEnActualizacion)
    # print("TurnoEntrante")
    # pp.pprint(turnoEntrante)    
    
    #Actualización por referencia del itinerario
    programacionEnActualizacion['itinerario'][ turnoEntrante['indiceDia']  ] = turnoEntrante
    
    #Actualizar los demás valores    
    programacionEnActualizacion['totalDiasLibre'] -= 1 
    programacionEnActualizacion['diasTrabajo'] += 1
    programacionEnActualizacion['conteoTiposTurno'][turnoEntrante['tipoTurno']] += 1
    
    #Actualización del número de días libre consecutivos
    programacionEnActualizacion['diasLibreConsecutivos'] = numeroDiasLibresConsecutivos(programacionEnActualizacion, len(programacionEnActualizacion['itinerario']))
    
    
    # #Mostrar actualización dentro de la función (diagnóstico)
    # print("------------------")
    # print("Estado del itinerario dentro d ela función")    
    # pp.pprint(programacionEnActualizacion)    
    # print("------------------")
    
    #Continuar acá con las otras actualizaciones
    #Continuar acá con las otras actualizaciones 
    
    

#Función para revisar cumplimiento de secuencias y condiciones en una programación de un empleado
def cumplimientoCondiciones(programacionEnRevision, turnoEntrante):
    
    #Revisar si el día está libre
    if programacionEnRevision['itinerario'][ turnoEntrante['indiceDia'] ] == list():
        
        #Revisar secuencias prohibidas
    
        #Revisar límites de ocupación        
        
        #Revisar número de días libres consecutivos en el itinerario
        
        #Revisar si cumple el número de días mínimo y máximo de cada tipo de turno
        
        #Si cumple todas las condiciones, retornar verdadero para que sea incorporado
        if(all[True,
               True]):
            #Reportar viabilidad al cumplir todas las condiciones
            return True
        else:
            #Reportar inviabilidad al incumplir alguna de las condiciones para incorporación
            return False
        
    else:
        #Si el día no está libre, reportar inviabilidad de la incorporación en el itinerario
        return False


#Sección principal
#-----------------

#Carga de la instancia que se va a trabajar
instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example1.json")

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
            
#Salida pedazos (turnos) de la matriz de requerimientos            
print("---------------------------")
print("Salida del listado plano de pedazos de turno (base codificación Park 2001): ")
for i,turnoK in enumerate(listadoTurnosPlano):
    print(f"Turno {i}: {turnoK}")
print("---------------------------")
    
#Establacer un orden (aleatorio o no) para recorrer esos pedazos
ordenCoberturaTurnos = list(range(len(listadoTurnosPlano)))
random.shuffle(ordenCoberturaTurnos)

#Salida de diagnóstico
print("---------------------------")
print("Orden de cobertura de turnos: ")
print(ordenCoberturaTurnos)
print("---------------------------")

#Recorrer los pedazos y acomodarlos entre el personal disponible
cuadroTurnos = list()

#Obtener los tipos de turno
tiposTurnoInstancia = list(instancia['detalleTurnos'].keys())
#Agregar turno vacío o de descanso
tiposTurnoInstancia.append("-")

# #Salida de diagnóstico
# print(f"Tipos de turno: {tiposTurnoInstancia} - tipo del contenedor: {type(tiposTurnoInstancia)}")
# input()#Pausa de ejecución

#Abrir la programación del primer empleado con el primer turno del orden de cobertura
cuadroTurnos.append(generarProgramacionEmpleado(dias,tiposTurno))

# #Salidas de diagnóstico de la creación del cuadro de turnos y primer turno
# print("Declaración del cuadro de turnos: ")
# pp.pprint(cuadroTurnos)
# print("---------")
# print("Diagnóstico del tipado del cuadro de turnos y el primer turno:")
# print(len(cuadroTurnos[-1]['itinerario']))
# [ print(type(elemento)) for elemento in cuadroTurnos[-1]['itinerario'] ]
# print(f"Indice del dia: {listadoTurnosPlano[ordenCoberturaTurnos[0]]['indiceDia']}")
# print(f"Tipado de la posición: {type(cuadroTurnos[-1]['itinerario'][ listadoTurnosPlano[ordenCoberturaTurnos[0]]['indiceDia'] ])}")
# print("---------")

#Reemplazar esta forma de agregar por incorporar (actualizando los parámetros)
#cuadroTurnos[-1]['itinerario'][ listadoTurnosPlano[ordenCoberturaTurnos[0]]['indiceDia'] ].append(listadoTurnosPlano[ ordenCoberturaTurnos[0] ]) 
#cuadroTurnos[-1]['itinerario'][ listadoTurnosPlano[ordenCoberturaTurnos[0]]['indiceDia'] ] = listadoTurnosPlano[ ordenCoberturaTurnos[0] ]

#Llamado a la incorporación adecuada
incorporarTurno(cuadroTurnos[-1], listadoTurnosPlano[ ordenCoberturaTurnos[0] ] )


#Salida de diagnóstico
print("Estado del cuadro de turnos después de inicializar (incorporar):")
pp.pprint(cuadroTurnos)

#Seccionar la programación del empleado según los días o el horizonte de tiempo
#Cada tripulante es un elemento de la lista cuadroTurnos, 
# y se representará con un diccionario que contiene la lista de turnos y otros indicadores
#cuadroTurnos.append(listadoTurnosPlano[ordenCoberturaTurnos[0]])

#Acomodar los demás turnos en el cuadro con la estrategia Park, 2001
for i in range(1,len(ordenCoberturaTurnos)):
    
    #Ejemplo de recorrido con la variación del subíndice
    #ordenCoberturaTurnos[i]
    
    #Por cada turno:
    """
    1) Tomar la programación en actualización e incorporar turno de la iteración actual (i-ésimo turno)
    2) Revisar condiciones: 
    2a) Si se cumplen continuar con el siguiente turno en la secuencia (turno i+1)
    2b) Si no se cumplen, descartar la secuencia 
    """
    
    pass