# Earnings Intelligence Suite

Transform dense quarterly earnings transcripts into actionable investment insights in under 30 seconds. Designed as a high-impact solution for retail investors and junior analysts to cut through "corporate fluff" to find hard data and sentiment shifts.

## Features

- **Document Ingest**: Upload PDF earnings transcripts directly via the sidebar.
- **Automated KPI Extraction**: Leverage LLMs to extract Revenue, EPS, and Guidance figures into a structured format.
- **Sentiment Heatmap**: Use FinBERT for domain-specific NLP to run a rolling sentiment check and identify "Bullish" vs "Bearish" narrative trends in the Q&A section.
- **Contextual Chat (RAG)**: Ask specific deep-dive questions against the document context (e.g., "What did they say about the supply chain?") using a Retrieval-Augmented Generation approach.

## Technical Architecture

- **UI Framework**: Streamlit
- **Orchestration**: LangChain, ChromaDB
- **Models**:
  - Main Analysis & Extraction: Google Gemini (via `langchain-google-genai`)
  - Sentiment Analysis: ProsusAI/finbert (via `transformers` and `torch`)
- **Processing**: PyPDF for text extraction.

## Setup & Installation

Follow these steps to run the application locally.

### 1. Requirements

Make sure you have Python 3.9+ installed and a virtual environment set up.

```bash
# Clone the repository
git clone https://github.com/Sanskritivv/Earnings-Intelligence-Suite.git
cd Earnings-Intelligence-Suite

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

Install the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory (or simply paste your API Key into the Streamlit UI configuration sidebar).

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Running the App

Start the Streamlit application:

```bash
streamlit run app.py
```

## Usage Flow

1. **Upload**: Drop a transcript PDF into the configuration sidebar.
2. **Configure**: Provide your Google API Key if it's not already in your `.env` file.
3. **Analyze**: Click "Analyze Transcript". The system will automatically chunk the text, process the data, extract KPIs, and run the sentiment analysis.
4. **View Insights**: 
   - **KPI Flash Cards**: Review extracted numbers and metrics.
   - **Sentiment Heatmap**: Observe the trend of the session (e.g., the Q&A portion).
   - **Contextual Chat**: Use the chatbox for specific, deep-dive questions based on the uploaded earnings context.
