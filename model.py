#create a model using gemini llm to use the model in the agent
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from IPython.display import display, Markdown
from langchain_core.messages import AIMessage

def create_gemini_model(
    model_name: str = "gemini-1.5-flash",
    temperature: float = 0.1,
    max_tokens: Optional[int] = None,
    top_p: float = 0.8,
    top_k: int = 40,
    api_key: Optional[str] = None
) -> BaseChatModel:
    """
    Create a Gemini model instance for use in the agent.
    
    Args:
        model_name (str): The Gemini model to use (default: "gemini-1.5-flash")
        temperature (float): Controls randomness in responses (0.0-1.0)
        max_tokens (Optional[int]): Maximum tokens in response
        top_p (float): Nucleus sampling parameter
        top_k (int): Top-k sampling parameter
        api_key (Optional[str]): Google API key (will use env var if not provided)
    
    Returns:
        BaseChatModel: Configured Gemini chat model
    
    Raises:
        ValueError: If API key is not found
        Exception: If model creation fails
    """
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Google API key not found. Please set GOOGLE_API_KEY environment variable "
            "or pass api_key parameter."
        )
    
    try:
        # Configure the model
        model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=temperature,
            max_output_tokens=max_tokens,
            top_p=top_p,
            top_k=top_k,
            convert_system_message_to_human=True,
            verbose=True
        )
        
        print(f"✅ Successfully created Gemini model: {model_name}")
        print(f"   Temperature: {temperature}")
        print(f"   Max tokens: {max_tokens or 'Not set'}")
        print(f"   Top-p: {top_p}")
        print(f"   Top-k: {top_k}")
        
        return model
        
    except Exception as e:
        print(f"❌ Error creating Gemini model: {str(e)}")
        raise Exception(f"Failed to create Gemini model: {str(e)}")



# Example usage and testing
if __name__ == "__main__":
    # Create a model for math tutoring
    model = create_gemini_model(model_name="gemini-2.5-pro")
    result = model.invoke("How to find the area of a circle?")
    print(f"Result_type: {type(result)}")
    
    # Extract and print the actual content
    if isinstance(result, AIMessage):
        content = result.content
        if isinstance(content, list):
            # If content is a list (e.g., multiple text blocks), join them
            combined = "\n\n".join([str(item) for item in content])
        else:
            # If content is a string, use it directly
            combined = str(content)
        
        print("\n" + "="*50)
        print("🤖 GEMINI RESPONSE:")
        print("="*50)
        print(combined)
        print("="*50)
    else:
        print(f"Unexpected result type: {type(result)}")
        print(f"Result: {result}")
  