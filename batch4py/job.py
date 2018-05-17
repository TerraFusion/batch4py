import uuid
import os
import subprocess
from collections import defaultdict
import uuid
from batch4py import constants
import errno
import time


class Job(object):
    
    _valid_sched = { 'pbs' : 'qsub' }
    '''Scheduler name to executable mappings'''

    def __init__( self, script, script_type=None, account=None ):
        '''
**DESCRIPTION**  
    Class responsible for submitting a single job to the PBS scheduler.  
**ARGUMENTS**  
    *script*  (str) -- Path to file, or string literal for the PBS script.  
    *script_type* (str) -- Choose from { 'file', 'literal' }. Specifies 
        whether script is a path (file) or a string literal. If it is literal,
        script is interpreted to be a file literal, in which case script
        will be printed to a file before passing to the scheduler. This file 
        will be stored in batch4py's installation directory.  

    *account* (str)   -- Specify any PBS account to submit the job under.  

**EFFECTS**  
    Submits job to the scheduler  
**RETURN**
    None
        '''
        # Generate a unique ID for this job
        self._id            = uuid.uuid4()

        # JOB SCRIPT
        #----------------------------------------------------------
        self._job_script    = None                                #
        self.set_script( script, script_type )                    #
        #----------------------------------------------------------

        # SCHEDULER VARIABLES
        #---------------------------------------------------------------
        # _sched_id is ID that scheduler itself will provide later on  #
        self._sched_id          = None                                 #
        self._sched_type        = None                                 #
        # override_sched changes behavior of sched_type interpretation #
        self._sched_override    = False                                #
        self._account           = account                              #
        #---------------------------------------------------------------

    def __hash__(self):
        return hash( self._id )

    def get_script( self ):
        '''
        Return path of self's scheduler file.
        '''

        return self._job_script

    def set_script( self, script, type = None ):
        '''
**DESCRIPTION**  
    Set the scheduler script to use for this job. Can either pass in a script
    literal or a path to a file. By default, function will attempt to
    interpret argument 'script' as either a literal or an existing file.

    This function should normally never be called because it is implicitly
    called in the class's constructor.  
**ARGUMENTS**  
    *script* (str)  -- Script literal or path to a script  
    *type* (str)   -- Set to 'file' or 'literal' to force interpretation of
        script.  
**EFFECTS**  
    Stores *script* in self's attributes.  
**RETURN**  
    None
        '''
        supported_types = ['file', 'literal']
        if type is not None and type not in supported_types:
            raise ValueError("Argument 'type' not a valid value.")

        # is_file expression generated by solving a Karnaugh map
        is_file = ( type is None and os.path.isfile( script ) ) or type == 'file'

        if not is_file:
            # Assign a unique name to PBS file and write the string literal 
            # to it
            pbs_name = '{}.pbs'.format( self._id )
            script_path = os.path.join( constants.PBS_DIR, pbs_name )
            
            try:
                os.makedirs( constants.PBS_DIR )
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            
            with open( script_path, 'w' ) as f:
                f.write( script )

                script = script_path

        self._job_script = os.path.abspath( script )


    #====================================================================
    def get_id( self ):
        '''
**DESCRIPTION**  
    Get the internal uuid identifier of self.  
**ARGUMENTS**  
    None  
**EFFECTS**  
    None  
**RETURN**  
    uuid object
        '''
        return self._id
        
    #====================================================================
    def set_sched_id( self, id ):
        '''
**DESCRIPTION**  
    Set self's identifier given by the system's scheduler.  
**ARGUMENTS**  
    *id* (str)  -- Identifier understood by the system scheduler.  
**EFFECTS** 
    Sets self's scheduler ID attribute.  
**RETURN**  
    None
        '''
        if not isinstance( id, str ):
            raise TypeError("Argument 'id' is not a str.")
        self._sched_id = id

    #====================================================================
    def get_sched_id( self ):
        '''
**DESCRIPTION**  
    Return self's ID as given by the system scheduler. Attribute will not
    contain a valid value until self is submitted to the scheduler 
    using submit().  
**ARGUMENTS**  
    None  
**EFFECTS**  
    None  
**RETURN**  
    Scheduler ID (str)
        '''
        return self._sched_id

    #====================================================================
    def set_sched( self, type, override=False ):
        '''
**DESCRIPTION**  
    Set the system scheduler type. Typical schedulers may be: pbs, slurm, moab.  
**ARGUMENTS**  
    *type* (str)    -- Type of scheduler to use. Supported values: pbs  
    *override* (bool)   -- If true, will use string passed in type as a
        command line literal. i.e. *type* must be an actual terminal command
        used for submitting jobs. If false, type will be internally mapped to
        valid scheduler command-line semantics.  
**EFFECTS**  
    Modifies private attribute.  
**RETURN**  
    None
        '''


        if not override and type not in self._valid_sched:
            raise ValueError('Invalid scheduler type.')

        self._sched_type = type
        self._sched_override = override
        
    #====================================================================
    def is_base( self, dependency ):
        '''
**DESCRIPTION**  
    Checks if self is the base of the dependency  
**ARGUMENTS**  
    *dependency* (Dependency)   -- The dependency to check if self is the base of  
**EFFECTS**  
    None  
**RETURN**  
    True/False
        '''
        return self == dependency.job_0

    def submit( self, dependency = None, params = None, stdin=None, stdout=None, \
                stderr=None, dry_run = False ):
        '''
**DESCRIPTION**  
    Submits the job to the system job scheduler.  
**ARGUMENTS**  
    *dependency* (list of Dependency) -- Specifies all job dependencies.  
    *params* (str) -- Extra command line arguments to add to the scheduler
        call.  
    *stdin* (stream) -- stdin to scheduler.  
    *stdout* (stream) -- stdout redirection of scheduler.  
    *stderr* (stream) -- stderr redirection of scheduler.  
    
**EFFECTS**  
    Submits job to the queue.  
**RETURN**  
    None
        '''

        # Perform automatic garbage collection of old PBS files
        # TODO implement this garbage collection


        dep = defaultdict(list)
        # Gather all the dependencies into a nice dict, perform sanity checks
        for i in dependency:
            if self is not i.get_base():
                raise RuntimeError("Listed a dependency in which self is not the base!")
            dep[ i.get_type() ].append( i.get_target() )

        # Create the command line arguments
        args = []
        # append executable name
        if self._sched_override:
            args.append( self._sched_type )
        else:
            args.append( self._valid_sched[ self._sched_type ] )

        # Add PBS dependencies
        for dep_type in dep:
            args.append( '-W' )
            dep_string = 'depend={}'.format( dep_type )
            for job in dep[dep_type]:
                sched_id = job.get_sched_id()

                if sched_id is None:
                    raise ValueError(\
                    'Job {} has not been submitted to the scheduler!'\
                    .format( job ) )

                dep_string += ':{}'.format( sched_id )

            args.append(dep_string)
        
        # Specify job account
        if self._account:
            args.append('-A')
            args.append( self._account )

        args.append( self._job_script )

        # We cd to the location of the PBS script because PBS will print out
        # log files in its current working directory. Just keep them all in
        # one place.
        os.chdir( os.path.dirname( self._job_script ) )

        if dry_run:
            print('\nDry run submission.')

        print( ' '.join(args) )
        
        if not dry_run:
            subproc = subprocess.Popen( args, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
            retcode = subproc.wait()

            # Retrieve the scheduler ID
            stderrFile = subproc.stderr
            sub_stderr = stderrFile.read()
            stdoutFile = subproc.stdout
            sub_stdout = stdoutFile.read()

            if stdout:
                stdout.write( sub_stdout )
            if stderr:
                stderr.write( sub_stderr )
            if retcode != 0:
                print( sub_stderr )
                print( sub_stdout )
                raise RuntimeError('Process exited with retcode {}'.format(retcode))

            self._sched_id = sub_stdout.strip().decode('UTF-8')
        else:
            # Use internal identifier instead of scheduler-supplied ID
            self._sched_id = self._id
 
