# liff-gps-map-web

## これは何か

**LINE LIFF** でログインし、バックエンド API から取得した **GPS 履歴（複数ポイント）** を **Google Maps（@react-google-maps/api）** 上にマーカー表示する **React** アプリです。  
車両トラッキング構想のうち、「リッチメニューから地図を開く」部分のイメージに近いサンプルです。

## 使っているもの

- React 18、Create React App（`react-scripts` 5）
- `@line/liff`
- `@react-google-maps/api`、`react-spinners`

## ホスティングの想定

- LIFF エンドポイント用に **HTTPS の静的ホスティング**。
- Google Maps の利用には **Maps JavaScript API キー**（`.env`）が必要です。キーには **HTTP リファラー制限** などを推奨します。

## 環境変数

`.env.example` を `.env` にコピーします。

| 変数 | 用途 |
|------|------|
| `REACT_APP_LIFF_ID` | LIFF ID |
| `REACT_APP_MAP_API` | 位置情報 JSON を返すバックエンド（POST、本文に LINE アクセストークン等） |
| `REACT_APP_GOOGLE_MAP_KEY` | Google Maps JavaScript API キー |

## 起動

```bash
npm install
npm start
```

## 注意

- API キーやトークンを **リポジトリに含めない**でください。
- 地図の読み込みには `REACT_APP_GOOGLE_MAP_KEY` が必須です。
