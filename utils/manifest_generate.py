import os
import json
import re
import soundfile as sf

# Define directories and output file
AUDIO_DIR = "lectures_wav_trimmed"       # Directory containing audio files
TRANSCRIPT_DIR = "transcripts_processed"  # Directory containing transcript files
OUTPUT_MANIFEST = "train_manifest.jsonl"  # Output JSON Lines file

# Sort filenames numerically based on digits in the filename
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

# Get all WAV files, sorted numerically
audio_files = sorted(
    [f for f in os.listdir(AUDIO_DIR) if f.endswith('.wav')],
    key=extract_number
)

missing_transcripts = 0  # Counter for missing transcripts

with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as manifest:
    for audio_file in audio_files:
        transcript_file = os.path.splitext(audio_file)[0] + ".txt"
        audio_path = os.path.join(AUDIO_DIR, audio_file)
        transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)
        
        # Replace backslashes with forward slashes for JSON consistency
        audio_path = audio_path.replace("\\", "/")
        transcript_path = transcript_path.replace("\\", "/")

        if not os.path.exists(transcript_path):
            missing_transcripts += 1
            continue  # Skip processing if transcript is missing

        try:
            # Read transcript content
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcription = f.read().replace("\n", " ").strip()

            # Get audio file duration
            duration = sf.info(audio_path).duration

            # Write the entry to the output file
            json.dump({"audio_filepath": audio_path, "duration": duration, "text": transcription}, manifest)
            manifest.write("\n")

            print(f"Processed: {audio_file}")

        except Exception as e:
            print(f"Error processing {audio_file}: {e}")

print(f"Manifest created: {OUTPUT_MANIFEST}")
if missing_transcripts > 0:
    print(f"Warning: {missing_transcripts} transcript files were missing.")