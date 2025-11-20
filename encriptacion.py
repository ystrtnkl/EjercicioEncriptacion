from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


print("Programa para encriptacion/desencriptacion de archivos")
print("Selecciona una opcion\n")
print("1) Encriptar archivo")
print("2) Desencriptar archivo")
print("3) Generar par de claves RSA")
opcion = input("Escribe un numero: ")
match opcion:
    case "1":
        import clavesRsa
        clavesRsa.generar()
    case "2":
        pass
    case "3":
        pass
    case _:
        print("Opcion invalida, ejecuta el programa de nuevo")
