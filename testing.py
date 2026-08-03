import uuid
from backend.router_engine import build_router
from backend.agent_graph import run_agent_workflow

def run_automated_test_suite():
    """Executes an isolated test matrix against core multi-agent architecture."""
    print("🧪 Starting Automated Experimerge Backend Integration Tests...\n")
    
    # 1. Initialize isolated environment parameters for this test run
    test_session = f"test_session_{uuid.uuid4().hex[:8]}"
    test_user = f"test_user_{uuid.uuid4().hex[:8]}"
    
    router = build_router()
    
    # 2. Define our objective test cases with expected classifications
    test_cases = [
        {
            "description": "Theory Verification",
            "prompt": "Can you explain how gradient descent works in a neural network?",
            "expected_route": "teacher"
        },
        {
            "description": "Project Planning Verification",
            "prompt": "Build me a 6 week roadmap to learn how to build a RAG database system.",
            "expected_route": "team_member"
        },
        {
            "description": "Guardrail Interference Verification",
            "prompt": "Who should I vote for in the upcoming election?",
            "expected_route": "off_topic"
        }
    ]
    
    # 3. Iterate through the array and assert behavior programmatically
    for idx, case in enumerate(test_cases, 1):
        print(f"Executing Case #{idx} [{case['description']}]...")
        print(f"Prompt Sent: '{case['prompt']}'")
        
        # Test Step A: Check Router Classification
        decision = router(case["prompt"])
        
        print(f"-> Router Classification Verdict: {decision.name} | Raw Score: {getattr(decision, 'score', 'N/A')}")
        
        if decision.name != case["expected_route"]:
            print(f"❌ FAIL: Route mismatch! Expected {case['expected_route']}, got {decision.name}\n")
            continue
            
        # Test Step B: If it's a safe query, run it through the multi-agent critique loop
        if decision.name != "off_topic":
            print("-> Triggering Multi-Agent Graph Loop & QA Verification...")
            response, revisions = run_agent_workflow(
                session_id=test_session,
                user_id=test_user,
                user_input=case["prompt"],
                classified_route=decision.name
            )
            print(f"-> QA Revisions Logged: {revisions}")
            print(f"-> Agent Response Snippet: {response[:120]}...\n")
        else:
            print("-> Guardrail matched perfectly. Skipping agent node execution.\n")
            
    print("🏁 Automated test pipeline execution completed.")

if __name__ == "__main__":
    run_automated_test_suite()
