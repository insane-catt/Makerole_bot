# ロールを作るbot
スラッシュコマンドでロールを作るDiscord botです。<br>
ロールの色をRGBや16進数カラーコードで指定できるのが一つの強みです。もちろんDiscord標準の色を設定することも可能です。<br>
ロールを作成したり、ロールの色を変更することが誰でもできるようになるbotですので、悪意を持ってロールをめちゃくちゃにする人のいない、身内のサーバーでの使用を想定しています。

# Makerole_bot
This is a Discord bot that allows you to create roles using slash commands.<br>
One of its strengths is the ability to specify role colors using RGB or hexadecimal color codes. Of course, it is also possible to set standard Discord colors.<br>
It is designed for use in private servers where everyone can create and change role colors, assuming there are no malicious users who would mess up the roles.

## 導入
**[日本語招待リンク](https://discord.com/oauth2/authorize?client_id=1230900199698726975)** <br>
↑これをクリックして導入できますが、今開いてるタブの中で開いてしまうので、新規タブで開くなどしてください。新規タブで開くようにGitHubでは設定できないらしいです！

## Installation
**[English Invite link](https://discord.com/oauth2/authorize?client_id=1344138056487145613)** <br>
Clicking this link will open it in the current tab, so please open it in a new tab. It seems that GitHub cannot be set to open in a new tab!

## bot導入時の注意 Things to watch out for when setting up a bot
Discordの仕様で、Discordのロール設定画面にて **変更を行いたいロールよりも、このbotのロールが上に並んでいない限り** 「権限がありません。」というエラーが発生する。<br>
なので、サーバーにこのbotを導入した際に、このbotのロールを設定画面内で上方に並べ替えるようにしてください。
Due to Discord's specifications, an "Insufficient permissions." error will occur on the Discord role settings screen unless the role of this bot is placed above the role you wish to modify.<br>
Therefore, when introducing this bot to your server, please rearrange the bot's role to be higher up in the settings screen.

## 使い方 How to use
### ロールを作る
`/makerole`コマンドを使用し、`rolename`の引数に作成したいロールの名前を入れる。`mentionable`の引数をはいにするとロールのメンションが可能になる。<br>
`give`の引数をはいにすると`member`の引数で指定したメンバーにロールを付与する。

### Creating Roles
Use the `/makerole` command, and put the name of the role you want to create in the `rolename` argument. If you set the `mentionable` argument to yes, the role will be mentionable.<br>
If you set the `give` argument to yes, the role will be assigned to the member specified in the `member` argument.

### ロールの色を変える
- `/changecolor`コマンドを使用し、`role`の引数で色を変えたいロールを選択して実行する。次に任意の色に対応したボタンをクリックする。
- `/changehexcolor`コマンドを使用し、`role`の引数で色を変えたいロールを選択し、`hex_color`の引数に16進数カラーコードを入れて実行する。
- `/changergb`コマンドを使用し、`role`の引数で色を変えたいロールを選択し、`R`、`G`、`B`の引数にRGBのそれぞれの値を入れて実行する。

### Changing Role Colors
- Use the `/changecolor` command, select the role you want to change the color of with the `role` argument, and execute it. Then click the button corresponding to the desired color.
- Use the `/changehexcolor` command, select the role you want to change the color of with the `role` argument, and execute it by entering the hexadecimal color code in the `hex_color` argument.
- Use the `/changergb` command, select the role you want to change the color of with the `role` argument, and execute it by entering the respective R, G, and B values in the `R`, `G`, and `B` arguments.

### ロールを付与・除去する
- `/grantrole`コマンドを使用し、`role`の引数に付与したいロール、`member`引数に付与したいメンバーをいれ、実行してロールを付与する。
- `/removerole`コマンドを使用し、`role`の引数に除去したいロール、`member`引数にロールを除去したいメンバーをいれ、実行してロールを除去する。

### Granting and Removing Roles
- Use the `/grantrole` command, specifying the role you want to grant in the `role` argument and the member you want to grant it to in the `member` argument, then execute it to grant the role.
- Use the `/removerole` command, specifying the role you want to remove in the `role` argument and the member you want to remove the role from in the `member` argument, then execute it to remove the role.

## 故障かな？と思ったら
このbotは私の家にあるRaspberry Pi 4の上にホストしています。うちのブレーカーが落ちたりすると当然botも使えなくなります。そしたらなるべく早く対処しようとは思っていますので、少し待っててください。また、たまにプログラムの更新・入れ替えなどでbotを止めることもあります。これもそんなに長く止めるわけじゃないので、少し待っててください。あんまりにも長かったら、以下の連絡先にでも凸してください。完全に挙動がおかしい！このページをちゃんと読み込んでも全然ダメ！という時も、以下の連絡先に凸してください。

## Thinking it might be broken?
This bot is hosted on a Raspberry Pi 4 at my home. If the circuit breaker trips, the bot will naturally go down. I will try to address it as soon as possible, so please wait a bit. Also, sometimes the bot will be stopped for program updates or replacements. This won't take too long, so please wait a bit. If it takes too long, please contact me at the following address. If the bot is behaving completely abnormally and reading this page doesn't help at all, please contact me at the following address.

### 連絡先・Contact（機能追加などの要望も）
X<br>
https://x.com/insane_catt

DMまでどうぞ
Feel free to DM me.

## バージョン履歴
- v1.2.7 helpにGitHubリポジトリのリンクを追加
- v1.2.6 READMEとhelpに文を追加
- v1.2.5 /grantroleコマンド、/removeroleコマンド、/deleterolefromguildコマンド、/helpコマンドを追加、/changecolorコマンドの改善
- v1.2.4 コマンドをより使いやすくした
- v1.2.3 翻訳動作の改善
- v1.2.2 細かな改善
- v1.2.1 2025年8月12日 バグ修正など
- v1.2 英語版の追加、/changergbコマンド、/changehexcolorコマンドの追加
- v1.1.2 色選択の際のロール消滅時の動作改善
- v1.1.1 /serverusageコマンドの実装、スクリプトの整理(笑)
- v1.1.0 Embedの導入、/changecolorコマンドの追加
- v1.0.0

## Version History
- v1.2.7 Add the GitHub repository link to help.
- v1.2.6 Add sentences to README and help.
- v1.2.5 Added /grantrole command, /removerole command, /deleterolefromguild command, /help command, and improved /changecolor command.
- v1.2.4 Made the command easier to use.
- v1.2.3 Improved translation behavior
- v1.2.2 Minor improvements
- v1.2.1 August 12, 2025 Bug fixes and improvements
- v1.2 Added English version, added /changergb command, added /changehexcolor command
- v1.1.2 Improved behavior when role disappears during color selection
- v1.1.1 Implemented /serverusage command, cleaned up script (lol)
- v1.1.0 Introduced Embed, added /changecolor command
- v1.0.0
