FROM python:3.11.7-alpine

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt && \
    rm ./requirements.txt

WORKDIR /api

COPY ./ /api/

EXPOSE 80

CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "80"]