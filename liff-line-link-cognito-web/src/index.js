/* LIFF + Cognito 連携アプリのエントリ（ルーティング） */
import React from "react";
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from "./Login";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
     <Routes>
      <Route path="/" element={<App/>}/>
        <Route path="login" element={<Login />}/>
     </Routes>
  </BrowserRouter>
);
