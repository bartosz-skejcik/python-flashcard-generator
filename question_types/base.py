from abc import ABC, abstractmethod
from typing import Dict, Any


class QuestionGenerator(ABC):
    @abstractmethod
    def generate_question(self, content: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_prompt_template(self) -> str:
        pass
