import operator

#Función ejemplo de carga normal
def cargarArchivoListaCompuesta(nombreArchivo):

    #Abrir el archivo
    manejadorArchivo = open(nombreArchivo)

    #Recoger la información bajo el formato especificado
    
    #Primera línea capacidad de la mochila
    #strip es para quitar caracteres esepciales
    primeraLinea = manejadorArchivo.readline()
    capacidadMochila = int(primeraLinea.strip())

    #Segunda línea, número total de ítems
    segundaLinea = manejadorArchivo.readline()
    numeroItems = int(segundaLinea.strip())

    #Número de lecturas a partir del número de ítems
    coleccionCargada = []
    for i in range(numeroItems):
        linea_n = manejadorArchivo.readline()
        linea_n = linea_n.strip()
        linea_n = linea_n.split(' ')     
        coleccionCargada.append( [ int(linea_n[0]), int(linea_n[1]), linea_n[2] ] )  

    #Cerrar el archivo
    manejadorArchivo.close()

    #Retornar los valores cargados de la instancia
    return capacidadMochila, numeroItems, coleccionCargada

arCapacidadMochila,arNumeroItems,arColeccion = cargarArchivoListaCompuesta('instancia1KP.txt')
print('Capacidad->',arCapacidadMochila)
print('NúmeroItems->',arNumeroItems)
print('Colección->',arColeccion)
input()