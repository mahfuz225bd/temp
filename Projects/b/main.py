from flask import Blueprint

app = Blueprint('project_b', __name__)

@app.route('/')
def home():
    return "Hello from b Project"
