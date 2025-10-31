from posit_sdk import ConnectServer
import os

# Connect to Posit Connect
connect = ConnectServer(
    url=os.getenv("CONNECT_SERVER"),
    api_key=os.getenv("CONNECT_API_KEY")
)

# Path to your local repo
app_dir = os.path.abspath(".")  # deploys current folder
app_name = "My GitHub Python App"

# Deploy app
app = connect.content.deploy(
    app_dir=app_dir,
    name=app_name,
    publish=True,
    environment_type="conda"  # uses conda-env.yml if present
)

# Optional: set environment variables for the app
connect.content.set_environment(
    guid=app.guid,
    environment={
        "EXAMPLE_VAR": "value",
        "PYTHON_VERSION": "3.12"
    }
)

print(f"App deployed! GUID: {app.guid}")
print(f"URL: {app.content_url}")
