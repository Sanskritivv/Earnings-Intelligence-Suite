from transformers import pipeline
import pandas as pd
import plotly.express as px

def analyze_sentiment(chunks):
    """
    Analyzes the sentiment of given text chunks using FinBERT.
    Uses a simple rolling sentiment over the document chunks.
    """
    # Initialize the sentiment analysis pipeline using FinBERT
    # (Huggingface will cache this the first time it downloads)
    analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    
    # Analyze the latter half of chunks to approximate the Q&A section
    half_idx = len(chunks) // 2
    qa_chunks = chunks[half_idx:]
    
    results = []
    
    for chunk in qa_chunks:
        # FinBERT has a max token length; trim to 500 chars for safety
        text = chunk.page_content[:500] 
        res = analyzer(text)[0]
        results.append({
            "chunk_id": chunk.metadata.get("chunk_id", 0),
            "label": res["label"],
            "score": res["score"],
            "text_preview": text[:100] + "..."
        })
        
    df = pd.DataFrame(results)
    
    color_map = {"positive": "green", "negative": "red", "neutral": "gray"}
    
    if not df.empty:
        fig = px.scatter(
            df, 
            x="chunk_id", 
            y="score", 
            color="label",
            color_discrete_map=color_map,
            hover_data=["text_preview"],
            title="Q&A Section Sentiment Trend"
        )
    else:
        fig = px.scatter(title="No Sentiment Data Available")
        
    return fig
