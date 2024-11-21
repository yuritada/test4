from flask import Flask
from blueprints.auth import auth_bp
from blueprints.reviews import reviews_bp
from blueprints.main import main_bp
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Blueprintの登録
app.register_blueprint(auth_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(main_bp)

# アップロード設定
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)