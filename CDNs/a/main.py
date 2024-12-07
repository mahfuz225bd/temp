from flask import Blueprint

app = Blueprint('cdn_a', __name__)

@app.route('/')
def home():
    return "Hello from a CDN"
