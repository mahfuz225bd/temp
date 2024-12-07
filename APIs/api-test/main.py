from flask import Blueprint

app = Blueprint('api_test', __name__)

@app.route('/')
def home():
    return "Hello from test API"
