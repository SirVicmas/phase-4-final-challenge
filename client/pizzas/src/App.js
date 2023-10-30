import './App.css';
import React from 'react';
import { Routes, Route, Link } from 'react-router-dom'; // Import the necessary components from React Router v6
import RestaurantList from './RestaurantList';
import AddRestaurant from './AddRestaurant';

function App() {
  return (
    <div>
      <ul>
        <li>
          <Link to="/">Restaurant List</Link> {/* Create a link to the Restaurant List page */}
        </li>
        <li>
          <Link to="/add-restaurant">Add Restaurant</Link> {/* Create a link to the Add Restaurant page */}
        </li>
      </ul>

      <Routes> {/* Define the routes for your application */}
        <Route path="/" element={<RestaurantList />} /> {/* Define the route for the Restaurant List page */}
        <Route path="/add-restaurant" element={<AddRestaurant />} /> {/* Define the route for the Add Restaurant page */}
      </Routes>
    </div>
  );
}

export default App;
