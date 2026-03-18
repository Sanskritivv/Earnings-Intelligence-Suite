import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_document(file_obj):
    """
    Processes an uploaded PDF file or text file, splits it into chunks.
    Args:
        file_obj: Streamlit UploadedFile object.
    Returns:
        List of Document chunks.
    """
    # Write uploaded file to a temporary file, as PyPDFLoader needs a file path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_obj.read())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    
    # Store the original text or metadata if needed for source grounding
    for i, chunk in enumerate(chunks):
        chunk.metadata['chunk_id'] = i
        
    return chunks
