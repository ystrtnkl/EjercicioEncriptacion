#!/bin/bash
#generar entorno
docker build -t entorno-python .
#ejecutar archivo
docker run -it --rm -v "$(pwd)":/app -u $(id -u):$(id -g) entorno-python python3 encriptacion.py

