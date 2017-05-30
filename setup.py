from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='easyaws',
    version='0.0.1',
    description='Tool to make AWS easy to use',
    long_description=long_description,
    url='https://github.com/mads-hartmann/easyaws',
    author='Mads Hartmann Jensen',
    author_email='mads379@gmail.com',
    license='MIT',
    classifiers=[],
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'boto3===1.4.4',
        'botocore==1.5.55',
        'PyYAML===3.12',
        'docopt==0.6.2',
        'tornado==4.5.1'
    ],
    extras_require={
        'dev': [
            'ptpython===0.39',
            'autopep8===1.3.1',
            'pylint===1.6.5',
            'flake8===3.3.0',
            'pydocstyle===1.1.1'
        ]
    },
    entry_points={
        'console_scripts': [
            'easyaws=easyaws.cli:run',
        ]
    }
)
