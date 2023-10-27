#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Pizza, Restaurant, RestaurantPizza
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db,render_as_batch=True)

db.init_app(app)
api = Api(app)
CORS(app)


class Restaurants(Resource):

    def get(self):

        response_dict_list = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response


class RestaurantById(Resource):
    def get(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            restaurant_data = restaurant.to_dict()
            response = make_response(
                jsonify(restaurant_data),
                200,
            )
        else:
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404,
            )
        return response
    
    def delete(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:

            RestaurantPizza.query.filter_by(restaurant_id=restaurant_id).delete()

            db.session.delete(restaurant)
            db.session.commit()
            return make_response('', 204)
        else:
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404
            )
            return response
        
class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizza_data = [pizza.to_dict() for pizza in pizzas]
        response = make_response(
            jsonify(pizza_data),
            200,
        )
        return response
    

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")

        if price is None or pizza_id is None or restaurant_id is None:
            response = make_response(
                jsonify({"errors": ["validation errors"]}),
                400
            )
            return response
        
        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            response = make_response(
                jsonify({"errors": ["validation errors"]}),
                400
            )
            return response
        
        restaurant_pizza = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id,
        )

        db.session.add(restaurant_pizza)
        db.session.commit()


        pizza_data = pizza.to_dict()
        response = make_response(
            jsonify(pizza_data),
            201,  
        )
        return response
            
api.add_resource(Restaurants, '/restaurants', endpoint='restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:restaurant_id>')
api.add_resource(Pizzas, '/pizzas', endpoint='pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas', endpoint='restaurant_pizzas')




if __name__ == '__main__':
    app.run(port=5555)