from abc import ABC, abstractmethod

class BaseAIService(ABC):

    @abstractmethod
    def analyze(self, defect: str, zone: str) -> str:
        pass
