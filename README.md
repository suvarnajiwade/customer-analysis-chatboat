# 🏠 Customer Analysis ChatBot

An AI-powered data analytics tool designed for the Real Estate industry. This application allows users to query customer lead databases using natural language (English) and get accurate, data-grounded answers.

## 🎯 Project Overview

Customer Analysis ChatBot solves the challenge of non-technical users needing to extract insights from complex Excel spreadsheets. By leveraging the **gemini-3.1-flash-lite-preview** model and **Pandas**, it converts plain English questions into precise data queries.

### How it works:
1. **NL to Code**: Gemini analyzes the user's question and the Excel schema to generate specific Pandas code.
2. **Deterministic Execution**: The generated code is executed on the actual dataset (ensuring zero AI hallucinations).
3. **Smart Summarization**: The raw data result is translated back into a professional, human-readable summary.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- A Gemini API Key (Get one for free at [Google AI Studio](https://aistudio.google.com/apikey))

### 2. Setting up Virtual Environment (Recommended)
Using a virtual environment ensures that the project's dependencies don't interfere with your global Python installation.

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

**On Mac/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Installation
Once the virtual environment is activated, install the required dependencies:

```bash
# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration
1. Create a file named `.env` in the root directory.
2. Add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 5. Running the App
Start the Streamlit interface:
```bash
streamlit run app.py
```
The app will automatically open in your default browser at `http://localhost:8501`.

---

## 🔍 Example Queries to Test

You can try these queries (included in the PDF assignment):
- *“How many customers have budget above 90 lakhs?”*
- *“List customers looking for 2BHK in Pune”*
- *“What is the average budget?”*
- *“Give a summary of all high-intent customers”*

**Bonus queries:**
- *“Which location has the most leads?”*
- *“Show me all customers who were 'Busy' during the last call.”*

---

## 🛠️ Tech Stack
- **AI Engine**: Google Gemini API
- **Frontend**: Streamlit
- **Data Processing**: Pandas / OpenPyxl
- **Environment**: Python-dotenv
