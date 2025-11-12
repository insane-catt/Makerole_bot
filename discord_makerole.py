# version 1.2.4

# 最初の設定
from config import TOKEN, LANG
import discord
from discord import app_commands
from discord.ui import Button, View
import os
from PIL import ImageColor
from datetime import datetime, timedelta
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# 翻訳
from languages import dictionary
def tr(text):
    if LANG == "jp":
        # 日本語の場合はそのまま返す
        return text
    else:
        try:
            return dictionary[LANG][text]
        except KeyError:
            return "Sorry, translation into English failed. Displaying message in Japanese: " + text
    
# bot名の確認
async def daily_task():
    await client.wait_until_ready()
    while not client.is_closed():
        print(f"このbotは{client.user.name}です")
        await client.change_presence(activity=discord.Game(name=f"{len(client.guilds)}" + tr("つのサーバーで稼働中")))
        now = datetime.now()
        # 翌日の0時を計算
        next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        sleep_time = (next_run - now).total_seconds()
        await asyncio.sleep(sleep_time)


# ボタンの処理
class ColorButton(Button):
    def __init__(self, label, r, g, b, role_id: int):
        super().__init__(label=label, style=discord.ButtonStyle.gray)
        self.r = r
        self.g = g
        self.b = b
        self.role_id = role_id
        self.clicked = False

    async def callback(self, interaction: discord.Interaction):
        if not self.clicked:
            self.clicked = True
            role_obj = interaction.guild.get_role(self.role_id)
            if role_obj:
                try:
                    await role_obj.edit(color=discord.Color.from_rgb(self.r, self.g, self.b))
                    embed = discord.Embed(
                        title=tr("ロールの色を変更しました"),
                        color=0x00ff00,
                        description=tr("変更されたロール：") + f"{role_obj.mention}\n" + f"```rgb({self.r}, {self.g}, {self.b})``` "
                    )
                    await interaction.response.send_message(embed=embed)
                except discord.errors.Forbidden:
                    embed = discord.Embed(
                        title=tr("エラー"),
                        color=0xff0000,
                        description=tr("このbotに次のロールの色を変更する権限がありません: ") + f"{role_obj.mention}\n" + tr("このbotのロールを一番上に設定するなどして、権限の調整を行ってから、再度試してみてください。")
                    )
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title=tr("エラー"),
                    color=0xff0000,
                    description=tr("次のロールが存在しません: ") + tr("色選択をする直前に削除されたものと思われます。")
                    )
                await interaction.response.send_message(embed=embed)
            self.disabled = True
            self.view.stop()

class ColorView(View):
    def __init__(self, role: discord.Role):
        super().__init__()
        role_id = role.id
        self.add_item(ColorButton("A1", 26, 188, 156, role_id))
        self.add_item(ColorButton("A2", 46, 204, 113, role_id))
        self.add_item(ColorButton("A3", 52, 152, 219, role_id))
        self.add_item(ColorButton("A4", 155, 89, 182, role_id))
        self.add_item(ColorButton("A5", 233, 30, 99, role_id))
        self.add_item(ColorButton("A6", 241, 196, 15, role_id))
        self.add_item(ColorButton("A7", 230, 126, 34, role_id))
        self.add_item(ColorButton("A8", 231, 76, 60, role_id))
        self.add_item(ColorButton("A9", 149, 165, 166, role_id))
        self.add_item(ColorButton("A10", 96, 125, 139, role_id))
        self.add_item(ColorButton("B1", 17, 128, 106, role_id))
        self.add_item(ColorButton("B2", 31, 139, 76, role_id))
        self.add_item(ColorButton("B3", 32, 102, 148, role_id))
        self.add_item(ColorButton("B4", 113, 54, 138, role_id))
        self.add_item(ColorButton("B5", 173, 20, 87, role_id))
        self.add_item(ColorButton("B6", 194, 124, 14, role_id))
        self.add_item(ColorButton("B7", 168, 67, 0, role_id))
        self.add_item(ColorButton("B8", 153, 45, 34, role_id))
        self.add_item(ColorButton("B9", 151, 156, 159, role_id))
        self.add_item(ColorButton("B10", 84, 110, 122, role_id))

