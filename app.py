import streamlit as st
import docx
import openai
import os

st.set_page_config(page_title="Store Performance Analyzer", layout="wide")

# Sidebar for OpenAI API key
st.sidebar.title("OpenAI API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
if api_key:
    openai.api_key = api_key

st.title("📊 Store Performance Analyzer (AI-powered)")

st.write("""
Upload a Word (.docx) file with store performance data. The AI will:
1. Identify the best performing store and why.
2. List the top 5 common practices most stores follow.
3. Identify the 3 stores that are lagging behind and explain the gaps.
4. Suggest a 3-step improvement plan for each underperforming store.

**Output:** Table with columns: Store | Current Performance | Key Practices | Improvement Plan
""")

uploaded_file = st.file_uploader("Upload your .docx file", type=["docx"])

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

if uploaded_file and api_key:
    with st.spinner("Extracting text from document..."):
        file_text = extract_text_from_docx(uploaded_file)

    st.subheader("Extracted Text Preview")
    st.text_area("Preview", file_text, height=200)

    prompt = f"""
You are an expert in retail analytics. Analyze the following store performance data:

{file_text}

Tasks:
1. Identify which store is performing the best and why.
2. List the top 5 common practices most stores follow.
3. Identify the 3 stores that are lagging behind and explain the gaps.
4. Suggest a 3-step improvement plan for each underperforming store.

Return your answer in this table format:

| Store | Current Performance | Key Practices | Improvement Plan |
|-------|---------------------|---------------|------------------|
"""

    if st.button("Analyze with AI"):
        with st.spinner("Analyzing with GPT-4.1..."):
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview", # or "gpt-4-0125-preview" or latest GPT-4.1 model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.2
            )
            result = response['choices'][0]['message']['content']
        st.subheader("Analysis Table")
        st.markdown(result)
else:
    st.info("Please upload a .docx file and enter your OpenAI API key.")

st.markdown("---")
st.caption("Powered by Streamlit & GPT-4.1")
