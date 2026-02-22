import os
import sqlite3
import logging
from langgraph.checkpoint.sqlite import SqliteSaver

logger = logging.getLogger(__name__)

# Global connection to keep SqliteSaver alive across requests
_conn = None
_checkpointer = None

def get_checkpointer():
    global _conn, _checkpointer
    if _checkpointer is None:
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "langgraph_checkpoints.sqlite")
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            # check_same_thread=False is needed for FastAPI since requests come on different threads
            _conn = sqlite3.connect(db_path, check_same_thread=False)
            
            # Setup SqliteSaver
            _checkpointer = SqliteSaver(_conn)
            logger.info("LangGraph SQLite Checkpointer initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize SQLite checkpointer: {e}")
            _checkpointer = None
            
    return _checkpointer
