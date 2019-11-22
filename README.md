FaceSmash

Utiliza anaconda para crear un entorno virtual e instalar los paquetes necesarios para utilizar Flask, puedes descargarlo aquí:
https://www.anaconda.com/distribution/
Al instalarlo asegurate de seleccionar la opción que pondrá el ejecutable “conda.exe” dentro de las variables de entorno.

Para crear un nuevo entorno virtual utiliza el siguiente comando dentro de la terminal:
	conda create –-name “nombre del ambiente” python=”versión de Python”

paquetes necesarios para utilizar FaceSmash:
	pip install flask
	pip install flask_login
	pip install flask_bcrypt
	pip install peewee
	pip install flask_wtf
