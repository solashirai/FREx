from abc import ABC, abstractmethod


class Explanation(ABC):

    @abstractmethod
    def get_explanation_string(self) -> str:
        pass
