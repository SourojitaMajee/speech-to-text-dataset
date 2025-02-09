import os
import sys
from pydub import AudioSegment

def trim_audio(input_file, output_file):
    # Load audio file
    audio = AudioSegment.from_wav(input_file)
    
    if len(audio) < 40000:
        print(f"Skipping {input_file}: Too short for trimming")
        return
    
    # Trim the first 10 and last 30 seconds
    trimmed_audio = audio[10000:-30000]
    
    # Export the processed file
    trimmed_audio.export(output_file, format="wav")
    print(f"Trimmed: {input_file} -> {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python processed_audio.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            trim_audio(input_path, output_path)