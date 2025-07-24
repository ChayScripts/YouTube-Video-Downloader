# YouTube Video Downloader

A Streamlit-based web application for downloading YouTube videos with quality selection and progress tracking.

## Features

- **Web Interface**: Clean Streamlit UI for easy video downloading
- **Quality Selection**: Choose from Best, 1080p, 720p, 480p, or 360p
- **Progress Tracking**: Real-time download progress with speed and ETA
- **Auto-Merge**: Automatically combines video and audio streams
- **Direct Download**: Download button for completed videos
- **FFmpeg Integration**: Uses imageio-ffmpeg for seamless video processing
- **Age-Restricted Support**: Handles age-restricted and high-resolution videos

## Requirements

- Python 3.7+
- Streamlit
- yt-dlp
- imageio-ffmpeg
- pathlib (built-in)

## Installation

1. Clone or download the script
2. Install dependencies:
```bash
pip install streamlit yt-dlp imageio-ffmpeg
```

## Usage

1. Run the application:
```bash
streamlit run youtube_downloader.py
```

2. Browser opens automatically. If not, open your browser and navigate to `http://localhost:8501`

3. Enter a YouTube URL in the input field

4. Select desired video quality from the dropdown

5. Click "Start Download" to begin the process

6. Once complete, use the "Download MP4" button to save the file

## File Structure

```
project_folder/
├── youtube_downloader.py
└── downloads/           # Auto-created folder for downloaded videos
    └── [downloaded files]
```

## Configuration

The script automatically:
- Creates a `downloads` folder for storing videos
- Downloads and configures FFmpeg via imageio-ffmpeg
- Sets optimal yt-dlp parameters for reliability

## Quality Options

- **Best Quality**: Highest available resolution (up to 4K)
- **1080p**: Full HD resolution
- **720p**: HD resolution  
- **480p**: Standard definition
- **360p**: Low resolution for faster downloads

## Error Handling

Common issues and solutions:
- **Download failed**: Try public, unlisted, or non-livestream videos
- **FFmpeg errors**: The app automatically handles FFmpeg installation
- **Network issues**: Check internet connection and URL validity

## Technical Details

- Uses `yt-dlp` for robust YouTube downloading
- Implements progress hooks for real-time updates
- Merges video/audio streams into MP4 format
- Handles age-restricted content with appropriate headers
- Supports up to 4K resolution downloads

## Authors

* **Chay** - [ChayScripts](https://github.com/ChayScripts)

## Contributing

Contributions are welcome\! If you have suggestions for improvements, bug fixes, or new features, please feel free to:

  * Open an issue to discuss your ideas.
  * Fork the repository and submit a pull request.
