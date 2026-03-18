import streamlit as st
import os

# Internal modules
from document_processor import process_document
from kpi_extractor import extract_kpis
from sentiment_analyzer import analyze_sentiment
from rag_chatbot import setup_rag

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

st.set_page_config(page_title="Earnings Intelligence Suite", layout="wide")

st.title("Earnings Intelligence Suite")
st.markdown("Transform 50-page earnings transcripts into actionable insights in seconds.")

# Sidebar setup
with st.sidebar:
    st.header("1. Configuration")
    api_key_input = st.text_input("Google API Key", type="password", value=os.environ.get("GOOGLE_API_KEY", ""))
    
    st.header("2. Upload Transcript")
    uploaded_file = st.file_uploader("Upload Earnings Transcript (PDF)", type=["pdf"])

# Session state initialization
for state_var in ["chunks", "rag_chain", "chat_history", "kpi_data", "sentiment_fig"]:
    if state_var not in st.session_state:
        st.session_state[state_var] = None if state_var != "chat_history" else []

def process_and_analyze():
    with st.spinner("Processing document..."):
        st.session_state.chunks = process_document(uploaded_file)
        st.success(f"Document processed into {len(st.session_state.chunks)} chunks.")
        
    with st.spinner("Extracting KPIs (This may take a moment)..."):
        st.session_state.kpi_data = extract_kpis(st.session_state.chunks, api_key_input)
        
    with st.spinner("Analyzing Q&A Sentiment with FinBERT..."):
        st.session_state.sentiment_fig = analyze_sentiment(st.session_state.chunks)
        
    with st.spinner("Setting up RAG Chatbot..."):
        st.session_state.rag_chain = setup_rag(st.session_state.chunks, api_key_input)

# Process Trigger
if uploaded_file and api_key_input:
    if st.button("Analyze Transcript"):
        process_and_analyze()
elif uploaded_file and not api_key_input:
    st.warning("Please provide a Google API Key in the sidebar.")

# Render UI if data exists
if st.session_state.chunks:
    tab1, tab2, tab3 = st.tabs(["KPI Flash Cards", "Sentiment Heatmap", "Contextual Chat"])
    
    with tab1:
        st.subheader("Key Performance Indicators")
        if st.session_state.kpi_data:
            st.markdown(st.session_state.kpi_data)
        else:
            st.info("Run analysis to see KPIs.")
            
    with tab2:
        st.subheader("Q&A Sentiment Trend")
        if st.session_state.sentiment_fig:
            st.plotly_chart(st.session_state.sentiment_fig, use_container_width=True)
        else:
            st.info("Run analysis to view sentiment.")
            
    with tab3:
        st.subheader("Deep-Dive Chat")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        # Chat input
        if prompt := st.chat_input("Ask a question about the earnings call..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = st.session_state.rag_chain.invoke(prompt)
                    st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
