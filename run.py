import streamlit as st
import pytesseract
import cv2
import numpy as np
import re
import pandas as pd



st.title("Invoice OCR Extractor")

uploaded_file = st.file_uploader("Upload invoice image", type=["png", "jpg", "jpeg"])

def extract(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ''

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    text = pytesseract.image_to_string(image, lang='eng', config='--oem 3 --psm 6')

    
    data = {
        'L/C No': extract(r'L\/C\s*No[:\s]*([^\s]+)', text),
        'IGM No': extract(r'IGM\s*(?:No\.?|Number)[:\s]*([^\s]+)', text),
        'IGM Date': extract(r'IGM\s*Date[:\s]*([^\s]+)', text),
        'GD No': extract(r'GD\s*(?:No\.?|Number)[:\s]*([^\s]+)', text),
        'GD Date': extract(r'GD\s*Date[:\s]*([^\s]+)', text),
        'Index No': extract(r'Index\s*(?:No\.?|Number)[:\s]*([^\s]+)', text),
        'Vessel Name': extract(r'Vessel\s*Name[:\s]*([A-Za-z0-9 .\-]+?)(?=\s+[A-Z][A-Z /]*:|$)', text).strip(),
        'Cash Number': extract(r'Cash\s*Number[:\s]*([^\s]+)', text).split('\n')[0].strip(),
        'Assessed Value': extract(r'Assessed\s*Value[:\s]*(.+)', text)
    }

    df = pd.DataFrame([data])
    st.subheader("Extracted Data:")
    st.dataframe(df)

    # (Optional) allow CSV download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "extracted_data.csv", "text/csv")

    st.subheader("OCR Text Output:")
    st.text(text)
