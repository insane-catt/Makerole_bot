# Makerole_bot
 スラッシュコマンドでロールを作るDiscord botです。<br>
 ロールを作成したり、ロールの色を変更することが誰でもできるようになるbotですので、悪意を持ってロールをめちゃくちゃにする人のいない、身内のサーバーでの使用を想定しています。

## 導入
**![招待リンク](https://discord.com/oauth2/authorize?client_id=1230900199698726975)** <br>
↑これをクリックして導入する

## 使い方
### ロールを作る
1. ロールを作り、自分に付与する場合<br>
「/makerole」コマンドを使用し、rolenameの値に作成したいロールの名前を入れる。giveをはいにすると自分にもそのロールを付与する。
1. ロールを作るのみ、自分にはそのロールを付与しない場合<br>
giveのところをいいえにするだけ
### ロールの色を変える
- 「/changecolor」コマンドを使用し、rolenameの値に色を変えたいロールの名前を入れて実行する。次に任意の色に対応したボタンをクリックする。<br><br>
*注意：* Discordの仕様で、Discordのロール設定画面にて **色を変更したいロールよりも、このbotのロールが上に並んでいない限り** 「ロールの色を変更する権限がありません。」というエラーが発生する。<br>
サーバーにこのbotを導入した際など（/changecolorコマンドを使用するより前）に、このbotのロールを設定画面の上方に並べ替えるようにすればこのエラーは発生しない。

## 故障かな？と思ったら
このbotは私の家にあるRaspberry Pi 4の上にホストしています。うちのブレーカーが落ちたりすると当然botも使えなくなります。そしたらなるべく早く対処しようとは思っていますので、少し待っててください。また、たまにプログラムの更新・入れ替えなどでbotを止めることもあります。これもそんなに長く止めるわけじゃないので、少し待っててください。あんまりにも長かったら、以下の連絡先にでも凸してください。完全に挙動がおかしい！このページをちゃんと読み込んでも全然ダメ！という時も、以下の連絡先に凸してください。

### 連絡先（機能追加などの要望も）
Twitter（X笑）
https://twitter.com/insane_catt

DMまでどうぞ

## バージョン履歴
- v1.1.0 Embedの導入、/changecolorコマンドの追加
- v1.0.0
