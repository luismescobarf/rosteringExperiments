#Constructivo (Park, 2001) adaptado a Rostering -> Rotación de personal
#----------------------------------------------------------------------

#Librerías
#---------
import cargaInstancias #Librería con funcionalidades desarrolladas para gestión de las instancias
import funcionesConstructivoPark as fc
import json
import pprint as pp 
import random
from copy import deepcopy

#Sección principal
#-----------------

#Carga de la instancia que se va a trabajar
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example1.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example2.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example3.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example4.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example5.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example6.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example7.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example8.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example9.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example10.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example11.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example12.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example13.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example14.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example15.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example16.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example17.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example18.json")
# instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example19.json")
instancia = cargaInstancias.cargaVersionJSON("instancias/versionJSON/Example20.json")

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
print("---------------------------")
pp.pprint(instancia)
print("---------------------------")
#input()#Detener ejecución para revisión
            
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

#input() #Pausar ejecución

#Recorrer los pedazos y acomodarlos entre el personal disponible
cuadroTurnos = list()
#Inicializar con un estimado del doble del personal disponible
# [cuadroTurnos.append(dict()) for _ in range(instancia['numeroEmpleados']*2)]
[cuadroTurnos.append(dict()) for _ in range(len(listadoTurnosPlano))]

#Obtener los tipos de turno
tiposTurnoInstancia = list(instancia['detalleTurnos'].keys())
#Agregar turno vacío o de descanso
tiposTurnoInstancia.append("-")

# #Salida de diagnóstico
# print(f"Tipos de turno: {tiposTurnoInstancia} - tipo del contenedor: {type(tiposTurnoInstancia)}")
# input()#Pausa de ejecución

#Abrir la programación del primer empleado con el primer turno del orden de cobertura
#cuadroTurnos.append(generarProgramacionEmpleado(dias,tiposTurno).copy())
#cuadroTurnos[0] = fc.generarProgramacionEmpleado(dias,tiposTurno).copy()
cuadroTurnos[0] = fc.generarProgramacionEmpleado(dias,tiposTurno).copy()

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

#Reemplazar estas formas de agregar por incorporar (actualizando los parámetros)
#cuadroTurnos[-1]['itinerario'][ listadoTurnosPlano[ordenCoberturaTurnos[0]]['indiceDia'] ].append(listadoTurnosPlano[ ordenCoberturaTurnos[0] ]) 
#cuadroTurnos[-1]['itinerario'][ listadoTurnosPlano[ordenCoberturaTurnos[0]]['indiceDia'] ] = listadoTurnosPlano[ ordenCoberturaTurnos[0] ]

#Llamado a la incorporación adecuada (no requiere validaciones por ser el inicio del cuadro de turnos)
# cuadroTurnos[-1] = incorporarTurno(list(cuadroTurnos)[-1].copy(), listadoTurnosPlano[ ordenCoberturaTurnos[0] ] )
cuadroTurnos[0] = fc.incorporarTurno( deepcopy(cuadroTurnos)[0].copy(), listadoTurnosPlano[ ordenCoberturaTurnos[0] ] )

#Salida de diagnóstico
print("Estado del cuadro de turnos después de inicializar (incorporar):")
pp.pprint(cuadroTurnos)

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
                    
                    
                    # print("-->->->->->->- Reingreso cuadro turnos -->->->->->->-")
                    # print("-->->->->->->- Reingreso cuadro turnos -->->->->->->-")
                    # pp.pprint(programacionEnActualizacion)
                    # print("-->->->->->->- Como quedo en el cuadro de turnos -->->->->->->-")
                    # pp.pprint(cuadroTurnos[j])
                    # print("-->->->->->->- Como quedo en el cuadro de turnos -->->->->->->-")
                    # #input()#Pausar ejecución
                    
                    #Reportar éxito al incorporar en alguna de las programaciones
                    incorporacionExitosa = True
                    break#Evitar más revisiones
                else:
                    print("Cumplimiento de condiciones no superado!")
                    #input()#Pausar la ejecución
                    
            else:
                print("No fue posible incorporar turno, retorno -1")
                #input()#Pausar la ejecución
        
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
                
    
    #Salida de diagnóstico cuadro de turnos en cada iteración    
    numeroTotalTurnos = 0
    numeroEmpleadosOcupados = 0
    print()
    print()
    print()
    for i,programacion in enumerate(cuadroTurnos):
        print('<<<<<**************************************************')
        pp.pprint(programacion)
        # print(f"Dias Libre Calculados -> {numeroDiasLibresConsecutivos(programacion, instancia['longitudProgramacion'])}")
        # print(f"Dias Trabajando Calculados -> {numeroDiasTrabajandoConsecutivos(programacion, instancia['longitudProgramacion'])}")
        
        #Acumular solamente si la programación está abierta
        if programacion != dict():
            numeroEmpleadosOcupados += 1            
            for turno in programacion['itinerario']:
                #Acumular solamente en días que están ocupados con un turno
                if turno != dict():
                    numeroTotalTurnos += 1
        
        print('<<<<<**************************************************')
        
    #input()#Pausar ejecución para realizar seguimiento
        
        
   
# #Revisión: recalcular días libre en cada programación
# for i in range(len(cuadroTurnos)):
#     cuadroTurnos[i]['diasLibreConsecutivos'] = numeroDiasLibresConsecutivos(cuadroTurnos[i], instancia['longitudProgramacion'])
#     cuadroTurnos[i]['diasTrabajandoConsecutivos'] = numeroDiasTrabajandoConsecutivos(cuadroTurnos[i], instancia['longitudProgramacion'])
    
#Mostrar cuadro de turnos final y cálculo de indicadores
numeroTotalTurnos = 0
numeroEmpleadosOcupados = 0
for i,programacion in enumerate(cuadroTurnos):
    print('**************************************************')
    pp.pprint(programacion)
    # print(f"Dias Libre Calculados -> {numeroDiasLibresConsecutivos(programacion, instancia['longitudProgramacion'])}")
    # print(f"Dias Trabajando Calculados -> {numeroDiasTrabajandoConsecutivos(programacion, instancia['longitudProgramacion'])}")
    
    #Acumular solamente si la programación está abierta
    if programacion != dict():
        numeroEmpleadosOcupados += 1            
        for turno in programacion['itinerario']:
            if turno != dict():
                numeroTotalTurnos += 1
    
    print('**************************************************')





#Reportar número de operadores o empleados ocupados con la secuencia aleatoria utilizada
print('-------------------------------------------------')
print('Reporte del constructivo')
print(f"Numero Operadores Abiertos: {len(cuadroTurnos)}")
print(f"Numero Operadores Ocupados: {numeroEmpleadosOcupados}")
print(f"Numero Operadores Disponibles: { instancia['numeroEmpleados']}")
print(f"Numero Total Turnos Insertados: { numeroTotalTurnos }")
print(f"Numero Total Turnos Demandados: { len(listadoTurnosPlano) }")
print('-------------------------------------------------')


#Continuar acá!!!
#Número de días trabajados consecutivos está funcionando de forma intermitente: depurar!