import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import liff from "@line/liff";
import "./App.css";
import { parseLambdaBody } from "./lib/api";

function App() {
  const navigate = useNavigate();

  useEffect(() => {
    liff.init({ liffId: process.env.REACT_APP_LIFF_ID }).then(() => {
      const line_accesstoken = liff.getAccessToken();
      const body = JSON.stringify({ access_token: line_accesstoken });
      // ローカル検証のみ: .env の REACT_APP_DEMO_ACCES_TOKEN を設定し、上記を差し替え可

      fetch(process.env.REACT_APP_VALID_TOKEN_API, {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
        body,
      })
        .then((response) => response.json())
        .then((data) => {
          const parsed = parseLambdaBody(data);
          const data_linkToken = parsed?.linkToken ?? parsed?.body?.linkToken;
          liff.ready.then(() => {
            setTimeout(() => {
              navigate("/login", { state: { data: data_linkToken } });
            }, 3000);
          });
        })
        .catch((err) => console.error(err));
    });
  }, [navigate]);

  return (
    <div className="App">
      <h1>Please Wait...</h1>
      <footer>ver 0.1</footer>
    </div>
  );
}

export default App;
