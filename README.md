## 🎬 Reelify — AI Highlight Reel Generator

An AI-powered Streamlit app that automatically creates 30-second vertical highlight reels (1080×1920) from videos or YouTube links using Faster-Whisper for transcription and FFmpeg for reel generation.

## 🚀 Features

- **Upload or YouTube URL:** Supports both local uploads and YouTube video downloads (via yt_dlp).

- **AI Transcription:** Uses Faster-Whisper for accurate English speech-to-text conversion.

- **Highlight Detection:** Automatically identifies the most engaging 30-second segment based on word density.

- **1080×1920 Vertical Reel:** Output optimized for Instagram, YouTube Shorts, and Reels.

- **Download Option:** Instantly preview and download your generated highlight reel.

## 🧩 Tech Stack

- Python 3.10+

- Streamlit : Web UI

- Faster-Whisper : Speech recognition

- FFmpeg : Video processing

- yt_dlp : YouTube video downloader

## 📦 Installation

1.Clone the repository

      git clone https://github.com/yourusername/file_name.git
      
      cd file_name


2.Create and activate virtual environment

- Windows:

      python -m venv venv
      
      venv\Scripts\activate


- Mac/Linux:

      python -m venv venv
  
      source venv/bin/activate


3.Install dependencies

       pip install -r requirements.txt


4.Install FFmpeg

- Download from FFmpeg.org and add it to your system PATH.

## ⚙️ Usage

- Run the Streamlit app:

        streamlit run app.py


  Open the link displayed in your terminal (usually http://localhost:8501).

## 🧠 How It Works

**1. Upload Video or Enter YouTube URL**

- Users can upload a local video file (mp4, mov, avi) or paste a YouTube video link.

**2. Video Download & Preparation**

- YouTube videos are automatically downloaded and saved locally.

- Ensures proper video format for processing.

**3. Audio Extraction & Transcription**

- Audio is extracted from the video and transcribed using Faster-Whisper.

**4. Highlight Detection**

- Segments with the most words in a 30-second window are identified as highlights.

**5. Reel Generation (Vertical 1080×1920)**

- A 30-second vertical reel is generated using FFmpeg.

- Video is resized and cropped for TikTok/Reels/Instagram.

**6. Reel Preview & Download**

- The generated reel is displayed in the app.

- Users can download the highlight reel directly.

**7. Repeatable Process**

- Users can process multiple videos or YouTube URLs without restarting the app.
