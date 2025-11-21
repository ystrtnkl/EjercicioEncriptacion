from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

def generar(nombre):
    privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    publica = privada.public_key()
    with open(nombre + "-privada.pem", "wb") as f:
        f.write(privada.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
    with open(nombre + "-publica.pem", "wb") as f:
        f.write(publica.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
    print("Claves para " + nombre + " generadas aqui (" + nombre + "-pubica.pem y " + nombre + "-privada.pem)")
    

def encriptar(nombre, texto):
    with open(nombre + "-publica.pem", "rb") as f:
        publica = serialization.load_pem_public_key(f.read())
        return publica.encrypt(texto,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

def desencriptar(nombre, texto):
    with open(nombre + "-privada.pem", "rb") as f:
        privada = serialization.load_pem_private_key(f.read(), password=None)
    return privada.decrypt(texto,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    #return decrypted_bytes.decode("utf-8")


