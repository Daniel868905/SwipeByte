import "./shims/fetch";
import { installLogoutIntercept } from "./logout-intercept";
installLogoutIntercept("/api/v1/users");
import "./urlfix.js";
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
