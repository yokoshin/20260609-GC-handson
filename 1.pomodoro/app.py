from flask import Flask, render_template, request, jsonify
from services.settings_manager import SettingsManager

app = Flask(__name__)
settings_manager = SettingsManager()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/settings", methods=["GET"])
def get_settings():
    """Get current user settings."""
    settings = settings_manager.load()
    return jsonify(settings.to_dict())


@app.route("/api/settings", methods=["POST"])
def update_settings():
    """Update user settings."""
    data = request.get_json()
    if data is None:
        data = {}
    
    try:
        if data:
            updated_settings = settings_manager.update(**data)
        else:
            updated_settings = settings_manager.load()
        return jsonify(updated_settings.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)

