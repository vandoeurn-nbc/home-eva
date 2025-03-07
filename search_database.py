import sqlite3

DATABASE_NAME = "search_history.db"

def create_database():
    """Create the SQLite database and table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_type TEXT,
            district TEXT,
            commune TEXT,
            price REAL,
            size REAL,
            bedrooms INTEGER,
            bathrooms INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_search(property_type, district, commune, price, size, bedrooms, bathrooms):
    """Save a search result to the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO searches (property_type, district, commune, price, size, bedrooms, bathrooms)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (property_type, district, commune, price, size, bedrooms, bathrooms))
    conn.commit()
    conn.close()

def get_recent_searches():
    """Retrieve the last 10 searches from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, property_type, district, commune, price, size, bedrooms, bathrooms
        FROM searches ORDER BY id DESC LIMIT 10
    ''')
    searches = cursor.fetchall()
    conn.close()
    return searches

def get_search_by_id(search_id):
    """Retrieve a specific search result by ID."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT property_type, district, commune, price, size, bedrooms, bathrooms
        FROM searches WHERE id = ?
    ''', (search_id,))
    search = cursor.fetchone()
    conn.close()
    return search
