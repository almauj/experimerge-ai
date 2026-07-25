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