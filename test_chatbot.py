import time  # Import the time module for response time measurement
from generictool import GenericTool  # Generic Tool handler
from ragtool import RAGTool  # RAG Tool handler

def test_generic_tool():
    """
    Tests the Generic Tool by sending predefined conversational queries
    and measures the response time for each query.
    """
    print("Testing Generic Tool:")
    
    # Create an instance of GenericTool
    generic_tool = GenericTool() 
    
    
    test_queries = [
        "Hello!",
        "How's the weather today?",
        "What's your favorite color?",
        "Tell me a joke.",
        "What are you?"
    ]
    for query in test_queries:
        print(f"\nUser: {query}")
        
        # Start the timer
        start_time = time.time()
        
        # Simulate the Generic Tool response
        response = generic_tool.get_response(query)
        
        # Stop the timer
        end_time = time.time()
        
        # Calculate the elapsed time
        response_time = end_time - start_time
        print(f"Bot: {response}")
        print(f"Response time: {response_time:.2f} seconds")


def test_rag_tool():
    """
    Tests the RAG Tool by sending predefined document-based queries
    and measures the response time for each query.
    """
    print("Testing RAG Tool:")
    
    # Create an instance of RAGTool
    rag_tool = RAGTool() 
    
    test_queries = [
        "What is Cassandra?",
        "What are the differences between Cassandra and Dynamo?",
        "what is spring boot?",
        "What is Angular?",
        "What files and folder structure does ng new generate by default, and why are they important?",
        "how to Create Spring Cloud Configuration Server?",
        "Can I run multiple Angular projects simultaneously on the same machine? If so, how?",
        "What are the benefits of Ahead-of-Time (AOT) compilation, and when should it be used?",
        "What API methods does Cassandra provide?",
        "What is application runner?",
        "How does Cassandra handle high availability?",
        "when is interceptor used in spring boot?"
    ]
    for query in test_queries:
        print(f"\nUser: {query}")
        
        # Start the timer
        start_time = time.time()
        
        # Simulate the RAG Tool response
        response = rag_tool.rag_response(query)
        
        # Stop the timer
        end_time = time.time()
        
        # Calculate the elapsed time
        response_time = end_time - start_time
        print(f"Bot: {response}")
        print(f"Response time: {response_time:.2f} seconds")


if __name__ == "__main__":
    print("Starting Virtual Assistant Tests...\n")
    
    # Run tests for Generic Tool
    test_generic_tool()
    print("\n" + "="*50 + "\n")
    
    # Run tests for RAG Tool
    test_rag_tool()
