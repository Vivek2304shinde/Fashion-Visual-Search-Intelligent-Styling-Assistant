import requests
import json
import time

api_url = "http://localhost:8000"

print("🔍 TESTING CONVERSATION MANAGER")
print("="*60)

# Start conversation
print("\n1️⃣ Starting conversation...")
resp = requests.post(f"{api_url}/api/stylist/conversation/start", json={
    "initial_message": "I need a navy blue suit for a wedding next month"
})

if resp.status_code != 200:
    print(f"❌ Error: {resp.status_code}")
    exit()

data = resp.json()
session_id = data['session_id']
print(f"✅ Session: {session_id}")
print(f"🤖 AI: {data['message']}")
print(f"📊 Collected: {data['collected_info']}")

# Send 3 messages to see if it learns
test_messages = [
    "I'm the groom, actually",
    "I prefer traditional style with modern touch",
    "My budget is around ₹50,000"
]

for i, msg in enumerate(test_messages, 2):
    print(f"\n{i}️⃣ Sending: '{msg}'")
    time.sleep(1)  # Small delay
    
    resp = requests.post(f"{api_url}/api/stylist/conversation/{session_id}/chat", json={
        "message": msg
    })
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"🤖 AI: {data['message']}")
        print(f"📊 Collected: {data['collected_info']}")
        
        # Check if it's still the canned response
        if data['message'] == "Hey! 😊 Tell me more about what you're looking for!":
            print("⚠️  WARNING: Still getting canned response!")
    else:
        print(f"❌ Error: {resp.status_code}")

print("\n" + "="*60)
print("If you're still getting canned responses, your conversation_manager.py")
print("needs to be replaced with the LLM version I provided.")