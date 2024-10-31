from .base import QuestionGenerator


class MultipleChoiceGenerator(QuestionGenerator):
    def generate_question(self, content):
        return {
            "question": content["question"],
            "correct_answer": content["correct_answer"],
            "options": content["options"]
        }

    def get_prompt_template(self) -> str:
        return """Generate multiple-choice questions from the following text.
        Return in JSON format:
        [
            {
                "question": "Clear question text",
                "correct_answer": "Correct option",
                "options": ["option1", "option2", "option3", "option4"]
            }
        ]
        Apply these NLP principles:
        - Create plausible distractors
        - Ensure one clear correct answer
        - Avoid obvious wrong answers
        - Make sure that the correct answer is included in the options
        The list must have at least 2 questions per topic
        """
