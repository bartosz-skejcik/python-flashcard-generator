import json
import time
import random
from typing import Dict, List
import logging
from openai import OpenAI
from utils.error_handler import LLMError


class LLMClient:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        # Add retry configuration
        self.max_retries = 3
        self.base_delay = 1  # Base delay in seconds
        self.max_delay = 32  # Max delay in seconds
        self.jitter = 0.1   # Random jitter factor

    def _exponential_backoff(self, attempt: int) -> float:
        """Calculate backoff delay with jitter."""
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        jitter = random.uniform(-self.jitter * delay, self.jitter * delay)
        return delay + jitter

    def generate_questions(self, text: str, question_generator, max_retries=3) -> List[Dict]:
        # Input validation
        if not text or not isinstance(text, str):
            raise ValueError("Text input must be a non-empty string")
        if not hasattr(question_generator, 'get_prompt_template'):
            raise ValueError("Invalid question generator")

        last_error = None
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[
                        {"role": "system",
                            "content": question_generator.get_prompt_template()},
                        {"role": "user", "content": text}
                    ]
                )

                # Validate and parse response
                content = response.choices[0].message.content
                print(content)
                if not content:
                    raise LLMError("Empty response received")

                # Parse JSON response
                try:
                    questions = json.loads(content)
                    return questions
                except json.JSONDecodeError:
                    raise LLMError("Invalid JSON response from API")

            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = self._exponential_backoff(attempt)
                    logging.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s")
                    time.sleep(delay)

        # If we get here, all retries failed
        raise LLMError(f"Failed after {max_retries} attempts. Last error: {
                       str(last_error)}")
