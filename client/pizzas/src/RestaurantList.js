import React, { useState, useEffect } from 'react';
import axios from 'axios';

function RestaurantList() {
  // Define a state variable 'restaurants' and a function 'setRestaurants' to update it
  const [restaurants, setRestaurants] = useState([]);

  // Use the 'useEffect' hook to make an API request when the component is mounted
  useEffect(() => {
    axios.get('http://localhost:5555/restaurants') // Make a GET request to the API endpoint
      .then((response) => {
        // Update the 'restaurants' state with the data received from the API response
        setRestaurants(response.data);
      })
      .catch((error) => {
        // Handle any errors that occur during the API request
        console.error('Error:', error);
      });
  }, []); // The empty dependency array ensures this effect runs only once, on component mount

  return (
    <div className="restaurant-list">
      <h2>Restaurant List</h2>
      <ul>
        {/* Map through the 'restaurants' array and display each restaurant's name */}
        {restaurants.map((restaurant) => (
          <li key={restaurant.id}>{restaurant.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default RestaurantList;
