import streamlit as st
import pymupdf4llm
import pymupdf as fitz
import io
import cv2
import numpy as np
import pytesseract
from PIL import Image

st.title("📄 PDF Extractor with OCR")
st.markdown("Upload a PDF file to extract text and tables (with OCR for images).")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Sidebar options
st.sidebar.header("Extraction Options")
use_ocr = st.sidebar.checkbox("Use OCR for Images", value=True)
language = st.sidebar.selectbox(
    "OCR Language",
    ["eng", "deu", "fra", "spa", "ita", "por", "nld", "rus", "chi_sim", "jpn"],
    index=1,  # Default to German
    format_func=lambda x: {
        "eng": "English",
        "deu": "German",
        "fra": "French",
        "spa": "Spanish",
        "ita": "Italian",
        "por": "Portuguese",
        "nld": "Dutch",
        "rus": "Russian",
        "chi_sim": "Chinese (Simplified)",
        "jpn": "Japanese"
    }[x]
)
table_strategy = st.sidebar.selectbox(
    "Table Strategy",
    ["lines_strict", "lines", "text"],
    index=0
)
page_separators = st.sidebar.checkbox("Show Page Separators", value=True)

def extract_text_from_image(image_bytes, lang):
    """Extract text from image using OCR"""
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL Image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Apply OCR with specified language
        text = pytesseract.image_to_string(opencv_image, lang=lang)
        return text
    except Exception as e:
        st.warning(f"OCR failed for image: {str(e)}")
        return ""

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    
    try:
        # Read the file content
        file_bytes = uploaded_file.getvalue()
        
        # Create a BytesIO object
        pdf_stream = io.BytesIO(file_bytes)
        
        # Open with PyMuPDF directly from stream
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        
        # Check if PDF has text or is image-based
        total_text = ""
        image_pages = []
        
        ocr_extracted_text = ""
        
        if use_ocr:
            st.info(f"Processing PDF with OCR for images (Language: {language})...")
            
            # Process each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text().strip()
                total_text += text
                
                # Check for images
                image_list = page.get_images()
                if not text and image_list:
                    image_pages.append(page_num + 1)
                    st.info(f"Processing images on page {page_num + 1} with OCR...")
                    
                    # Extract images and apply OCR
                    for img_index, img in enumerate(image_list):
                        try:
                            xref = img[0]
                            pix = fitz.Pixmap(doc, xref)
                            
                            # Convert to PNG bytes
                            if pix.n < 5:  # Grayscale or RGB
                                img_data = pix.tobytes("png")
                            else:  # CMYK: convert to RGB first
                                pix = fitz.Pixmap(fitz.csRGB, pix)
                                img_data = pix.tobytes("png")
                            
                            # Apply OCR
                            image_text = extract_text_from_image(img_data, language)
                            if image_text.strip():
                                ocr_extracted_text += "\n--- OCR Text from Page " + str(page_num + 1) + ", Image " + str(img_index + 1) + " ---\n"
                                ocr_extracted_text += image_text
                            
                            pix = None  # Free pixmap
                        except Exception as e:
                            st.warning(f"Failed to process image on page {page_num + 1}: {str(e)}")
        
        # Extract using PyMuPDF4LLM with the document object
        md_text = pymupdf4llm.to_markdown(
            doc,
            table_strategy=table_strategy,
            page_separators=page_separators
        )
        
        doc.close()
        
        # Display results
        if md_text.strip() or ocr_extracted_text.strip() or total_text.strip():
            st.subheader("Extracted Content")
            
            # Show PyMuPDF4LLM results
            if md_text.strip():
                st.markdown("### Text & Tables (PyMuPDF4LLM)")
                st.markdown(md_text)
            
            # Show OCR results
            if ocr_extracted_text.strip():
                st.markdown("### OCR Extracted Text")
                st.text_area("OCR Content", ocr_extracted_text, height=200)
            
            # Show raw text as fallback
            if not md_text.strip() and total_text.strip():
                st.markdown("### Raw Text Extraction")
                st.text_area("Raw Text", total_text, height=200)
            
            # Combine all text for download
            combined_text = ""
            if md_text.strip():
                combined_text += md_text
            if ocr_extracted_text.strip():
                combined_text += "\n\n" + ocr_extracted_text
            if not md_text.strip() and total_text.strip():
                combined_text = total_text
                
            st.download_button(
                label="Download All Extracted Content",
                data=combined_text,
                file_name="extracted_content.md",
                mime="text/markdown"
            )
        else:
            st.warning("No content extracted. This PDF might be password-protected, corrupted, or empty.")
            
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
else:
    st.info("Please upload a PDF file to begin extraction.")
    
# Information section
st.markdown("---")
st.subheader("About This Tool")
st.markdown("This tool extracts text and tables from PDF files:")
st.markdown("1. **Text-based PDFs**: Uses PyMuPDF4LLM for accurate extraction")
st.markdown("2. **Image-based PDFs**: Uses OCR (Tesseract) to extract text from images")
st.markdown("3. **Mixed PDFs**: Combines both approaches for comprehensive extraction")
st.markdown("**Requirements for OCR:**")
st.markdown("- Tesseract OCR must be installed on your system")
st.markdown("- Add Tesseract to your system PATH")
st.markdown("- Download language packs for better accuracy (e.g., German language pack for German text)")
st.markdown("- Download from: https://github.com/tesseract-ocr/tesseract")