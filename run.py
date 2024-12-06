from pathlib import Path
from typing_extensions import Annotated
import typer
from llm import gemini_qa
from utils import download_audio, transcribe_audio, try_cleanup_file, write_anki_compatible_csv
from rich.progress import Progress, SpinnerColumn, TextColumn
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

app = typer.Typer()

def create_progress():
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    )

@app.command()
def make_flashcards(youtube_url: str, output_csv_path: str):
    with create_progress() as progress:
        progress.add_task("Downloading audio...", total=None)
        audio_file_path = download_audio(youtube_url)
        
        progress.add_task("Transcribing audio...", total=None)
        transcript = transcribe_audio(audio_file_path)
        try_cleanup_file(audio_file_path)

        progress.add_task("Calling Google Gemini model...", total=None)
        flashcards = gemini_qa(transcript)

        progress.add_task(f"Writing Anki CSV to {output_csv_path}...", total=None)
        write_anki_compatible_csv(flashcards, output_csv_path)

    print(f"✨ Anki flashcards have been saved to {output_csv_path}")

@app.command()
def transcribe(youtube_url: str, output_path: Annotated[str | None, typer.Argument()] = None):
    with create_progress() as progress:
        progress.add_task("Downloading audio...", total=None)
        audio_file_path = download_audio(youtube_url)
        
        progress.add_task("Transcribing audio...", total=None)
        transcript = transcribe_audio(audio_file_path)
        try_cleanup_file(audio_file_path)

    if output_path:
        Path(output_path).write_text(transcript)
        print(f"✨ Transcript saved to {output_path}")
    else:
        print(transcript)

@app.command()
def qa(youtube_url: str):
    with create_progress() as progress:
        progress.add_task("Downloading audio...", total=None)
        audio_file_path = download_audio(youtube_url)
        
        progress.add_task("Transcribing audio...", total=None)
        transcript = transcribe_audio(audio_file_path)
        try_cleanup_file(audio_file_path)

    print("\n✨ Transcript loaded. You can now ask questions about it.")
    print("Type 'quit' to exit")

    while True:
        question = input("\nEnter your question: ")
        if question.lower() == 'quit':
            break
            
        with create_progress() as progress:
            progress.add_task("Getting answer from Gemini...", total=None)
            answer = gemini_qa(question, transcript)
        
        print(answer)
        print("===")


if __name__ == "__main__":
    app()
