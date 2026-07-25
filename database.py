import os
import psycopg2
from dotenv import load_dotenv

# Loading environments
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def save_chat(session_id, role, content):
    """Save chat history to learning agent database."""
    
    # database instance
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # save chat history to table
    cur.execute("INSERT INTO chat_history(session_id, role, content) VALUES(%s, %s, %s); ", (session_id, role, content))
    
    # make changes persistant
    conn.commit()
    
    # close cursor and connection to database
    cur.close()
    conn.close()
    
    print("Chat History Saved Successfully...")
    


def get_chat_history(session_id, limit=5):
    """View recent chat history from a single session in order."""
        
    # database instance
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
        
    # view chat history and fetch rows (newest ones first)
    cur.execute("SELECT role, content FROM chat_history WHERE session_id = %s ORDER BY id DESC LIMIT %s;", (session_id, limit))
    rows = cur.fetchall()
        
    # make changes persistant
    conn.commit()
        
    # close cursor and connection to database
    cur.close()
    conn.close()
        
    print("Data Fetched Successfully...")
    
    return rows[::-1] # oldest to newest

def get_user_profile(user_id):
    """Retrieves the compact long-term behavioral profile for a specific user."""
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cur.execute(
        "SELECT patterns_and_behaviors, core_motivations, identified_weaknesses FROM user_profile WHERE user_id = %s;",
        (user_id,)
    )
    row = cur.fetchone()
    
    cur.close()
    conn.close()
    
    # If the user has profile, return it as a structured dictionary to agents
    if row:
        return {
            "patterns": row[0],
            "motivations": row[1],
            "weaknesses": row[2]
        }
    
    # If no profile exists yet, return default and create new
    return {
        "patterns": "No behavioral patterns logged yet.",
        "motivations": "No specific professional motivations logged yet.",
        "weaknesses": "No concrete technical weaknesses logged yet."
    }
    

def save_user_profile(user_id, patterns, motivations, weaknesses):
    """Performs an UPSERT to save or update the long-term episodic memory metrics."""
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Senior SQL Syntax: ON CONFLICT dynamically changes the action based on key existence
    sql_query = """
        INSERT INTO user_profile (user_id, patterns_and_behaviors, core_motivations, identified_weaknesses, last_updated)
        VALUES (%s, %s, %s, %s, NOW())
        ON CONFLICT (user_id) 
        DO UPDATE SET 
            patterns_and_behaviors = EXCLUDED.patterns_and_behaviors,
            core_motivations = EXCLUDED.core_motivations,
            identified_weaknesses = EXCLUDED.identified_weaknesses,
            last_updated = NOW();
    """
    
    cur.execute(sql_query, (user_id, patterns, motivations, weaknesses))
    
    conn.commit()
    cur.close()
    conn.close()