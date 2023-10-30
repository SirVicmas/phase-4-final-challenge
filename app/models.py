from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# Create a SQLAlchemy database instance
db = SQLAlchemy()

# Define the Restaurant model
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    # Define fields in the Restaurant table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # Define a relationship between Restaurant and RestaurantPizza, allowing you to access pizzas for a restaurant
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')

    def __repr__(self):
        return f'<Restaurant {self.name}>'

    # Serialization rules for this model to control what data is included in JSON responses
    serialize_rules = ('-restaurant_pizzas.restaurant', )

# Define the Pizza model
class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    # Define fields in the Pizza table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # Define a relationship between Pizza and RestaurantPizza, allowing you to access restaurants serving the pizza
    pizza_restaurant = db.relationship('RestaurantPizza', backref='pizza')

    def __repr__(self):
        return f'<Pizza {self.name}'

    # Serialization rules for this model to control what data is included in JSON responses
    serialize_rules = ('-pizza_restaurant.pizza', )

# Define the RestaurantPizza model
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    # Define fields in the RestaurantPizza table
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    # Constructor to initialize a RestaurantPizza instance
    def __init__(self, price, restaurant_id, pizza_id):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        self.price = price
        self.restaurant_id = restaurant_id
        self.pizza_id = pizza_id

    def __repr__(self):
        return f'<RestaurantPizza {self.price} at Restaurant {self.restaurant_id} for Pizza {self.pizza_id}'

    # Serialization rules for this model to control what data is included in JSON responses
    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.pizza_restaurant', )
