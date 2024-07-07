FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY app /app

RUN ls -l

# RUN apt-get install python3-psycopg2

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r ./requirements.txt