"""
config.py
---------
Central configuration for the "Chat with Customer Data" tool.
Loads environment variables, configures Gemini API, and exposes
all app-wide constants from a single place.
"""

import os
from dotenv import load_dotenv

# ── Load .env file ─────────────────────────────────────────────────────────────
load_dotenv()

# ── Gemini API ──────────────────────────────────────────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# Validate that the key is present
if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY is not set.\n"
        "Please add it to your .env file:\n"
        "  GEMINI_API_KEY=your_key_here\n"
        "Get a free key at: https://aistudio.google.com/apikey"
    )

# ── Model Settings ──────────────────────────────────────────────────────────────
# Model used for code generation and summarization
GEMINI_MODEL: str = "gemini-1.5-flash"

# Temperature for code generation (low = more deterministic/accurate)
CODE_GEN_TEMPERATURE: float = 0.1

# Temperature for summarization (slightly higher = more natural language)
SUMMARY_TEMPERATURE: float = 0.3

# Maximum output tokens for generated responses
MAX_OUTPUT_TOKENS: int = 2048

# Maximum retries if Pandas code execution fails
MAX_RETRIES: int = 3

# ── Data Settings ───────────────────────────────────────────────────────────────
# Default Excel file (provided with the assignment)
DEFAULT_DATA_FILE: str = "pune_real_estate_leads_updated.xlsx"

# Number of sample rows to include in the schema sent to Gemini for context
SCHEMA_SAMPLE_ROWS: int = 3

# ── App UI Settings ─────────────────────────────────────────────────────────────
APP_TITLE: str = "Customer Analysis ChatBot"
APP_ICON: str = "🏠"
APP_SUBTITLE: str = "Ask any question about the real estate customer data in plain English."

# Example queries shown in the sidebar (from the PDF + extras)
EXAMPLE_QUERIES: list = [
    "How many customers have budget above 90 lakhs?",
    "List customers looking for 2BHK in Pune",
    "What is the average budget?",
    "Give a summary of all high-intent customers",
    "Which location has the most customers?",
    "Show customers with Connected call status",
    "What is the highest budget customer's name?",
    "How many customers want 3BHK?",
]
