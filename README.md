[![Build Status](https://travis-ci.com/TerraFusion/batch4py.svg?branch=master)](https://travis-ci.com/TerraFusion/batch4py)
# batch4py

## Introduction
batch4py is a lightweight Python module that provides a programmatic interface to many common High Performance Computing (HPC) batch schedulers. It also provides a simple way to define directed acyclic graphs (DAG) of job chains.

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

## Installation
batch4py is on PyPi and can be installed using the normal commands:

`pip install --user batch4py`

## Compatability

Currently, batch4py is only compatible with TORQUE schedulers.
