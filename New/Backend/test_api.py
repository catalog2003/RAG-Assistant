import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health:", response.json())
    return response.status_code == 200

def test_upload():
    """Test PDF upload"""
    with open("pdfs\\The-History-of-AI_Avicena.pdf", "rb") as f:
        files = {"file": ("The-History-of-AI_Avicena.pdf", f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/upload/", files=files)
    print("Upload:", response.json())
    return response.status_code == 200

def test_ask():
    """Test question answering"""
    data = {"question": "What is AI?", "session_id": "test_session"}
    response = requests.post(f"{BASE_URL}/ask/", json=data)
    print("Ask:", json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_history():
    """Test history retrieval"""
    response = requests.get(f"{BASE_URL}/history/test_session")
    print("History:", json.dumps(response.json(), indent=2))
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing RAG API...")
    
    if test_health():
        print("✅ Health check passed")
    
    if test_upload():
        print("✅ Upload test passed")
    
    if test_ask():
        print("✅ Question answering test passed")
    
    if test_history():
        print("✅ History test passed")