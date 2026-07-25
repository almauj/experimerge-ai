import os

from database import save_chat, get_chat_history
from semantic_router import build_router
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def start_terminal_agent():
    
    
    print("Initializing Experimerge.ai Learning Agent....")
    
    # initializing the components 
    router = build_router()
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    # test session 
    session_id = "test_session"
    
    print("System Ready: Type 'exit' or 'quit' to close terminal.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            break
        
        if not user_input:
            continue
        
        # Save session information
        save_chat(session_id, "user", user_input)
        
        # check router
        route_decision = router(user_input)
        
        # routing logic 
        if route_decision.name == 'off_topic':
            response_text = "Hello! I am your Learning Agent Mentor, what would you like to learn today?"
            print(f"Agent:{response_text}\n")
            save_chat(session_id, "assistant", response_text)
        elif route_decision.name == 'chatting':
            response_text = "I am specifically optimized to help you with your learning goals. Let's keep our focus!"
            print(f"Agent: {response_text}\n")
            save_chat(session_id, "assistant", response_text)
        else: 
            print("Agent: (Thinking...)")
            
            # agent personality
            messages = [
                SystemMessage(
                    content="You are a patient, expert Senior Software Engineer mentoring a junior developer. Break down complex math and programming concepts simply without writing the code for them. ")
            ]
            
            # retrieve past conversations from database (using docker)
            db_history = get_chat_history(session_id, limit=6)
            
            # format to langchain objects
            for role, content in db_history:
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
                    
            messages.append(HumanMessage(content=user_input))
            ai_response = llm.invoke(messages)
            
            final_reply = ai_response.content
            print(f"Agent: {final_reply}\n")
            save_chat(session_id, "assistant", final_reply)
            
            
        

if __name__=="__main__":
    start_terminal_agent()