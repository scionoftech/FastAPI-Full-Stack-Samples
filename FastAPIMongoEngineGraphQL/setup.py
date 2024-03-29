from setuptools import setup

setup(
    name='FastAPIMongoEngineGraphQL',
    version='0.0.1',
    author='scionoftech',
    description='FastAPIMongoEngineGraphQL is a simple Python API Application',
    platforms='any',
    install_requires=[
        'fastapi',
        'uvicorn',
        'gunicorn',
        'pandas',
        'numpy',
        'mongoengine',
        'passlib'
        'python-jose',
        'python-multipart',
        'async-exit-stack'
        'async-generator',
    ],
)
