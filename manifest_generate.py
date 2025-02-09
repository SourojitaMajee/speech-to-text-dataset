import os
import json
import re
import soundfile as sf

AUDIO_DIR = "lectures_processed" #input directory
TRANSCRIPT_DIR = "transcripts_processed" #input directory
OUTPUT_MANIFEST = "train_manifest.jsonl"  #output directory


# Generate JSON Lines file
with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as manifest:
    # get all audio files and sort them numerically
    audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.wav')]
    audio_files.sort(key=lambda x: int(os.path.splitext(x)[0]))  # Sort by the numeric part of filename
    
    for audio_file in audio_files:
        # corresponding transcript file (assuming same name, different extension)
        transcript_file = os.path.splitext(audio_file)[0] + ".txt"
        audio_path = os.path.join(AUDIO_DIR, audio_file)
        transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)
        
        # replace backslashes for JSON consistency
        audio_path = audio_path.replace("\\", "/")
        transcript_path = transcript_path.replace("\\", "/")
        
        if not os.path.exists(transcript_path):
            print(f"Warning: Transcript file {transcript_path} not found.")
            continue
            
        # Read and clean transcription
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcription = f.read().strip()
        
        # Remove newlines
        transcription = re.sub(r"\s+", " ", transcription)
        
        # Get audio duration
        with sf.SoundFile(audio_path) as audio:
            duration = len(audio) / audio.samplerate
        
        # Create JSON object
        entry = {
            "audio_filepath": audio_path,
            "duration": duration,
            "text": transcription
        }
        manifest.write(json.dumps(entry) + "\n")
        print(f"Processed file: {audio_file}")  # progress indicator

print(f"Training manifest file created: {OUTPUT_MANIFEST}")
