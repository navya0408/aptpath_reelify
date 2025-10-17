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

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/reelify.git
cd reelify

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # (on Windows)
# or
source venv/bin/activate  # (on Mac/Linux)

# Install dependencies
pip install -r requirements.txt
If FFmpeg is not installed, download it from FFmpeg.org and add it to your system PATH.

⚙️ Usage
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Then open the link displayed in your terminal (usually http://localhost:8501).

🧠 How It Works
Upload or Download Video

Upload a local video or enter a YouTube URL.

Transcription

Audio is transcribed using Faster-Whisper.

Highlight Detection

The app scans for the most word-dense 30-second segment.

Reel Generation

The segment is cropped and converted into a 1080×1920 vertical reel using FFmpeg.

Preview & Download

The generated reel is displayed for preview, with a download option.

🧬 Example Output

Input: YouTube or uploaded .mp4

Output: downloads/highlight_reel.mp4 (30 seconds, 1080×1920)
