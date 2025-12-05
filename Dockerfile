# Dockerfile
FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./system_agent.yaml /code/system_agent.yaml

# Usar argumentos de construcción para las variables de entorno
ARG OPENAI_API_KEY
ARG PG_HOST
ARG PG_DATABASE
ARG PG_USER
ARG PG_PASSWORD
ARG PG_PORT

# Configurar las variables de entorno en el contenedor
ENV OPENAI_API_KEY=$OPENAI_API_KEY \
    PG_HOST=$PG_HOST \
    PG_DATABASE=$PG_DATABASE \
    PG_USER=$PG_USER \
    PG_PASSWORD=$PG_PASSWORD \
    PG_PORT=$PG_PORT

CMD ["uvicorn", "app.api:api", "--host", "0.0.0.0", "--port", "80"]
