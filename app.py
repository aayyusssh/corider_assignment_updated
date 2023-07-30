# app.py
from flask import Flask
from users import user_bp

from pymongo import MongoClient

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
