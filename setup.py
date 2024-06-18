from setuptools import find_packages, setup

from os import path
from io import open

ver_file = path.join('llm-a*', 'version.py')
with open(ver_file) as f:
    exec(f.read())

this_directory = path.abspath(path.dirname(__file__))

def readme():
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()

with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='llm-a*',
    version=__version__,
    description='RouteAgent: A Python package for route planning and evaluation with LLMs.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Silin Meng',
    author_email='silinmeng@gmail.com',
    url='https://github.com/SilinMeng0510/RouteAgent',
    download_url='https://github.com/SilinMeng0510/RouteAgent/archive/refs/heads/main.zip',
    keywords=['LLMs', 'route planning', 'deep learning', 'neural networks', 'research', 'LLMs agent'],
    packages=find_packages(),
    install_requires=requirements,
    setup_requires=['setuptools>=38.6.0']
)