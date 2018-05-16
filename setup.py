#from distutils.core import setup
from setuptools import setup

setup(
    name='batch4py',
    version='0.1.0',
    author='Landon T. Clipp',
    author_email='clipp2@illinois.edu',
    packages=['batch4py'],
    description='Batch API',
    long_description='None',
    install_requires=[ 'pyyaml' ],
)
