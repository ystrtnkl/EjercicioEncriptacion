import clavesRsa
import codificarAes
import empaquetar
import administracion
import os
import sys
import shlex
import rutas


#Lo que ocurre en la opcion de encriptar
def proceso_encriptar():
    print("Elige los archivos a encriptar (rutas separadas por espacios)")
    archivos = input("Archivos: ")
    print("")
    #archivos = archivos.split(" ")
    correcto = True
    if os.path.isdir(archivos) == False:
        archivos = shlex.split(archivos)
        if len(archivos) == 0:
            correcto = False
        else:
            for e in archivos:
                if os.path.exists(rutas.normalizar_ruta(e)) == False:
                    print("No se ha encontrado " + e)
                    correcto = False
    else:
        print("ATENCION: debido a diferencias entre sistemas operativos, es posible que empaquetar una carpeta (en lugar de archivos) pueda generar errores.")
    if correcto:
        decision_empaquetar = ""
        if len(archivos) > 1 or os.path.isdir(archivos):    
            print("¿Deseas empaquetar los archivos encriptados en un solo archivo?")
            decision_empaquetar = input("(en blanco = no, escribir nombre de archivo empaquetado = si, usando ese archivo): ")
            print("")
            
        print("Se generara una clave AES128 aleatoria, ¿Deseas encriptar esta clave con una clave pública RSA? Ten en cuenta que solo quien tenga la clave privada podra desencriptarlos")
        print("En caso de que si el nombre con la clave publica (tiene que haber en esta carpeta un archivo llamado <nombre>-publica.pem, si no lo hay reinicia el programa y usa la opcion 3)")
        publica = input("(en blanco = no, escribir nombre = si, usando ese nombre): ")
        print("")
        if os.path.exists(publica + "-publica.pem") == False and publica != "":
            print("No se ha encontrado el archivo " + publica + "-publica.pem, la clave AES128 NO se encriptara (puedes cerrar el programa y volver a intentarlo con otro nombre)")
            publica = ""
        if publica != "":
            aes128 = codificarAes.generar_clave()
            print("¿Deseas mostrar la clave AES128 por consola o guardarla en un archivo? (si el archivo ya existe se sobreescribira)")
            guardar_aes128 = input("(en blanco = mostrar por consola, escribir nombre de archivo = guardar en ese archivo): ")
            print("")
            aes128_encriptada = clavesRsa.encriptar(publica, aes128)
            if guardar_aes128 == "":
                print("Clave AES128 (para desencriptar los archivos) encriptada con la clave publica:")
                print(aes128_encriptada)
            else:
                with open(rutas.normalizar_ruta(guardar_aes128), "wb") as f:
                    f.write(aes128_encriptada)
                    print("Clave guardada en " + guardar_aes128)
        else:
            aes128 = codificarAes.generar_clave()
            print("¿Deseas mostrar la clave AES128 por consola o guardarla en un archivo? (si el archivo ya existe se sobreescribira)")
            guardar_aes128 = input("(en blanco = mostrar por consola, escribir nombre de archivo = guardar en ese archivo): ")
            print("")
            if guardar_aes128 == "":
                print("Clave AES128 (para desencriptar los archivos):")
                print(aes128)
            else:
                with open(rutas.normalizar_ruta(guardar_aes128), "wb") as f:
                    f.write(aes128)
                    print("Clave guardada en " + guardar_aes128)
                        
        if decision_empaquetar == "":
            sufijo = input("Sufijo para los archivos encriptados para diferenciarlos (por defecto .aes): ")
            print("")
            if sufijo == "":
                sufijo = ".aes"
            for e in archivos:
                codificarAes.encriptar(e, e + sufijo, aes128)
                    
            print("Proceso finalizado, esto es lo que ha ocurrido:")
            if guardar_aes128 == "":
                guardar_aes128 = "la consola"
            if publica == "":
                    print("Se ha generado una version encriptada de los archivos " + ", ".join(archivos) + " acabados en " + sufijo + " y la clave para desencriptarlos esta en " + guardar_aes128 + ", dicha clave no esta encriptada (ten cuidado)")
            else:
                print("Se ha generado una version encriptada de los archivos " + ", ".join(archivos) + " acabados en " + sufijo + " y la clave para desencriptarlos esta en " + guardar_aes128 + " encriptada con RSA bajo el nombre de " + publica)
        else:
            empaquetar.empaquetar(rutas.normalizar_ruta(decision_empaquetar) + ".temp", archivos)
            codificarAes.encriptar(decision_empaquetar + ".temp", decision_empaquetar, aes128)
            os.remove(decision_empaquetar + ".temp")
            print("Proceso finalizado, esto es lo que ha ocurrido:")
            if guardar_aes128 == "":
                    guardar_aes128 = "la consola"
            if publica == "":
                print("Los archivos " + ", ".join(archivos) + "se han empaquetado en " + decision_empaquetar + " encriptados bajo la clave AES128 que esta en " + guardar_aes128 + ", dicha clave no esta encriptada (ten cuidado)")
            else:
                print("Los archivos " + ", ".join(archivos) + "se han empaquetado en " + decision_empaquetar + " encriptados bajo la clave AES128 que esta en " + guardar_aes128 + " encriptada con RSA bajo el nombre de " + publica)

        if decision_empaquetar == "":
            administracion.guardar_registro_clave(aes128, publica, archivos, sufijo)
        else:
            administracion.guardar_registro_clave(aes128, publica, decision_empaquetar, " (empaquetado)")
    else:
        print("Intentalo otra vez con archivos que existan")

