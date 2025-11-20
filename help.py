text = {
    "jp": 
    """# ロールを作るbot
スラッシュコマンドでロールを作るDiscord botです。
ロールの色をRGBや16進数カラーコードで指定できるのが一つの強みです。もちろんDiscord標準の色を設定することも可能です。
**ロールを作成したり、削除したり、ロールの色を変更することが誰でもできるようになる**botですので、悪意を持ってロールをめちゃくちゃにする人のいない、身内のサーバーでの使用を想定しています。

## bot導入時の注意
Discordの仕様で、Discordのロール設定画面にて **変更を行いたいロールよりも、このbotのロールが上に並んでいない限り** 「権限がありません。」というエラーが発生する。
なので、サーバーにこのbotを導入した際に、このbotのロールを設定画面内で上方に並べ替えるようにしてください。

## 使い方
### ロールを作る
**`/makerole`**コマンドを使用し、`rolename`の引数に作成したいロールの名前を入れる。`mentionable`の引数をはいにするとロールのメンションが可能になる。`give`の引数をはいにすると`member`の引数で指定したメンバーにロールを付与する。
### ロールの色を変える
- **`/changecolor`**コマンドを使用し、`role`の引数で色を変えたいロールを選択して実行する。次に任意の色に対応したボタンをクリックする。
- **`/changehexcolor`**コマンドを使用し、`role`の引数で色を変えたいロールを選択し、`hex_color`の引数に16進数カラーコードを入れて実行する。
- **`/changergb`**コマンドを使用し、`role`の引数で色を変えたいロールを選択し、`R`、`G`、`B`の引数にRGBのそれぞれの値を入れて実行する。
### ロールの名前を変える
- **`/changerolename`**コマンドを使用し、`role`の引数に名前を変更したいロール、`new_name`の引数に新しいロール名を入れて実行する。
### ロールを付与・除去する
- **`/grantrole`**コマンドを使用し、`role`の引数に付与したいロール、`member`引数に付与したいメンバーをいれ、実行してロールを付与する。
- **`/removerole`**コマンドを使用し、`role`の引数に除去したいロール、`member`引数にロールを除去したいメンバーをいれ、実行してロールを除去する。
### ロールの順位を変更する（botより下位のロールに限り有効）
- **`/movetoprole`**コマンドを使用し、`role`の引数で指定されたロールを可能な限り上の順位に移動する。

## 故障かな？と思ったら
このbotは私の家にあるRaspberry Pi 4の上にホストしています。うちのブレーカーが落ちたりすると当然botも使えなくなります。そしたらなるべく早く対処しようとは思っていますので、少し待っててください。また、たまにプログラムの更新・入れ替えなどでbotを止めることもあります。これもそんなに長く止めるわけじゃないので、少し待っててください。あんまりにも長かったら、以下の連絡先にでも凸してください。完全に挙動がおかしい！このページをちゃんと読み込んでも全然ダメ！という時も、以下の連絡先に凸してください。

### 連絡先（機能追加などの要望も）
X
https://x.com/insane_catt

### GitHubリポジトリ
https://github.com/insane-catt/Makerole_bot
""",
    "en": 
    """# Makerole_bot
This is a Discord bot that allows you to create roles using slash commands.
One of its strengths is the ability to specify role colors using RGB or hexadecimal color codes. Of course, it is also possible to set standard Discord colors.
This is a bot that **allows anyone to create, delete, and change the color of roles,** so it is intended for use within a private server where malicious users will not mess up the roles.

## Things to watch out for when setting up a bot
Due to Discord's specifications, an "Insufficient permissions." error will occur on the Discord role settings screen unless the role of this bot is placed above the role you wish to modify.
Therefore, when introducing this bot to your server, please rearrange the bot's role to be higher up in the settings screen.

## How to use
### Creating Roles
Use the **`/makerole`** command, and put the name of the role you want to create in the `rolename` argument. If you set the `mentionable` argument to yes, the role will be mentionable. If you set the `give` argument to yes, the role will be assigned to the member specified in the `member` argument.
### Changing Role Colors
- Use the **`/changecolor`** command, select the role you want to change the color of with the `role` argument, and execute it. Then click the button corresponding to the desired color.
- Use the **`/changehexcolor`** command, select the role you want to change the color of with the `role` argument, and execute it by entering the hexadecimal color code in the `hex_color` argument.
- Use the **`/changergb`** command, select the role you want to change the color of with the `role` argument, and execute it by entering the respective R, G, and B values in the `R`, `G`, and `B` arguments.
### Changing Role Names
- Use the **`/changerolename`** command, specifying the role whose name you want to change in the `role` argument and entering the new role name in the `new_name` argument, then execute it.
### Granting and Removing Roles
- Use the **`/grantrole`** command, specifying the role you want to grant in the `role` argument and the member you want to grant it to in the `member` argument, then execute it to grant the role.
- Use the **`/removerole`** command, specifying the role you want to remove in the `role` argument and the member you want to remove the role from in the `member` argument, then execute it to remove the role.
### Reorder Roles (Only effective for roles lower than the bot)
- Use the **`/movetoprole`** command and move the role specified by the `role` argument to the highest possible position.

## Thinking it might be broken?
This bot is hosted on a Raspberry Pi 4 at my home. If the circuit breaker trips, the bot will naturally go down. I will try to address it as soon as possible, so please wait a bit. Also, sometimes the bot will be stopped for program updates or replacements. This won't take too long, so please wait a bit. If it takes too long, please contact me at the following address. If the bot is behaving completely abnormally and reading this page doesn't help at all, please contact me at the following address.

### Contact
X
https://x.com/insane_catt

### GitHub Repository
https://github.com/insane-catt/Makerole_bot
"""
}