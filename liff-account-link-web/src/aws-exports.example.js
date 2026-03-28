/* eslint-disable */
// aws-exports.js としてコピーし、Amplify Console / amplify pull の値を設定してください。
// 本ファイルはリポジトリに含め、実値の aws-exports.js は .gitignore します。

const awsmobile = {
  aws_project_region: "ap-northeast-1",
  aws_cognito_identity_pool_id: "ap-northeast-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  aws_cognito_region: "ap-northeast-1",
  aws_user_pools_id: "ap-northeast-1_XXXXXXXXX",
  aws_user_pools_web_client_id: "xxxxxxxxxxxxxxxxxxxxxxxxxx",
  oauth: {},
  aws_cognito_social_providers: [],
  aws_cognito_mfa_configuration: "OFF",
  aws_cognito_password_protection_settings: {
    passwordPolicyMinLength: 8,
    passwordPolicyCharacters: [],
  },
};

export default awsmobile;
