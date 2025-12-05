FROM public.ecr.aws/lambda/python:3.11

# Instalar compiladores (aumenta el tamaño de la imagen)
RUN yum install -y gcc gcc-c++ && yum clean all

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ${LAMBDA_TASK_ROOT}

CMD ["app.api.lambda_handler"]