#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, Request
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
api.add_resource(Restaurants, '/restaurants')





if __name__ == '__main__':
    app.run(port=5555)