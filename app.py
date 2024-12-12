from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from scrape import fetch_weather

app = Flask(__name__)
api = Api(app)

# Route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Resource to handle GET requests with location data
class GetWeather(Resource):
    def get(self):
        city = request.args.get('city', 'Unknown City')
        state = request.args.get('state', 'Unknown State')
        pincode = request.args.get('pincode', 'Unknown Pincode')

        weather_data = fetch_weather(city,state,pincode,unit_fix=True)
        # Return a JSON response
        return jsonify({
            "status": "success",
            "weather_data": weather_data,
        })

# Adding the resource to the API
api.add_resource(GetWeather, '/get_weather')

if __name__ == '__main__':
    app.run(debug=True,threaded=True,port=5000,host="localhost")
