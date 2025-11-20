# Encriptaciones
Programa para encriptar y desencriptar archivos usando AES128 y RSA

# Funcionamiento
- Se encripta un archivo/archivos(a elegir por el usuario) usando AES128, la clave aleatoria generada luego se encripta con una clave pública (opcional y a elegir por el usuario)
- Para desencriptar el archivo, hace falta el archivo encriptado en sí, la clave privada referente a la pública con la que se encriptó la clave AES128 y la clave AES128
- El programa permite encriptar solo con AES128 mostrando la clave o también encriptar dicha clave mediante RSA
- Básicamente es un programa pensado para que persona A le pase archivos a persona B (aunque este programa no los manda, solo los encripta)

## License
This project is licensed under the GNU General Public License v3.0.  
See the [LICENSE](./LICENSE.txt) file for details.
