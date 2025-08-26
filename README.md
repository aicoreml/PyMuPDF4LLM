# PDF Extractor with OCR

This application extracts text and tables from PDF files, including both text-based and image-based PDFs. It uses PyMuPDF4LLM for text/table extraction and Tesseract OCR for image-based text recognition.

## Features

- Extracts text and tables from text-based PDFs using PyMuPDF4LLM
- Performs OCR on image-based PDFs using Tesseract
- Supports multiple languages for OCR (English, German, French, Spanish, Italian, Portuguese, Dutch, Russian, Chinese, Japanese)
- Flexible table extraction strategies
- User-friendly web interface built with Streamlit
- Combines all extracted content into a single downloadable file

## File Structure

```
PyMuPDF4LLM/
├── .env
├── app_pymupdf4llm_tesseract.py
├── ert_notes.txt
├── flow.md
├── requirements.txt
└── output_tesseract/
    ├── extracted_content_DE.md
    └── extracted_content_EN.md
```

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd PyMuPDF4LLM
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR on your system:
   - Windows: Download from https://github.com/tesseract-ocr/tesseract
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

4. (Optional) Download additional language packs for better OCR accuracy:
   - Download from: https://github.com/tesseract-ocr/tessdata

## Usage

1. Run the application:
   ```
   streamlit run app_pymupdf4llm_tesseract.py
   ```

2. Upload a PDF file through the web interface

3. Configure extraction options as needed:
   - Enable/disable OCR for images
   - Select OCR language
   - Choose table extraction strategy
   - Toggle page separators

4. View extracted content in the browser

5. Download the combined content as a markdown file

## Requirements

- Python 3.7+
- Streamlit 1.29.0+
- PyMuPDF4LLM 0.0.10+
- PyMuPDF 1.23.0+
- Tesseract OCR
- OpenCV 4.8.0+
- NumPy 1.24.0+
- Pillow 10.0.0+
- Pytesseract 0.3.10+

## Development Notes

For development and testing instructions, see `ert_notes.txt`.

## Sample Outputs

Sample processed outputs can be found in the `output_tesseract/` directory:
- `extracted_content_DE.md`: German language content extraction example
- `extracted_content_EN.md`: English language content extraction example

## How It Works

For a detailed description of the application flow and structure, see `flow.md`.