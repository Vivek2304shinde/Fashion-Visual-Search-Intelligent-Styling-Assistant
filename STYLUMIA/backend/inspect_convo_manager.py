import os
import inspect

# Try to import the conversation manager
try:
    from ai_stylist.agents.conversation_manager import ConversationManager
    
    print("📁 Conversation Manager Location:")
    print(f"   {inspect.getfile(ConversationManager)}")
    print()
    
    # Check the source code briefly
    import inspect
    source = inspect.getsource(ConversationManager)
    
    if "self.SYSTEM_PROMPT" in source:
        print("✅ Using LLM-powered version (has SYSTEM_PROMPT)")
        print("   First 200 chars of source:")
        print("-" * 40)
        print(source[:200] + "...")
    elif "QUESTIONS = {" in source:
        print("❌ Using OLD hardcoded version (has QUESTIONS dict)")
        print("   This needs to be replaced!")
    else:
        print("⚠️ Unknown version")
        
except ImportError as e:
    print(f"❌ Error importing: {e}")
except Exception as e:
    print(f"❌ Error: {e}")