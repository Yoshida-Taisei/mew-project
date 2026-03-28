# amplify-cognito-login-web

## これは何か

**AWS Amplify（Amazon Cognito ユーザープール）** でサインインする最小の **React（Create React App）** アプリです。  
LINE や LIFF は使わず、**ホストされた UI（`withAuthenticator`）** だけでログイン・サインアウトを試す用途向けです。

## 使っているもの

- React 18、Create React App（`react-scripts` 5）
- `aws-amplify` / `@aws-amplify/ui-react`

## ホスティングの想定

ビルド結果は静的ファイル（`npm run build` の `build/`）です。次のような場所に載せられます。

- **AWS Amplify Hosting**
- **Amazon S3 + CloudFront**
- その他の静的ホスティング

Cognito の **アプリクライアント設定** で、ホストするオリジンをコールバック URL に登録してください。

## セットアップ

1. **Node.js 20.x** 推奨（親ディレクトリの `.nvmrc` 参照）。
2. `src/aws-exports.example.js` を `src/aws-exports.js` にコピーし、**自分の Amplify / Cognito の値**で上書きするか、`amplify pull` で生成された `aws-exports.js` を置く。
3. 依存関係をインストール（このプロジェクトは **npm** の `package-lock.json` あり）。

```bash
npm install
npm start
```

## 注意

- **`src/aws-exports.js` は Git に含めない**運用にしてください（`.gitignore` 済み）。公開リポジトリにはプレースホルダの `aws-exports.example.js` のみ載せます。
- 画面上に **ID トークンを出さない**ようにしてあります（学習用でも漏洩リスクが高いため）。
