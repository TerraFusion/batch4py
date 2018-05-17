import batch4py

job1 = batch4py.Job( "./batch.pbs" )
job2 = batch4py.Job( "./batch.pbs" )

print( job1.get_id() )
print( job2.get_id() )

chain = batch4py.JobChain( 'pbs' )

chain.add_job(job1)
chain.add_job(job2)

chain.set_dep( job2, job1, 'afterany' )

chain.submit(print_map=True, dry_run=True)

