from .job import Job

'''Class that defines a single job in a job-chain workflow'''

class Dependency(object):
    
    _supported_dep = [ 'after', 'afterany', 'afterok', 'afternotok', \
        'before', 'beforeany', 'beforeok', 'beforenotok' ]
    
    def __init__(self, base, target, type='afterany' ):
        
        if type not in self._supported_dep:
            raise ValueError("Value for argument 'type' is not a supported \
                PBS dependency.")
        
        if not isinstance( base, Job ):
            raise TypeError("Argument 'base' is not of type Job")
        if not isinstance( target, Job ):
            raise TypeError("Argument 'target' is not of type Job")
 
        self._base      = base
        self._target    = target
        self._type      = type

    def __eq__( self, other ):
        if not isinstance( self, type(other) ):
            return False

        return self._base.get_id() == other._base.get_id() \
            and self._target.get_id() == other._target.get_id()

    def __hash__(self):
        return hash((self._base, self._target, self._type))
    
    def get_base(self):
        '''
**DESCRIPTION**  
    Get the base of the dependency.  
**ARGUMENTS**  
    None  
**EFFECTS**  
    None  
**RETURN**  
    Job object
        '''
        return self._base

    def get_target(self):
        '''
**DESCRIPTION**  
    Get the target of the dependency.  
**ARGUMENTS**  
    None  
**EFFECTS**  
    None  
**RETURN**  
    Job object
        '''
        return self._target

    def get_type(self):
        '''
**DESCRIPTION**  
    Get the type of the dependency. Valid values are defined by the system
    job scheduler.  
**ARGUMENTS**  
    None  
**EFFECTS**  
    None  
**RETURN**  
    str
        '''
        return self._type
