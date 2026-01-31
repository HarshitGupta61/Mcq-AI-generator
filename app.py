import streamlit as st
from llm import generate_mcqs
from pdf_utils import extract_text_from_pdf, clean_pdf_text
from pdf_exporter import generate_pdf

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI MCQ Generator", layout="centered")
st.title("📘 AI MCQ Generator")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
div.stDownloadButton > button {
    background-color: #FF6F00;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
input_type = st.radio("Choose input type:", ["Text", "PDF"])
text = ""

if input_type == "Text":
    text = st.text_area("Enter text:", height=250)
else:
    pdf = st.file_uploader("Upload PDF (first pages recommended)", type="pdf")
    if pdf:
        raw_text = extract_text_from_pdf(pdf)
        text = clean_pdf_text(raw_text)

num_questions = st.slider("Number of MCQs", 5, 20, 10)

# ---------------- GENERATE ----------------
if st.button("Generate MCQs"):
    if not text.strip():
        st.warning("Please provide text or upload a PDF.")
    else:
        with st.spinner("Generating MCQs..."):
            mcqs = generate_mcqs(text, num_questions)

        if not isinstance(mcqs, list):
            st.error("❌ AI response format error. Try smaller text or fewer questions.")
        else:
            st.session_state.mcqs = mcqs
            st.success("✅ MCQs Generated Successfully!")

# ---------------- DISPLAY ----------------
if "mcqs" in st.session_state:
    st.subheader("📌 Generated MCQs")

    for i, mcq in enumerate(st.session_state.mcqs, start=1):
        st.markdown(f"### Q{i}. {mcq['question']}")

        correct = mcq["answer"]

        for key, value in mcq["options"].items():
            if key == correct:
                st.markdown(
                    f"<span style='color:green; font-weight:bold;'>✅ {key}. {value}</span>",
                    unsafe_allow_html=True
                )
            else:
                st.write(f"{key}. {value}")

    # ---------------- PDF DOWNLOAD ----------------
    pdf_path = "mcqs.pdf"
    generate_pdf(st.session_state.mcqs, pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button(
            "📄 Download as PDF",
            f,
            file_name="mcqs.pdf",
            mime="application/pdf"
        )
