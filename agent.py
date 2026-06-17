import os
import json
import requests
import trafilatura
import time
from dotenv import load_dotenv
from ddgs import DDGS

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
# Using the confirmed working bridge IP
ANKI_URL = "http://172.28.64.1:8766"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def autonomous_research(query):
    print(f"[*] Searching web for: {query}...")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            url = results[0].get('href') if results else None
            
        if not url:
            print("[!] No search results found.")
            return None

        print(f"[*] Scraping: {url}")
        downloaded = trafilatura.fetch_url(url)
        return trafilatura.extract(downloaded) if downloaded else None
    except Exception as e:
        print(f"[!] Research Error: {e}")
        return None

def generate_flashcards(text, topic):
    prompt = f"""You are an expert tutor. Create high-quality Anki flashcards for the topic: '{topic}'. 
    Return JSON with a 'vocabulary' list. Each item must have:
    'Term' (The concept), 
    'Meaning' (A clear, concise explanation), 
    'Example' (A concrete problem or application).
    Do not just list website headers."""
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"{prompt}\n\nSource Content: {text[:6000]}"}],
        "response_format": {"type": "json_object"}
    }
    response = requests.post(GROQ_URL, headers=headers, json=data)
    
    # Debugging print to see if LLM returned valid JSON
    content = response.json()['choices'][0]['message']['content']
    return json.loads(content)

def add_to_anki(card_data, deck_name):
    # 1. Try to add to the topic deck
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name, # Try the topic name
                "modelName": "Basic",
                "fields": {
                    "Front": card_data.get('Term', 'Concept'),
                    "Back": f"{card_data.get('Meaning', '')}<br><b>Example:</b> {card_data.get('Example', '')}"
                }
            }
        }
    }
    
    resp = requests.post(ANKI_URL, json=payload, timeout=5)
    result = resp.json()
    
    # 2. If deck doesn't exist, fallback to "Default"
    if result.get('error') and "deck was not found" in result.get('error'):
        payload['params']['note']['deckName'] = "Default"
        resp = requests.post(ANKI_URL, json=payload, timeout=5)
        result = resp.json()

    if result.get('error'):
        print(f"[!] Anki Error: {result['error']}")
        return False
    return True

if __name__ == "__main__":
    topic = input("Enter research topic: ")
    content = autonomous_research(topic)
    
    if content:
        print("[*] Generating smart flashcards...")
        try:
            data = generate_flashcards(content, topic)
            if data and 'vocabulary' in data:
                print(f"[*] Found {len(data['vocabulary'])} cards. Adding to Anki...")
                for card in data['vocabulary']:
                    if add_to_anki(card, topic):
                        print(f"[+] Added: {card['Term']}")
                    else:
                        print(f"[-] Failed: {card['Term']}")
                    time.sleep(0.5) # Throttle to prevent API congestion
        except Exception as e:
            print(f"[!] Generation Error: {e}")
            
    print("[*] Done.")