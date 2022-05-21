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
    programacionEmpleado['diasTrabajandoConsecutivos'] = 0
    
    #Retornar una copia (evitar paso por referencia por defecto de Python)
    return programacionEmpleado.copy()

#Función para obtener el número de días consecutivos libres de un itinerario
def numeroDiasLibresConsecutivos(programacionEnRevision, horizonteTiempo):
    
    #Estructura para acumular el tamaño de las secuencias con días libres consecutivos
    tamaniosSecuenciasLibres = []     
    
    #Inicializar la longitud de la secuencia actual
    longitudSecuenciaActualLibres = 0        
    
    #Recorrer todo el horizonte de tiempo
    for i in range(horizonteTiempo):          
        
        #Si el día actual del empleado está libre
        if programacionEnRevision['itinerario'][i] == dict():
            longitudSecuenciaActualLibres += 1                
        else:#El día no está libre, se rompe la secuencia                                
            #Acumular el tamaño de secuencia (si es diferente de cero)
            if longitudSecuenciaActualLibres != 0:                
                tamaniosSecuenciasLibres.append(longitudSecuenciaActualLibres)
            #Reiniciar el tamaño de la secuencia
            longitudSecuenciaActualLibres = 0
            
    #Revisar cuando los días libres llegan hasta el final del horizonte de tiempo y no se descargó la secuencia
    if longitudSecuenciaActualLibres !=0:
        tamaniosSecuenciasLibres.append(longitudSecuenciaActualLibres)        
    
    #Al finalizar todo el proceso, retornar la longitud mayor   
    if tamaniosSecuenciasLibres == list():
        return 0#Asegurar el retorno si no se encuentran secuencias de días libres   
    else:
        return max(tamaniosSecuenciasLibres)#Retornar la secuencia más larga encontrada
    
    
#Función para obtener el número de días consecutivos ocupados en la programación de un empleado
def numeroDiasTrabajandoConsecutivos(programacionEnRevision, horizonteTiempo):
    
    #Estructura para acumular el tamaño de las secuencias con días ocupados consecutivos
    tamaniosSecuenciasOcupados = []     
    
    #Inicializar la longitud de la secuencia actual
    longitudSecuenciaActual = 0        
    
    #Recorrer todo el horizonte de tiempo
    for i in range(horizonteTiempo):          
        
        #Si el día actual del empleado está ocupado
        if programacionEnRevision['itinerario'][i] != dict():
            longitudSecuenciaActual += 1                
        else:#El día está libre, se rompe la secuencia                                
            #Acumular el tamaño de secuencia (si es diferente de cero)
            if longitudSecuenciaActual != 0:                
                tamaniosSecuenciasOcupados.append(longitudSecuenciaActual)
            #Reiniciar el tamaño de la secuencia
            longitudSecuenciaActual = 0
            
    #Revisar cuando los días libres llegan hasta el final del horizonte de tiempo y no se descargó la secuencia
    if longitudSecuenciaActual !=0:
        tamaniosSecuenciasOcupados.append(longitudSecuenciaActual)        
        
    #Salida de diagnóstico
    print("---------------")
    print(f"Estado de detección de secuencias ocupadas (bloques de trabajo encadenados) {tamaniosSecuenciasOcupados}")
    print("---------------")
    
    #Al finalizar todo el proceso, retornar la longitud mayor   
    if tamaniosSecuenciasOcupados == list():
        return 0#Asegurar el retorno si no se encuentran secuencias de días trabajados   
    else:
        return max(tamaniosSecuenciasOcupados)#Retornar la secuencia más larga encontrada
    
    

#Función para incorporar turno en el itinerario de un empleado (actualización de indicadores)
#--------------------------------------------------------------------------------------------
def incorporarTurno(programacionEnActualizacion, turnoEntrante):
    
    #Revisión de disponibilidad antes de incorporar y validar
    if programacionEnActualizacion['itinerario'][ turnoEntrante['indiceDia']  ] == dict():
                
        #Actualización por referencia del itinerario
        programacionEnActualizacion['itinerario'][ turnoEntrante['indiceDia']  ] = turnoEntrante
        
        #Actualizar los demás valores    
        programacionEnActualizacion['totalDiasLibre'] -= 1 
        programacionEnActualizacion['diasTrabajo'] += 1
        programacionEnActualizacion['conteoTiposTurno'][turnoEntrante['tipoTurno']] += 1       
        
        
        #Actualización del número de días libre consecutivos
        programacionEnActualizacion['diasLibreConsecutivos'] = numeroDiasLibresConsecutivos(programacionEnActualizacion, len(programacionEnActualizacion['itinerario']))
        
        #Actualización del número de días trabajando consecutivos
        programacionEnActualizacion['diasTrabajandoConsecutivos'] = numeroDiasTrabajandoConsecutivos(programacionEnActualizacion, len(programacionEnActualizacion['itinerario']) ) 
            
    else:#Si no había disponibilidad, retornar una bandera de -1 y realizar el control correspondiente
        return -1
    
    #Si se incorporó bajo disponibilidad, retornar programación para las validaciones restantesa
    return programacionEnActualizacion.copy()
          

