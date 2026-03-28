import { Amplify } from 'aws-amplify';

import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

import awsExports from './aws-exports';
Amplify.configure(awsExports);


function App({ signOut, user }) {

  return (
    <>
      <h1>Hello {user.username}</h1>
      <p>ID トークンは画面に表示していません（公開リポジトリ用）。</p>

      <button onClick={signOut}>Sign out</button>
    </>
  );

}

export default withAuthenticator(App,{
  hideSignUp : true
})