# ロールを作るbot
スラッシュコマンドでロールを作るDiscord botです。<br>
ロールを作成したり、ロールの色を変更することが誰でもできるようになるbotですので、悪意を持ってロールをめちゃくちゃにする人のいない、身内のサーバーでの使用を想定しています。

# Role Creation Bot
This is a Discord bot that allows you to create roles using slash commands.<br>
It is designed for use in private servers where everyone can create and change role colors, assuming there are no malicious users who would mess up the roles.

## 導入
**[日本語招待リンク](https://discord.com/oauth2/authorize?client_id=1230900199698726975)** <br>
↑これをクリックして導入できますが、今開いてるタブの中で開いてしまうので、新規タブで開くなどしてください。新規タブで開くようにGitHubでは設定できないらしいです！

## Installation
**[English Invite link](https://discord.com/oauth2/authorize?client_id=1344138056487145613)** <br>
Clicking this link will open it in the current tab, so please open it in a new tab. It seems that GitHub cannot be set to open in a new tab!

## 使い方 How to use
### ロールを作る
1. ロールを作り、自分に付与する場合<br>
`/makerole`コマンドを使用し、`rolename`の引数に作成したいロールの名前を入れる。`give`をはいにすると自分にもそのロールを付与する。
1. ロールを作るのみ、自分にはそのロールを付与しない場合<br>
`give`のところをいいえにするだけ

### Creating Roles
1. To create a role and assign it to yourself<br>
Use the `/makerole` command and enter the name of the role you want to create in the `rolename` argument. If you set `give` to "Give", the role will also be assigned to you.
1. To create a role without assigning it to yourself<br>
Just set `give` to "Do not give".

### ロールの色を変える
- `/changecolor`コマンドを使用し、`rolename`の引数に色を変えたいロールの名前を入れて実行する。次に任意の色に対応したボタンをクリックする。
- `/changehexcolor`コマンドを使用し、`rolename`の引数に色を変えたいロールの名前を入れ、`hex_color`の引数に16進数カラーコードを入れて実行する。
- `/changergb`コマンドを使用し、`rolename`の引数に色を変えたいロールの名前を入れ、`R`、`G`、`B`の引数にRGBのそれぞれの値を入れて実行する。
<br><br>
*注意：* Discordの仕様で、Discordのロール設定画面にて **色を変更したいロールよりも、このbotのロールが上に並んでいない限り** 「ロールの色を変更する権限がありません。」というエラーが発生する。<br>
サーバーにこのbotを導入した際など（`/changecolor`コマンドを使用するより前）に、このbotのロールを設定画面の上方に並べ替えるようにすればこのエラーは発生しない。

### Changing Role Colors
- Use the `/changecolor` command and enter the name of the role you want to change the color of in the `rolename` argument, then execute it. Next, click the button corresponding to the desired color.
- Use the `/changehexcolor` command and enter the name of the role you want to change the color of in the `rolename` argument, and enter the hexadecimal color code in the `hex_color` argument, then execute it.
- Use the `/changergb` command and enter the name of the role you want to change the color of in the `rolename` argument, and enter the RGB values in the `R`, `G`, and `B` arguments, then execute it.
<br><br>
*Note:* Due to Discord's specifications, an error stating "You do not have permission to change the color of this role" will occur unless the bot's role is positioned above the role you want to change in the Discord role settings screen.<br>
To avoid this error, arrange the bot's role above the role you want to change in the settings screen before using the `/changecolor` command.

### `/serverusage`コマンドってなに？いる？
このbotがいくつのサーバーに入っているか作者が知りたいので付け足したコマンドです。

### What is the `/serverusage` command? Is it necessary?
This command was added so that the author can know how many servers this bot is in.

## 故障かな？と思ったら
このbotは私の家にあるRaspberry Pi 4の上にホストしています。うちのブレーカーが落ちたりすると当然botも使えなくなります。そしたらなるべく早く対処しようとは思っていますので、少し待っててください。また、たまにプログラムの更新・入れ替えなどでbotを止めることもあります。これもそんなに長く止めるわけじゃないので、少し待っててください。あんまりにも長かったら、以下の連絡先にでも凸してください。完全に挙動がおかしい！このページをちゃんと読み込んでも全然ダメ！という時も、以下の連絡先に凸してください。

## Troubleshooting
This bot is hosted on a Raspberry Pi 4 at my home. If the circuit breaker trips, the bot will naturally go down. I will try to address it as soon as possible, so please wait a bit. Also, sometimes the bot will be stopped for program updates or replacements. This won't take too long, so please wait a bit. If it takes too long, please contact me at the following address. If the bot is behaving completely abnormally and reading this page doesn't help at all, please contact me at the following address.

### 連絡先（機能追加などの要望も）
Xとかいうだっせえ名前のSNS<br>
https://x.com/insane_catt

DMまでどうぞ

### Contact (for feature requests, etc.)
A social network with a lame name called X<br>
https://x.com/insane_catt

Feel free to DM me.

## バージョン履歴
- v1.2.1 2025年8月12日 バグ修正など
- v1.2 英語版の追加、/changergbコマンド、/changehexcolorコマンドの追加
- v1.1.2 色選択の際のロール消滅時の動作改善
- v1.1.1 /serverusageコマンドの実装、スクリプトの整理(笑)
- v1.1.0 Embedの導入、/changecolorコマンドの追加
- v1.0.0

## Version History
- v1.2.1 August 12, 2025 Bug fixes and improvements
- v1.2 Added English version, added /changergb command, added /changehexcolor command
- v1.1.2 Improved behavior when role disappears during color selection
- v1.1.1 Implemented /serverusage command, cleaned up script (lol)
- v1.1.0 Introduced Embed, added /changecolor command
- v1.0.0
