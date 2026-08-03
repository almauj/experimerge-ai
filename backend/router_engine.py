from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.layer import RouteLayer


def build_router():
    """Builds a high-speed vector classification layer mapping queries to specialized sub-agents."""
    
    THRESHOLD = 0.70
    
    # admin greeting casual talk
    chat_route = Route(
        name="manager",
        utterances=[
            'hi', 'hello', 'hey there', 'good morning', 'thanks', 'bye', 
            'clear the context', 'who are you', 'how are you doing'
        ],
        score_threshold=THRESHOLD
    )
    
    # theories, concepts, algorithms
    teacher_route = Route(
        name="teacher",
        utterances=[
            'explain linear regression math', 'what is a loss function', 
            'how do transformers work', 'explain gradient descent to a beginner',
            'what does overfitting mean', 'break down the math behind neural networks',
            'can you teach me about enterprise level practices'
        ],
        score_threshold=THRESHOLD
    )
    
    # roadmaps, timeline, projects
    team_route = Route(
        name="team_member",
        utterances=[
            'build a roadmap for a full stack app', 'create a study plan for ai engineering',
            'how should I structure this git repo', 'break this project into 2 week sprints',
            'what tools should I use to build a rag application', 'design a learning timeline',
            'i want to build', "build me a 2 day roadmap to learn hackathon workflows", 
            'what tools should I use to build an rag project'
        ],
        score_threshold=THRESHOLD
    )
    
    # code reviews, interview prep, career advice
    mentor_route = Route(
        name="mentor",
        utterances=[
            'review my python script for bugs', 'why am i getting an indexerror here',
            'optimize this sql database join query', 'how do i pass an entry level machine learning interview',
            'look at this code snippet and find security vulnerabilities', 'mock interview practice',
            'can you review my portfolio against current market needs'
        ],
        score_threshold=THRESHOLD
    )
    
    guardrail_route = Route(
        name="off_topic",
        utterances=[
            'who should i vote for', 'play a game for me', 'what will the weather be today',
            'tell me about the playoffs', 'what sports teams are here', 'where should i eat today',
        ],
        score_threshold=THRESHOLD
    )
    
    # initialize embedding encoder
    encoder = HuggingFaceEncoder(model_name="BAAI/bge-small-en-v1.5")
    
    # router assembly 
    rl = RouteLayer(encoder=encoder, routes=[chat_route, teacher_route, team_route, mentor_route, guardrail_route])
    
    return rl
