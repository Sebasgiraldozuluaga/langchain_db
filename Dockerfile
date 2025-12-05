# Dockerfile
FROM public.ecr.aws/lambda/python:3.13

# Paquetes del sistema si necesitas psycopg2 nativo; si usas psycopg2-binary, puedes omitir build-base
# RUN yum install -y postgresql15-libs

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Instalar dependencias necesaria
# Copiar el resto del código
COPY . .
CMD ["app.api.lambda_handler"]
