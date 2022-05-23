#Librería de constructivos enfocados en el problema de rotación de personal
#-------------------------------------------------------------------------

#Librerías adicionales
#---------------------
import funcionesConstructivoPark as fc
from copy import deepcopy

#Constructivo (Park, 2001) adaptado a Rostering -> Rotación de personal
def constructivoPark(instancia, ordenCoberturaTurnos):

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
    
    #Recorrer los pedazos y acomodarlos entre el personal disponible
    cuadroTurnos = list()
    #Inicializar con un estimado del doble del personal disponible
    # [cuadroTurnos.append(dict()) for _ in range(instancia['numeroEmpleados']*4)]
    [cuadroTurnos.append(dict()) for _ in range(len(listadoTurnosPlano))]

    #Obtener los tipos de turno
    tiposTurnoInstancia = list(instancia['detalleTurnos'].keys())
    #Agregar turno vacío o de descanso
    tiposTurnoInstancia.append("-")

    #Abrir la programación del primer empleado con el primer turno del orden de cobertura    
    cuadroTurnos[0] = fc.generarProgramacionEmpleado(dias,tiposTurno).copy()    
    #Llamado a la incorporación adecuada (no requiere validaciones por ser el inicio del cuadro de turnos)
    cuadroTurnos[0] = fc.incorporarTurno( deepcopy(cuadroTurnos)[0].copy(), listadoTurnosPlano[ ordenCoberturaTurnos[0] ] )
    
    #Seccionar la programación del empleado según los días o el horizonte de tiempo
    #Cada tripulante es un elemento de la lista cuadroTurnos, 
    # y se representará con un diccionario que contiene la lista de turnos y otros indicadores
    #cuadroTurnos.append(listadoTurnosPlano[ordenCoberturaTurnos[0]])

    #Acomodar los demás turnos en el cuadro con la estrategia Park, 2001
    for i in range(1,len(ordenCoberturaTurnos)):
        
        #Ejemplo de acceso a cada turno con el subíndice del ciclo general
        #Subíndice -> ordenCoberturaTurnos[i] 
        #Turno -> listadoTurnosPlano[ ordenCoberturaTurnos[i] ]
        
        """
        ------------------------------------------------------------------
        Algoritmo Constructivo Turnos:
        1) Por cada turno i de la secuencia:
            1.1) Por cada programación j del cuadro de turnos:        
                1.1.1) Tomar la programación j en actualización (copia) e incorporar turno de la iteración actual (i-ésimo turno)
                1.1.2) Revisar condiciones: 
                    1.1.2.a) Si se cumplen -> continuar con el siguiente turno i en la secuencia
                    1.1.2.b) Si no se cumplen -> probar con la programación j+1               
            1.2) Si no fue posible acomodar en ninguna programación el turno:
                    -> abrir programación para un nuevo empleado
                    -> adicionar turno i a la programación abierta
                    -> incorporar programación al cuadro de turnos 
        ------------------------------------------------------------------
        """
        
        #Bandera de incorporación exitosa en alguno de los turnos
        incorporacionExitosa = False #Se inicializa falso porque el turno i-ésimo no ha sido incorporado exitosamente (respetando las restricciones)
        
        #Recorrer todas las programaciones (empleados) del cuadro de turnos
        for j in range(len(cuadroTurnos)):        
            #Revisar que no se trate de una programación sin iniciar
            if cuadroTurnos[j] != dict():        
                programacionEnActualizacion = fc.incorporarTurno(deepcopy(cuadroTurnos)[j].copy(), listadoTurnosPlano[ ordenCoberturaTurnos[i] ] )
                #Si es superada la disponibilidad del empleado j-ésimo
                if isinstance(programacionEnActualizacion, dict) :
                    #Proceder a revisar la programación antes de actualizar el cuadro de turnos
                    if fc.cumplimientoCondiciones(programacionEnActualizacion, instancia, tiposTurno):
                        #Actualizar la programación en el cuadro de turnos                    
                        cuadroTurnos[j] = programacionEnActualizacion.copy()                                                
                        #Reportar éxito al incorporar en alguna de las programaciones
                        incorporacionExitosa = True
                        break#Evitar más revisiones
                    else:
                        # print("Cumplimiento de condiciones no superado!")
                        #input()#Pausar la ejecución
                        pass
                        
                else:
                    # print("No fue posible incorporar turno, retorno -1")
                    #input()#Pausar la ejecución
                    pass
            
        #Si no fue exitosa, abrir una nueva programación en el cuadro de turnos con el turno i-ésimo actual    
        if incorporacionExitosa == False:
            #Buscar la primera programación sin abrir 
            for j in range(len(cuadroTurnos)):           
                if cuadroTurnos[j] == dict():           
                    #Nueva programación (ocupación de un nuevo empleado)
                    cuadroTurnos[j] = fc.generarProgramacionEmpleado(dias,tiposTurno).copy()
                    #Actualizar los valores de la nueva programación
                    cuadroTurnos[j] = fc.incorporarTurno(deepcopy(cuadroTurnos)[j].copy(), listadoTurnosPlano[ ordenCoberturaTurnos[i] ] )
                    #Romper el ciclo una vez el turno fue acomodado en las programaciones
                    break    
        
    #Cálculo de indicadores del cuadro de turnos generado
    numeroTotalTurnos = 0
    numeroEmpleadosOcupados = 0
    for i,programacion in enumerate(cuadroTurnos):        
        #Acumular solamente si la programación está abierta
        if programacion != dict():
            numeroEmpleadosOcupados += 1            
            for turno in programacion['itinerario']:
                if turno != dict():
                    numeroTotalTurnos += 1
    
    #Envolver la solución generada: diccionario con cuadro de turnos y el número de empleados ocupados
    solucion = {
        'cuadroTurnos': cuadroTurnos,
        'empleadosOcupados' : numeroEmpleadosOcupados,
        'numeroTotalTurnosCargados' : numeroTotalTurnos        
    }
    
    #Retornar la solución para que sea evaluada en otro contexto
    return solucion