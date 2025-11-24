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
#build en linux
docker run -it --rm -v "$(pwd)":/app -u $(id -u):$(id -g) entorno-python sh -c "cd /app && pyinstaller --onefile --clean --noconfirm encriptacion.py"
#build en windows (ejecutar en powershell en una maquina virtual de windows con python3 y pip installados)
pip install pyinstaller
pyinstaller --onefile --clean --noconfirm encriptacion.py

#build en linux y ejecutar todo en uno (solo desarrollo)
docker run -it --rm -v "$(pwd)":/app -u $(id -u):$(id -g) entorno-python sh -c "cd /app && pyinstaller --onefile --clean --noconfirm encriptacion.py" ; rm -rf build-linux ; mv build build-linux ; cd dist ; echo "" > claves.bin ; ./encriptacion
