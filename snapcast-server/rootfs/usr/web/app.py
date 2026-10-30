import os

from flask import Flask, jsonify, render_template, request

import eq

app = Flask(__name__)

PORT = int(os.environ.get("EQ_WEB_PORT", 1706))


@app.route("/")
def index():
    """Render the main page of the web interface."""
    return render_template("index.html")


@app.route("/api/state")
def api_state():
    """Return the current state of the equalizer."""
    return jsonify(eq.state_for_web())


@app.route("/api/apply")
def api_apply():
    """Apply the current equalizer settings."""
    enabled = request.args.get("enabled") == "1"
    bands = request.args.get("bands", "")
    gain = request.args.get("gain", "0")
    try:
        active = eq.apply(enabled, bands, gain)
    except eq.ApplyError as err:
        return jsonify({"ok": False, "error": str(err)}), 400
    return jsonify({"ok": True, "active": active})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
