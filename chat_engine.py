"""
chat_engine.py
--------------
The core logic engine that converts Natural Language to Pandas code,
executes it, and summarizes the results using Gemini API.
"""

import google.generativeai as genai
import pandas as pd
import numpy as np
import re
from typing import Any, Dict, List, Tuple
from config import (
    GEMINI_API_KEY, GEMINI_MODEL, CODE_GEN_TEMPERATURE, 
    SUMMARY_TEMPERATURE, MAX_RETRIES
)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

class ChatEngine:
    def __init__(self):
        self.code_model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={"temperature": CODE_GEN_TEMPERATURE}
        )
        self.summary_model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={"temperature": SUMMARY_TEMPERATURE}
        )

    def _get_code_prompt(self, question: str, context: str) -> str:
        return f"""
You are a expert Data Scientist. Your task is to write Python/Pandas code to answer a user question based on a DataFrame named 'df'.

{context}

RULES:
1. Output ONLY the python code. No explanations. No markdown blocks.
2. The final result must be stored in a variable named 'result'.
3. Use only pandas and numpy.
4. If the user asks for a 'list', 'result' should be a list, a series, or a smaller dataframe.
5. If the user asks for a 'count' or 'average', 'result' should be a single value.
6. Handle case-insensitive string matches if possible.

Question: {question}
"""

    def _get_summary_prompt(self, question: str, result: Any) -> str:
        return f"""
You are a helpful Real Estate Assistant. 
The user asked: "{question}"
The data-accurate result is: {result}

Provide a polite, professional, and concise summary of this result for the user.
If the result is a list of names or details, format them clearly.
"""

    def generate_code(self, question: str, context: str) -> str:
        prompt = self._get_code_prompt(question, context)
        response = self.code_model.generate_content(prompt)
        code = response.text.strip()
        # Clean up in case Gemini wraps it in backticks
        code = re.sub(r'^```python\n|```$', '', code, flags=re.MULTILINE).strip()
        return code

    def execute_code(self, code: str, df: pd.DataFrame) -> Any:
        # Create a restricted namespace for safety
        local_vars = {'df': df, 'pd': pd, 'np': np, 'result': None}
        try:
            exec(code, {}, local_vars)
            return local_vars.get('result')
        except Exception as e:
            return f"Error executing code: {e}"

    def get_summary(self, question: str, result: Any) -> str:
        prompt = self._get_summary_prompt(question, result)
        response = self.summary_model.generate_content(prompt)
        return response.text.strip()

    def run_query(self, question: str, df: pd.DataFrame, context: str) -> Dict[str, Any]:
        """
        Full pipeline: NL -> Code -> Execution -> Summary
        """
        code = self.generate_code(question, context)
        result = self.execute_code(code, df)
        
        # If execution failed, we don't summarize the error as a "result"
        if isinstance(result, str) and result.startswith("Error"):
             summary = "I encountered an issue while processing the data. Please try rephrasing your question."
        else:
             summary = self.get_summary(question, result)
             
        return {
            "question": question,
            "generated_code": code,
            "raw_result": result,
            "summary": summary
        }
