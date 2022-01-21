#Librerías
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
            
            # #Salida de diagnóstico
            # print(f"{rutaArchivo} Abierto exitosamente!!")
            
            #Agregar nombre del caso
            casoEstudio['nombreCaso'] = rutaArchivo.split('/')[-1].split('.')[0]
            
            #Longitud de la programación (horizonte de tiempo -> 7 días o una semana)            
            f.readline() #Saltar encabezado de la longitud de programación
            casoEstudio['longitudProgramacion'] = int(f.readline().strip())        
            
            #Número de empleados
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado
            casoEstudio['numeroEmpleados'] = int(f.readline().strip())        
            
            #Número de turnos
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado
            casoEstudio['numeroTurnos'] = int(f.readline().strip())        
            
            #Matriz de requerimientos
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado
            matrizRequerimientos = list()
            for _ in range(casoEstudio['numeroTurnos']):               
                matrizRequerimientos.append(list(map(lambda x:int(x), f.readline().strip().split())))
            casoEstudio['matrizRequerimientos'] = matrizRequerimientos      
            
            # #Especificación de los turnos
            # f.readline() #Saltar línea vacía
            # f.readline() #Saltar encabezado
            # casoEstudio['detalleTurnos'] = list()
            # for _ in range(casoEstudio['numeroTurnos']):
            #     arregloLinea = f.readline().strip().split()
            #     arregloNumerico = list(map(lambda x:int(x), arregloLinea[1:] ))
            #     casoEstudio['detalleTurnos'].append({
            #         'nombreTurno'    : arregloLinea[0],
            #         'inicio'         : arregloNumerico[0],
            #         'longitud'       : arregloNumerico[1],
            #         'longMinBloques' : arregloNumerico[2],
            #         'longMaxBloques' : arregloNumerico[3]                    
            #     }) 
            
            #Especificación de los turnos (diccionario de diccionarios)
            f.readline() #Saltar línea vacía
            f.readline() #Saltar encabezado
            casoEstudio['detalleTurnos'] = dict()
            for _ in range(casoEstudio['numeroTurnos']):
                arregloLinea = f.readline().strip().split()
                arregloNumerico = list(map(lambda x:int(x), arregloLinea[1:] ))
                casoEstudio['detalleTurnos'][ arregloLinea[0] ] = {
                        'inicio'         : arregloNumerico[0],
                        'longitud'       : arregloNumerico[1],
                        'longMinBloques' : arregloNumerico[2],
                        'longMaxBloques' : arregloNumerico[3]
                    }
                  
    except:
        print("Error abriendo la instancia de rostering!!!")
    
    #Retornar la estructura de datos con el caso de estudio
    return casoEstudio


#Sección Principal
#-----------------
casoEstudio = cargarInstanciaMusliu("instancias/Example2.txt")
pp.pprint(casoEstudio)

print("Ejemplo de consulta de la segunda propuesta de almacenamiento")
print("A qué hora empieza el bloque de la mañana?")
print(f"Bloque de la mañana empieza en el minuto: {casoEstudio['detalleTurnos']['D']['inicio']}")
print(f"Nombres de los turnos: {casoEstudio['detalleTurnos'].keys()}")
print(f"Información de la mañana: {casoEstudio['detalleTurnos']['A']}")

#Convertir el diccionario a archivo JSON para facilitar la carga en corridas posteriores
crearSobreescribir_JSON_Instancia(casoEstudio)

#Ejemplo cargando instancia ya convertida a JSON
casoObtenidoJSON = cargaVersionJSON('instancias/versionJSON/Example1.json')
print("---------------------------------------")
print("---------------------------------------")
pp.pprint(casoObtenidoJSON)

