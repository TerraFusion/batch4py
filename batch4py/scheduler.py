from abc import ABC, abstractmethod

class Scheduler(ABC):
    '''
    Abstract class that wraps the core scheduler functionalities.
    We make it abstract to be agnostic to different scheduler semantics.
    '''

    @abstractmethod
    def __init__():
        pass


    @abstractmethod
    def submit():
        pass