#Función para revisar cumplimiento de secuencias y condiciones en una programación de un empleado
def cumplimientoCondiciones(programacionEnRevision, instancia, tiposTurno):   
        
    #Revisar cumplimiento de número de días libres consecutivos en el itinerario (tanto límite inferior como límite superior)    
    cNumeroDiasLibresConsecutivos = programacionEnRevision['diasLibreConsecutivos'] <= instancia['longitudDiasLibre']['longitudMaxima']

    #Revisar cumplimiento de límites de ocupación    
    cLimitesOcupacion = programacionEnRevision['diasTrabajandoConsecutivos'] <= instancia['longitudBloquesTrabajo']['longitudMaxima']
    
    #Revisar si cumple el número de días mínimo y máximo de cada tipo de turno
    booleanosTiposTurno = []
    for tipoTurno in tiposTurno:
        booleanosTiposTurno.append( programacionEnRevision['conteoTiposTurno'][tipoTurno] <= instancia['detalleTurnos'][tipoTurno]['longMaxBloques'] )
    cTiposTurno = all(booleanosTiposTurno)    
    
    #Revisar que no hay secuencias prohibidas en la programación
    #-----------------------------------------------------------
    
    #Suponer que se cumplen las restricciones y falsear durante la revisión si es el casos
    cSecuenciasNP_Longitud2 = True 
    cSecuenciasNP_Longitud3 = True
    
    #NP Longitud 2
    if instancia['numeroSecuenciasNoPermitidas']['SecuenciaDeLongitud2'] != 0:
        #Recorrer la programación de 2 en 2 (en este caso 2 días)
        for i in range(instancia['longitudProgramacion'] - 1):
            #Generar versión string de la subsecuencia
            strSubsecuencia = str()
            #Día i-ésimo
            if(programacionEnRevision['itinerario'][i]!=dict()):
                strSubsecuencia += programacionEnRevision['itinerario'][i]['tipoTurno']
            #Día i-ésimo + 1
            if(programacionEnRevision['itinerario'][i+1]!=dict()):
                strSubsecuencia += programacionEnRevision['itinerario'][i+1]['tipoTurno']            
            #Revisar si está en las prohibidas de longitud 2
            if strSubsecuencia != str() and strSubsecuencia in instancia['strSecuenciasTurnosNP']['longitud2']:
                cSecuenciasNP_Longitud2 = False #Falsear cuando incumple
                
                #Salida de diagnóstico
                print(f"Secuencias Prohibidas Longitud 2: {instancia['strSecuenciasTurnosNP']['longitud2']}")
                print(f"Secuencia Incumpliendo: {strSubsecuencia}")
                
                break #Detenerse para bajar costo computacional
            
    #NP Longitud 3
    if instancia['numeroSecuenciasNoPermitidas']['SecuenciaDeLongitud3'] != 0:
        #Recorrer la programación de 3 en 3 (en este caso 3 días)
        for i in range(instancia['longitudProgramacion'] - 2):
            #Generar versión string de la subsecuencia
            strSubsecuencia = str()
            #Día i-ésimo
            if(programacionEnRevision['itinerario'][i]!=dict()):
                strSubsecuencia += programacionEnRevision['itinerario'][i]['tipoTurno']
            else:
                strSubsecuencia += '-'
            #Día i-ésimo + 1
            if(programacionEnRevision['itinerario'][i+1]!=dict()):
                strSubsecuencia += programacionEnRevision['itinerario'][i+1]['tipoTurno']
            else:
                strSubsecuencia += '-'
            #Día i-ésimo + 2
            if(programacionEnRevision['itinerario'][i+2]!=dict()):
                strSubsecuencia += programacionEnRevision['itinerario'][i+2]['tipoTurno']            
            else:
                strSubsecuencia += '-'
            #Revisar si está en las prohibidas de longitud 3
            if strSubsecuencia != str() and strSubsecuencia in instancia['strSecuenciasTurnosNP']['longitud3']:
                cSecuenciasNP_Longitud3 = False #Falsear cuando incumple
                
                #Salida de diagnóstico
                print(f"Secuencias Prohibidas Longitud 3: {instancia['strSecuenciasTurnosNP']['longitud3']}")
                print(f"Secuencia Incumpliendo: {strSubsecuencia}")
                
                break #Detenerse para bajar costo computacional
    
    #Si cumple todas las condiciones, retornar verdadero para que sea incorporado
    #Nota: en este trabajo se revisarán solamente límites superiores como experimento para observar si disminuye la ocupación de los tripulantes o empleados
    if all([cNumeroDiasLibresConsecutivos,
           cLimitesOcupacion,
           cTiposTurno,
           cSecuenciasNP_Longitud2,
           cSecuenciasNP_Longitud3]):#Actualizar una vez estén implementadas todas las condiciones
        #Reportar viabilidad al cumplir todas las condiciones
        return True
    else:
        #Reportar inviabilidad al incumplir alguna de las condiciones para incorporación
        return False