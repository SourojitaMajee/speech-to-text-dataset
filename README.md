# Speech_To_Text Dataset
The goal of this project is to create a data pipeline for a Speech-to-Text dataset using NPTEL lectures.The link to NPTEL Deep Learning course is https://nptel.ac.in/courses/106106184.


## 1. Installation
  1. **Clone the Repository**
  2. **Create and Activate virtual environment :** 
     ```sh
      python -m venv venv
      venv\Scripts\activate
  3. **Install Dependencies :**
     ```sh
     pip install -r requirements.txt
     ```

## 2. Downloading lectures and transcripts
### Scripts :
- **downloaded_transcripts.py** : downloads transcripts through web scraping.
- **downloaded_lectures.py** : downloads lectures.
### How to run :
1. **Download Transcripts**  
    ```sh
    # Run the script to download transcripts
    python ./utils/downloaded_transcripts.py

    # Paste the URL when prompted and press Enter
    ```
2. **Download Lectures** 
   ```sh
    # Run the script to download transcripts
    python ./utils/downloaded_lectures.py

    # Paste the URL when prompted and press Enter
    ```
### Observations : 
1. **downloaded_lectures.py**
   - Uses `selenium` for web scraping.
   - Uses `XPATH` to navigate and interact with the elements like weeks, lessons and youtube links(first traverses iframe and then uses anchor tag to get the youtube link).
   - Downloads leactures audio using ` yt-dlp ` in mp3 format from the youtube links, `tqdm` tracks progress.
   - Saves downloaded lectures in ` lectures/ ` directory.
 2. **downloaded_transcripts.py**
    - Uses selenium for web scraping for the course url entered, tqdm and logging for progress and error handling.
    - Uses relative `XPATH` of the elements to navigate and interact, scrollIntoView(true) to avoid conflicts.
    - Extracts Google Drive PDF download links and downloads them, Saves files in ` transcripts/ ` directory.
 **The script uses Selenium for web scraping, so Google Chrome and ChromeDriver must be installed.**

  ** NOTE : The mp3 lecture audios can be downloaded from the youtube playlist url - **https://www.youtube.com/playlist?list=PLyqSpQzTE6M9gCgajvQbc68Hk_JKGBAYT** itself, iterating over the playlist and using yt-dlp alone(without selenium), but the lectures are not sequentially arranged in the playlist.**

 ## 3. Preprocessing Audio
 ### Scripts : 
 - **downloaded_lectures_wav.sh** : converts .mp3 to .wav format.
 - **processed_audio.py** : trims first 10 seconds and last 30 seconds of the audio.
 ### How to run :
 1. **processed_audio_wav.sh**
    ```sh
     bash # to open wsl terminal in vscode
     sudo apt update
     sudo apt install parallel # to install parallel.
     sudo apt install ffmpeg # to install ffmpeg.

     #check if ffmpeg and ffprobe are installed
     ffmpeg -version
     ffprobe -version
    
     chmod +x processed_audio_wav.sh
     bash processed_audio_wav.sh lectures/ lectures_wav/ 4  # here 4 is the number of cores/cpus to use(can be increased or decreased); `lectures/` is the input directory and `lectures_wav/` is the output directory.
     exit # to get back to vscode powershell terminal.
     ``` 
      **Alternatively**
      - Open Command Prompt (cmd), type `wsl` and press Enter.
      - Reach the desired directory.
      - Rest same as above.
      - `exit` to end the wsl terminal.
 3. **processed_audio.py**
    ```sh
      python utils/processed_audio.py lectures_wav/ lectures_wav_trimmed/

    # here `lectures_wav/` is the input directory and `lectures_wav_trimmed/` is the output directory.
    ```
 ### Observations :
 1. **processed_audio_wav.sh** 
    - Converts all .mp3 files to .wav format, with a 16KHz sampling rate, mono channel format
    - Uses `ffmpeg` for audio conversion, `parallel` for parallel processing.
    - Saves the .wav files in `lectures_wav/` directory.
 2. **processed_audio.py**
    - Trims first 10 seconds(intro music) and last 30 seconds(outro music) of the audio using pydub.
    - Saves the trimmed .wav files in `lectures_wav_trimmed/` directory.

## 4. Preprocessing Transcripts
### Scripts :
- **processed_transcripts.py** : preprocesses the transcripts.
### How to run :
  ```sh
    python utils/processed_transcripts.py transcripts/ transcripts_processed/

# here `transcripts/` is the input directory and `transcripts_processed/` is the output directory.
  ```
### Observations :
1. **processed_transcripts.py**
    - Uses fitz (PyMuPDF) to extract text from PDFs, ignoring images, `tqdm` tracks progress.
    - Converts text to lowercase, uses regex and num2words to convert numbers into words and handle alphanumeric combinations.
    - Removes punctuations, timestamps, headers and subheaders using regex.
    - Saves the preprocessed transcripts in `transcripts_processed/` directory.

 ## 5. Creating the train manifest file

 ### Scripts :
 - **manifest_generate.py** : creates the train manifest file
 ### How to run :
  ```sh
    python utils/manifest_generate.py

# here `transcripts_processed/` is the input directory and `train_manifest.jsonl` is the output file.
  ```
 ### Observations :
 1. **manifest_generate.py**
    - Reads all .txt files in `transcripts_processed/` directory, and all .wav files in `lectures_wav_trimmed/` directory in sorted order.
    - Replaces `\\` with `/` for JSON consistency and removes `\n`(newlines) from the transcripts.
    - Calculates audio duration using `soundfile` library.
    - Creates a manifest file with the following format: audio_filepath, duration, text.
    - Saves the manifest file in `train_manifest.jsonl` file.
    
 ## 6. Dashboard
 ### Scripts :
 - **dashboard.py** : creates the dashboard.
 ### How to run :
  ```sh
    streamlit run utils/dashboard.py
  ```
 ### Observations :
 1. **dashboard.py**
    - Creates dashboard using streamlit
    - Displays the dashboard with the following metrics:
        - Key Statistics (total hours - 26.22, total utterances - 117, vocabulary size - 5753, alphabet size - 26)
    - Alphabet in dataset
    - Data distribution using histogram using `Altair` (comapred duration per file, words per file, characters per file with frequency)
    - Observation using `Plotly` in the form of donut charts
      - Total hours vs Utterances
      - Vocabulary(unique words) vs Alphabet Size(unique characters)
        
![Screenshot 2025-02-10 195841](https://github.com/user-attachments/assets/0948ebb2-3dc5-40f0-9527-eada075bd70b)

![Screenshot 2025-02-10 200014](https://github.com/user-attachments/assets/7ebfcab4-575b-4d15-b003-8c319255b9f0)

 
