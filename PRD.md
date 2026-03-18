This Product Requirements Document (PRD) outlines the **Earnings Intelligence Suite**. Since this is a project designed for rapid development, the focus is on a **high-impact MVP** (Minimum Viable Product).

---

# PRD: AI-Powered Earnings Intelligence Suite (v1.0)

## 1. Executive Summary
**Product Goal:** To transform dense, 50-page quarterly earnings transcripts into actionable investment insights in under 30 seconds.
**Target User:** Retail investors and junior analysts who need to cut through "corporate fluff" to find hard data and sentiment shifts.

---

## 2. User Features & Functionality
| Feature | Description | Priority |
| :--- | :--- | :--- |
| **PDF/Text Ingest** | Users upload a transcript file or paste a link to a financial transcript. | **P0 (Must)** |
| **Automated KPI Extraction** | LLM extracts Revenue, EPS, and Guidance into a structured table. | **P0 (Must)** |
| **Sentiment Heatmap** | FinBERT scans the Q&A section to color-code "Bullish" vs "Bearish" executive responses. | **P1 (High)** |
| **Contextual Chat (RAG)** | A chat interface to ask specific questions (e.g., "What did they say about the supply chain?"). | **P1 (High)** |
| **Confidence Scoring** | The system provides the exact quote (source) for every number it extracts to prevent hallucinations. | **P2 (Nice)** |

---

## 3. Technical Architecture & Tools
* **Orchestration:** **LangChain** or **LlamaIndex** (for RAG and document chunking).
* **Model Tier:**
    * **Reasoning:** `gpt-4o` or `Claude 3.5 Sonnet` or `gemini 3 pro` (Main analysis).
    * **Sentiment:** `ProsusAI/finbert` (Hugging Face) for domain-specific NLP.
* **Vector Database:** **ChromaDB** (Local/Simple) or **Pinecone** (Cloud).
* **UI Framework:** **Streamlit** (Fastest for Python-based vibe coding).

---

## 4. User Flow
1.  **Upload:** User drops a transcript PDF into the Streamlit sidebar.
2.  **Process:** The system splits text into $1,000$ character chunks with $200$ character overlap.
3.  **Analyze:**
    * **Step A:** LLM runs a "Map-Reduce" summary of the whole document.
    * **Step B:** FinBERT runs a rolling sentiment check on the Q&A section.
4.  **View:** The user sees a dashboard with:
    * A "Flash Card" of key numbers.
    * A "Sentiment Trend" chart.
    * A chat box for deep-dive questions.

---

## 5. Success Metrics (KPIs)
* **Accuracy Rate:** $> 95\%$ match between extracted KPIs and official investor relations data.
* **Latency:** Full analysis generated in $< 45$ seconds.
* **Hallucination Rate:** $0\%$ (Ensured by forcing the model to cite specific text segments).

---

## 6. Constraints & Risks
* **Token Limits:** Transcripts can exceed $20,000$ tokens. 
    * *Mitigation:* Use **Map-Reduce** chains to summarize segments before the final synthesis.
* **Hallucinations:** LLMs might "invent" growth percentages.
    * *Mitigation:* Implementation of **Source Grounding** (Return the chunk index with every answer).

---

