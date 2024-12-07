from flask import Blueprint

app = Blueprint('project_a', __name__)

@app.route('/')
def home():
    return "Hello from a Project"
