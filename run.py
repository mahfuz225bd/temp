import sys
import os
from flask import Flask, jsonify

def register_sub_app(root_folder, folder, project_root_route, project_route):
    """
    Registers a sub-app as a blueprint in the main Flask app.

    Args:
    - root_folder: The root folder where the sub-app resides.
    - folder: The specific folder of the sub-project.
    - project_root_route: The root route for the project.
    - project_route: The route for the sub-project.
    """
    # Build the path to the sub-app's directory
    sub_app_path = os.path.join(os.path.dirname(__file__), root_folder, folder)

    # Add the sub-app's path to sys.path
    sys.path.insert(0, sub_app_path)

    # Import the app (main.py) as sub_app from the sub-project
    from main import app as sub_app  # Adjust this to the correct path based on the sub-app's location

    # Create a unique name by combining root_folder, folder, and project_route
    blueprint_name = f"{root_folder}_{folder}_{project_route}"

    # Register sub-app as a blueprint under the main app with a unique name
    app.register_blueprint(sub_app, url_prefix=f'/{project_root_route}/{project_route}', name=blueprint_name)

# Main app setup
app = Flask(__name__)

# List of sub-apps to register
sub_apps = [
    {
        "root_folder": "APIs",  # Root folder in your project where the sub-app is located
        "folder": "api-speechbrain",  # The folder of the sub-project
        "project_root_route": "api",  # Root route for the API part of the URL
        "project_route": "speechbrain"  # Specific route for this sub-project
    },
    {
        "root_folder": "APIs",
        "folder": "api-test",
        "project_root_route": "api",
        "project_route": "test"
    },
    {
        "root_folder": "Projects",
        "folder": "a",
        "project_root_route": "project",
        "project_route": "a"
    },
    {
        "root_folder": "Projects",
        "folder": "b",
        "project_root_route": "project",
        "project_route": "b"
    },
    {
        "root_folder": "CDNs",
        "folder": "a",
        "project_root_route": "cdn",
        "project_route": "a"
    },
    {
        "root_folder": "CDNs",
        "folder": "b",
        "project_root_route": "cdn",
        "project_route": "a"
    },
    # You can add more sub-app configurations here
]

# Register each sub-app dynamically
for sub_app_config in sub_apps:
    register_sub_app(
        root_folder=sub_app_config["root_folder"],
        folder=sub_app_config["folder"],
        project_root_route=sub_app_config["project_root_route"],
        project_route=sub_app_config["project_route"]
    )

# Main route (index)
@app.route('/')
def index():
    # Group sub-apps by their root_folder
    grouped_apps = {}

    for sub_app_config in sub_apps:
        root_folder = sub_app_config["root_folder"]
        project_route = sub_app_config["project_route"]
        app_route = f"/{sub_app_config['project_root_route']}/{project_route}"

        # Initialize group for the root folder if not already present
        if root_folder not in grouped_apps:
            grouped_apps[root_folder] = []
        grouped_apps[root_folder].append(app_route)

    # Build the HTML response with grouped lists and inline CSS for styling
    html_response = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 20px;
                }
                h1 {
                    color: #2c3e50;
                }
                h2 {
                    font-size: 18px;
                    color: #7f8c8d;
                }
                h3 {
                    color: #3498db;
                }
                ul {
                    list-style-type: none;
                    padding-left: 0;
                }
                li {
                    background-color: #ecf0f1;
                    margin: 5px 0;
                    padding: 10px;
                    border-radius: 4px;
                }
                a {
                    text-decoration: none;
                    color: #2980b9;
                }
                a:hover {
                    color: #1abc9c;
                }
                input[type="text"] {
                    padding: 10px;
                    width: 100%;
                    margin-bottom: 20px;
                    border-radius: 4px;
                    border: 1px solid #ccc;
                }
            </style>
        </head>
        <body>
            <h1>All Sub Applications</h1>
            <h2>Hosted under domain: https://mahfuz225bd.pythonanywhere.com/</h2>
            <input type="text" id="search" placeholder="Search for sub-apps..." onkeyup="filterList()">
            <div id="apps-list">
    """

    for root_folder, apps in grouped_apps.items():
        html_response += f"<h3>{root_folder}</h3><ul class='app-list'>"
        for app in apps:
            html_response += f"<li class='app-item'><a href='{app}'>{app}</a></li>"
        html_response += "</ul>"

    html_response += """
        </div>
        <script>
            function filterList() {
                let searchTerm = document.getElementById('search').value.toLowerCase();
                let appItems = document.getElementsByClassName('app-item');
                
                for (let i = 0; i < appItems.length; i++) {
                    let appName = appItems[i].textContent || appItems[i].innerText;
                    if (appName.toLowerCase().includes(searchTerm)) {
                        appItems[i].style.display = '';
                    } else {
                        appItems[i].style.display = 'none';
                    }
                }
            }
        </script>
        </body>
    </html>
    """

    return html_response

@app.route('/test')
def test():
    return "/test"

if __name__ == '__main__':
    app.run(debug=True)