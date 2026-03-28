import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Amplify } from "aws-amplify";
import { withAuthenticator } from "@aws-amplify/ui-react";
import "@aws-amplify/ui-react/styles.css";
import awsExports from "./aws-exports";
import liff from "@line/liff";

Amplify.configure(awsExports);

function Login({ signOut, user }) {
  const location = useLocation();
  const [opened, setOpened] = useState(false);

  useEffect(() => {
    if (!location.state?.data) {
      console.error("linkToken がありません。トップから開き直してください。");
      return;
    }
    const idtoken_jwt = user.signInUserSession.idToken.jwtToken;

    fetch(process.env.REACT_APP_NONCE_API, {
      method: "GET",
      mode: "cors",
      headers: {
        Authorization: idtoken_jwt,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const data_nonce = data.nonce;
        const data_linktoken = location.state.data;
        const redirect_url =
          "https://access.line.me/dialog/bot/accountLink?linkToken=" +
          encodeURIComponent(data_linktoken) +
          "&nonce=" +
          encodeURIComponent(data_nonce);
        setOpened(true);
        liff.openWindow({
          url: redirect_url,
          external: true,
        });
      })
      .catch((err) => console.error(err));
  }, [location.state, user.signInUserSession.idToken.jwtToken]);

  return (
    <div className="App">
      <h1>アカウント連携</h1>
      <h2>Please Wait...</h2>
      <button type="button" onClick={signOut}>
        Sign out
      </button>
      {opened ? <p>LINE 連携用の画面を開きました。</p> : null}
    </div>
  );
}

export default withAuthenticator(Login, {
  hideSignUp: true,
});
