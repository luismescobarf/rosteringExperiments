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
            
            #Lectura de la duracion de los turnos
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor (" Minimum and maximum length of days-off blocks  ")
            casoEstudio['duracionTurnos'] = list()
            arregloLinea = f.readline().strip().split()
            casoEstudio['duracionTurnos'].append({
                        'DuracionMin'    : arregloLinea[0],
                        'DuracionMax'    : arregloLinea[1],
                                       
                    }) 

            #Lectura de la longitud minima y maxima de los bloques de trabajo
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor (" Minimum and maximum length of work blocks  ")
            casoEstudio['longitudTurnos'] = list()
            arregloLinea = f.readline().strip().split()
            casoEstudio['longitudTurnos'].append({
                        'LongitudMin'    : arregloLinea[0],
                        'LongitudMax'    : arregloLinea[1],
                                       
                    }) 

        
            #Lectura de la secuencia de turnos
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor ("Number of not allowed shift sequences: NrSequencesOfLength2, NrSequencesOfLength3:   ")
            casoEstudio['secuenciaTurnos'] = list()
            arregloLinea = f.readline().strip().split()
            casoEstudio['secuenciaTurnos'].append({
                        'SecuenciaDeLongitud1'    : arregloLinea[0],
                        'SecuenciaDeLongitud2'    : arregloLinea[1],
                                       
                    }) 
           

            #Lectura de la secuencia de turnos no permitidos
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado que hace referencia al valor ("Not allowed shift sequences ")
            casoEstudio['SecuenciaTurnosNP'] = list()
            for _ in range(casoEstudio['numeroTurnos']):
                arregloLinea = f.readline().strip().split()
                casoEstudio['SecuenciaTurnosNP'].append({
                    'Turno 1'         : arregloLinea[0],
                    'Turno 2'         : arregloLinea[1],               
                }) 
            

    #Mensaje por si sucede algun error              
    except:
        print("Error abriendo la instancia de rostering!!!")
    
    #Retornar la informacion que se obtuvo 
    return casoEstudio


#Sección Principal del codigo 
#--------------------------------------------------

#Aca cargamos el archivo que vamos a utlizar 
casoEstudio = cargarInstanciaMusliu("instancias/Example20.txt")
#Aca imprimimos los datos 
pp.pprint(casoEstudio)


#Convertir el diccionario a archivo JSON para facilitar la carga en corridas posteriores
crearSobreescribir_JSON_Instancia(casoEstudio)



