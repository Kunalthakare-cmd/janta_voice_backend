from flask import Flask
from flask_cors import CORS
from .routes.complaints import complaints_bp


app = Flask(__name__)
CORS(app)

# Register complaint route
app.register_blueprint(complaints_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
