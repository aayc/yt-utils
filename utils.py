from pathlib import Path
import pandas as pd
import os
import yt_dlp
import whisper

def transcribe_audio(audio_file_path: str) -> str:
    # Load Whisper model
    model = whisper.load_model("base")  # You can choose 'tiny', 'base', 'small', 'medium', 'large'
    
    # Transcribe audio
    result = model.transcribe(audio_file_path)
    transcript = result['text']
    return transcript

def download_audio(youtube_url: str) -> None:
    # Downloads audio from a YouTube video using youtube-dl or yt-dlp
    # Install yt-dlp: pip install yt-dlp

    output_audio_path = str((Path(__file__).parent / "_downloaded_audio").resolve())

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_audio_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return output_audio_path + ".wav"

def try_cleanup_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)

def write_anki_compatible_csv(flashcards: list[dict[str, str]], output_csv_path: str) -> None:
    # Write flashcards to CSV in Anki format using pandas
    df = pd.DataFrame([{
        'Question': card['question'],
        'Answer': card['answer']
    } for card in flashcards])
    
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
