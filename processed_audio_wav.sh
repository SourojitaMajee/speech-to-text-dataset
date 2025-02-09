#!/bin/bash

# Ensure the script stops on errors
set -e

# Take user inputs
INPUT_DIR=$1
OUTPUT_DIR=$2
NUM_CPUS=$3

mkdir -p "$OUTPUT_DIR"

# Function to process a single file
process_audio() {
    input_file=$1
    output_file="$OUTPUT_DIR/$(basename "$input_file" .mp3).wav"

    echo "Processing: $input_file"
    ffmpeg -i "$input_file" -ar 16000 -ac 1 "$output_file" -y
    echo "Finished: $input_file"
}

export -f process_audio
export OUTPUT_DIR

# Find all audio files and process them in parallel
find "$INPUT_DIR" -type f -name "*.mp3" | parallel -j "$NUM_CPUS" process_audio {}

