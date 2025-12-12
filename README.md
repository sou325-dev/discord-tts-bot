読み上げbot作った。
Pythonの`discord.py`で動かしてて、音声生成は VOICEVOX

 BOTの使い方は
 `!join` → BOTを自分のいるボイスチャンネルに呼べる
 `!leave` → BOTをVCから追い出せる
チャットにテキスト送ると自動で音声化してVCで再生してくれる
技術ポイントは
 VOICEVOXのAPIでテキストを音声に変換
 一時ファイルに保存して `FFmpegPCMAudio` で再生
 再生中でも次のメッセージが来たら上書き再生できる
 サーバーごとに接続状況を管理して複数サーバーでも安心

注意点は
VOICEVOXは自分のPCで起動しておく必要があるからね。
 再生後は一時ファイルを削除してるよ

引用はhttps://note.com/vyome/n/n13cd2eec7336
