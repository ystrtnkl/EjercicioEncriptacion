#!/bin/bash
#generar entorno
docker build -t entorno-python .
#ejecutar archivo
docker run -it --rm -v "$(pwd)":/app entorno-python python3 encriptacion.py
