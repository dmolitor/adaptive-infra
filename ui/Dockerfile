FROM python:3.11.7-alpine

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt && \
    rm ./requirements.txt

WORKDIR /app

COPY ./ /app

EXPOSE ${APP_PORT}

CMD uvicorn app:app --host 0.0.0.0 --port ${APP_PORT}