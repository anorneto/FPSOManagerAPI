from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='FPSOManagerAPI',

    version='0.0.1',

    description='Python backend to manage different equipment of an FPSO.',
    long_description_content_type="text/markdown",
    long_description=long_description,

    url='https://github.com/anorneto/FPSOManagerAPI',

    author='Anor Neto',
    author_email='anornetoo@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 1- Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords='fpso - manager - api',

    packages=find_packages(
        include=['api', 'api.*'], exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3.6',
    install_requires=['fastapi', 'uvicorn', 'pydantic','sqlalchemy','pytest','faker'],
    entry_points={
        'console_scripts': ['fpso-manager=api.main:main']
    },
)
