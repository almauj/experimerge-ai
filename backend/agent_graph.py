import os
from backend.database import save_chat, get_chat_history, get_user_profile
from backend.agents_pool import get_agent_prompts
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def run_agent_workflow(session_id, user_id, user_input, classified_route):
    """Executes the specialized agent workflow with a verification guardrail loop."""
    
    # state, llm, and prompt configuration/initialization 
    state = {
        "user_input": user_input,
        "target_agent": classified_route if classified_route else "manager", # return to manager if None
        "draft_response": "",
        "critique": "",
        "revision_count": 0,
        "max_revisions": 2
    }
    
    llm = ChatOllama(model="llama3.2", temperature=0.2)
    prompts = get_agent_prompts()
    
    # pull user profile memory from database
    profile_data = get_user_profile(user_id)
    profile_context = f"Patterns: {profile_data['patterns']} | Motivations: {profile_data['motivations']} | Weaknesses: {profile_data['weaknesses']}"
    
    # refinement loop
    while state["revision_count"] <= state["max_revisions"]:
        active_agent = state["target_agent"]
        prompt_template = prompts[active_agent]
        
        # integrate user profile memory into agent persona
        system_instruction = prompt_template.messages[0].prompt.template.format(user_profile=profile_context)
        
        
        langchain_messages = [SystemMessage(content=system_instruction)]
        
        # short-term memory context fetch
        history = get_chat_history(session_id, limit=5)
        for role, content in history:
            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
                
        # inject critique if exists from previous iteration
        execution_prompt = state["user_input"]
        if state["critique"]:
            execution_prompt += f"\n\n[REVISION NOTICE] Your previous draft was rejected. Fix this specific critique: {state['critique']}"
            
        langchain_messages.append(HumanMessage(content=execution_prompt))
        
        # worker agent output
        worker_output = llm.invoke(langchain_messages)
        state["draft_response"] = worker_output.content
        
        # ----- verify worker agent output-----
        qa_template = prompts["verification"]
        
        # format user message to verificaiton template
        qa_content = qa_template.messages[0].prompt.template.format(
            draft_content=state["draft_response"],
            user_input=state["user_input"]
        )
        
        qa_verdict = llm.invoke([HumanMessage(content=qa_content)]).content.strip()
        
        if "APPROVED" in qa_verdict.upper():
            break
        else:
            # save crique and continue revision loop
            state["critique"] = qa_verdict
            state["revision_count"] += 1
            
    # add finalized response to data base
    save_chat(session_id, "assistant", state["draft_response"])
    return state["draft_response"], state["revision_count"]
