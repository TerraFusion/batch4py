import batch4py
import pytest
import os

class TestJobTORQUE(object):
    def test_simple( self ):
        job1 = batch4py.job.TORQUE( "./batch.pbs" )
        job2 = batch4py.job.TORQUE( "./batch.pbs" )

        print( job1.get_id() )
        print( job2.get_id() )

        chain = batch4py.JobChain( 'pbs' )

        chain.add_job(job1)
        chain.add_job(job2)

        chain.set_dep( job2, job1, 'afterany' )
        print( chain.submit(print_map=True, dry_run=True) )
      
    def test_cycle( self ):
        job1 = batch4py.job.TORQUE( "./batch.pbs" )
        job2 = batch4py.job.TORQUE( "./batch.pbs" )
        job3 = batch4py.job.TORQUE( "./batch.pbs" )
        chain = batch4py.JobChain( 'pbs' )

        chain.add_job(job1)
        chain.add_job(job2)
        chain.add_job(job3)

        chain.set_dep(job1, job2, 'afterany' )
        chain.set_dep(job2, job3, 'afterany' )
        chain.set_dep(job3, job1, 'afterany' )

        with pytest.raises( RuntimeError ):
            chain.submit( dry_run = True )

    def test_abstract( self ):
        with pytest.raises( TypeError ):
            job = batch4py.job.Job()

    def test_constructor_bad_type( self ):
        with pytest.raises( ValueError ):
            job = batch4py.job.TORQUE('this_file_never_exists04949103', 'bad' )

    def test_constructor_create_file( self ):
        job = batch4py.job.TORQUE( 'test file' )
        with open( job.get_script(), 'r' ) as f:
            try:
                assert f.read() == 'test file'
            finally:
                os.remove( job.get_script() )
                
    def test_set_config( self ):
        job = batch4py.job.TORQUE( os.path.join( os.path.dirname(__file__), 'batch.pbs' ))
        
        with pytest.raises( KeyError ):
            job.set_config( no_parameter = 0 )

        job.set_config( nodes='10', ppn='32', walltime='03:00:00', account='A', node_type='XE')

    def test_depends( self ):
        job1 = batch4py.job.TORQUE( os.path.join( os.path.dirname(__file__), 'batch.pbs' ))
        job2 = batch4py.job.TORQUE( os.path.join( os.path.dirname(__file__), 'batch.pbs' ))
        
        with pytest.raises( ValueError):
            job1.depends( job2, 'bad_depends' )

        depends = ['after', 'afterany', 'afterok', 'afternotok', 'before', 'beforeany', 
            'beforeok', 'beforenotok' ]
        for i in depends:
            job1.depends( job2, i )
