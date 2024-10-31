from enum import Enum
from typing import Dict, Any
from .progress_logger import ProgressLogger


class QuestionType(Enum):
    SIMPLE_QA = "Simple Question & Answer"
    MULTIPLE_CHOICE = "Multiple Choice"


class ExportFormat(Enum):
    TEXT = "Plain Text"
    CSV = "CSV Format"
    ANKI = "Anki Flashcards"


class MenuManager:
    def __init__(self):
        self.logger = ProgressLogger("Menu")
        self.settings: Dict[str, Any] = {}

    def display_welcome(self):
        self.logger.info("Welcome to Flashcard Generator!")
        self.logger.info("==============================")

    def get_question_type(self) -> QuestionType:
        self.logger.info("\nSelect Question Type:")
        for i, qtype in enumerate(QuestionType, 1):
            self.logger.info(f"{i}. {qtype.value}")

        while True:
            try:
                choice = int(input("\nEnter your choice (1-2): "))
                if 1 <= choice <= len(QuestionType):
                    return list(QuestionType)[choice-1]
                self.logger.error("Invalid choice")
            except ValueError:
                self.logger.error("Please enter a number")

    def get_export_format(self) -> ExportFormat:
        self.logger.info("\nSelect Export Format:")
        for i, fmt in enumerate(ExportFormat, 1):
            self.logger.info(f"{i}. {fmt.value}")

        while True:
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if 1 <= choice <= len(ExportFormat):
                    return list(ExportFormat)[choice-1]
                self.logger.error("Invalid choice")
            except ValueError:
                self.logger.error("Please enter a number")

    def get_pdf_path(self) -> str:
        while True:
            path = input("\nEnter PDF file path: ").strip()
            from .input_validation import PDFValidator
            is_valid, error = PDFValidator.validate_pdf_path(path)
            if is_valid:
                return path
            self.logger.error(error)

    def configure_settings(self) -> Dict[str, Any]:
        self.display_welcome()
        self.settings["question_type"] = self.get_question_type()
        self.settings["export_format"] = self.get_export_format()
        self.settings["pdf_path"] = self.get_pdf_path()

        self.logger.success("\nConfiguration complete!")
        return self.settings
