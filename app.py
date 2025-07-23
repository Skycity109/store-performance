import streamlit as st
import docx
import requests

st.set_page_config(page_title="Store Performance Analyzer (Hugging Face)", layout="wide")

st.title("📊 Store Performance Analyzer by Abhishek")

st.write("""
Upload a Word (.docx) file with store performance data. The app will send the text to a free Hugging Face model for analysis.
""")

uploaded_file = st.file_uploader("Upload your .docx file", type=["docx"])

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

if uploaded_file:
    with st.spinner("Extracting text from document..."):
        file_text = extract_text_from_docx(uploaded_file)
    st.subheader("Extracted Text Preview")
    st.text_area("Preview", file_text, height=200)

    # Send to Hugging Face Inference API (using a conversational model)
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {}  # You can add 'Authorization': 'Bearer YOUR_HF_API_KEY' for higher limits
    prompt = f"""Analyze the following store performance data and provide insights as a table with columns: Store | Current Performance | Key Practices | Improvement Plan:\n{file_text}"""

    with st.spinner("Analyzing with Hugging Face model..."):
        response = requests.post(api_url, headers=headers, json={"inputs": prompt})
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and 'generated_text' in result[0]:
                st.subheader("AI Analysis Table")
                st.markdown(result[0]['generated_text'])
            elif "error" in result:
                st.error(result["error"])
            else:
                st.write(result)
        else:
            st.error(f"API Error: {response.text}")
else:
    st.info("Please upload a .docx file to analyze.")

st.markdown("---")
st.caption("Powered by Streamlit & Hugging Face Inference API")
