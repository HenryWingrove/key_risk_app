from flask import Flask, render_template, request, jsonify
from geopy.distance import geodesic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Serves the HTML page

@app.route('/calculate_risk', methods=['POST'])
def calculate_risk():
    data = request.json
    home_coords = (data['home_lat'], data['home_lon'])
    lost_coords = (data['lost_lat'], data['lost_lon'])

    # Calculate the distance between home and lost key location
    distance = geodesic(home_coords, lost_coords).meters

    # Example risk score based on distance
    if distance < 100:  # Less than 100 meters
        risk_score = 0.9
    elif distance < 1000:  # Between 100 meters and 1 km
        risk_score = 0.5
    else:
        risk_score = 0.1

    return jsonify({'distance': distance, 'risk_score': risk_score})

if __name__ == '__main__':
    app.run(debug=True)