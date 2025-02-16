import logo from './logo.svg';
import React from 'react';
import './App.css';
import AuthComponent from './AuthComponent'; // Import the AuthComponent

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Welcome to the Banking System</h1>
                <AuthComponent /> {/* Use the AuthComponent here */}
            </header>
        </div>
    );
}

export default App;