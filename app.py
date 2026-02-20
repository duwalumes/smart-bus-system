from flask import Flask, render_template, request, jsonify
from math import radians, cos, sin, sqrt, atan2
import os

app = Flask(__name__)

# Store buses in memory
buses = {}

BUS_SPEED_KMH = 40  # average speed


# Distance calculation
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


@app.route("/")
def tracker():
    return render_template("tracker.html")


@app.route("/bus/<bus_id>")
def bus(bus_id):
    return render_template("bus.html", bus_id=bus_id)


@app.route("/update_location/<bus_id>", methods=["POST"])
def update_location(bus_id):
    data = request.json
    buses[bus_id] = data
    print(f"Bus {bus_id}:", data)
    return jsonify({"status": "updated"})


@app.route("/get_buses")
def get_buses():
    return jsonify(buses)


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    passenger = data["passenger"]
    bus = data["bus"]

    distance = calculate_distance(
        passenger["lat"], passenger["lng"],
        bus["lat"], bus["lng"]
    )

    eta_minutes = (distance / BUS_SPEED_KMH) * 60

    return jsonify({
        "distance_km": round(distance, 2),
        "eta_minutes": round(eta_minutes, 1)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
