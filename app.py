from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from scrape import get_weather

app = Flask(__name__)
api = Api(app)

# Route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Resource to handle GET requests with location data
class GetWeather(Resource):
    def get(self):
            data = request.args.to_dict()  # Extract all query parameters as a dictionary
            # Validate required parameters
            if not all(key in data for key in ('latitude','longitude')):
                return jsonify({
                    "status": "error",
                    "message": "Please provide 'latitude', and 'longitude' as query parameters."
                }), 400
            
            # Fetch weather data
            weather_data = get_weather(float(data['latitude']),float(data['longitude']))
            
            return jsonify({
                "status": "success",
                "weather_data": weather_data,
            })

# Adding the resource to the API
api.add_resource(GetWeather, '/get_weather')

if __name__ == '__main__':
    app.run(debug=True,threaded=True,port=5000,host="localhost")
