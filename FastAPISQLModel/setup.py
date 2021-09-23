from setuptools import setup

setup(
    name='FastAPISQLModel',
    version='0.0.1',
    author='scionoftech',
    description='FastAPISQLModel is a simple Python API Application',
    platforms='any',
    install_requires=[
        'fastapi',
        'uvicorn',
        'gunicorn',
        'pandas',
        'numpy',
        'psycopg2',
        'sqlalchemy',
        'passlib'
        'python-jose',
        'python-multipart',
        'async-exit-stack'
        'async-generator',
    ],
)