# changecolorコマンド
@tree.command(name="changecolor", description=tr("ロールの色を変更します"))
@app_commands.describe(
    role=tr("色を変更するロールを選択してください")
)
async def changecolor(interaction: discord.Interaction, role: discord.Role):
    if role:
        file_path = os.path.join(os.path.dirname(__file__), "discord_rolecolors_edit.png")
        file = discord.File(file_path, filename="discord_rolecolors_edit.png")
        embed = discord.Embed(
            title=tr("ロールの色を変更します"),
            color=0x00ff00,
            description=tr("以下から色を選択してください")
        )
        embed.set_image(url="attachment://discord_rolecolors_edit.png")
        await interaction.response.send_message(file=file, embed=embed, view=ColorView(role))
    else:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("ロールが存在しません。")
            )
        await interaction.response.send_message(embed=embed)

# changergbコマンド
@tree.command(name="changergb", description=tr("ロールの色をRGBで指定して変更します"))
@app_commands.describe(
    role=tr("色を変更するロールを選択してください"),
    r=tr("赤の値 (0-255)"),
    g=tr("緑の値 (0-255)"),
    b=tr("青の値 (0-255)")
)
async def changergb(interaction: discord.Interaction, role: discord.Role, r: int, g: int, b: int):
    if role:
        try:
            await role.edit(color=discord.Color.from_rgb(r, g, b))
            embed = discord.Embed(
                title=tr("ロールの色を変更しました"),
                color=0x00ff00,
                description=tr("変更されたロール：") + f"{role.mention}\n" + f"```rgb({r}, {g}, {b})```"
            )
            await interaction.response.send_message(embed=embed)
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title=tr("エラー"),
                color=0xff0000,
                description=tr("このbotに次のロールの色を変更する権限がありません: ") + f"{role.mention}\n" + tr("このbotのロールを一番上に設定するなどして、権限の調整を行ってから、再度試してみてください。")
            )
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("ロールが存在しません。")
        )
        await interaction.response.send_message(embed=embed)

# changehexcolorコマンド
@tree.command(name="changehexcolor", description=tr("ロールの色を16進数カラーコードで指定して変更します"))
@app_commands.describe(
    role=tr("色を変更するロールを選択してください"),
    hex_color=tr("16進数カラーコード (例: #ff5733)")
)
async def changehexcolor(interaction: discord.Interaction, role: discord.Role, hex_color: str):
    if role:
        try:
            # 16進数カラーコードをRGBに変換
            rgb = ImageColor.getcolor(hex_color, "RGB")
            await role.edit(color=discord.Color.from_rgb(*rgb))
            embed = discord.Embed(
                title=tr("ロールの色を変更しました"),
                color=0x00ff00,
                description=tr("変更されたロール：") + f"{role.mention}\n" + f"```{hex_color}```" + "\n" + f"```rgb{rgb}```"
            )
            await interaction.response.send_message(embed=embed)
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title=tr("エラー"),
                color=0xff0000,
                description=tr("このbotに次のロールの色を変更する権限がありません: ") + f"{role.mention}\n" + tr("このbotのロールを一番上に設定するなどして、権限の調整を行ってから、再度試してみてください。")
            )
            await interaction.response.send_message(embed=embed)
        except ValueError:
            embed = discord.Embed(
                title=tr("エラー"),
                color=0xff0000,
                description=tr("無効な16進数カラーコードです: ") + f"**{hex_color}**"
            )
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("ロールが存在しません。")
        )
        await interaction.response.send_message(embed=embed)

