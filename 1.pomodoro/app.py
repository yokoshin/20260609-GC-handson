from flask import Flask, render_template, request, jsonify
from services.settings_manager import SettingsManager
from models.settings import Settings

app = Flask(__name__)
settings_manager = SettingsManager()


def validate_settings_update(data):
    """Validate settings update data.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return True, None
    
    # Validate work_duration
    if 'work_duration' in data and data['work_duration'] not in Settings.VALID_WORK_DURATIONS:
        return False, f"Invalid work_duration. Must be one of {Settings.VALID_WORK_DURATIONS}"
    
    # Validate break_duration
    if 'break_duration' in data and data['break_duration'] not in Settings.VALID_BREAK_DURATIONS:
        return False, f"Invalid break_duration. Must be one of {Settings.VALID_BREAK_DURATIONS}"
    
    # Validate theme
    if 'theme' in data and data['theme'] not in Settings.VALID_THEMES:
        return False, f"Invalid theme. Must be one of {Settings.VALID_THEMES}"
    
    return True, None


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
        # Validate the update
        is_valid, error_msg = validate_settings_update(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        if data:
            updated_settings = settings_manager.update(**data)
        else:
            updated_settings = settings_manager.load()
        return jsonify(updated_settings.to_dict())
    except (ValueError, KeyError, TypeError):
        return jsonify({"error": "Invalid settings data"}), 400


if __name__ == "__main__":
    app.run(debug=True)

