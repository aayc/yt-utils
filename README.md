# yt-utils

A versatile CLI toolkit for learning from YouTube videos, featuring transcription, AI-powered Q&A, and flashcard generation capabilities using Google's Gemini AI.

## Features

- 💬 Interactive Q&A with video content using Google Gemini
- 📝 Transcribe YouTube videos to text
- 🎴 Generate Anki-compatible flashcards
- 🚀 Simple CLI interface

## Prerequisites

- Python 3.8+
- Google Gemini API key
- FFmpeg installed on your system

## Installation and Usage

1. Clone the repo
2. `pip install -r requirements.txt`
3. `export GEMINI_API_KEY=<your-api-key>`
4. `python run.py qa <youtube-url>`
5. `python run.py transcribe <youtube-url> <output_path>`
6. `python run.py flashcards <youtube-url> <output_csv_path>`
