# SVNtoTeams
TortoiseSVNのコミット情報をTeamsに送信するツールです。

Teamsの任意のチャンネルにて"Incoming Webhook"というコネクタの接続、
<br/>本アプリをWindowsスケジューラー等で定期実行する
<br/>ことでコミットメッセージを自動でTeamsへ送信することが出来ます。

## Setting.json
「setting.json」の設定は下記となります。
- {project name}：SVNのURL記載のプロジェクト名を設定してください。
- {notification title}：Teamsへ投稿する際のタイトルを設定してください。
- {svn project URL}：コミットメッセージを取得する、SVNのURLを設定してください。
- {teams web hook URL}：Incomng Webhookにて取得したURLを設定してください。
- {Revision No}：最新のRevisionNoを設定してください。この番号以降のコミットを取得します。

```json
﻿{
    "{project name}": {
        "tag": "{project name}",
        "name": "{notification title}",
        "svnurl": "{svn project URL}",
        "teamswebhookurl": "{teams web hook URL}",
        "lastRevNo": {Revision No}
    }
}
```
※複数プロジェクトを指定可能です。


<br/>通知は下記のように表示されます。
<br/>※情報保護のため一部伏せてあります。

<img width="50%" src="https://github.com/cotoro-lab/SVNtoTeams/assets/76488848/039b4be4-a791-47f6-bc8f-cac8d2b2d360">

