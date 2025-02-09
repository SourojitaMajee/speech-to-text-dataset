# Speech_To_Text Dataset
The goal of this project is to create a data pipeline for a Speech-to-Text dataset using NPTEL lectures.The link to NPTEL Deep Learning course is https://nptel.ac.in/courses/106106184.

## Installation
  1. **Clone the Repository**
  3. **Navigate to the project directory :** `using cd`
  3. **Create and Activate virtual environment :** 
     ` ```python -m venv venv
     venv\Scripts\activate``` ` 
  4. **Install Dependencies :** ```pip install -r requirements.txt```

## Downloading lectures and transcripts

### Scripts - 
- **downloaded_transcripts.py** : downloads transcripts through web scraping
- **downloaded_lectures.py** : downloads lectures

### How to run -
1. Download Transcripts -
   - `python downloaded_transcripts.py`
   - Paste the URL and press Enter.

2. Download Lectures - 
   - `python downloaded_transcripts.py`
     
### Observations - 
1. ` downloaded_lectures.py ` 
   - Navigates the youtube playlist URL
   - Downloads leactures audio using ` yt-dlp ` in mp3 format
   - Saves downloaded lectures in ` lectures/ ` directory

 2. ` downloaded_transcripts.py `
    - Uses selenium for web scraping for the course url entered
    - uses relative xpath of the elements to navigate and interact
    - scrollIntoView(true) to avoid conflicts
    - Extracts Google Drive PDF download links and downloads them.
    - Saves files in ` transcripts/ ` directory.
 
 **The script uses Selenium for web scraping, so Google Chrome and ChromeDriver must be installed.**

 ## Preprocessing Audio

 ### Scripts - 
 - **downloaded_lectures_wav.sh :** converts .mp3 to .wav
