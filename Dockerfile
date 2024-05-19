# Utiliza una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /code

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto en el contenedor
COPY . /code/

# Ejecuta las migraciones y el servidor de desarrollo de Django
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
