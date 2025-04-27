import streamlit as st
import os
from openai import OpenAI
from fpdf import FPDF
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="CaseGPT",
    page_icon="🩺",
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "case_generated" not in st.session_state:
    st.session_state.case_generated = False
if "diagnosis_revealed" not in st.session_state:
    st.session_state.diagnosis_revealed = False

class ClinicalCaseSystem:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.case_details = ""
        self.correct_diagnosis = ""
        
    def generate_case(self):
        system_prompt = """You are an experienced medical educator. Create a detailed clinical case including:
        - Patient demographics
        - Chief complaint
        - Relevant medical history
        - Physical examination findings
        - Diagnostic clues
        End with the correct diagnosis in this format: [CORRECT_DIAGNOSIS: <diagnosis>]"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}]
        )
        
        full_case = response.choices[0].message.content
        if "[CORRECT_DIAGNOSIS:" in full_case:
            self.case_details, self.correct_diagnosis = full_case.split("[CORRECT_DIAGNOSIS:")
            self.correct_diagnosis = self.correct_diagnosis.strip(" ]")
        return self.case_details, self.correct_diagnosis

    def answer_question(self, question):
        prompt = f"Based on this case: {self.case_details}\n\nQuestion: {question}"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

def remove_emojis(text):
    # Remove all non-ASCII characters (including emojis)
    return re.sub(r'[^\x00-\x7F]+', '', text)

def generate_pdf(history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Clinical Case Discussion", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for msg in history:
        pdf.set_font("Arial", style='B')
        pdf.cell(0, 10, txt=f"{msg['role'].capitalize()}:", ln=True)
        pdf.set_font("Arial", style='')
        clean_content = remove_emojis(msg['content'])
        pdf.multi_cell(0, 10, txt=clean_content)
        pdf.ln(5)
    
    return pdf.output(dest="S").encode("latin-1")

def is_correct_diagnosis(user_input, correct_answer):
    user_input = user_input.lower().strip()
    correct_answer = correct_answer.lower().strip()
    # Accept if user_input is a substring of correct_answer or vice versa
    return user_input in correct_answer or correct_answer in user_input

# Main app interface
st.title("CaseGPT: Your DDX Friend")

# Initialize system with API key from .env
try:
    case_system = ClinicalCaseSystem()
except ValueError as e:
    st.error(f"Authentication error: {str(e)}")
    st.stop()

# Sidebar controls
with st.sidebar:
    st.subheader("Case Controls")
    if st.button("Generate New Case") or not st.session_state.case_generated:
        case, diagnosis = case_system.generate_case()
        st.session_state.case_details = case
        st.session_state.correct_diagnosis = diagnosis
        # Only add the new case as the first message in chat history
        st.session_state.messages = [{"role": "assistant", "content": case}]
        st.session_state.case_generated = True
        st.session_state.diagnosis_revealed = False

# Chat interface (shows case as first message, then user/assistant Q&A)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask question about the case..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.spinner("Analyzing..."):
        response = case_system.answer_question(prompt)
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Diagnosis submission and PDF generation
col1, col2 = st.columns(2)
with col1:
    with st.form("diagnosis_form"):
        diagnosis = st.text_input("Enter your diagnosis:")
        submitted = st.form_submit_button("Submit Diagnosis")
        
        if submitted and diagnosis:
            feedback = f"Your diagnosis: {diagnosis}\n\n"
            if is_correct_diagnosis(diagnosis, st.session_state.correct_diagnosis):
                feedback += "✅ Correct! Well done!"
            else:
                feedback += "❌ Incorrect. Keep analyzing the case."
            
            st.session_state.messages.extend([
                {"role": "user", "content": f"Diagnosis Submitted: {diagnosis}"},
                {"role": "assistant", "content": feedback}
            ])
            st.rerun()

with col2:
    if st.button("Reveal Correct Diagnosis"):
        st.session_state.diagnosis_revealed = True
        reveal_text = f"Correct Diagnosis: {st.session_state.correct_diagnosis}"
        st.session_state.messages.append({
            "role": "assistant", 
            "content": reveal_text
        })
        st.rerun()
    
    if st.download_button("Download Case Discussion", 
                         data=generate_pdf(st.session_state.messages),
                         file_name="clinical_case.pdf",
                         mime="application/pdf"):
        st.success("PDF generated successfully!")
