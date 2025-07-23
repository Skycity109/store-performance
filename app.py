import streamlit as st
import docx
import openai

st.set_page_config(page_title="Abhishek's AI enabled IKEA Store Performance Analyzer", layout="wide")

st.sidebar.title("OpenAI API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

st.title("📊 Abhishek's AI enabled IKEA Store Performance Analyzer")

st.write("""
- Upload a Word (.docx) file with store performance data to get an analysis.
- Or, just type any question below to chat with the AI!
""")

uploaded_file = st.file_uploader("Upload your .docx file (optional)", type=["docx"])
user_question = st.text_input("Ask any question (or leave blank to analyze document):")

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

if api_key:
    prompt = ""
    if uploaded_file:
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
    elif user_question:
        prompt = user_question
    else:
        st.info("Upload a document or enter a question above.")
    
    if prompt and st.button("Ask AI"):
        with st.spinner("Thinking..."):
            try:
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.2
                )
                result = response.choices[0].message.content
                st.subheader("AI Response")
                st.markdown(result)
            except openai.RateLimitError:
                st.error("You have hit your OpenAI rate limit! Please wait and try again later, or check your usage/quota at https://platform.openai.com/usage.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your OpenAI API key.")

st.markdown("---")
st.caption("Powered by Abhishek's brain")
