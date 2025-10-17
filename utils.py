import os
import subprocess
import json
import tempfile
import yt_dlp
import ffmpeg
import streamlit as st
from faster_whisper import WhisperModel

# Load Faster-Whisper model once
@st.cache_resource
def load_whisper_model():
    # Choose model: tiny, base, small, medium, large
    return WhisperModel("base", device="cpu", compute_type="int8_float16")


def download_youtube_video(url):
    try:
        os.makedirs("downloads", exist_ok=True)
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def extract_audio(video_path):
    """
    Extract audio from video using ffmpeg
    """
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    cmd = ["ffmpeg", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000", audio_path, "-y"]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return audio_path


def transcribe_audio(audio_path):
    """
    Transcribe audio using Faster-Whisper
    """
    model = load_whisper_model()
    st.info("🎧 Extracting and transcribing audio (Faster-Whisper)...")

    segments, info = model.transcribe(audio_path, beam_size=5)
    transcript_text = ""
    for segment in segments:
        transcript_text += segment.text + " "
    return transcript_text.strip()


def analyze_with_gpt(transcript):
    """
    Optional GPT-based highlight detection (keep if you want)
    """
    st.warning("⚠️ GPT highlight analysis removed. Using dummy segment.")
    return {"start": "00:00:30", "end": "00:01:00", "caption": "Interesting moment"}


def create_highlight(video_path, start_time, end_time, captions):
    """
    Generates a 30s clip with captions burned in
    """
    output_path = os.path.join("downloads", f"highlight_{os.path.basename(video_path)}")
    os.makedirs("downloads", exist_ok=True)

    temp_srt = os.path.join(tempfile.gettempdir(), "subs.srt")
    with open(temp_srt, "w", encoding="utf-8") as f:
        f.write(f"1\n00:00:00,000 --> 00:00:30,000\n{captions}\n")

    # Create 30s clip with subtitles
    (
        ffmpeg
        .input(video_path, ss=start_time, to=end_time)
        .output(output_path,
                vf=f"subtitles={temp_srt}:force_style='Fontsize=20'",
                codec="libx264",
                acodec="aac",
                preset="ultrafast",
                y=None)
        .run(quiet=True)
    )
    return output_path
