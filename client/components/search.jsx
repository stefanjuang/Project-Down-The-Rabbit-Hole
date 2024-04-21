"use client";

import React, { useState } from 'react';
import axios from 'axios';
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

const SearchComponent = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting query:', query);
    try {
      const response = await axios.post('http://127.0.0.1:8000/searchUsrTweets', {query});

      const data = response.data;
      console.log('Response data:', data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center bg-gray-200 p-2 rounded-lg">
      <Input
        type="text"
        value={query}
        onChange={handleInputChange}
        placeholder="Enter something..."
        className="flex-1 mr-2"
      />
      <button type="submit" className="text-gray-500 hover:text-gray-700">
        <Search size={20} />
      </button>
    </form>
  );
};

export default SearchComponent;
