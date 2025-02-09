# Speech_To_Text Dataset
The goal of this project is to create a data pipeline for a Speech-to-Text dataset using NPTEL lectures.The link to NPTEL Deep Learning course is https://nptel.ac.in/courses/106106184.


## Installation
  1. **Clone the Repository**
  2. **Create and Activate virtual environment :** 
     ` ```python -m venv venv
     venv\Scripts\activate``` ` 
  3. **Install Dependencies :** ```pip install -r requirements.txt```


## Downloading lectures and transcripts

### Scripts - 
- **downloaded_transcripts.py** : downloads transcripts through web scraping.
- **downloaded_lectures.py** : downloads lectures.


### How to run -
1. **Download Transcripts** -
   - `python ./utils/downloaded_transcripts.py` and press Enter.
   - Paste the URL and press Enter.

2. **Download Lectures** - 
   - `python ./utils/downloaded_lectures.py` and press Enter.
     
### Observations - 
1. **downloaded_lectures.py**
   - Navigates the youtube playlist URL.
   - Downloads leactures audio using ` yt-dlp ` in mp3 format.
   - Saves downloaded lectures in ` lectures/ ` directory.

 2. **downloaded_transcripts.py**
    - Uses selenium for web scraping for the course url entered.
    - uses relative xpath of the elements to navigate and interact.
    - scrollIntoView(true) to avoid conflicts.
    - Extracts Google Drive PDF download links and downloads them.
    - Saves files in ` transcripts/ ` directory.
    - tqdm and logging for progress and error handling.
 
 **The script uses Selenium for web scraping, so Google Chrome and ChromeDriver must be installed.**


 ## Preprocessing Audio

 ### Scripts - 
 - **downloaded_lectures_wav.sh** : converts .mp3 to .wav format
 - **processed_audio.py** : trims first 10 seconds and last 30 seconds of the audio

 ### How to run - 
 1. **processed_audio_wav.sh**
      - Type `bash` in terminal, to open wsl terminal in vscode.
      - `sudo apt update` and `sudo apt install parallel` to install parallel.
      - `sudo apt install ffmpeg` to install ffmpeg.
      - `ffmpeg -version` and `ffprobe -version` to check if ffmpeg and ffprobe are installed.
      - `chmod +x processed_audio_wav.sh`
      - `bash processed_audio_wav.sh lectures/ lectures_wav/ 4`, here 4 is the number of cores/cpus to use(can be increased or decreased); `lectures/` is the input directory and `lectures_wav/` is the output directory.
      - Type `exit` to get back to vscode powershell terminal.

      **Alternatively**
      - Open Command Prompt (cmd), type `wsl` and press Enter.
      - Reach the desired directory.
      - Rest same as above.
      - `exit` to end the wsl terminal.

 2. **processed_audio.py** 
      - `python utils/processed_audio.py lectures_wav/ lectures_wav_trimmed/`, here `lectures_wav/` is the input directory and `lectures_wav_trimmed/` is the output directory.

 ### Observations - 
 1. **processed_audio_wav.sh** 
    - Converts all .mp3 files to .wav format, with a 16KHz sampling rate, mono channel format.
    - Uses `ffmpeg` for audio conversion, `parallel` for parallel processing.
    - Saves the .wav files in `lectures_wav/` directory.

 2. **processed_audio.py**
    - Trims first 10 seconds(intro music) and last 30 seconds(outro music) of the audio using pydub.
    - Saves the trimmed .wav files in `lectures_wav_trimmed/` directory.


## Preprocessing Transcripts

### Scripts - 
- **processed_transcripts.py** : preprocesses the transcripts

### How to run - 
1. `python utils/processed_transcripts.py transcripts/ transcripts_processed/`, here `transcripts/` is the input directory and `transcripts_processed/` is the output directory.

### Observations - 
1. **processed_transcripts.py**
    - Uses fitz (PyMuPDF) to extract text from PDFs, ignoring images.
    - Converts text to lowercase.
    - Uses regex and num2words to convert numbers into words and handle alphanumeric combinations.
    - Removes punctuations, timestamps, headers and subheaders using regex.
    - `tqdm` tracks progress.
    - Saves the preprocessed transcripts in `transcripts_processed/` directory.


 ## Creating the train manifest file

 ### Scripts - 
 - **manifest_generate.py** : creates the train manifest file

 ### How to run - 
 1. `python utils/manifest_generate.py`, here `transcripts_processed/` is the input directory and `train_manifest.jsonl` is the output file.

 ### Observations - 
 1. **manifest_generate.py**
    - Reads all .txt files in `transcripts_processed/` directory, and all .wav files in `lectures_wav_trimmed/` directory in sorted order.
    - Replaces `\\` with `/` for JSON consistency and removes `\n`(newlines) from the transcripts.
    - Calculates audio duration using `soundfile` library.
    - Creates a manifest file with the following format: audio_filepath, duration, text.
    - Saves the manifest file in `train_manifest.jsonl` file.
    

 ## Dashboard
 
 ### Scripts - 
 - **dashboard.py** : creates the dashboard

 ### How to run - 
 1. `streamlit run utils/dashboard.py`

 ### Observations - 
 1. **dashboard.py**
    - Creates dashboard using streamlit
    - Displays the dashboard with the following metrics:
        - Key Statistics (total hours, total utterances, total words, total characters)
    - Alphabet in dataset
    - Data distribution using histogram using `Altair` (comapred duration per file, words per file, characters per file with frequency)
    - Observation using `Plotly` in the form of donut charts
      - Total hours vs Utterances
      - Vocabulary(unique words) vs Alphabet Size(unique characters)

 