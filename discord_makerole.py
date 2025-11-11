# version 1.2.3

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
    def __init__(self, label, r, g, b, role):
        super().__init__(label=label, style=discord.ButtonStyle.gray)
        self.r = r
        self.g = g
        self.b = b
        self.role = role
        self.clicked = False

    async def callback(self, interaction: discord.Interaction):
        if not self.clicked:
            self.clicked = True
            role_obj = discord.utils.get(interaction.guild.roles, name=self.role)
            if role_obj:
                try:
                    await role_obj.edit(color=discord.Color.from_rgb(self.r, self.g, self.b))
                    embed = discord.Embed(
                        title=tr("ロールの色を変更しました"),
                        color=0x00ff00,
                        description=tr("変更されたロール：") + f"**{self.role}**\n" + f"```rgb({self.r}, {self.g}, {self.b})``` "
                    )
                    await interaction.response.send_message(embed=embed)
                except discord.errors.Forbidden:
                    embed = discord.Embed(
                        title=tr("エラー"),
                        color=0xff0000,
                        description=tr("このbotに次のロールの色を変更する権限がありません: ") + f"**{self.role}**\n" + tr("このbotのロールを一番上に設定するなどして、権限の調整を行ってから、再度試してみてください。")
                    )
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title=tr("エラー"),
                    color=0xff0000,
                    description=tr("次のロールが存在しません: ") + f"**{self.role}**\n" + tr("色選択をする直前に削除されたものと思われます。")
                    )
                await interaction.response.send_message(embed=embed)
            self.disabled = True
            self.view.stop()

class ColorView(View):
    def __init__(self, role):
        super().__init__()
        self.add_item(ColorButton("A1", 26, 188, 156, role))
        self.add_item(ColorButton("A2", 46, 204, 113, role))
        self.add_item(ColorButton("A3", 52, 152, 219, role))
        self.add_item(ColorButton("A4", 155, 89, 182, role))
        self.add_item(ColorButton("A5", 233, 30, 99, role))
        self.add_item(ColorButton("A6", 241, 196, 15, role))
        self.add_item(ColorButton("A7", 230, 126, 34, role))
        self.add_item(ColorButton("A8", 231, 76, 60, role))
        self.add_item(ColorButton("A9", 149, 165, 166, role))
        self.add_item(ColorButton("A10", 96, 125, 139, role))
        self.add_item(ColorButton("B1", 17, 128, 106, role))
        self.add_item(ColorButton("B2", 31, 139, 76, role))
        self.add_item(ColorButton("B3", 32, 102, 148, role))
        self.add_item(ColorButton("B4", 113, 54, 138, role))
        self.add_item(ColorButton("B5", 173, 20, 87, role))
        self.add_item(ColorButton("B6", 194, 124, 14, role))
        self.add_item(ColorButton("B7", 168, 67, 0, role))
        self.add_item(ColorButton("B8", 153, 45, 34, role))
        self.add_item(ColorButton("B9", 151, 156, 159, role))
        self.add_item(ColorButton("B10", 84, 110, 122, role))

# changecolorコマンド
@tree.command(name="changecolor", description=tr("ロールの色を変更します"))
@app_commands.describe(rolename=tr("色を変更するロールの名前"))
async def changecolor(interaction: discord.Interaction, rolename: str):
    role_obj = discord.utils.get(interaction.guild.roles, name=rolename)
    if role_obj:
        file_path = os.path.join(os.path.dirname(__file__), "discord_rolecolors_edit.png")
        file = discord.File(file_path, filename="discord_rolecolors_edit.png")
        embed = discord.Embed(
            title=tr("ロールの色を変更します"),
            color=0x00ff00,
            description=tr("以下から色を選択してください")
        )
        embed.set_image(url="attachment://discord_rolecolors_edit.png")
        await interaction.response.send_message(file=file, embed=embed, view=ColorView(rolename))
    else:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("次のロールが存在しません: ") + f"**{rolename}**"
            )
        await interaction.response.send_message(embed=embed)

