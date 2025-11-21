import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

#Simplemente devuelve una clave AES128 aleatoria
def generar_clave():
    return os.urandom(16)

#Encripta un archivo (archivo_in) mediante una clave AES128 y lo guarda (archivo_out)
def encriptar(archivo_in, archivo_out, clave, silencioso = False):
    iv = os.urandom(16)
    with open(archivo_in, "rb") as f:
        datos = f.read()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(datos) + padder.finalize()
    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    with open(archivo_out, "wb") as f:
        f.write(iv + ciphertext)
    if silencioso == False:
        print("Archivo encriptado en " + archivo_out)

#Desencripta un archivo (archivo_in) mediante una clave AES128 y lo guarda (archivo_out)
def desencriptar(archivo_in, archivo_out, claves, silencioso = False):
    with open(archivo_in, "rb") as f:
        filedata = f.read()
    iv = filedata[:16]
    ciphertext = filedata[16:]
    cipher = Cipher(algorithms.AES(claves), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    with open(archivo_out, "wb") as f:
        f.write(plaintext)
    if silencioso == False:
        print("Archivo desencriptado en " + archivo_out)

