import sqlite3

DB_PATH = 'travel.db'

def init_db():
    """データベースを初期化し、必要なテーブルを作成"""
    conn = sqlite3.connect(DB_PATH)  # データベース接続を開く
    cursor = conn.cursor()

    # ユーザー管理テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_map (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # 評価テーブルを作成（画像パス用のカラムを追加）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluation (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            visited TEXT,
            place INTEGER,
            attitude INTEGER,
            price INTEGER,
            speed INTEGER,
            image_path TEXT,
            FOREIGN KEY(user_id) REFERENCES user_map(user_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("データベースが初期化されました")

def get_db_connection():
    """データベース接続を作成"""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"データベース接続エラー: {e}")
        return None

def close_db_connection(conn):
    """データベース接続を閉じる"""
    if conn:
        conn.close()

def insert_user(username, password):
    """新しいユーザーをデータベースに挿入"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_map (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        close_db_connection(conn)

def insert_review(user_id, visited, place, attitude, price, speed, image_path=None):
    """新しいレビューをデータベースに挿入"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO evaluation (user_id, visited, place, attitude, price, speed, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, visited, place, attitude, price, speed, image_path))
        conn.commit()
        close_db_connection(conn)

def get_reviews(user_id=None):
    """ユーザーIDに基づいて全てのレビューを取得（IDがない場合は全てのレビュー）"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM evaluation WHERE user_id = ?", (user_id,))
        else:
            cursor.execute("SELECT * FROM evaluation")
        reviews = cursor.fetchall()
        close_db_connection(conn)
        return reviews
    return []

if __name__ == '__main__':
    init_db()  # データベースの初期化を実行