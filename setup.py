"""
Hatch.sh makes it easy to build services using AWS.
"""

from setuptools import setup, find_packages

from hatch.version import VERSION

setup(
    name='hatch-cli',
    version=VERSION,
    description='Command line interface for hatch.sh',
    long_description=__doc__,
    url='https://github.com/mads-hartmann/hatch',
    download_url='https://github.com/mads-hartmann/hatch/archive/{}.tar.gz'.format(VERSION),
    author='Mads Hartmann Jensen',
    author_email='mads379@gmail.com',
    license='MIT',
    classifiers=[],
    keywords=[],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={'': ['README.md']},
    install_requires=[
        'boto==2.47.0',
        'boto3==1.4.4',
        'botocore==1.5.55',
        'PyYAML==3.12',
        'docopt==0.6.2',
        'tornado==4.5.1'
    ],
    extras_require={
        'dev': [
            'ptpython==0.39',
            'autopep8==1.3.1',
            'pylint==1.6.5',
            'flake8==3.3.0',
            'flake8-print==2.0.2',
            'pydocstyle==1.1.1',
            'infi.docopt-completion==0.2.7'
        ]
    },
    entry_points={
        'console_scripts': [
            'hatch=hatch.cli:run',
        ]
    }
)
