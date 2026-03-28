# liff-account-link-web

## これは何か

**LINE LIFF** で取得したアクセストークンをバックエンドに送り、**アカウント連携用の linkToken** を受け取ったあと、**Amazon Cognito（Amplify）でログイン**し、ID トークンを使って **nonce を返す API** を呼び出し、**LINE のアカウント連携 URL** へ誘導する流れをまとめた **React** アプリです。

バックエンド（API Gateway + Lambda 等）は **別リポジトリ／別デプロイ** を想定しています。

## 使っているもの

- React 18、Create React App（`react-scripts` 2 系 ※古め）
- `@line/liff`
- `aws-amplify` / `@aws-amplify/ui-react`、`react-router-dom`
- **yarn**（`yarn.lock` あり）

## ホスティングの想定

- **LIFF アプリのエンドポイント URL** に、ビルド後の静的サイト（例: Amplify Hosting、S3+CloudFront、Vercel 等）を指定します。
- バックエンド API の CORS に、そのオリジンを許可してください。

## 環境変数

`.env.example` を `.env` にコピーして埋めます。

| 変数 | 用途 |
|------|------|
| `REACT_APP_LIFF_ID` | LINE Developers の LIFF ID |
| `REACT_APP_ACCOUNT_LINK_API` | LINE トークン検証・linkToken 発行 API |
| `REACT_APP_NONCE_API` | Cognito の **ID トークン**を `Authorization` に載せ、nonce を返す API |

任意: ローカル検証用に `REACT_APP_DEMO_ACCES_TOKEN` を設定し、`App.jsx` 内のコメントに従って body を差し替え。

## Amplify 設定

`src/aws-exports.example.js` を `src/aws-exports.js` にコピーし、実値を設定してください（`aws-exports.js` は `.gitignore` 対象）。

## 起動

```bash
yarn install
yarn start
```

## 注意

- **チャネルアクセストークンやユーザーのアクセストークンを画面に表示しない**でください。
- 本番の LIFF では **HTTPS** のエンドポイントが必要です。
