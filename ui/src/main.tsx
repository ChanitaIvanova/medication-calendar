import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import routes from './Routes'
import { BrowserRouter as Router, RouterProvider, Link } from 'react-router-dom';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
     <RouterProvider router={routes} />
  </React.StrictMode>,
)
