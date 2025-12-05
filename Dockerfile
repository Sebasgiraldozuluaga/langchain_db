FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./.env /code/.env
COPY ./system_agent.yaml /code/system_agent.yaml


CMD ["uvicorn", "app.api:api", "--host", "0.0.0.0", "--port", "80"]