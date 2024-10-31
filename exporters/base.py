from abc import ABC, abstractmethod
from typing import List, Dict


class Exporter(ABC):
    @abstractmethod
    def export(self, questions: List[Dict], output_path: str):
        pass
