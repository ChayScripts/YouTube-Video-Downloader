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

# New: Output format selector
format_options = {
    "Video (MP4)": "mp4",
    "Audio (MP3)": "mp3"
}
format_label = st.selectbox("📦 Output Format", list(format_options.keys()))
output_format = format_options[format_label]

# ===============================
# Download Button
# ===============================
if st.button("⬇️ Start Download") and url:
    with st.spinner("🔍 Fetching media info..."):
        # Base options
        ydl_opts = {
            'outtmpl': str(download_folder / '%(title)s.%(ext)s'),
            'ffmpeg_location': FFMPEG_PATH,
            'noplaylist': True,
            'quiet': False,
            'http_headers': {'User-Agent': 'Mozilla/5.0'},
            'extractor_args': {'youtube': ['--no-check-certificate']},
        }

        # Choose formats by output type
        if output_format == 'mp3':
            # Audio-only: best audio, then extract to MP3 via FFmpeg
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    # '0' lets FFmpeg pick best quality; adjust to '192' if a target kbps is desired
                    'preferredquality': '0'
                }],
                # Ensure intermediate video is removed (default), explicit here for clarity
                'keepvideo': False,
            })
        else:
            # Video MP4: best video up to selected resolution + best audio, merge to MP4
            ydl_opts.update({
                'format': (
                    f'bestvideo[height<={resolution}]+bestaudio/best'
                    if resolution != 'best' else
                    'bestvideo[height<=2160]+bestaudio/best'
                ),
                'merge_output_format': 'mp4',
            })

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
                # This message applies to both cases; merging for video, conversion for audio happens afterward
                status.text("✅ Download complete. Finalizing file...")

        ydl_opts['progress_hooks'] = [hook]
        bar = st.progress(0)
        status = st.empty()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'media')
                st.subheader(f"🎬 Title: *{title}*")
                status.text("Starting download...")
                ydl.download([url])

            # Pick file pattern by output type
            pattern = "*.mp3" if output_format == "mp3" else "*.mp4"
            downloaded_files = list(download_folder.glob(pattern))
            if not downloaded_files:
                st.error("File not found after download.")
            else:
                final_file = max(downloaded_files, key=lambda f: f.stat().st_mtime)
                st.success("🎉 Successfully downloaded!")
                with open(final_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download MP3" if output_format == "mp3" else "⬇️ Download MP4",
                        data=f,
                        file_name=final_file.name,
                        mime="audio/mpeg" if output_format == "mp3" else "video/mp4"
                    )
        except Exception as e:
            st.error("❌ Download failed.")
            st.code(str(e))
            st.warning("Try a public, unlisted, or non-livestream video.")
# ===============================
# Footer
# ===============================
st.markdown("---")
