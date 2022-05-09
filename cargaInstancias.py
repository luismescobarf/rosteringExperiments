#Importacion de Librerías
import pprint as pp 
import json

#Carga de instancias en versión json
def cargaVersionJSON(rutaArchivo):
    #Cargar en memoria la información de un archivo json
    casoEstudio = dict()
    try:
        with open(rutaArchivo) as f:
            casoEstudio = json.load(f)
    except:
        print("Fallo cargando el caso de estudio en JSON!")
        
    #Versión string de las secuencias prohibidas para facilitar validación
    casoEstudio['strSecuenciasTurnosNP'] = {
        'longitud2': list(),
        'longitud3': list()
    }
    
    #Recorrer las secuencias no permitidas para cargarlas en format string (opcional)
    for i,secuenciaNP in enumerate(casoEstudio['SecuenciaTurnosNP']):
        #Revisar si corresponde a las de longitud 2
        if i < casoEstudio['numeroSecuenciasNoPermitidas']['SecuenciaDeLongitud2']:
            casoEstudio['strSecuenciasTurnosNP']['longitud2'].append(
                secuenciaNP['Turno 1']+secuenciaNP['Turno 2']
            )            
        else:#Para las de longitud 3
            casoEstudio['strSecuenciasTurnosNP']['longitud3'].append(
                secuenciaNP['Turno 1']+secuenciaNP['Turno 2']+secuenciaNP['Turno 3']
            )
    
    #Retornar el diccionario obtenido del archivo JSON
    return casoEstudio    

#Crear/Sobreescribir un archivo json a partir de una estructura de datos
def crearSobreescribir_JSON_Instancia(estructuraDatos):
    try: 
        with open('instancias/versionJSON/'+estructuraDatos['nombreCaso']+'.json','w') as f:
            json.dump(estructuraDatos,f)
    except:
        print("Problemas escribiendo la estructura de datos en el archivo json!!!")
        
