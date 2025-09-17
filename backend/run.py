from app import createApp
from flask_cors import CORS

app = createApp()

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers="*")
#Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
if __name__ == "__main__":
    app.run(debug=True, port="8080")