from dotenv import load_dotenv
import os
import genanki
import PyPDF2
from typing import List, Dict, Any

from question_types.simple_qa import SimpleQAGenerator
from question_types.multiple_choice import MultipleChoiceGenerator
from exporters.text_exporter import TextExporter
from llm.client import LLMClient
from utils.error_handler import error_handler
from utils.progress_logger import ProgressLogger
from utils.menu import MenuManager
from utils.input_validation import PDFValidator

# Initialize components
logger = ProgressLogger()
menu = MenuManager()


def pdf_to_text(pdf_path: str) -> str:
    """Convert PDF to text with progress tracking."""
    logger.info(f"Converting PDF to text: {pdf_path}")

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)
        text = ''

        for page_num in range(total_pages):
            logger.progress(f"Processing page", page_num + 1, total_pages)
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text


def create_flashcards(notes: List[tuple]) -> List[genanki.Note]:
    """Create Anki flashcard notes from question-answer pairs."""
    logger.info("Creating flashcard notes...")

    model = genanki.Model(
        1091735104,
        "Simple Model",
        fields=[{"name": "Question"}, {"name": "Answer"}],
        templates=[{
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}",
        }]
    )

    flashcards = []
    for question, answer in notes:
        note = genanki.Note(model=model, fields=[question, answer])
        flashcards.append(note)

    logger.success(f"Created {len(flashcards)} flashcard notes")
    return flashcards


def build_deck(deck_name: str, notes: List[genanki.Note]) -> None:
    """Build and save Anki deck."""
    logger.info(f"Building Anki deck: {deck_name}")

    deck = genanki.Deck(2059400110, deck_name)
    for note in notes:
        deck.add_note(note)

    output_file = f"{deck_name}.apkg"
    genanki.Package(deck).write_to_file(output_file)
    logger.success(f"Deck saved as: {output_file}")


@error_handler
def main() -> None:
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY not found in environment variables")
        return

    # Initialize LLM client
    client = LLMClient(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1/"
    )

    # Get configuration through menu
    settings = menu.configure_settings()
    pdf_path = settings["pdf_path"]

    # Get deck name
    while True:
        deck_name = input("\nEnter deck name: ").strip()
        if deck_name:
            break
        logger.error("Deck name cannot be empty")

    # Process PDF and generate questions
    logger.info(f"\nProcessing {pdf_path}")
    text = pdf_to_text(pdf_path)

    # Create appropriate generator based on settings
    generator = SimpleQAGenerator(
    ) if settings["question_type"].value == "Simple Question & Answer" else MultipleChoiceGenerator()

    # Generate questions
    logger.info("\nGenerating questions...")
    try:
        questions = client.generate_questions(text, generator)
    except Exception as e:
        logger.error(f"Failed to generate questions: {str(e)}")
        return

    # Create and export based on format
    if settings["export_format"].value == "Anki Flashcards":
        notes = create_flashcards(questions)
        build_deck(deck_name, notes)

    # Always create text export as backup
    exporter = TextExporter()
    exporter.export(questions, f"{deck_name}_questions.txt")

    logger.success("\nProcess completed successfully!")


if __name__ == "__main__":
    main()