# grantroleコマンド
@tree.command(name="grantrole", description=tr("指定したロールを指定したメンバーに付与します"))
@app_commands.describe(
    role=tr("付与するロール"),
    member=tr("付与するメンバー (省略するとあなた自身)")
)
async def grantrole(interaction: discord.Interaction, role: discord.Role, member: discord.Member = None):
    guild = interaction.guild
    if not guild:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("サーバー内でのみ使用できるコマンドです。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    target = member if member else interaction.user

    # 外部サービス管理ロールは付与できない
    if role.managed:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このロールは外部サービスによって管理されているため付与できません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 対象が既にロールを持っているか
    if role in target.roles:
        embed = discord.Embed(title=tr("情報"), color=0xffa500, description=tr("このメンバーは既にそのロールを持っています。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Bot がそのロールを操作できるか（位置チェック）
    bot_member = guild.me
    if bot_member and bot_member.top_role.position <= role.position:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("このbotはそのロールを付与する権限がありません。サーバー内のロールの順位を確認してください。")
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 付与処理（実行者の権限は問わない）
    try:
        await target.add_roles(role, reason=f"Granted by {interaction.user} via /grantrole")
        embed = discord.Embed(
            title=tr("ロールを付与しました"),
            color=0x00ff00,
            description=tr("付与されたロール: ") + f"{role.mention}\n" + tr("次のユーザーに付与しました: ") + f"{target.mention}"
        )
        await interaction.response.send_message(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("このbotはそのロールを付与する権限がありません。サーバー内のロールの順位を確認してください。")
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("ロール付与中にエラーが発生しました: ") + str(e)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# removeroleコマンド
@tree.command(name="removerole", description=tr("指定したメンバーから指定したロールを除去します"))
@app_commands.describe(
    role=tr("除去するロール"),
    member=tr("対象メンバー (省略するとあなた自身)")
)
async def removerole(interaction: discord.Interaction, role: discord.Role, member: discord.Member = None):
    guild = interaction.guild
    if not guild:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("サーバー内でのみ使用できるコマンドです。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    target = member if member else interaction.user

    # 外部サービス管理ロールは除去できない
    if role.managed:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このロールは外部サービスによって管理されているため除去できません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 対象がそのロールを持っているか
    if role not in target.roles:
        embed = discord.Embed(title=tr("情報"), color=0xffa500, description=tr("このメンバーはそのロールを持っていません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 除去処理（実行者の権限は問わない）
    try:
        await target.remove_roles(role, reason=f"Removed by {interaction.user} via /removerole")
        embed = discord.Embed(
            title=tr("ロールを除去しました"),
            color=0x00ff00,
            description=tr("除去されたロール: ") + f"{role.mention}\n" + tr("対象ユーザー: ") + f"{target.mention}"
        )
        await interaction.response.send_message(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("このbotはそのロールを除去する権限がありません。サーバー内のロールの順位を確認してください。")
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("ロール除去中にエラーが発生しました: ") + str(e)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# makeroleコマンド
@tree.command(name="makerole", description=tr("ロールを作成します"))
@app_commands.describe(
    rolename=tr("ロール名"),
    give=tr("そのロールを付与する"),
    mentionable=tr("ロールをメンション可能にする"),
    member=tr("付与するメンバー (省略するとあなた自身)")
)
@app_commands.choices(
    give=[
        discord.app_commands.Choice(name=tr("はい"), value=1),
        discord.app_commands.Choice(name=tr("いいえ"), value=0)
    ],
    mentionable=[
        discord.app_commands.Choice(name=tr("はい"), value=1),
        discord.app_commands.Choice(name=tr("いいえ"), value=0)
    ]
)
async def makerole(interaction: discord.Interaction, rolename: str, give: int, mentionable: int, member: discord.Member = None):
    guild = interaction.guild
    existing_role = discord.utils.get(guild.roles, name=rolename)
    if existing_role:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("次のロールは既に存在します: ") + f"**{rolename}**"
            )
        await interaction.response.send_message(embed=embed)
    else:
        new_role = await guild.create_role(name=rolename, mentionable=bool(mentionable))
        # 付与処理
        if bool(give):
            target = member if member else interaction.user
            try:
                await target.add_roles(new_role)
                give_text = "\n" + tr("次のユーザーに付与しました: ") + f"{target.mention}"
            except discord.errors.Forbidden:
                give_text = "\n" + tr("ロールの付与に失敗しました。") + "\n" + tr("このbotのロールを一番上に設定するなどして、権限の調整を行ってから、再度試してみてください。")
        else:
            give_text = "\n" + tr("このロールはこの時点ではどのユーザーにも付与していません。")
        # mentionable 表示
        if bool(mentionable):
            mentionable_text = "\n" + tr("このロールはメンションできます。")
        else:
            mentionable_text = "\n" + tr("このロールはメンションできません。")
        embed = discord.Embed(
            title=tr("ロールを作成しました"),
            color=0x00ff00,
            description=tr("作成されたロール: ") + f"**{rolename}**" + give_text + mentionable_text
            )
        await interaction.response.send_message(embed=embed)

# 以下はテスト用のコマンド
'''
@tree.command(name="hello", description="Hello, world!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}!')
'''

# ログイン
@client.event
async def on_ready():
    await tree.sync()
    print("login complete")
    client.loop.create_task(daily_task())

client.run(TOKEN)