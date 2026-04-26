import requests
import json
import time

def test_chat_streaming(query):
    url = "http://127.0.0.1:8080/chat"
    payload = {
        "message": query,
        "session_id": "test_session",
        "user_name": "TestUser"
    }
    
    print(f"Query: {query}")
    start_time = time.time()
    first_chunk_time = None
    full_response = ""
    
    try:
        with requests.post(url, json=payload, stream=True) as response:
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    if first_chunk_time is None:
                        first_chunk_time = time.time() - start_time
                    full_response += chunk
                    # print(chunk, end="", flush=True)
            
            end_time = time.time() - start_time
            print(f"\n\n--- Stats ---")
            print(f"Time to first chunk: {first_chunk_time:.2f}s")
            print(f"Total time: {end_time:.2f}s")
            print(f"Response Length: {len(full_response)}")
            print(f"Response: {full_response}")
            
            # Check for noise
            if "transfer_to_agent" in full_response:
                print("!!! NOISE DETECTED: 'transfer_to_agent' found in response !!!")
            
            # Check for accuracy
            if "Wankhede" in full_response:
                 print("!!! ACCURACY ISSUE: 'Wankhede' found in response !!!")
            if "Narendra Modi" in full_response:
                 print("[OK] Narendra Modi Stadium confirmed.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_chat_streaming("Where am I and who is playing?")
