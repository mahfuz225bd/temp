from flask import Blueprint

app = Blueprint('cdn_b', __name__)

@app.route('/')
def home():
    return "Hello from b CDN"
