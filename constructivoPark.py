#Constructivo (Park, 2001) adaptado a Rostering -> Rotación de personal
#----------------------------------------------------------------------

#Librerías
#---------
import cargaInstancias
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
    programacionEmpleado['itinerario'] = [ [ ] ] * len(horizonteTiempo)
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
        while i < len(horizonteTiempo):            
            #Si el día actual está libre
            if programacionEnRevision['itinerario'][i] == list():
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
        if i == len(horizonteTiempo)-1:
            break
    #Al finalizar todo el proceso, retornar la longitud mayor
    return longitudSecuencia

#Función para incorporar turno en el itinerario de un empleado (actualización de indicadores)
#--------------------------------------------------------------------------------------------
def incorporarTurno(programacionEnActualizacion, turnoEntrante, numeroDiasLibresConsecutivos):
    
    #Actualización por referencia del itinerario
    programacionEnActualizacion['itinerario'][ turnoEntrante['indiceDia']  ] = turnoEntrante['indiceDia']
    
    #Actualizar los demás valores    
    programacionEnActualizacion['totalDiasLibre'] -= 1 
    programacionEnActualizacion['diasTrabajo'] += 1
    programacionEnActualizacion['conteoTiposTurno'][turnoEntrante['tipoTurno']] += 1
    
    #Actualización del número de días libre consecutivos
    
    
    #Continuar acá
    #Continuar acá
    #Continuar acá
    
    

#Función para revisar cumplimiento de secuencias y condiciones en una programación de un empleado
def cumplimientoCondiciones(programacionEnRevision, turnoEntrante):
    
    #Revisar si el día está libre
    if programacionEnRevision['itinerario'][ turnoEntrante['indiceDia'] ] == list():
        
        #Revisar secuencias prohibidas
    
        #Revisar límites de ocupación        
        
        #Revisar número de días libres consecutivos en el itinerario        
        
        #Si cumple todas las condiciones, retornar verdadero para que sea incorporado
        if(all[True,True]):
            return True
        
    else:
        #Si el día no está libre, reportar inviabilidad de la incorporación en el itinerario
        return False


#Sección principal
#-----------------

#Carga de la instancia que se va a trabajar
instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example1.json")

#Partir la matriz de requerimientos en pedazos y formar un listado

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
for i,turnoK in enumerate(listadoTurnosPlano):
    print(f"Turno {i}: {turnoK}")
    
#Establacer un orden (aleatorio o no) para recorrer esos pedazos
ordenCoberturaTurnos = list(range(len(listadoTurnosPlano)))
random.shuffle(ordenCoberturaTurnos)

#Salida de diagnóstico
print(ordenCoberturaTurnos)

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
cuadroTurnos[-1]['itinerario'][ listadoTurnosPlano[ordenCoberturaTurnos[0]]['indiceDia']  ] = listadoTurnosPlano[ ordenCoberturaTurnos[0] ] 

#Salida de diagnóstico
print("Cuadro de turnos:")
print(cuadroTurnos)

#Seccionar la programación del empleado según los días o el horizonte de tiempo
#Cada tripulante es un elemento de la lista cuadroTurnos, 
# y se representará con un diccionario que contiene la lista de turnos y otros indicadores
#cuadroTurnos.append(listadoTurnosPlano[ordenCoberturaTurnos[0]])

#Acomodar los demás turnos en el cuadro con la estrategia Park, 2001
for i in range(1,len(ordenCoberturaTurnos)):
    
    #Ejemplo de recorrido
    #ordenCoberturaTurnos[i]
    
    pass