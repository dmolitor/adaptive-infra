FROM python:3.11.7-alpine

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt && \
    rm ./requirements.txt

# Generate SSL/TSL certificate
RUN apk update && \
    apk add --no-cache openssl && \
    openssl req -x509 -newkey rsa:4096 -keyout /key.pem -out /cert.pem -sha256 -days 3650 -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=CommonNameOrHostname"

WORKDIR /api

COPY ./ /api/

EXPOSE ${API_CONTAINER_PORT}

CMD uvicorn main:api --host 0.0.0.0 --port ${API_CONTAINER_PORT} --ssl-keyfile=/key.pem --ssl-certfile=/cert.pem