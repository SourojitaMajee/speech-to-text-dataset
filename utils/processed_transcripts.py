import fitz  # PyMuPDF
import os
import re
from num2words import num2words
from tqdm import tqdm

# Input and output directories
input_dir = "transcripts"
output_dir = "transcripts_processed"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF while removing timestamps and images."""
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        page_text = page.get_text("text")  # Extract text only (ignore images)
        text += page_text + "\n"

    return text

def preprocess_text(text):
    """Convert text to lowercase, remove punctuations, numbers to words, and remove unwanted sections."""
    text = text.lower()  # Convert to lowercase
    
    # Convert numbers to words and add space between alphanumeric combinations
    text = re.sub(r'(\d+)([a-zA-Z])', lambda x: num2words(int(x.group(1))) + " " + x.group(2), text)
    text = re.sub(r'([a-zA-Z])(\d+)', lambda x: x.group(1) + " " + num2words(int(x.group(2))), text)
    text = re.sub(r'\d+', lambda x: num2words(int(x.group())), text)  # Convert remaining numbers to words
    
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuations

    # Remove timestamps like (Refer Slide Time: 03:10)
    text = re.sub(r"refer slide time\s+[a-zA-Z]+", '', text, flags=re.IGNORECASE)
    
    # Pattern to match only the header at the start:
    pattern = r"""(?ix)     # Case insensitive and verbose mode
    ^                       # Must start at beginning of document
    (?:                     # Non-capturing group for the entire header
        \s*.*?(?:deep\s*learning|professor|prof).*?\n   # Deep learning or professor line
        \s*.*?department.*?\n            # Department line
        \s*.*?institute.*?\n             # Institute line
        \s*.*?lecture.*?\n               # Lecture number line
        \s*.*?\n                         # Lecture title line
    )
    """

    text = re.sub(pattern, '', text, flags=re.VERBOSE | re.IGNORECASE | re.DOTALL)
    
    return text.strip()

def process_pdf(pdf_path, output_txt_path):
    """Extract and preprocess text from a PDF, then save it as a .txt file."""
    raw_text = extract_text_from_pdf(pdf_path)
    processed_text = preprocess_text(raw_text)

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(processed_text)

    print(f"Processed text saved to: {output_txt_path}")

# Process all PDFs in the input directory in sorted order
pdf_files = [f for f in sorted(os.listdir(input_dir)) if f.endswith(".pdf")]
for filename in tqdm(pdf_files, desc="Processing PDFs"):
    input_pdf_path = os.path.join(input_dir, filename)
    output_txt_path = os.path.join(output_dir, filename.replace(".pdf", ".txt"))
    process_pdf(input_pdf_path, output_txt_path)
