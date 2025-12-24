from flask import Flask, jsonify, send_from_directory, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "../backend/spikealert.db"  # path to your SQLite DB from frontend
VIS_DIR = "visualizations"            # folder with chart HTML files

# Serve visualization HTML files
@app.route('/visualizations/<filename>')
def get_visualization(filename):
    return send_from_directory(VIS_DIR, filename)

# API endpoint for dropdown options
@app.route('/api/options')
def get_options():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT commodity FROM commodity_prices")
    commodities = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT market FROM commodity_prices")
    markets = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT state FROM commodity_prices")
    states = [row[0] for row in cursor.fetchall()]

    conn.close()
    return jsonify({"commodities": commodities, "markets": markets, "states": states})

# Optional filtered visualization API (future)
@app.route('/api/filter')
def filter_data():
    commodity = request.args.get("commodity", "all")
    market = request.args.get("market", "all")
    state = request.args.get("state", "all")
    # Implement logic to filter charts based on selections if needed
    return jsonify({"status": "ok"})

# Serve index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run()
