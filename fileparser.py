import pdfplumber
import os
import tiktoken 
import logging


def read_pdf(file_path):
    """
    Reads the content of a PDF file using pdfplumber.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    if text:
        logging.info(f"PDF file {file_path} read successfully.")
    else:
        logging.warning(f"No text found in the PDF file {file_path}.")
    return text


def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Splits the text into chunks of a specified size with optional overlap.
    Args:
        text (str): The text to be chunked.
        chunk_size (int): The size of each chunk.
        overlap (int): The number of overlapping characters between chunks.
    Returns:
        list: A list of text chunks.
    """
    # Get the encoding object for the "cl100k_base" tokenizer
    encoding = tiktoken.get_encoding("cl100k_base")
    
    # Encode the input text into tokens
    tokens = encoding.encode(text)
    
    # Initialize an empty list to store the chunks
    chunks = []
    
    # Start index for the first chunk
    start = 0
    
    # Loop through the tokens and create chunks
    while start < len(tokens):
        # Calculate the end index for the current chunk
        end = start + chunk_size
        
        # Extract the current chunk of tokens
        chunk = tokens[start:end]
        
        # Decode the chunk back into text and append to the chunks list
        chunks.append(encoding.decode(chunk))
        
        # Move the start index forward, accounting for overlap
        start += chunk_size - overlap
    
    # Return the list of text chunks
    logging.info(f"Text chunked into {len(chunks)} chunks.")
    return chunks



if __name__ == "__main__":
    # Example usage
    file_path = "fragments_on_machines.pdf"  # Replace with your PDF file path
    text = read_pdf(file_path)
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
        print("-" * 40) # Separator between chunks          
        # Save chunks to a text file
    with open("output_chunks.txt", "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"Chunk {i+1}:\n{chunk}\n")
            f.write("-" * 40 + "\n")  # Separator between chunks