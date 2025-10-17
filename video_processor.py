import os
import streamlit as st
import subprocess
import yt_dlp
from faster_whisper import WhisperModel

# -----------------------------
# Load Faster-Whisper model once
# -----------------------------
@st.cache_resource
def load_whisper_model():
    return WhisperModel("base", device="cpu", compute_type="int8")


# -----------------------------
# Download YouTube video
# -----------------------------
def download_youtube_video(url):
    try:
        os.makedirs("downloads", exist_ok=True)

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "quiet": False,
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)
            st.success(f"✅ Downloaded video: {video_file}")
            return video_file

    except Exception as e:
        st.error(f"❌ Error downloading video: {e}")
        return None


# -----------------------------
# Transcribe video audio
# -----------------------------
def transcribe_audio(video_path):
    model = load_whisper_model()
    st.info("🎧 Extracting and transcribing audio...")
    segments, info = model.transcribe(video_path, beam_size=5)

    transcript_text = ""
    for segment in segments:
        transcript_text += segment.text + " "
    return transcript_text.strip()


# -----------------------------
# Analyze highlights
# -----------------------------
def analyze_highlights(transcript_text, video_path=None):
    """
    Identify a 30-second highlight segment with the most words.
    """
    st.info("🧠 Analyzing transcript for highlight moments...")

    model = load_whisper_model()
    # Use actual video path if provided, else default temp
    path_to_use = video_path if video_path else "uploads/temp.mp4"
    segments, _ = model.transcribe(path_to_use, beam_size=5)
    segment_list = list(segments)

    windows = []
    i = 0
    while i < len(segment_list):
        start = segment_list[i].start
        end = start + 30.0
        words = []
        j = i
        while j < len(segment_list) and segment_list[j].end <= end:
            words.append(segment_list[j].text)
            j += 1
        if words:
            windows.append({
                "start": start,
                "end": end,
                "text": " ".join(words),
                "word_count": len(" ".join(words).split())
            })
        i += 1

    if not windows:
        return []

    # Pick window with most words
    best = max(windows, key=lambda x: x["word_count"])

    def format_time(seconds):
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02}:{m:02}:{s:02}"

    return [{
        "start": format_time(best["start"]),
        "end": format_time(best["end"]),
        "caption": best["text"]
    }]


# -----------------------------
# Generate vertical 1080x1920 reel
# -----------------------------

def parse_timestamp(ts):
    """Convert 'HH:MM:SS.xx' or 'MM:SS' string into float seconds."""
    if isinstance(ts, (int, float)):
        return float(ts)
    if not isinstance(ts, str):
        return 0.0
    parts = ts.strip().split(":")
    try:
        parts = [float(p) for p in parts]
        if len(parts) == 3:
            h, m, s = parts
            return h * 3600 + m * 60 + s
        elif len(parts) == 2:
            m, s = parts
            return m * 60 + s
        elif len(parts) == 1:
            return parts[0]
    except ValueError:
        pass
    return 0.0


def generate_reel(video_path, highlight, output_path="downloads/highlight_reel.mp4"):
    """
    Generate a 30-second vertical 1080x1920 highlight reel using ffmpeg.
    Works for both landscape and portrait videos.
    """

    import json

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Safely parse timestamps
    start = parse_timestamp(highlight.get("start", 0))
    end = parse_timestamp(highlight.get("end", start + 30))
    duration = max(0, min(30, end - start))  # limit to 30s max

    # --- Get input video dimensions ---
    try:
        probe_cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "json",
            os.path.abspath(video_path),
        ]
        probe = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        meta = json.loads(probe.stdout)
        width = meta["streams"][0]["width"]
        height = meta["streams"][0]["height"]
    except Exception:
        width, height = 1280, 720  # fallback

    # --- Adaptive filter: handle portrait or landscape ---
    if width >= height:
        # Landscape → fit width to 1080, pad vertically to 1920
        vf_filter = (
            "scale=1080:-2:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1"
        )
    else:
        # Portrait → fit height to 1920, pad horizontally to 1080
        vf_filter = (
            "scale=-2:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1"
        )

    # --- FFmpeg Command ---
    command = [
        "ffmpeg",
        "-y",
        "-ss", str(start),
        "-i", os.path.abspath(video_path),
        "-t", str(duration),
        "-vf", vf_filter,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        os.path.abspath(output_path),
    ]

    # --- Run FFmpeg safely ---
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("❌ FFmpeg error:\n", result.stderr)
            return None

        if os.path.exists(output_path):
            print("✅ 1080x1920 reel generated successfully:", output_path)
            return output_path
        else:
            print("❌ Output file missing after ffmpeg.")
            return None

    except Exception as e:
        print("❌ Exception while running ffmpeg:", str(e))
        return None

