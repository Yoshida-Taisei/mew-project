# SigfoxとLIFF(LINE)を利用した車両トラッキングデバイス構想(mew-project)
LINE Developers Communityで発表したプロダクトです。
https://linedevelopercommunity.connpass.com/event/275767/

## 詳細Qiita記事
詳細な背景はこちらを参照してください。
https://qiita.com/taiyyytai/items/c006b35cd2e23973c76c

### 概要
![overview](overview.png)

### アーキテクチャ
![overview_architecture](overview_architecture.png)

## 含まれるプロジェクト

| ディレクトリ | 内容 |
|--------------|------|
| `amplify-cognito-login-web` | **Amazon Cognito（Amplify Auth）** によるログイン画面のみの最小サンプル。 |
| `liff-account-link-web` | **LIFF** から連携用トークン取得 → **Cognito + アカウント連携** フロー。 |
| `liff-line-link-cognito-web` | LIFF + トークン検証 API + **Cognito 設定を環境変数で注入**する版。 |
| `liff-gps-map-web` | LIFF + バックエンドから GPS 履歴取得 + **Google Maps** 表示。 |

## 推奨環境

- **Node.js 20.x**（ルートの `.nvmrc` 参照）
- パッケージマネージャはプロジェクトごとに **npm または yarn** が混在しています。各 README に従ってください。

## ライセンス

`LICENSE`（MIT）を参照してください。
