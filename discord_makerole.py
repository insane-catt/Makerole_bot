# version 1.1.0

# 最初の設定
import config
import discord
from discord import app_commands
from discord.ui import Button, View
import os

TOKEN = config.TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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
                        title="ロールの色を変更しました",
                        color=0x00ff00,
                        description=f"{self.role} の色を rgb({self.r}, {self.g}, {self.b}) に変更しました。"
                    )
                    await interaction.response.send_message(embed=embed)
                except discord.errors.Forbidden:
                    embed = discord.Embed(
                        title="エラー",
                        color=0xff0000,
                        description=f"ロール **{self.role}** の色を変更する権限がありません。このbotのロールを一番上に設定するなどして、権限の調整を行ってから、再度試してみてください。"
                    )
                    await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"{self.role} というロールは存在しません。")
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

# ロールの色を変更
@tree.command(name="changecolor", description="ロールの色を変更します")
@app_commands.describe(rolename="色を変更するロールの名前")
async def changecolor(interaction: discord.Interaction, rolename: str):
    role_obj = discord.utils.get(interaction.guild.roles, name=rolename)
    if role_obj:
        file_path = os.path.join(os.path.dirname(__file__), "discord_rolecolors_edit.png")
        file = discord.File(file_path, filename="discord_rolecolors_edit.png")
        embed = discord.Embed(
            title="ロールの色を変更します",
            color=0x00ff00,
            description="以下から色を選択してください"
        )
        embed.set_image(url="attachment://discord_rolecolors_edit.png")
        await interaction.response.send_message(file=file, embed=embed, view=ColorView(rolename))
    else:
        embed = discord.Embed(
            title="エラー",
            color=0xff0000,
            description=f"**{rolename}** というロールは存在しません。"
            )
        await interaction.response.send_message(embed=embed)

# 以下はテスト用のコマンド
'''
@tree.command(name="hello", description="Hello, world!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}!')
'''

# 以下スクリプト
@tree.command(name="makerole", description="ロールを作成します。")
@app_commands.describe(rolename='ロール名', give='そのロールを付与する')
@app_commands.choices(
    give=[
        discord.app_commands.Choice(name="はい", value="True"),
        discord.app_commands.Choice(name="いいえ", value="False")
    ]
)
async def makerole(interaction: discord.Interaction, rolename: str, give: str):
    guild = interaction.guild
    existing_role = discord.utils.get(guild.roles, name=rolename)
    if existing_role:
        embed = discord.Embed(
            title="エラー",
            color=0xff0000,
            description=f'**{rolename}** というロールは既に存在するため、新しく作成できませんでした。'
            )
        await interaction.response.send_message(embed=embed)
    else:
        new_role = await guild.create_role(name=rolename)
        if give == 'True':
            await interaction.user.add_roles(new_role)
            embed = discord.Embed(
                title="ロールを作成しました",
                color=0x00ff00,
                description=f"ロール **{rolename}** を作成し、{interaction.user.mention}に付与しました。"
                )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="ロールを作成しました",
                color=0x00ff00,
                description=f"ロール **{rolename}** を作成しました。"
                )
            await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="ロールを作ります"))
    await tree.sync()
    print("login complete")

client.run(TOKEN)