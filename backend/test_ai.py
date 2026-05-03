import json
from app.services.ai_engine import analyze_lead

def test_analyze_lead():
    print("Testing analyze_lead...")
    
    lead_name = "John Doe"
    lead_message = "Hi, I'm interested in your premium business automation software. We have a budget of $50k and need to implement it ASAP."
    
    print(f"Input Name: {lead_name}")
    print(f"Input Message: {lead_message}")
    print("-" * 40)
    
    response = analyze_lead(lead_name, lead_message)
    
    print("Response object:")
    print(response)
    print("-" * 40)
    
    print("Response JSON representation:")
    print(response.model_dump_json(indent=2))
    
if __name__ == "__main__":
    test_analyze_lead()
