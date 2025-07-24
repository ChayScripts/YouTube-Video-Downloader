import streamlit as st
import yt_dlp
import imageio_ffmpeg as ffmpeg
from pathlib import Path

# ===============================
# App Config
# ===============================
st.set_page_config(page_title="YouTube Video Downloader", page_icon="🎥", layout="centered")

st.title("🎥 YouTube Video Downloader")
st.write("Download any public YouTube video. Works with age-restricted & high-res videos.")

# ===============================
# Downloads folder
# ===============================
download_folder = Path("downloads")
download_folder.mkdir(exist_ok=True)

# ===============================
# Get FFmpeg path
# ===============================
try:
    FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()
except Exception as e:
    st.error(f"❌ FFmpeg failed to load: {e}")
    st.stop()

# ===============================
# User Inputs
# ===============================
url = st.text_input("🔗 Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

quality_options = {
    "Best Quality": "best",
    "1080p": "1080",
    "720p": "720",
    "480p": "480",
    "360p": "360"
}
selected_label = st.selectbox("🎥 Select Quality", list(quality_options.keys()))
resolution = quality_options[selected_label]

# ===============================
# Download Button
# ===============================
if st.button("⬇️ Start Download") and url:
    with st.spinner("🔍 Fetching video info..."):
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best' if resolution != 'best' else 'bestvideo[height<=2160]+bestaudio/best',
            'outtmpl': str(download_folder / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'ffmpeg_location': FFMPEG_PATH,
            'noplaylist': True,
            'quiet': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            },
            'extractor_args': {'youtube': ['--no-check-certificate']},
        }

        def hook(d):
            if d['status'] == 'downloading':
                pct = d.get('_percent_str', '0%').replace('%', '')
                try:
                    progress = float(pct) / 100
                except:
                    progress = 0
                bar.progress(min(progress, 1.0))
                status.text(f"📥 {d.get('_speed_str', 'N/A')} | ETA: {d.get('_eta_str', 'N/A')}")
            elif d['status'] == 'finished':
                status.text("✅ Download complete. Merging video...")

        ydl_opts['progress_hooks'] = [hook]
        bar = st.progress(0)
        status = st.empty()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                st.subheader(f"🎬 Video: *{title}*")

                status.text("Starting download...")
                ydl.download([url])

            downloaded_files = list(download_folder.glob("*.mp4"))
            if not downloaded_files:
                st.error("File not found after download.")
            else:
                final_file = max(downloaded_files, key=lambda f: f.stat().st_mtime)
                st.success("🎉 Successfully downloaded!")
                with open(final_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download MP4",
                        data=f,
                        file_name=final_file.name,
                        mime="video/mp4"
                    )
        except Exception as e:
            st.error("❌ Download failed.")
            st.code(str(e))
            st.warning("Try a public, unlisted, or non-livestream video.")

# ===============================
# Footer
# ===============================
st.markdown("---")
