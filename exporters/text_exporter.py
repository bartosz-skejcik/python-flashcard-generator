from typing import Dict, List
from .base import Exporter


class TextExporter(Exporter):
    def export(self, questions: List[Dict], output_path: str):
        with open(output_path, 'w', encoding='utf-8') as f:
            for q in questions:
                if 'correct_answer' in q:  # Multiple choice question
                    options = '\n  - '.join([''] + q['options'])
                    f.write(f"{q['question']}\t{
                            q['correct_answer']}{options}\n\n")
                else:  # Simple Q&A
                    f.write(f"{q['question']}\t{q['answer']}\n")
