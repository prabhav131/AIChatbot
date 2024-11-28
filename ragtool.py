# import necessary libraries
import fitz  # PyMuPDF for PDF extraction
from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time

class RAGTool:
    def __init__(self, folder_path="docs", chunk_size=500, similarity_threshold=0.45):
        # Load embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.faiss_index = faiss.IndexFlatL2(self.dimension)  # Initialize FAISS for similarity search

        # Initialize document storage
        self.documents = []
        self.document_embeddings = []
        self.similarity_threshold = similarity_threshold

        start_time = time.time()
        
        # Load and chunk PDFs
        self.load_and_chunk_pdfs(folder_path, chunk_size)
        print(f"Time taken for loading docs: {time.time() - start_time} seconds")
        # Initialize the response generation model and template
        self.model = OllamaLLM(model="tinydolphin")
        # self.model = OllamaLLM(model="orca-mini")
        # self.model = OllamaLLM(model="dolphin-phi")
        self.template = """
        You are a helpful assistant. Answer the question below using the information provided in the context below. 
        If you are not sure what something means in the question, always reply with "I don't understand. Could you please try again?"

        Question: {question}
        Context: {context}
        """
        self.prompt = ChatPromptTemplate.from_template(template=self.template)
        self.chain = self.prompt | self.model

    def load_and_chunk_pdfs(self, folder_path, chunk_size=500):
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                doc_path = os.path.join(folder_path, filename)
                doc = fitz.open(doc_path)
                text = ""
                
                # Extract text from each page
                for page in doc:
                    text += page.get_text("text")
                
                # Split text into chunks
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                for chunk in chunks:
                    self.add_document(chunk)
        print("Loading docs complete.")

    def add_document(self, text):
        self.documents.append(text)
        embedding = self.embedding_model.encode([text])[0]
        self.document_embeddings.append(embedding)
        self.faiss_index.add(np.array([embedding]))

    def is_relevant_query(self, user_query):
        # Generate embedding for the user query
        query_embedding = self.embedding_model.encode([user_query])[0]
        
        # Search for the most similar document chunk
        _, indices = self.faiss_index.search(np.array([query_embedding]), k=1)
        
        # Compute similarity with the top chunk
        top_doc_embedding = self.document_embeddings[indices[0][0]]
        similarity = util.pytorch_cos_sim(query_embedding, top_doc_embedding).item()


        # Check if the similarity meets the threshold
        return similarity >= self.similarity_threshold

    def rag_response(self, user_query):
        # Check for relevance first
        if not self.is_relevant_query(user_query):
            return "I'm sorry, I didn't understand that. Could you rephrase or ask something else?"

        # Encode the user query and retrieve top 3 document chunks
        query_embedding = self.embedding_model.encode([user_query])[0]
        _, indices = self.faiss_index.search(np.array([query_embedding]), k=3)
        
        # Retrieve top document chunks based on indices
        top_docs = [self.documents[idx] for idx in indices[0]]
        context = "\n".join(top_docs)  # Combine top chunks as context
        
        # Generate answer using the chain
        result = self.chain.invoke({"question": user_query, "context": context})
        return result

    def handle_rag_conversation(self):
        
        print("RAG Assistant is ready! Type 'exit_rag' to quit questioning from the docs")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit_rag':
                break
            response = self.rag_response(user_input)
            print("RAG Bot: ", response)
            
        return "continue"    

# Start the RAG conversation loop
if __name__ == "__main__":
    rag_tool = RAGTool()
    rag_tool.handle_rag_conversation()
