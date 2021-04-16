from setuptools import setup

setup(
    name='FastAPIMongoEngine',
    version='0.0.1',
    author='scionoftech',
    description='FastAPIMongoEngine is a simple Python API Application',
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
