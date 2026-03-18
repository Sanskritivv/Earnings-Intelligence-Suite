from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os

def extract_kpis(chunks, api_key=None):
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.1)

    map_prompt = PromptTemplate.from_template("""
You are a financial analyst. Analyze the following document chunk from an earnings transcript.
Extract any information related to:
1. Revenue
2. Earnings Per Share (EPS)
3. Future Guidance / Forward-looking statements

Provide the exact quote as the source for any number extracted. If the information is not in this chunk, output "Nothing relevant."

Chunk:
{text}

Extraction:
""")
    
    map_chain = map_prompt | llm
    
    # Group 1000-character chunks into larger 30,000-character blocks
    # This ensures we don't spam the API with hundreds of requests and hit the free-tier limit of 15 Requests Per Minute!
    mega_chunks = []
    current_mega_chunk = ""
    for chunk in chunks:
        current_mega_chunk += chunk.page_content + "\n\n"
        if len(current_mega_chunk) > 30000:
            mega_chunks.append(current_mega_chunk)
            current_mega_chunk = ""
    if current_mega_chunk:
        mega_chunks.append(current_mega_chunk)

    extracted_summaries = []
    for text_block in mega_chunks:
        try:
            res = map_chain.invoke({"text": text_block})
            content = res.content.strip()
            if "Nothing relevant" not in content and "nothing relevant" not in content.lower():
                extracted_summaries.append(content)
        except Exception as e:
            print(f"Failed to process mega-chunk: {e}")
            
    if not extracted_summaries:
        return "No relevant KPIs found in the document."

    combined_text = "\n\n---\n\n".join(extracted_summaries)

    reduce_prompt = PromptTemplate.from_template("""
The following is a set of extracted financial metrics from various parts of an earnings transcript:

{doc_summaries}

Synthesize these extractions into a clear, concise summary of the company's:
1. Revenue (include exact quote citation)
2. Earnings Per Share (EPS) (include exact quote citation)
3. Guidance (include exact quote citation)

Format the output as a Markdown table with columns: Metric, Value, Source Quote.
If a metric was not found, state "Not found".
""")
    
    reduce_chain = reduce_prompt | llm
    final_res = reduce_chain.invoke({"doc_summaries": combined_text})
    return final_res.content
