from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os


app = Flask(__name__)
CORS(app)  # allow frontend calls

# ✅ Database connection config (read from environment variables for Docker Compose)
db_config = {
    "host": os.getenv("MYSQL_HOST", "db"),          # service name of MySQL container
    "port": int(os.getenv("MYSQL_PORT", 3306)),     # default MySQL port
    "user": os.getenv("MYSQL_USER", "stockuser"),
    "password": os.getenv("MYSQL_PASSWORD", "stockpass"),
    "database": os.getenv("MYSQL_DATABASE", "stocks")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# ✅ Fetch all stock records
@app.route("/stocks", methods=["GET"])
def get_stocks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stocks;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Moving average rule (last 3 days → tomorrow’s predicted price)
def moving_average(prices, window=3):
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window

# ✅ Rule-based prediction endpoint
@app.route("/predict", methods=["GET"])
def predict():
    ticker = request.args.get("ticker", "AAPL").upper()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT price FROM stocks
            WHERE ticker = %s
            ORDER BY date DESC
            LIMIT 3;
        """, (ticker,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(rows) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        prices = [r[0] for r in rows][::-1]  # oldest → newest
        prediction = moving_average(prices)

        return jsonify({
            "ticker": ticker,
            "last_prices": prices,
            "predicted_price": round(prediction, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
