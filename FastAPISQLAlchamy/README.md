# FastAPI-SQLAlchemy

FastAPI-SQLAlchemy is a Python API Application with FastAPI, JWT Authentication,
Postgresql, SQLAlchamy, Docker and Jenkins Pipeline

## Features

* Full **Docker** integration (Docker based).
* **Production ready** Python web server using Uvicorn and Gunicorn.
* Python <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> backend:
    * **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic).
    * **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
    * **Easy**: Designed to be easy to use and learn. Less time reading docs.
    * **Short**: Minimize code duplication. Multiple features from each parameter declaration.
    * **Robust**: Get production-ready code. With automatic interactive documentation.
    * **Standards-based**: Based on (and fully compatible with) the open standards for APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> and <a href="http://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.
    * <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">**Many other features**</a> including automatic validation, serialization, interactive documentation, authentication with OAuth2 JWT tokens, etc.
* **Secure password** hashing by default.
* **JWT token** authentication.
* **SQLAlchemy** models (independent of Flask extensions, so they can be used with Celery/Redis-rq workers directly).
* Basic starting models for users (modify and remove as you need).
* **CORS** (Cross Origin Resource Sharing).
* Load balancing between frontend and backend with **Nginx**, so you can have both under the same domain, separated by path, but served by different containers.
* Let's Encrypt **HTTPS** certificates automatic generation.


## How to use it

**psycopg2**

psycopg2 is postgresql adapter for sqlalchamy this can't be installed directly
in linux using pip, use below command to install

```bash 
sudo apt-get install python3-psycopg2
sudo apt-get install libpq-dev python3-dev
```

## JWT token authentication

JWT-Signature using RSA256 algorithm.

You can generate a 2048-bit RSA key pair with the following commands:

```bash
openssl genpkey -algorithm RSA -out rsa_private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in rsa_private.pem -pubout -out rsa_public.pem
```

## Create SSL Certificates using Certbot

Generate SSL cerificates from trusted thirdparty or openssl

	For Open SSL use Certbot (Let'sencrypt)
```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get install certbot python3-certbot-nginx

sudo certbot -d example.com certonly
```
certificates will be found in "/etc/letsencrypt/live/example.com/"

Generate a set of 4096-bit diffie-hellman parameters to improve security for some types of ciphers. 
```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl dhparam -out /etc/nginx/ssl/dhp-4096.pem 4096
```

## Deployment

FastAPI Backend can be deployed using docker. Use below docker image for deployment.

tiangolo/uvicorn-gunicorn-fastapi-docker - [Docker image with Uvicorn managed by Gunicorn for high-performance FastAPI web applications in Python 3.6 and above with performance auto-tuning. Optionally with Alpine Linux.](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)


#### References

The fundamental repositories:
- FastAPI - [FastAPI framework, high performance, easy to learn, fast to code, ready for production](https://fastapi.tiangolo.com/)
- full-stack-fastapi-postgresql - [Full stack, modern web application generator. Using FastAPI, PostgreSQL as database, Docker, automatic HTTPS and more.](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- blog-posts - [Build a web API from scratch with FastAPI - the workshop](https://github.com/tiangolo/blog-posts/tree/master/pyconby-web-api-from-scratch-with-fastapi)
- uvicorn - [The lightning-fast ASGI server.](https://www.uvicorn.org/deployment/)
- tiangolo/uvicorn-gunicorn-fastapi-docker - [Docker image with Uvicorn managed by Gunicorn for high-performance FastAPI web applications in Python 3.6 and above with performance auto-tuning. Optionally with Alpine Linux.](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)
- sqlalchemy - [SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL](https://www.sqlalchemy.org/)
