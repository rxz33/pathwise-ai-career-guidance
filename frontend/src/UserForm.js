import React, { useState } from 'react';

const UserForm = () => {
  const [userInput, setUserInput] = useState({
    name: '',
    email: '',
    strengths: '',
    weaknesses: '',
    experience: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserInput({
      ...userInput,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Send user input to the FastAPI backend
    const response = await fetch('http://localhost:8000/submit-user-details', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userInput), // Send the form data as JSON
    });

    const data = await response.json();
    console.log('Response from backend:', data);

    // Handle the dynamic questions in the frontend (if needed)
    const dynamicQuestions = data.dynamic_questions;
    // You can display these dynamic questions to the user
    alert('Dynamic questions generated!');
    // You can use these questions to show them on your page
  };

  return (
    <div className="user-form">
      <h2>Enter Your Details</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={userInput.name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={userInput.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="strengths">Strengths</label>
          <input
            type="text"
            id="strengths"
            name="strengths"
            value={userInput.strengths}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="weaknesses">Weaknesses</label>
          <input
            type="text"
            id="weaknesses"
            name="weaknesses"
            value={userInput.weaknesses}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="experience">Experience</label>
          <input
            type="text"
            id="experience"
            name="experience"
            value={userInput.experience}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default UserForm;
