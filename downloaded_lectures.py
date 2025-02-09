import os
import yt_dlp

# YouTube playlist URL
YOUTUBE_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLyqSpQzTE6M9gCgajvQbc68Hk_JKGBAYT"

# O/P Directory
OUTPUT_DIR = "lectures"
os.makedirs(OUTPUT_DIR, exist_ok=True)
def download_audio(playlist_url, output_dir):
    print("[INFO] Downloading apyudio from YouTube playlist...")
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(autonumber)01d.%(ext)s',  
        'autonumber_start': 0,  # Start numbering from 0
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])
    print("[INFO] Audio download completed.")

if __name__ == "__main__":
    download_audio(YOUTUBE_PLAYLIST_URL, OUTPUT_DIR)
