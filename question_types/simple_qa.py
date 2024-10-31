from .base import QuestionGenerator


class SimpleQAGenerator(QuestionGenerator):
    def generate_question(self, content):
        return {
            "question": content["question"],
            "answer": content["answer"]
        }

    def get_prompt_template(self) -> str:
        return """Generate simple question-answer pairs from the following text.
        Return in JSON format:
        [
            {
                "question": "Clear, concise question",
                "answer": "Clear, accurate answer"
            }
        ]
        Apply these NLP principles:
        - Use clear, grammatically correct language
        - Focus on key concepts
        - Vary question complexity
        - Ensure answers are concise but complete
        The list must have at least 2 questions per topic
        """
