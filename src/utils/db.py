from sqlalchemy import create_engine

def get_db_engine():
    return create_engine("sqlite:///task_manager.db")