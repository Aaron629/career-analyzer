import React from "react";
import UserForm from "./UserForm"; // 確保路徑正確
import './App.css';   // App 專用樣式

function App() {
  return (
    <div className="app-container">
      <div className="main-content">
        <h1 className="text-cyber app-title">CYBER SYSTEM</h1>
        <UserForm onSubmit={(data) => console.log(data)} />
      </div>
    </div>
  );
}

export default App;