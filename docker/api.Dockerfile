FROM python:3.10-slim as builder

WORKDIR /home/mindbox

RUN groupadd -r mindbox && useradd -d /home/mindbox -r -g mindbox mindbox \
    && chown mindbox:mindbox -R /home/mindbox

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/home/mindbox"

COPY ./task_2/requirements.txt ./

RUN pip install -r requirements.txt

COPY ./task_2/ .

USER mindbox

CMD ["python", "main.py"]