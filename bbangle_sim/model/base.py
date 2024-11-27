# abc 패키지

from abc import ABC, abstractmethod

class BaseModel(ABC):

    def __init__(self):
        pass
    
    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass