import streamlit as st
import pandas as pd
from config import (
    APP_TITLE, APP_ICON, APP_SUBTITLE, 
    EXAMPLE_QUERIES, DEFAULT_DATA_FILE
)
from data_loader import load_data, get_dataframe_context
from chat_engine import ChatEngine

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

# Custom CSS for Premium UI
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Chat Message Bubbles */
    .stChatMessage {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
        border: 1px solid rgba(0,0,0,0.03) !important;
    }
    
    /* User Message Specific */
    [data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%) !important;
        border-left: 5px solid #4a90e2 !important;
    }

    /* Assistant Message Specific */
    [data-testid="stChatMessageAssistant"] {
        border-left: 5px solid #2ecc71 !important;
    }

    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        color: #2c3e50;
        font-weight: 700;
    }
    
    /* Button Styling */
    .stButton>button {
        border-radius: 10px;
        transition: all 0.3s ease;
        border: none;
        background: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: 1px solid #4a90e2;
    }

    /* Hide default Streamlit footer */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ── Initialization ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "engine" not in st.session_state:
    st.session_state.engine = ChatEngine()

# State for processing a button-clicked query
if "active_query" not in st.session_state:
    st.session_state.active_query = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.info(APP_SUBTITLE)
    
    st.divider()
    
    # Data Loading
    try:
        df = load_data(DEFAULT_DATA_FILE)
        context = get_dataframe_context(df)
        
        st.success("✅ Dataset Loaded")
        print("Data Loaded")
        st.metric("Total Leads", len(df))
        
        with st.expander("📊 Preview Data"):
            st.dataframe(df.head(10), use_container_width=True)
            
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    st.divider()
    
    st.subheader("💡 Example Queries")
    for query in EXAMPLE_QUERIES:
        if st.button(query, use_container_width=True):
            st.session_state.active_query = query
            st.rerun()

    st.divider()
    
    # Chat History / Recent Questions Bar
    st.subheader("📜 Recent Questions")
    user_questions = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
    if user_questions:
        for q in reversed(user_questions[-5:]): # Show last 5
            st.caption(f"• {q}")
    else:
        st.caption("No questions yet.")

    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.active_query = None
        st.rerun()

# ── Main Chat Interface ──────────────────────────────────────────────────────
st.header(f"{APP_TITLE}")

# Display Welcome Card if history is empty
if not st.session_state.messages:
    st.markdown(f"""
    <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.05); margin-bottom: 30px;">
        <h2 style="margin-top:0;">Welcome to {APP_TITLE}! 👋</h2>
        <p style="color: #666; font-size: 1.1em;">
            I am your intelligent assistant for customer data analysis. 
            You can ask me questions about your leads in plain English, and I will generate 
            precise data insights for you.
        </p>
        <p style="background: #f0f7ff; padding: 10px 15px; border-radius: 10px; color: #0056b3; font-weight: 500; display: inline-block;">
            
        
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "code" in message:
            with st.expander("🔍 View logic", expanded=False):
                st.code(message["code"], language="python")

# Processing Logic
prompt = st.chat_input("Ask about your customers...")
if st.session_state.active_query:
    prompt = st.session_state.active_query
    st.session_state.active_query = None # Reset after grabbing

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            response = st.session_state.engine.run_query(prompt, df, context)
            
            st.markdown(response["summary"])
            
            # Subtler logic view (Raw result removed as requested)
            with st.expander("🔍 View logic", expanded=False):
                st.code(response["generated_code"], language="python")
            
            # Save assistant response to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response["summary"],
                "code": response["generated_code"]
            })
