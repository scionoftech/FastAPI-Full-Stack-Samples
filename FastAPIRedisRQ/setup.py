from setuptools import setup

setup(
    name='FastAPIRedisRQ',
    version='0.0.1',
    author='scionoftech',
    description='FastAPIRedisRQ is a simple Python API Application with Redis RQ ',
    platforms='any',
    install_requires=[
        'fastapi',
        'uvicorn',
        'gunicorn',
        'python-jose',
        'python-multipart',
        'async-exit-stack'
        'async-generator',
        'redis',
        'rq'
    ],
)
