class Archivo:
    
    def read(self, ruta):
        with open(ruta, 'r') as leer:
            contenido = leer.read().split('\n')
        i = 0
        for line in contenido:
            contenido[i] = line.split(',')
            i = i + 1

        leer.close()
        return contenido

    def write(self, ruta, contenido):
        escribir = open(ruta , 'w')
        escribir.write(contenido)
        escribir.close()

    def copiar(self, RutaOrigen, RutaDestino):
        if os.path.exists(RutaOrigen):
            with open(RutaOrigen, 'rb') as FileOrigen:
                with open(RutaDestino, 'wb') as FileDestino:
                    shutil.copyfileobj(FileOrigen, FileDestino)
                    print("Archivo copiado")
