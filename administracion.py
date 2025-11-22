import os
import clavesRsa
import codificarAes

#Crea un registro en claves.bin para el administrador a partir de los datos de una encriptacion. claves.bin esta encriptado mediante la AES128 del admin, encriptada con las RSA de admin-privada.pem y admin-publica.pem
def guardar_registro_clave(clave, nombre, archivos, sufijo):
    archivos_str = ", ".join(archivos) + "(" + sufijo + ")"
    #linea = f"{nombre}: {archivos_str} == {clave}\n".encode("utf-8")
    linea = f"{nombre}: {archivos_str} == ".encode("utf-8") + clave + b"\n" #Informacion en texto + clave en binario (puede neceistar conversion externa a binario para guardarlo en un archivo aislado)
    with open("admin.key", "rb") as f:
        encrypted_admin_key = f.read()
    admin_aes_key = clavesRsa.desencriptar("admin", encrypted_admin_key)
    if os.path.exists("claves.bin") and os.path.getsize("claves.bin") >= 16:
        codificarAes.desencriptar("claves.bin", "claves.bin.temp", admin_aes_key, silencioso=True)
        with open("claves.bin.temp", "rb") as f:
            original = f.read()
        os.remove("claves.bin.temp")
    else:
        original = b""
    nuevo_contenido = original + linea
    with open("claves.bin.temp2", "wb") as f:
        f.write(nuevo_contenido)
    codificarAes.encriptar("claves.bin.temp2", "claves.bin", admin_aes_key, silencioso=True)
    os.remove("claves.bin.temp2")

#Se dice que el usuario se puede autenticar como admin cuando tiene acceso a nivel de sistema de archivos a admin.key, admin-publica.pem y admin-privada.pem, lo que quiere decir que ha ejecutado el programa como root o como administrador
def autenticar():
    #Comprobar que hay acceso de lectura a admin.key, admin-privada.pem y admin-publica.pem
    return (os.path.exists("admin.key") and os.access("admin.key", os.R_OK) and os.path.exists("admin-privada.pem") and os.access("admin-privada.pem", os.R_OK) and os.path.exists("admin-publica.pem") and os.access("admin-publica.pem", os.R_OK))

#Genera una copia sin encriptar de todas las claves, solo el administrador deberia hacer esto y es responsable de borrar luego el archivo
def mostrar_claves(archivo_out):
    if not os.path.exists("claves.bin"):
        return ""
    with open("admin.key", "rb") as f:
        encrypted_admin_key = f.read()
    admin_aes_key = clavesRsa.desencriptar("admin", encrypted_admin_key)
    codificarAes.desencriptar("claves.bin", "claves.bin.temp", admin_aes_key, silencioso=True)
    with open("claves.bin.temp", "rb") as f:
        contenido = f.read()
    os.remove("claves.bin.temp")
    with open(archivo_out, "wb") as f:
        f.write(contenido)

