# version 1.0.0


# 最初の設定
import config
TOKEN = config.TOKEN

import discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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
        discord.app_commands.Choice(name="はい",value="True"),
        discord.app_commands.Choice(name="いいえ",value="False")
    ]
)
async def makerole(interaction: discord.Interaction, rolename: str, give: str):
    guild = interaction.guild
    existing_role = discord.utils.get(guild.roles, name=rolename)
    if existing_role:
        await interaction.response.send_message(f'**{rolename}** というロールは既に存在するため、新しく作成できませんでした。')
    else:
        new_role = await guild.create_role(name=rolename)
        if give == 'True':
            await interaction.user.add_roles(new_role)
            await interaction.response.send_message(f"ロール「**{rolename}**」を作成し、{interaction.user.mention}に付与しました。")
        else:
            await interaction.response.send_message(f"ロール「**{rolename}**」を作成しました。")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="ロールを作ります"))
    await tree.sync()
    print("login complete")

client.run(TOKEN)