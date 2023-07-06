from setuptools import setup, find_packages

setup(
    name='basekit',
    version='1.0.11',
    description='Uma biblioteca para auxiliar no desenvolvimento de aplicativos Python, fornecendo funcionalidades comuns e utilitários',
    author='Marco Souza',
    author_email='marco.rsouza@gmail.com',
    packages=find_packages(),
    install_requires=[
        'attrs',
        'bcrypt',
        'blinker',
        'click',
        'colorama',
        'dependency-injector',
        'flasgger',
        'Flask',
        'Flask-JWT-Extended',
        'flask-marshmallow',
        'Flask-SQLAlchemy',
        'flask-swagger',
        'greenlet',
        'injector',
        'itsdangerous',
        'Jinja2',
        'jsonschema',
        'MarkupSafe',
        'marshmallow',
        'marshmallow-sqlalchemy',
        'mistune',
        'mysqlclient',
        'packaging',
        'PyJWT',
        'pyrsistent',
        'python-dotenv',
        'PyYAML',
        'six',
        'SQLAlchemy',
        'typing_extensions',
        'Werkzeug',
        'requests'
    ],
)