#Lo que ocurre en la opcion de desencriptar
def proceso_desencriptar():
    print("Antes de desencriptar, responde con sinceridad estas preguntas (si no lo haces los archivo(s) podrian no desencriptarse correctamente)")
    print("¿Tu archivo esta empaquetado?")
    empaquetado = input("(en blanco = no, nombre del archivo empaquetado = si y usar ese archivo): ")
    print("")
    if empaquetado != "" and os.path.exists(rutas.normalizar_ruta(empaquetado)) == False:
        print(empaquetado + " no se ha encontrado, saliendo...")
        sys.exit()
    print("¿Tu clave AES128 fue encriptada con RSA? Si asi es se necesita el nombre de la clave Y tener guardada la clave privada")
    nombreRsa = input("(en blanco = no fue encriptada, escribir nombre = fue encriptada Y desencriptar con ese nombre): ")
    print("")
    if nombreRsa != "" and os.path.exists(nombreRsa + "-privada.pem") == False:
        print(empaquetado + "-privada.pem no se ha encontrado, es necesario tener la clave privada para desencriptar el AES128, y por lo tanto desencriptar el archivo. Saliendo...")
        sys.exit()
    print("¿Donde esta el archivo con la clave?")
    clave = input("Introduce el nombre del archivo, si no existe dicho archivo se tomara como clave el texto escrito: ")
    print("")
    if os.path.exists(rutas.normalizar_ruta(clave)):
        with open(rutas.normalizar_ruta(clave), "rb") as f:
            clave = f.read()

    if empaquetado == "":
        print("Elige los archivos a desencriptar (rutas separadas por espacios)")
        archivos = input("Archivos: ")
        print("")
        #archivos = archivos.split(" ")
        archivos = shlex.split(archivos)
        correcto = True
        if len(archivos) == 0:
            correcto = False
        else:
            for e in archivos:
                if os.path.exists(rutas.normalizar_ruta(e)) == False:
                    print("No se ha encontrado " + e)
                    correcto = False
        if correcto:
            print("¿Que sufijo quieres agregar a los archivos desencriptados para diferenciarlos? (por defecto .unaes)")
            sufijo = input("Prefijo (en blanco para .unaes): ")
            if sufijo == "":
                sufijo = ".unaes"
            print("")
            if nombreRsa != "":
                clave = clavesRsa.desencriptar(nombreRsa, clave)
            for e in archivos:
                codificarAes.desencriptar(e, e + sufijo, clave)
        else:
            print("Intentalo otra vez con archivos que existan")
    else:
        print("¿Donde quieres que se exporten los archivos? (en blanco para dejarlos aqui)")
        carpeta = input("Ubicacion: ")
        print("")
        if carpeta == "":
            carpeta = "."
        else:
            carpeta = rutas.normalizar_ruta(carpeta)
        if nombreRsa != "":
            clave = clavesRsa.desencriptar(nombreRsa, clave)
        codificarAes.desencriptar(empaquetado, empaquetado + ".temp", clave)
        empaquetar.desempaquetar(empaquetado + ".temp", carpeta=carpeta)
        os.remove(empaquetado + ".temp")
            
            
            
            
print("Programa para encriptacion/desencriptacion de archivos")
print("Selecciona una opcion\n")
print("1) Encriptar archivo")
print("2) Desencriptar archivo")
print("3) Generar par de claves RSA")
print("4) Administracion (ver claves)")
print("4) Informacion")
print("5) Salir")
opcion = input("\nEscribe un numero/opcion: ")
print("")

match opcion:
    case "1":
        proceso_encriptar()
    case "2":
        proceso_desencriptar()
    case "3":
        #Opcion para generar claves RSA
        print("Las claves (archivos .pem) se almacenan segun el nombre del usuario, intentar hacer otras claves con el mismo nombre sobreescribirán las ya existentes.")
        clavesRsa.generar(input("Escribe tu nombre: "))
    case "4":
        print("Para esta accion (ver todas las claves AES128 sin encriptar) necesitas autenticarte como administrador")
        print("Autenticando...")
        if administracion.autenticar():
            print("Autenticado correctamente, ¿Donde quieres guardar una copia sin encriptar de las claves?")
            donde = input("Ubicacion: ")
            print("")
            administracion.mostrar_claves(donde)
            print("Guardado. Tienes la responsabilidad de borrar luego ese archivo y usarlo para el bien")
            print("Las claves estan ahora guardadas en un archivo de texto sin encriptar pero estan en formato binario, copialas en un archivo aparte y usalo como clave para desencriptar (es posible que tengas que convertirlo de vuelta a binario)")
        else:
            print("No hay permisos de acceso, por lo que no eres administrador")
    case "5":
        print("Consulta mas informacion en README.md o en el pdf")
    case "6":
        print("SALIENDO...")
        exit()
    case _:
        print("Opcion invalida, ejecuta el programa de nuevo")
print("")
print("")
input("(ENTER para salir)")