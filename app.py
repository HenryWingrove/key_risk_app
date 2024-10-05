from flask import Flask, render_template, request, jsonify
from geopy.distance import geodesic
import math

app = Flask(__name__)

def estimate_search_time(home_coords, lost_coords, housing_density, time_per_house=30, max_radius=5000, step=100):

    distance = geodesic(home_coords, lost_coords).meters

    housing_density_per_m2 = housing_density / 1_000_000

    total_time = 0
    found = False

    for radius in range(step, max_radius + step, step):
        area_of_ring = math.pi * (((radius)**2) - ((radius - step)**2))
        houses_in_ring = area_of_ring * housing_density_per_m2
        time_to_check_ring = houses_in_ring * time_per_house
        total_time += time_to_check_ring
        if distance <= radius:
            found = True
            break

    if not found:
        total_time = "House not found within maximum search radius."

    return total_time, distance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_risk', methods=['POST'])
def calculate_risk():
    data = request.json
    home_coords = (data['home_lat'], data['home_lon'])
    lost_coords = (data['lost_lat'], data['lost_lon'])

    housing_density = 3000  

    estimated_time, distance = estimate_search_time(home_coords, lost_coords, housing_density)

    if distance < 100:
        risk_score = 0.9
    elif distance < 1000:
        risk_score = 0.5
    else:
        risk_score = 0.1

    return jsonify({
        'distance': distance,
        'risk_score': risk_score,
        'estimated_time': estimated_time  
    })

if __name__ == '__main__':
    app.run(debug=True)