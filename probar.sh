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
#build en windows
docker pull mcr.microsoft.com/powershell
docker run -it --rm -v /your/project/path:/app mcr.microsoft.com/powershell cmd /S /C "cd /app && pyinstaller --onefile --clean --noconfirm your_script.py"

