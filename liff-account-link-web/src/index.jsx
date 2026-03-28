/* LIFF アプリのエントリ（ルーティング） */
import React from "react";
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Conf from './conf';
import Login from "./Login";
import App from "./App";
import Thank from "./Thank";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
     <Routes>
      <Route path="/" element={<App/>}/>
        <Route path="conf" element={<Conf />} />
        <Route path="login" element={<Login />}/>
        <Route path="thank" element={<Thank />}/>
     </Routes>
  </BrowserRouter>
);
