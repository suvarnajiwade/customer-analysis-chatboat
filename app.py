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

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ── Initialization ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "engine" not in st.session_state:
    st.session_state.engine = ChatEngine()

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
        st.metric("Total Leads", len(df))
        
        with st.expander("📊 Preview Data"):
            st.dataframe(df.head(10), use_container_width=True)
            
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    st.divider()
    
    st.subheader("💡 Example Queries")
    st.caption("Click to try:")
    for query in EXAMPLE_QUERIES:
        if st.button(query, use_container_width=True, key=query):
            # Programmatically set the chat input is not direct in streamlit, 
            # so we manually append to messages
            st.session_state.messages.append({"role": "user", "content": query})
            
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()

# ── Main Chat Interface ──────────────────────────────────────────────────────
st.header(f"{APP_TITLE}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "code" in message:
            with st.expander("🛠️ View Computed Code"):
                st.code(message["code"], language="python")
        if "data" in message and message["data"] is not None:
             with st.expander("📋 View Raw Result"):
                st.write(message["data"])

# Chat Input
if prompt := st.chat_input("Ask about your customers..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            response = st.session_state.engine.run_query(prompt, df, context)
            
            st.markdown(response["summary"])
            
            # Show code and data in sub-sections
            with st.expander("🛠️ View Computed Code"):
                st.code(response["generated_code"], language="python")
            
            if response["raw_result"] is not None:
                with st.expander("📋 View Raw Result"):
                    st.write(response["raw_result"])
            
            # Save assistant response to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response["summary"],
                "code": response["generated_code"],
                "data": response["raw_result"]
            })
