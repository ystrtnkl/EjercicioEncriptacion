import shlex
import os

#Para que el programa soporte rutas absolutas en Windows y Linux se normalizan asi
def normalizar_ruta(ruta):
    ruta = ruta.strip('"').strip("'")
    path = os.path.expanduser(ruta)
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path) if not os.path.isabs(path) else path
    return path
