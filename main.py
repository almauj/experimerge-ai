import os
import uuid

from backend.database import save_chat
from backend.router_engine import build_router
from backend.agent_graph import run_agent_workflow

def start_terminal_agent():
    """Orchestrates mapping multi-agent workflow and database interations."""
    print("Initializing Experimerge.ai Learning Agent....")
    
    # initializing and dest cases
    router = build_router()
    
    session_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    
    
    print("System Ready: Type 'exit' or 'quit' to close terminal.")
    print("Session Id: {session_id}")
    
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
        if route_decision.name == 'chatting':
            response_text = "Hello! I am your Learning Agent Mentor, what would you like to learn today?"
            print(f"Agent:{response_text}\n")
            save_chat(session_id, "assistant", response_text)
        elif route_decision.name == 'off_topic':
            response_text = "I am specifically optimized to help you with your learning goals. Let's keep our focus!"
            print(f"Agent: {response_text}\n")
            save_chat(session_id, "assistant", response_text)
        else: 
            print("Agent: (Activating Specialized Multi-Agent Network...)")
            
            final_reply, revisions_made = run_agent_workflow(
                session_id=session_id,
                user_id=user_id,
                user_input=user_input,
                classified_route=route_decision.name
            )
            
            print(f"Agent [Revisions: {revisions_made}]: {final_reply}\n")
            
            
        

if __name__=="__main__":
    start_terminal_agent()