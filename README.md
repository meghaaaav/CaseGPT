# CaseGPT: Clinical Diagnosis Practice Tool

A web-based interactive trainer for clinical diagnosis, powered by OpenAI and Streamlit.

---

## Features

- **Generates realistic clinical cases** for diagnostic practice
- **Interactive Q&A chat** about the case (powered by GPT)
- **Diagnosis submission** with flexible answer matching (accepts equivalent/partial answers)
- **Reveal correct diagnosis** on demand
- **Download the entire case discussion as a PDF** (with Unicode-safe export)
- **Dark mode friendly UI** 

---

### 1. Clone the repository

```bash
git clone 
cd 
```

### 2. Install dependencies

```bash
pip install streamlit openai fpdf python-dotenv
```

### 3. Set up your OpenAI API key

Create a `.env` file in the project root with:

```
OPENAI_API_KEY=sk-
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## Usage

- Click **"Generate New Case"** in the sidebar to start a new clinical scenario.
- The case will appear as the first message in the chat.
- Use the chat input to ask questions about the case.
- Enter your diagnosis and submit.
- The app will accept both exact and partial matches (e.g., "Pneumonia" for "Community Acquired Pneumonia").
- Click **"Reveal Correct Diagnosis"** to see the answer.
- Download the full discussion as a PDF.

---

