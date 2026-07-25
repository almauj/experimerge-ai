from semantic_router import Route 
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.layer import RouteLayer

def build_router():
    """Configures semantic paths to classify user intent."""
    
    # basic chat route with basic intros and exits 
    chat_route = Route(
        name="chatting",
        utterences=['hi', 'hello', 'whats up?', 'bye', 'thanks!', 'talk to you later']
    )
    
    # guardrail route, off topic or bad questions
    ban_route = Route(
        name="off_topic",
        utterences=['who should I vote for?', 'what is the weather today?', 'play a video game']
    )
    
    # local mathematical encoder
    encoder = HuggingFaceEncoder()
    
    # route layer instance
    rl = RouteLayer(encoder=encoder, routes=[chat_route, ban_route])
    
    return rl