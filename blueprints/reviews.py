from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from db import get_db_connection, close_db_connection
from config import allowed_file, UPLOAD_FOLDER
import os

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_id = session['user_id']
        visited = request.form['visited']
        place = request.form['place']
        attitude = request.form['attitude']
        price = request.form['price']
        speed = request.form['speed']
        image_file = request.files.get('image')

        # 画像の保存
        image_path = None
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)

        # データベースに保存
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO evaluation (user_id, visited, place, attitude, price, speed, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, visited, place, attitude, price, speed, image_path))
        conn.commit()
        close_db_connection(conn)

        return redirect(url_for('reviews.profile'))

    return render_template('add.html')

@reviews_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evaluation WHERE user_id = ?", (user_id,))
    evaluation = cursor.fetchall()
    cursor.execute("SELECT username FROM user_map WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    username = result[0] if result else "Unknown"
    close_db_connection(conn)

    return render_template('profile.html', evaluation=evaluation, username=username)