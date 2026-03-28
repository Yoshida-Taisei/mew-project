# liff-line-link-cognito-web

## これは何か

`liff-account-link-web` に近い **LINE アカウント連携 + Cognito** の流れですが、Amplify の設定を **`aws-exports.js` ではなく環境変数**（Identity Pool / User Pool / リージョン）から読み込む版です。

1. LIFF でアクセストークンを取得  
2. **`REACT_APP_VALID_TOKEN_API`** で検証し linkToken を取得  
3. Cognito でログイン後、**`REACT_APP_ACCOUNT_LINK_API`** で nonce を取得し LINE 連携へ

## 使っているもの

- React 18、Create React App（`react-scripts` 5）
- `@line/liff`、`react-router-dom`
- `@aws-amplify/ui-react`（Auth 設定は `Login.jsx` 内の `Amplify.configure`）

## ホスティングの想定

LIFF の URL 先に静的ホスティング（Amplify Hosting、S3+CloudFront 等）を載せる想定です。

## 環境変数

`.env.example` を参照してください。Cognito 関連は **ユーザープール・ID プール・Web クライアント ID** を設定します。

## 起動

```bash
npm install
npm start
```

## 注意

- `.env` は **コミット禁止**。
- デバッグ用トークンはソースにベタ書きせず、必要なら `.env` の `REACT_APP_DEMO_ACCES_TOKEN` のみ利用してください。
