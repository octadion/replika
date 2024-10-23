import psycopg2, os
from psycopg2 import sql

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DBNAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS msg (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            is_user BOOLEAN NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id SERIAL PRIMARY KEY,
            entity_type VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            message_id INTEGER REFERENCES msg(id),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def save_message(content, is_user):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        sql.SQL("INSERT INTO msg (content, is_user) VALUES (%s, %s) RETURNING id"),
        (content, is_user)
    )
    message_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return message_id

def save_entity(entity_type, content, message_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM msg WHERE id = %s", (message_id,))
    if cur.fetchone() is None:
        print(f"Warning: message_id {message_id} does not exist in messages table. Skipping entity save.")
        conn.close()
        return
    
    cur.execute(
        sql.SQL("INSERT INTO entities (entity_type, content, message_id) VALUES (%s, %s, %s)"),
        (entity_type, content, message_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def update_entities(entities, message_id):
    for entity_type, entity_data in entities.items():
        for content in entity_data['content']:
            save_entity(entity_type, content, message_id)