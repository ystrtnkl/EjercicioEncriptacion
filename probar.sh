#!/bin/bash
#generar entorno para desarrollar
docker build -t entorno-python .
#ejecutar archivo
docker run -it --rm -v "$(pwd)":/app -u $(id -u):$(id -g) entorno-python python3 encriptacion.py
#restringir permisos al admin
sudo chown root:root claves.bin
sudo chown root:root admin-privada.pem
sudo chown root:root admin-publica.pem
sudo chown root:root admin.key
