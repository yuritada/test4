from flask import Blueprint, render_template
import sqlite3

main_bp = Blueprint('main', __name__)

def get_reviews(Calum, db_name):
    conn = sqlite3.connect('travel.db')
    c = conn.cursor()
    c.execute(f'SELECT {Calum} FROM {db_name}')
    reviews = c.fetchall()
    conn.close()
    return reviews

@main_bp.route('/')
def home():
    reviews = get_reviews("*", "evaluation")
    return render_template('index.html', evaluation=reviews)