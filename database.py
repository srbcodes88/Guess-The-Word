import sqlite3
from datetime import date

DB_FILE="word_bank.db"
WORD_TABLE=[
    "ADOPT", "BLAZE", "CATCH", "DOUSE", "EPOXY", "FROCK", "GRAND", "HITCH", "ICHOR", "JOWAR", "KELPS", "LACED", "MIRTH", "NOVEL", "ORBIT", "PLANT", "QUERY", "ROVER", "SHEAR", "TROVE"
]

def init_db():
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'player'))
                )
                ''')
    
    cur.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT UNIQUE NOT NULL
                )
                ''')
    
    cur.execute('''
                CREATE TABLE IF NOT EXISTS guesses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    game_date DATE NOT NULL,
                    target_word TEXT NOT NULL,
                    guess_num INTEGER NOT NULL,
                    guessed_word TEXT NOT NULL,
                    is_correct BOOLEAN NOT NULL
                )
                ''')
    
    cur.execute('SELECT COUNT(*) FROM words')
    if cur.fetchone()[0] == 0:
        for w in WORD_TABLE:
            cur.execute('INSERT INTO words(word) VALUES (?)', (w,))
    conn.commit()
    conn.close()

def register_user(username, password, role):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    try:
        # Check if username already exists
        cur.execute('SELECT 1 FROM users WHERE username=?', (username,))
        if cur.fetchone():
            return False  # Username exists

        # Insert user if not exists
        cur.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                    (username, password, role))
        con.commit()
        return True
    except Exception as e:
        print(f"Error in register_user: {e}")  # For debugging
        return False
    finally:
        con.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT role FROM users WHERE username=? AND password=?', (username, password))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def get_daily_guess_count(username):
    today = str(date.today())
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(DISTINCT target_word) FROM guesses WHERE username=? AND game_date=?', (username, today))
    cnt = cur.fetchone()[0]
    conn.close()
    return cnt

def get_random_word():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT word FROM words ORDER BY RANDOM() LIMIT 1')
    w = cur.fetchone()[0]
    conn.close()
    return w

def log_guess(username, target_word, guessed_word, guess_num, win):
    today = str(date.today())
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''
        INSERT INTO guesses (username, game_date, target_word, guess_num, guessed_word, is_correct)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, today, target_word, guess_num, guessed_word, int(win)))
    conn.commit()
    conn.close()

def admin_daily_report(report_date):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        SELECT COUNT(DISTINCT username), SUM(win)
        FROM guesses WHERE game_date=?
        AND guess_num=(SELECT MIN(guess_num) FROM guesses g2 WHERE g2.username=guesses.username AND g2.target_word=guesses.target_word)
    ''', (report_date,))
    res = cur.fetchone()
    conn.close()
    num_users = res[0] if res else 0
    num_wins = res[1] if res and res[1] is not None else 0
    return num_users, num_wins

def admin_user_report(username):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        SELECT game_date, COUNT(DISTINCT target_word), SUM(win)
        FROM guesses
        WHERE username=?
        GROUP BY game_date
        ORDER BY game_date
    ''', (username,))
    data = cur.fetchall()
    conn.close()
    return data

def get_all_usernames():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT username FROM users WHERE role="player"')
    names = [x[0] for x in cur.fetchall()]
    conn.close()
    return names