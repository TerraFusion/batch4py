[![Build Status](https://travis-ci.com/TerraFusion/batch4py.svg?branch=master)](https://travis-ci.com/TerraFusion/batch4py) [![PyPI version](https://badge.fury.io/py/batch4py.svg)](https://badge.fury.io/py/batch4py) 
# batch4py

## Introduction
batch4py is a lightweight Python 3 module that provides a programmatic interface to many common High Performance Computing (HPC) batch schedulers. It also provides a simple way to define directed acyclic graphs (DAG) of job chains.

A common workflow to submit jobs on a batch scheduler looks something like this:

```
$ qsub job1.pbs  
INFO: Job submitted to account: jq0
8625371
$ qsub -W afterany:8625371 job2.pbs
INFO: Job submitted to account: jq0
8625372
$ qsub -W afterany:8625371 job3.pbs
INFO: Job submitted to account: jq0
8625373
$ qsub -W afterany:8625372 job4.pbs
INFO: Job submitted to account: jq0
8625374
```

Performing these steps manually is fine for a handful of jobs, but doing it for dozens or hundreds of jobs becomes impractical. A 100-batch job that has a simple linear chain of dependence looks like this in batch4py:

```
job_list = []  
chain = batch4py.JobChain( 'pbs' )
for i in range(100):
    new_job = batch4py.Job( list_of_job_files[i] )
    job_list.append( new_job )
    chain.add_job( new_job )
    
# Define a simple linear tree
for i in range(99):
    chain.set_dep( job_list[i], job_list[i+1], 'afterany' )
    
# Submit job chain
chain.submit()
```

Users can also submit single jobs very easily:

```
>>> job = batch4py.Job( '/path/to/pbs/file/batch.sh' )
>>> job.submit()
```

Users may even pass file literals to batch4py (whereby the batch.sh file does not exist):

```
>>> job = batch4py.Job( '''#!/bin/bash
... #PBS -l nodes=1:ppn=32
... aprun -n 1 -- echo "Hello world!"
... ''')

>>> job.get_script()
'/path/to/install/dir/batch4py/pbs_files/e78d32d0-9299-4735-bbde-05fcb208b5cf.pbs'
```

Complete function documentation is maintained in the source code and can be accessed using Python's help() built-in.

## Installation
batch4py is on PyPi and can be installed using the normal commands:

`pip install --user batch4py`

## Compatability
Currently, batch4py is only compatible with TORQUE schedulers.

## Contributions
Pull requests are welcome. Please submit any issues or feature requests in the GitHub Issues tracker.

