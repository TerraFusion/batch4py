#from distutils.core import setup
from setuptools import setup

setup(
    name='batch4py',
    version='0.1.0',
    author='Landon T. Clipp',
    author_email='clipp2@illinois.edu',
    packages=['batch4py'],
    description='Programmatic interface to batch schedulers.',
    long_description='batch4py provides a Python intreface to many common \
        batch schedulers. It rests on top of command-line executables like \
        qsub and allows for users to define complex job chains.',
    install_requires=[ 'pyyaml' ],
    url = 'https://github.com/TerraFusion/batch4py',
    download_url='https://github.com/TerraFusion/batch4py/archive/0.1.0.tar.gz',
    keywords = ['batch', 'torque', 'pbs', 'pbs-torque', 'hpc', 'python', 'python3', 'cluster' ],
)
