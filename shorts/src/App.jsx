import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import "@fontsource/poppins/700.css"; // or 600/800

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100">
      <Navbar />
      <Hero />
    </div>
  );
}

export default App;
