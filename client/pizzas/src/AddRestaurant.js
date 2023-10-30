import React, { useState } from 'react';
import axios from 'axios';

function AddRestaurant() {
  const [newRestaurantName, setNewRestaurantName] = useState('');

  const handleRestaurantNameChange = (e) => {
    setNewRestaurantName(e.target.value);
  };

  const handleAddRestaurant = () => {
    const data = { name: newRestaurantName };

    axios.post('http://localhost:5555/restaurants', data)
      .then((response) => {
        // Handle the response (newly added restaurant) here
        console.log('New Restaurant:', response.data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <h2>Add a Restaurant</h2>
      <input
        type="text"
        placeholder="Restaurant Name"
        value={newRestaurantName}
        onChange={handleRestaurantNameChange}
      />
      <button onClick={handleAddRestaurant}>Add Restaurant</button>
    </div>
  );
}

export default AddRestaurant;
