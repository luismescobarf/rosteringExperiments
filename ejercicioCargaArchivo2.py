import operator

#Función ejemplo de carga diccionario
def cargarArchivoDiccionario(nombreArchivo):

    #Abrir el archivo
    manejadorArchivo = open(nombreArchivo)

    #Recoger la información bajo el formato especificado
    
    #Primera línea capacidad de la mochila
    primeraLinea = manejadorArchivo.readline()
    capacidadMochila = int(primeraLinea.strip())

    #Segunda línea, número total de ítems
    segundaLinea = manejadorArchivo.readline()
    numeroItems = int(segundaLinea.strip())

    #Número de lecturas a partir del número de ítems
    coleccionCargada = {}
    for i in range(numeroItems):
        linea_n = manejadorArchivo.readline()
        linea_n = linea_n.strip()
        linea_n = linea_n.split(' ')     
        coleccionCargada.update( {linea_n[2] : {"beneficio":int(linea_n[0]), "peso":int(linea_n[1])} } )  
        
    #Cerrar el archivo
    manejadorArchivo.close()

    #Retornar los valores cargados de la instancia
    return capacidadMochila, numeroItems, coleccionCargada

arCapacidadMochila,arNumeroItems,arColeccion = cargarArchivoDiccionario('instancia1KP.txt')
print('Capacidad->',arCapacidadMochila)
print('NúmeroItems->',arNumeroItems)
print('Colección->',arColeccion)
input()