import React from 'react';
const Header = () => {
  return (
    <header className="fixed top-0 left-0 w-full px-8 py-4 z-50 flex items-center justify-between">
      <h1 className="text-xxl font-bold text-indigo-600">ShortsyAI</h1>
      <nav className="flex space-x-6 text-gray-700">
        <a href="#">About us</a>
        <a href="#">Advantages</a>
        <a href="#">Product options</a>
        <a href="#">Platforms</a>
        <a href="#">Statistics</a>
      </nav>
      <button className="bg-black text-white rounded-full px-4 py-2 shadow-md">
        Try it now
      </button>
    </header>
  );
};

export default Header;