#Carga instancias Musliu
def cargarInstanciaMusliu(rutaArchivo):
    
    #Inicializar estructura de datos (diccionario)
    casoEstudio = dict()
    
    #Intentar abrir el archivo que llegó por el parámetro rutaArchivo    
    try:    
        #Mientras está abierto el archivo, realizar la carga en la estructura de datos
        with open(rutaArchivo) as f:
            
            #Lectura del nombre del archivo
            casoEstudio['nombreCaso'] = rutaArchivo.split('/')[-1].split('.')[0]
            
            #Lectura de la longitud de la programacion ( En dias )      
            f.readline() #Saltar el encabezado que hace referencia al valor ("Length of the schedule")
            casoEstudio['longitudProgramacion'] = int(f.readline().strip())        
            
            #Lectura del Número de empleados
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor ("Number of Employees")
            casoEstudio['numeroEmpleados'] = int(f.readline().strip())        
            
            #Lectura del Número de turnos
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor ("Number of Shifts")
            casoEstudio['numeroTurnos'] = int(f.readline().strip())        
            
            #Lectura para la Matriz de requerimientos
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor ("Temporal Requirements Matrix")
            matrizRequerimientos = list()
            for _ in range(casoEstudio['numeroTurnos']):               
                matrizRequerimientos.append(list(map(lambda x:int(x), f.readline().strip().split())))
            casoEstudio['matrizRequerimientos'] = matrizRequerimientos      
            
            #Lectura para la Especificación de los turnos (diccionario de diccionarios)
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor ("ShiftName, Start, Length, Name, MinlengthOfBlocks, MaxLengthOfBlocks")
            casoEstudio['detalleTurnos'] = dict()
            for _ in range(casoEstudio['numeroTurnos']):
                arregloLinea = f.readline().strip().split()
                arregloNumerico = list(map(lambda x:int(x), arregloLinea[1:] ))
                casoEstudio['detalleTurnos'][ arregloLinea[0] ] = {
                        'Inicio'         : arregloNumerico[0],
                        'longitud'       : arregloNumerico[1],
                        'longMinBloques' : arregloNumerico[2],
                        'longMaxBloques' : arregloNumerico[3]
                    }
            
            #Lectura de la longitud mínima y máxima de días libres
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor (" Minimum and maximum length of days-off blocks  ")
            arregloLinea = f.readline().strip().split()
            casoEstudio['longitudDiasLibre'] = {
                'longitudMinima' : int(arregloLinea[0]),
                'longitudMaxima' : int(arregloLinea[1])
            }           
            
            
            #Lectura de la longitud minima y maxima de los bloques de trabajo
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor (" Minimum and maximum length of work blocks  ")
            arregloLinea = f.readline().strip().split()            
            casoEstudio['longitudBloquesTrabajo'] = {
                'longitudMinima' : int(arregloLinea[0]),
                'longitudMaxima' : int(arregloLinea[1])
            }            
        
            #Lectura del número de secuencias no permitidas
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor ("Number of not allowed shift sequences: NrSequencesOfLength2, NrSequencesOfLength3:   ")            
            arregloLinea = f.readline().strip().split()
            casoEstudio['numeroSecuenciasNoPermitidas'] = {
                        'SecuenciaDeLongitud2'    : int(arregloLinea[0]),
                        'SecuenciaDeLongitud3'    : int(arregloLinea[1]),                                       
                    }           

            #Lectura de la secuencia de turnos no permitidos
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor ("Not allowed shift sequences ")          
            casoEstudio['SecuenciaTurnosNP'] = list()           
            
            #Recorrido controlado por los valores cargados previamente            
            for i in range(casoEstudio['numeroSecuenciasNoPermitidas']['SecuenciaDeLongitud2']):
                arregloLinea = f.readline().strip().split()
                casoEstudio['SecuenciaTurnosNP'].append({
                    'Turno 1'         : arregloLinea[0],
                    'Turno 2'         : arregloLinea[1],               
                })                
                                
            for i in range(casoEstudio['numeroSecuenciasNoPermitidas']['SecuenciaDeLongitud3']):
                arregloLinea = f.readline().strip().split()
                casoEstudio['SecuenciaTurnosNP'].append({
                    'Turno 1'         : arregloLinea[0],
                    'Turno 2'         : arregloLinea[1],               
                    'Turno 3'         : arregloLinea[2],               
                })         

    #Mensaje por si sucede algun error              
    except:
        print("Error abriendo la instancia de rostering!!!")
    
    #Retornar la informacion que se obtuvo 
    return casoEstudio


# #Sección Principal del codigo (uso de la librería)
# #--------------------------------------------------

# #Listado de instancias
# nombresInstancias = ["instancias/Example1.txt",
#                      "instancias/Example2.txt",
#                      "instancias/Example3.txt",
#                      "instancias/Example4.txt",
#                      "instancias/Example5.txt",
#                      "instancias/Example6.txt",
#                      "instancias/Example7.txt",
#                      "instancias/Example8.txt",
#                      "instancias/Example9.txt",
#                      "instancias/Example10.txt",
#                      "instancias/Example11.txt",
#                      "instancias/Example12.txt",
#                      "instancias/Example13.txt",
#                      "instancias/Example14.txt",
#                      "instancias/Example15.txt",
#                      "instancias/Example16.txt",
#                      "instancias/Example17.txt",
#                      "instancias/Example18.txt",
#                      "instancias/Example19.txt",
#                      "instancias/Example20.txt"]

# #nombresInstancias = ["instancias/Example12.txt"]

# #Carga de cada uno de los archivos del listado previo
# for rutaArchivo in nombresInstancias:   
     
#     #Salida de diagnóstico
#     print("Caso que se está cargando: ",rutaArchivo)
    
#     casoEstudio = cargarInstanciaMusliu(rutaArchivo)
    
#     # # #Salida ordenada de diagnóstico
#     # pp.pprint(casoEstudio)
    
#     #Salida de diagnóstico
#     print("Caso que se está escribiendo: ",rutaArchivo)
    
#     #Convertir el diccionario a archivo JSON para facilitar la carga en corridas posteriores
#     crearSobreescribir_JSON_Instancia(casoEstudio)