import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import "../src/styles/styles.scss";
import { AuthProvider } from "./contexts/AuthProvider";
import { BrowserRouter, Routes, Route } from "react-router-dom"

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path='/*' element = {<App />}/>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
)
