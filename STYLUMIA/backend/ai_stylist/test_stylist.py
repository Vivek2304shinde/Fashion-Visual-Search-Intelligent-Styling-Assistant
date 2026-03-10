import requests
import json
import time

api_url = "http://localhost:8000"

def test_conversation():
    print("🎨 TESTING FIXED CONVERSATION MANAGER")
    print("="*60)
    
    # Start conversation
    print("\n1️⃣ Starting conversation...")
    resp = requests.post(f"{api_url}/api/stylist/conversation/start", json={
        "initial_message": "I need an outfit for a beach wedding",
        "gender": "male"
    })
    
    if resp.status_code != 200:
        print(f"❌ Error: {resp.status_code}")
        print(resp.text)
        return
    
    data = resp.json()
    session_id = data['session_id']
    print(f"✅ Session: {session_id}")
    print(f"🤖 AI: {data['message']}")
    print(f"📊 Collected: {data['collected_info']}")
    
    time.sleep(1)
    
    # Send first message
    print("\n2️⃣ Sending: 'I like light blue colors'")
    resp = requests.post(f"{api_url}/api/stylist/conversation/{session_id}/chat", json={
        "message": "I like light blue colors"
    })
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"🤖 AI: {data['message']}")
        print(f"📊 Collected: {data['collected_info']}")
    
    time.sleep(1)
    
    # Send second message
    print("\n3️⃣ Sending: 'My budget is around ₹20000'")
    resp = requests.post(f"{api_url}/api/stylist/conversation/{session_id}/chat", json={
        "message": "My budget is around ₹20000"
    })
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"🤖 AI: {data['message']}")
        print(f"📊 Collected: {data['collected_info']}")
        
        if data['ready_for_recommendation']:
            print("\n✨ Ready for recommendations!")
            
            # Get recommendations
            print("\n4️⃣ Getting outfit recommendations...")
            resp = requests.post(f"{api_url}/api/stylist/conversation/{session_id}/recommend", json={})
            
            if resp.status_code == 200:
                data = resp.json()
                print("\n✅ OUTFIT PLAN:")
                print(json.dumps(data.get('outfit_plan', {}), indent=2))
                
                if data.get('styling_advice'):
                    print(f"\n💡 {data['styling_advice']}")
            else:
                print(f"❌ Error getting recommendations: {resp.status_code}")

if __name__ == "__main__":
    test_conversation()