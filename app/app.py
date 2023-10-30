#!/usr/bin/env python3

# Import required Flask modules
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Pizza, Restaurant, RestaurantPizza  # Import your SQLAlchemy models
from flask_cors import CORS
from flask_restful import Api, Resource

# Create a Flask application
app = Flask(__name__)

# Configure the Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Use SQLite as the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db, render_as_batch=True)  # Initialize the database migration

# Initialize the SQLAlchemy database with the Flask application
db.init_app(app)

# Create an instance of Flask-RESTful API
api = Api(app)

# Enable Cross-Origin Resource Sharing (CORS) to allow cross-origin requests
CORS(app)

# Define a resource for handling restaurant-related operations
class Restaurants(Resource):
    def get(self):
        # Retrieve a list of restaurants and convert them to a dictionary
        response_dict_list = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

        # Create a JSON response with the list of restaurants
        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

# Define a resource for handling restaurant by ID operations
class RestaurantById(Resource):
    def get(self, restaurant_id):
        # Retrieve a restaurant by its ID
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            # If the restaurant exists, convert it to a dictionary
            restaurant_data = restaurant.to_dict()
            response = make_response(
                jsonify(restaurant_data),
                200,
            )
        else:
            # If the restaurant is not found, return a 404 error response
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404,
            )
        return response

    def delete(self, restaurant_id):
        # Retrieve a restaurant by its ID
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            # Delete related RestaurantPizza entries and then delete the restaurant
            RestaurantPizza.query.filter_by(restaurant_id=restaurant_id).delete()
            db.session.delete(restaurant)
            db.session.commit()
            return make_response('', 204)
        else:
            # If the restaurant is not found, return a 404 error response
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404
            )
            return response

# Define a resource for handling pizza-related operations
class Pizzas(Resource):
    def get(self):
        # Retrieve a list of pizzas and convert them to a dictionary
        pizzas = Pizza.query.all()
        pizza_data = [pizza.to_dict() for pizza in pizzas]
        response = make_response(
            jsonify(pizza_data),
            200,
        )
        return response

# Define a resource for creating restaurant-pizza relationships
class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")

        if price is None or pizza_id is None or restaurant_id is None:
            # Handle validation errors and return a 400 error response
            response = make_response(
                jsonify({"errors": ["validation errors"]}),
                400
            )
            return response

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            # Handle validation errors and return a 400 error response
            response = make_response(
                jsonify({"errors": ["validation errors"]}),
                400
            )
            return response

        # Create a new RestaurantPizza entry with the provided data
        restaurant_pizza = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id,
        )

        db.session.add(restaurant_pizza)
        db.session.commit()

        # Convert the associated pizza to a dictionary for the response
        pizza_data = pizza.to_dict()
        response = make_response(
            jsonify(pizza_data),
            201,
        )
        return response

# Add resources and endpoints to the Flask-RESTful API
api.add_resource(Restaurants, '/restaurants', endpoint='restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:restaurant_id>')
api.add_resource(Pizzas, '/pizzas', endpoint='pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas', endpoint='restaurant_pizzas')

# Run the Flask application on port 5555 if this script is the main entry point
if __name__ == '__main__':
    app.run(port=5555)
