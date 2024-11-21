from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_db_connection, close_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """ユーザー登録"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # データベース接続
        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーが既に存在するかチェック
        cursor.execute("SELECT * FROM user_map WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "このユーザー名はすでに使われています"
        
        # 新しいユーザーをデータベースに挿入
        cursor.execute("INSERT INTO user_map (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        # 接続を閉じる
        close_db_connection(conn)

        return redirect(url_for('auth.login'))  # ログインページにリダイレクト

    return render_template('register.html')  # ユーザー登録フォームを表示

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    """ユーザーログイン"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # データベース接続
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_map WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        # 接続を閉じる
        close_db_connection(conn)

        if user:
            session['user_id'] = user[0]  # ユーザーIDをセッションに保存
            userid = user[0]
            return redirect(url_for('reviews.profile'))
        else:
            return "ログイン失敗"

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.home'))