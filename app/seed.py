from app import app, db, Restaurant, Pizza, RestaurantPizza
from faker import Faker

# Create a Flask app context
with app.app_context():
    # Create or update the database schema
    db.create_all()

    # Initialize the Faker object
    fake = Faker()

    # Seed data for restaurants
    restaurants_data = []

    for _ in range(10):  # Generate 10 random restaurants
        restaurant_info = {
            "name": fake.company(),
            "address": fake.address(),
        }
        restaurants_data.append(restaurant_info)

    for restaurant_info in restaurants_data:
        restaurant = Restaurant(**restaurant_info)
        db.session.add(restaurant)

    # Seed data for pizzas
    pizzas_data = []

    for _ in range(10):  # Generate 10 random pizzas
        pizza_info = {
            "name": fake.word(),
            "ingredients": fake.sentence(),
        }
        pizzas_data.append(pizza_info)

    for pizza_info in pizzas_data:
        pizza = Pizza(**pizza_info)
        db.session.add(pizza)

    # Seed data for restaurant pizzas
    restaurant_pizzas_data = []

    for _ in range(20):  # Generate 20 random restaurant pizzas
        restaurant_pizza_info = {
            "price": fake.random_int(min=5, max=20),
            "restaurant_id": fake.random_element(elements=range(1, 11)),
            "pizza_id": fake.random_element(elements=range(1, 11)),
        }
        restaurant_pizzas_data.append(restaurant_pizza_info)

    for restaurant_pizza_info in restaurant_pizzas_data:
        restaurant_pizza = RestaurantPizza(**restaurant_pizza_info)
        db.session.add(restaurant_pizza)

    # Commit the changes to the database
    db.session.commit()

# The context will be automatically popped when the `with` block exits

print("Database seeded successfully.")
