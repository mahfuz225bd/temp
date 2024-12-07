import os
import sys
from flask import Flask, request, render_template

# Environment variables to resolve SpeechBrain symlink issues
# os.environ["SB_FETCH_STRATEGY"] = "copy"  # Avoid symlinks on Windows
# os.environ["TORCH_HOME"] = os.path.join(os.getcwd(), "cache")

def register_sub_app(root_folder, folder, root_route, project_route):
    """
    Register a sub-app using Flask Blueprints.

    Args:
        root_folder (str): The root folder where sub-app directories are located (e.g., "APIs").
        folder (str): The specific folder name within the root folder (e.g., "api-speechbrain").
        root_route (str): The main route prefix for the root folder (e.g., "api").
        project_route (str): The specific sub-route for the project (e.g., "speechbrain").
    """
    sub_app_path = os.path.join(root_folder, folder)
    sys.path.insert(0, sub_app_path)  # Add sub-app to the path

    try:
        from main import app as blueprint  # Ensure sub-app exposes a Blueprint
        url_prefix = f'/{root_route}/{project_route}'
        app.register_blueprint(blueprint, url_prefix=url_prefix)
        print(f"Registered sub-app from {sub_app_path} under {url_prefix}")
    except Exception as e:
        print(f"Failed to register sub-app from {sub_app_path}: {e}")

# Main Flask app setup
app = Flask(__name__)

# List of sub-app configurations
sub_apps = [
    {
        "root_folder": "APIs",
        "folder": "api-speechbrain",
        "root_route": "api",
        "project_route": "speechbrain"
    },
    {
        "root_folder": "APIs",
        "folder": "api-test",
        "root_route": "api",
        "project_route": "test"
    },
    {
        "root_folder": "Projects",
        "folder": "a",
        "root_route": "project",
        "project_route": "a"
    },
    {
        "root_folder": "Projects",
        "folder": "b",
        "root_route": "project",
        "project_route": "b"
    },
    {
        "root_folder": "CDNs",
        "folder": "a",
        "root_route": "cdn",
        "project_route": "a"
    },
    {
        "root_folder": "CDNs",
        "folder": "b",
        "root_route": "cdn",
        "project_route": "b"
    },
    # Add more configurations as needed
]

# Register each sub-app dynamically
for sub_app_config in sub_apps:
    register_sub_app(
        root_folder=sub_app_config["root_folder"],
        folder=sub_app_config["folder"],
        root_route=sub_app_config["root_route"],
        project_route=sub_app_config["project_route"]
    )

@app.route('/')
def index():
    root_url = request.url_root.rstrip("/")
    grouped_apps = {}

    for sub_app_config in sub_apps:
        root_folder = sub_app_config["root_folder"]
        root_route = sub_app_config["root_route"]
        project_route = sub_app_config["project_route"]
        sub_route = f"{root_route}/{project_route}"
        grouped_apps.setdefault(root_folder, []).append(sub_route)

    # Pass dynamic content to the template
    return render_template(
        "index.html",
        root_url=root_url,
        grouped_apps=grouped_apps
    )

if __name__ == '__main__':
    app.run(debug=True)