# -----------------------------
# Main video processor
# -----------------------------
def process_video():
    st.header("🎬 Reelify — Create AI Highlight Reels")

    # Ensure necessary folders exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)

    # Initialize session state
    if "video_path" not in st.session_state:
        st.session_state.video_path = None
    if "input_option" not in st.session_state:
        st.session_state.input_option = "📁 Upload File"
    if "reel_generated" not in st.session_state:
        st.session_state.reel_generated = False

    # Choose input type
    option = st.radio(
        "Choose input type:",
        ["📁 Upload File", "🔗 YouTube URL"],
        index=0 if st.session_state.input_option == "📁 Upload File" else 1
    )

    # Reset everything if input type changes
    if option != st.session_state.input_option:
        st.session_state.video_path = None
        st.session_state.input_option = option
        st.session_state.reel_generated = False

        reel_path = "downloads/highlight_reel.mp4"
        if os.path.exists(reel_path):
            try:
                os.remove(reel_path)
                time.sleep(0.2)  # wait to ensure file release
            except Exception:
                pass

    # -----------------------------
    # 📁 Upload Local File
    # -----------------------------
    if option == "📁 Upload File":
        uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
        if uploaded_file:
            # Remove old video if exists
            if st.session_state.get("video_path") and os.path.exists(st.session_state.video_path):
                try:
                    os.remove(st.session_state.video_path)
                    time.sleep(0.2)
                except Exception:
                    pass

            video_path = os.path.join("uploads", "temp.mp4")
            with open(video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state.video_path = video_path
            st.session_state.reel_generated = False
            st.success("✅ Video uploaded successfully!")

    # -----------------------------
    # 🔗 YouTube URL
    # -----------------------------
    elif option == "🔗 YouTube URL":
        url = st.text_input("Paste YouTube link:", key="youtube_url")

        if st.button("Download Video") and url:
            # Remove old video
            if st.session_state.get("video_path") and os.path.exists(st.session_state.video_path):
                try:
                    os.remove(st.session_state.video_path)
                    time.sleep(0.2)
                except Exception:
                    pass

            video_path = download_youtube_video(url)
            if video_path:
                st.session_state.video_path = video_path
                st.session_state.reel_generated = False
                st.success("✅ Video downloaded successfully!")

    # -----------------------------
    # ▶️ Show current video
    # -----------------------------
    if st.session_state.video_path and os.path.exists(st.session_state.video_path):
        st.video(st.session_state.video_path)
    elif st.session_state.video_path:
        st.warning("⚠️ The selected video file is missing. Please re-upload or redownload.")

    # -----------------------------
    # 🚀 Generate Highlight Reel
    # -----------------------------
    if st.session_state.video_path and st.button("🚀 Generate 30-second Highlight Reel"):
        with st.spinner("Processing video..."):
            reel_path = os.path.join("downloads", "highlight_reel.mp4")

            # Remove old reel safely
            if os.path.exists(reel_path):
                try:
                    os.remove(reel_path)
                    time.sleep(0.2)
                except Exception:
                    pass

            # Step 1: Transcribe
            transcript = transcribe_audio(st.session_state.video_path)

            # Step 2: Analyze highlights
            highlights = analyze_highlights(transcript, st.session_state.video_path)

            if not highlights:
                st.warning("No highlights found. Try another video.")
                return

            st.subheader("✨ Highlights Found:")
            for h in highlights:
                st.write(f"🕒 {h['start']} → {h['end']}: {h['caption']}")

            # Step 3: Generate highlight reel
            first_highlight = highlights[0]
            generate_reel(st.session_state.video_path, first_highlight, reel_path)

            # Step 4: Display reel safely
            if os.path.exists(reel_path):
                try:
                    st.video(reel_path)
                    st.success("✅ 30-second highlight reel generated!")
                    with open(reel_path, "rb") as f:
                        st.download_button(
                            "⬇️ Download Reel", f, file_name="highlight_reel.mp4"
                        )
                    st.session_state.reel_generated = True
                except Exception as e:
                    st.error(f"⚠️ Could not load reel: {e}")
            else:
                st.warning("⚠️ Reel file not found. Try generating again.")
