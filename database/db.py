from pathlib import Path
import sqlite3

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DB_PATH : Path = BASE_DIR / "data/db.db"

def get_connection():
    """
    Creates a connection with a DB table.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """
    Checks for the existence of a sqlite table, if it does not exist -> create it.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS VPS_SERVERS(
        OWNER_ID INTEGER NOT NULL,
        IP TEXT NOT NULL,
        LOGIN TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        RENT_END TEXT NOT NULL,
        PROJECT_NAME TEXT NOT NULL,
        REMINDED BOOL DEFAULT FALSE,
        UNIQUE(OWNER_ID, IP)
        )""")
    conn.commit()
    conn.close()
