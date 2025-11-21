from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

#Genera un par de claves RSA publica y privada, el nombre indica como se van a guardar: <nombre>-privada.pem <nombre>-publica.pem
def generar(nombre):
    if nombre == "admin":
        print("Error. Por cuestiones de seguridad no se permite generar claves a nombre de admin (estas claves ya estan en uso por el administrador, y poder reemplazarlas generaria una vulnerabilidad)")
        print("Si tu eres el encargado de preparar este programa, genera tus claves en otro programa (como gnupg), dejalas junto al ejecutable con los nombres admin-publica.pem y admin-privada.pem y bloquea su acceso al resto de usuarios (por ejemplo con root)")
        return
    privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    publica = privada.public_key()
    #Se guardan en el contexto donde este corriendo el programa (luego se pueden mover sin problema)
    with open(nombre + "-privada.pem", "wb") as f:
        f.write(privada.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
    with open(nombre + "-publica.pem", "wb") as f:
        f.write(publica.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
    print("Claves para " + nombre + " generadas aqui (" + nombre + "-pubica.pem y " + nombre + "-privada.pem)")
    
#Las claves se buscan y crean identificadas por nombre en la carpeta donde este el contexto a la hora de ejecutar el programa    

#Encripta un texto mediante una clave publica (buscando por nombre) y devuelve el contenido encriptado
def encriptar(nombre, texto):
    with open(nombre + "-publica.pem", "rb") as f:
        publica = serialization.load_pem_public_key(f.read())
        return publica.encrypt(texto,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

#Desencripta un texto mediante una clave privada (buscando por nombre) y devuelve el contenido desencriptado
def desencriptar(nombre, texto):
    with open(nombre + "-privada.pem", "rb") as f:
        privada = serialization.load_pem_private_key(f.read(), password=None)
    return privada.decrypt(texto,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    #return decrypted_bytes.decode("utf-8")
