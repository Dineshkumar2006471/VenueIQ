import httpx
import json

def test_query(message):
    print(f"Querying: {message}")
    url = "http://127.0.0.1:8080/chat"
    payload = {"message": message, "session_id": "test_session"}
    
    try:
        with httpx.stream("POST", url, json=payload, timeout=60.0) as r:
            if r.status_code != 200:
                print(f"Error: {r.status_code}")
                return
            for chunk in r.iter_text():
                print(chunk, end="", flush=True)
            print("\n" + "-"*20)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    # Test food/snack question
    test_query("What snacks are available near Gate 4?")
    # Test match question
    test_query("What is the live score?")