# changergbコマンド
@tree.command(name="changergb", description=tr("ロールの色をRGBで指定して変更します"))
@app_commands.describe(
    rolename=tr("色を変更するロールの名前"),
    r=tr("赤の値 (0-255)"),
    g=tr("緑の値 (0-255)"),
    b=tr("青の値 (0-255)")
)
async def changergb(interaction: discord.Interaction, rolename: str, r: int, g: int, b: int):
    role_obj = discord.utils.get(interaction.guild.roles, name=rolename)
    if role_obj:
        try:
            await role_obj.edit(color=discord.Color.from_rgb(r, g, b))
            embed = discord.Embed(
                title=tr("ロールの色を変更しました"),
                color=0x00ff00,
                description=tr("変更されたロール：") + f"**{rolename}**\n" + f"```rgb({r}, {g}, {b})```"
            )
            await interaction.response.send_message(embed=embed)
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title=tr("エラー"),
                color=0xff0000,
                description=tr("このbotに次のロールの色を変更する権限がありません: ") + f"**{rolename}**\n" + tr("このbotのロールを一番上に設定するなどして、権限の調整を行ってから、再度試してみてください。")
            )
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title=tr("エラー"),
            color=0xff0000,
            description=tr("次のロールが存在しません: ") + f"**{rolename}**"
        )
        await interaction.response.send_message(embed=embed)

# changehexcolorコマンド
@tree.command(name="changehexcolor", description=tr("ロールの色を16進数カラーコードで指定して変更します"))
@app_commands.describe(
    rolename=tr("色を変更するロールの名前"),
    hex_color=tr("16進数カラーコード (例: #ff5733)")
)
async def changehexcolor(interaction: discord.Interaction, rolename: str, hex_color: str):
    role_obj = discord.utils.get(interaction.guild.roles, name=rolename)
    if role_obj:
        try:
            # 16進数カラーコードをRGBに変換
            rgb = ImageColor.getcolor(hex_color, "RGB")
            await role_obj.edit(color=discord.Color.from_rgb(*rgb))
            embed = discord.Embed(
                title=tr("ロールの色を変更しました"),
                color=0x00ff00,
                description=tr("変更されたロール：") + f"**{rolename}**\n" + f"```{hex_color}```" + "\n" + f"```rgb{rgb}```"
            )
            await interaction.response.send_message(embed=embed)
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title=tr("エラー"),
                color=0xff0000,
                description=tr("このbotに次のロールの色を変更する権限がありません: ") + f"**{rolename}**\n" + tr("このbotのロールを一番上に設定するなどして、権限の調整を行ってから、再度試してみてください。")
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
            description=tr("次のロールが存在しません: ") + f"**{rolename}**"
        )
        await interaction.response.send_message(embed=embed)

# makeroleコマンド
@tree.command(name="makerole", description=tr("ロールを作成します"))
@app_commands.describe(
    rolename=tr("ロール名"),
    give=tr("そのロールを付与する"),
    mentionable=tr("ロールをメンション可能にする")
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
async def makerole(interaction: discord.Interaction, rolename: str, give: int, mentionable: int):
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
        new_role = await guild.create_role(name=rolename, mentionable=mentionable)
        def give_or_not(give):
            if bool(give):
                return "\n" + tr("次のユーザーに付与しました: ") + f"{interaction.user.mention}"
            else:
                return "\n" + tr("このロールはこの時点ではどのユーザーにも付与していません。")
        def mentionable_or_not(mentionable):
            if bool(mentionable):
                return "\n" + tr("このロールはメンションできます。")
            else:
                return "\n" + tr("このロールはメンションできません。")
        if bool(give): 
            await interaction.user.add_roles(new_role)
        embed = discord.Embed(
            title=tr("ロールを作成しました"),
            color=0x00ff00,
            description=tr("作成されたロール: ") + f"**{rolename}**" + give_or_not(give) + mentionable_or_not(mentionable)
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