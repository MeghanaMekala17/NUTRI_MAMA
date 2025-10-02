from app.models.chatbot_model import ChatbotModel
import time
import json

chatbot = ChatbotModel()

def generate_text(prompt: str):
    return chatbot.generate(prompt)

if __name__ == '__main__':
    # Test case relevant to the project
    test_prompt = "What are safe Indian foods to eat during the first trimester of pregnancy?"
    
    print("-" * 60)
    print("STARTING GENERATE TEXT SERVICE TEST")
    print(f"Test Prompt: '{test_prompt}'")
    
    start_time = time.time()
    
    try:
        # Call the service function
        response_text = generate_text(test_prompt)
        
        end_time = time.time()
        
        # Check if the response is an error string from the Gemini service
        if response_text.startswith("Error:") or response_text.startswith("API Error:"):
            print("-" * 60)
            print(f"[FAIL] SERVICE FAILED: {response_text}")
        else:
            print("-" * 60)
            print("[SUCCESS] SERVICE SUCCESS: Text Received")
            print("\nResponse Snippet:")
            # Use basic cleaning to remove unnecessary markdown artifacts for display
            cleaned_response = response_text.replace('**', '').replace('*', ' -')
            print(cleaned_response[:500] + "...")
        
        print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        print(f"\n[FAIL] UNHANDLED EXCEPTION: Test failed. Details: {e}")
        
    print("-" * 60)