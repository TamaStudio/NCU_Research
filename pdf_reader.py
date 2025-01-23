import re
import os
import pymupdf
import fitz
import spacy
from tqdm import tqdm

#def column_boxes(page: pymupdf.Page, foter_margin: int = 0, no_image_text: bool = True) -> list:

def read_pdf(source_path, result_path):
    # Processing PDF
    pdf_input_path = "source_path"
    pdf_output_path = "result_path"
    result = process_pdfs_in_folder(pdf_input_path, pdf_output_path)
    return result

#Extract Text From PDF
def extract_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    header = 30
    footer = 30

    try:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            #extracting the text block on the page
            blocks = page.get_text("blocks")
            blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

            page_width = page.rect.width
            mid_page = page_width / 2

            page_height = page.rect.height
            mid_page_height = page_height / 2

            left_column = ""
            right_column = ""
            mid_column = ""

            for block in blocks:
                x0, y0, x1, y1, text_block, a, b = block
                if y1 <= page_height - footer and y0 >= header:
                    if x1 < mid_page:
                        left_column += text_block + " "
                    elif x0 > mid_page:
                        right_column += text_block + " "
                    else:
                        mid_column += text_block + " "

            #full_text += "\n\n Mid column: \n\n" + mid_column + "\n\n Left column: \n\n" + left_column + "\n\n Right column \n\n" + right_column + "\n\n"
            full_text += mid_column + " " + left_column + " " + right_column

        return full_text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    

#Cleaning Extracted PDF Text
def cleaning_extracted_pdf(raw_text):
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', raw_text)
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove common unwanted sections like references
    text = re.sub(r'(References|Bibliography).*', '', text, flags=re.IGNORECASE | re.DOTALL)
    # Optional: Remove page numbers or section headers (pattern may vary by document)
    text = re.sub(r'\bPage\s?\d+\b', '', text)
    # Remove all text befor ABSTRACT
    text = re.sub(r'^.*?ABSTRACT', 'ABSTRACT', text, flags=re.DOTALL)
    # Remove all after Introduction
    text = re.sub(r'(?s)LITERATURE\s*REVIEW.*$', '', text)
    # Remove number references
    text = re.sub(r'([\d])', '', text)
    return text.strip()

#Export text into file
def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

#Processing All PDF File
def process_pdfs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF files in {input_folder}. Start processing...")

    for filename in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
        pdf_path = os.path.join(input_folder, filename)
        print(f"Processing {filename}...")

        text = extract_pdf(pdf_path)
        cleaned_text = cleaning_extracted_pdf(text)

        output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        print(f"Saved to {output_file}")
        return cleaned_text