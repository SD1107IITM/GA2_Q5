from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "ak_svnm5z37mm49cfrrsn8pb1p2"
MY_EMAIL = "24f3002514@iitm.study.ac.in"  # <-- put your real email

@app.route("/analytics", methods=["POST"])
def analytics():
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json()
    events = data.get("events", [])

    total_events = len(events)
    unique_users = len(set(e["user"] for e in events))
    revenue = sum(e["amount"] for e in events if e["amount"] > 0)

    user_totals = {}
    for e in events:
        if e["amount"] > 0:
            user_totals[e["user"]] = user_totals.get(e["user"], 0) + e["amount"]

    top_user = max(user_totals, key=user_totals.get)

    return jsonify({
        "email": MY_EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
