# 🎬 Reelify — AI Highlight Reel Generator

> An AI-powered Streamlit app that automatically creates **30-second vertical highlight reels (1080×1920)** from videos or YouTube links using **Faster-Whisper** for transcription and **FFmpeg** for reel generation.

---

## 🚀 Features

- 🎥 **Upload or YouTube URL:** Supports both local uploads and YouTube video downloads (via `yt_dlp`).
- 🧠 **AI Transcription:** Uses **Faster-Whisper** for accurate English speech-to-text conversion.
- ✨ **Highlight Detection:** Automatically identifies the most engaging 30-second segment based on word density.
- 🎵 **Works for Songs Too:** Can process music videos and generate reels from lyrical or vocal sections.
- 📱 **1080×1920 Vertical Reel:** Output optimized for Instagram, YouTube Shorts, and Reels.
- 💾 **Download Option:** Instantly preview and download your generated highlight reel.

---

## 🧩 Tech Stack

- **Python 3.10+**
- **Streamlit** — Web UI
- **Faster-Whisper** — Speech recognition
- **FFmpeg** — Video processing
- **yt-dlp** — YouTube video downloader

---

## 📦 Installation

1.Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/reelify.git
cd reelify

2.Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # (on Windows)
source venv/bin/activate  # (on Mac/Linux)

3.Install dependencies
```bash
pip install -r requirements.txt

If FFmpeg is not installed, download it from FFmpeg.org and add it to your system PATH.

## ⚙️ Usage
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Then open the link displayed in your terminal (usually http://localhost:8501).

## 🧠 How It Works
1.Upload Video or Enter YouTube URL
     Users can upload a local video file (mp4, mov, avi) or paste a YouTube video link.
2.Video Download & Preparation
     If a YouTube URL is provided, the video is automatically downloaded and saved locally.  
     The system ensures proper video format conversion for processing.
3.Audio Extraction & Transcription
     Audio is extracted from the video and transcribed using Faster-Whisper.
4.Highlight Detection
     Segments with the most words in a 30-second window are identified as highlights.
5.Reel Generation (Vertical 1080×1920)
     A 30-second vertical reel is created using FFmpeg.
     Videos are resized and cropped for TikTok/Reels/Instagram.
6.Reel Preview & Download
     The generated reel is displayed directly in the app.
     Users can download the highlight reel with a single click.
7.Repeatable Process
     Users can process multiple videos or YouTube URLs without restarting the app.


