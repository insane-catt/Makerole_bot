# version 1.2.9

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

            # ボタンを無効化してメッセージを更新（UI に反映）
            for item in self.view.children:
                item.disabled = True
            try:
                # 元のメッセージの view を編集して無効化を反映
                if interaction.message:
                    await interaction.message.edit(view=self.view)
            except Exception:
                pass

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

        # キャンセルボタンを最後に追加（B10 の下に表示されます）
        cancel_button = Button(label=tr("キャンセル"), style=discord.ButtonStyle.secondary)
        async def cancel_callback(interaction: discord.Interaction):
            for item in self.children:
                item.disabled = True
            try:
                await interaction.response.edit_message(view=self)
            except Exception:
                try:
                    await interaction.message.edit(view=self)
                except Exception:
                    pass
            try:
                embed = discord.Embed(
                    description=tr("色選択をキャンセルしました。")
                )
                await interaction.followup.send(embed=embed)
            except Exception:
                pass
            self.stop()
        cancel_button.callback = cancel_callback
        self.add_item(cancel_button)

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

# movetoproleコマンド
@tree.command(name="movetoprole", description=tr("選択したロールを可能な限り上の順位に移動します"))
@app_commands.describe(
    role=tr("移動するロールを選択してください")
)
async def movetoprole(interaction: discord.Interaction, role: discord.Role):
    guild = interaction.guild
    if not guild:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("サーバー内でのみ使用できるコマンドです。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    if role is None:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("ロールが見つかりません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # @everyone は移動不可
    if role == guild.default_role:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("@everyone ロールは移動できません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 外部サービス管理ロールは移動不可
    if role.managed:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このロールは外部サービスによって管理されているため移動できません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    bot_member = guild.me
    if bot_member is None:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このサーバーでのbot情報が取得できませんでした。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Bot に manage_roles が必要
    if not bot_member.guild_permissions.manage_roles:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このbotにロールを管理する権限(manage_roles)がありません。botの権限を確認してください。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Bot の役職より上に移動できない
    if bot_member.top_role.position <= role.position:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このbotはそのロールを上に移動する権限がありません。サーバー内のロールの順位を確認してください。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 目標位置は bot のトップロールの直下
    target_position = bot_member.top_role.position - 1

    old_position = role.position
    try:
        # role オブジェクトをキーにして位置を更新
        await guild.edit_role_positions(positions={role: target_position}, reason=f"Moved by {interaction.user} via /movetoprole")
        # 最新の役職情報を取得
        new_role = guild.get_role(role.id)
        new_position = new_role.position if new_role else target_position
        embed = discord.Embed(
            title=tr("ロールを上位に移動しました"),
            color=0x00ff00,
            description=tr("移動されたロール: ") + f"{new_role.mention if new_role else role.name}\n" +
                        tr("移動前の順位: ") + f"{old_position}\n" +
                        tr("移動後の順位: ") + f"{new_position}"
        )
        await interaction.response.send_message(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このbotにロールの順位を変更する権限がありません。botのロール配置を確認してください。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("ロール移動中にエラーが発生しました: ") + str(e))
        await interaction.response.send_message(embed=embed, ephemeral=True)

# deleterolefromguildコマンド
class ConfirmDeleteView(View):
    def __init__(self, role: discord.Role, author_id: int):
        super().__init__(timeout=60)
        self.role = role
        self.author_id = author_id

    @discord.ui.button(label=tr("削除"), style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(tr("この操作は実行者のみ行えます。"))
            return

        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)

        try:
            await self.role.delete(reason=f"Deleted by {interaction.user} via /deleterolefromguild")
            embed = discord.Embed(
                title=tr("ロールを削除しました"),
                color=0x00ff00,
                description=tr("削除されたロール: ") + f"**{self.role.name}**"
            )
            await interaction.followup.send(embed=embed)
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title=tr("エラー"),
                color=0xff0000,
                description=tr("このbotにそのロールを削除する権限がありません。サーバー内のロールの順位を確認してください。")
            )
            await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title=tr("エラー"),
                color=0xff0000,
                description=tr("ロール削除中にエラーが発生しました: ") + str(e)
            )
            await interaction.followup.send(embed=embed)
        finally:
            self.stop()

    @discord.ui.button(label=tr("キャンセル"), style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(tr("この操作は実行者のみ行えます。"))
            return
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(tr("ロールの削除をキャンセルしました。"))
        self.stop()

@tree.command(name="deleterolefromguild", description=tr("指定したロールをサーバーから削除します"))
@app_commands.describe(
    role=tr("削除するロールを選択してください")
)
async def deleterolefromguild(interaction: discord.Interaction, role: discord.Role):
    guild = interaction.guild
    if not guild:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("サーバー内でのみ使用できるコマンドです。"))
        await interaction.response.send_message(embed=embed)
        return

    # 実行者の権限チェックは行わない（実行者に manage_roles または administrator がなくても実行可能）

    # 存在チェック
    if role is None:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("ロールが見つかりません。"))
        await interaction.response.send_message(embed=embed)
        return

    # @everyone 保護
    if role == guild.default_role:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("@everyone ロールは削除できません。"))
        await interaction.response.send_message(embed=embed)
        return

    # 外部サービス管理ロールは削除できない
    if role.managed:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このロールは外部サービスによって管理されているため削除できません。"))
        await interaction.response.send_message(embed=embed)
        return

    # Bot がそのロールを操作できるか（位置チェック）
    bot_member = guild.me
    if bot_member and bot_member.top_role.position <= role.position:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このbotはそのロールを削除する権限がありません。サーバー内のロールの順位を確認してください。"))
        await interaction.response.send_message(embed=embed)
        return

    # Bot が manage_roles 権限を持っているか確認
    if bot_member and not bot_member.guild_permissions.manage_roles:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このbotにロールを管理する権限(manage_roles)がありません。botの権限を確認してください。"))
        await interaction.response.send_message(embed=embed)
        return

    # 確認メッセージ（実行者以外はボタン操作不可）
    embed = discord.Embed(
        title=tr("ロールを削除します"),
        color=0xffa500,
        description=tr("本当に次のロールをサーバーから削除してもよろしいですか？\n削除されたロールは元に戻せません。\n") + f"**{role.name}**"
    )
    view = ConfirmDeleteView(role, interaction.user.id)
    await interaction.response.send_message(embed=embed, view=view)

# changerolenameコマンド
@tree.command(name="changerolename", description=tr("任意のロールの名前を変更します"))
@app_commands.describe(
    role=tr("変更するロールを選択してください"),
    new_name=tr("新しいロール名")
)
async def changerolename(interaction: discord.Interaction, role: discord.Role, new_name: str):
    guild = interaction.guild
    if not guild:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("サーバー内でのみ使用できるコマンドです。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    if role is None:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("ロールが見つかりません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # @everyone は変更不可
    if role == guild.default_role:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("@everyone ロールの名前は変更できません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 外部サービス管理ロールは変更不可
    if role.managed:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このロールは外部サービスによって管理されているため名前を変更できません。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    bot_member = guild.me
    # Bot のロール順位チェック
    if bot_member and bot_member.top_role.position <= role.position:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このbotはそのロールの名前を変更する権限がありません。サーバー内のロールの順位を確認してください。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Bot に manage_roles が必要
    if bot_member and not bot_member.guild_permissions.manage_roles:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このbotにロールを管理する権限(manage_roles)がありません。botの権限を確認してください。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 同名のロールが既に存在するか
    existing = discord.utils.get(guild.roles, name=new_name)
    if existing and existing.id != role.id:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("同じ名前のロールが既に存在します: ") + f"**{new_name}**")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    old_name = role.name
    try:
        await role.edit(name=new_name, reason=f"Renamed by {interaction.user} via /changerolename")
        embed = discord.Embed(
            title=tr("ロール名を変更しました"),
            color=0x00ff00,
            description=tr("変更前: ") + f"**{old_name}**\n" + tr("変更後: ") + f"**{new_name}**"
        )
        await interaction.response.send_message(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("このbotはそのロールの名前を変更する権限がありません。サーバー内のロールの順位を確認してください。"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        embed = discord.Embed(title=tr("エラー"), color=0xff0000, description=tr("ロール名変更中にエラーが発生しました: ") + str(e))
        await interaction.response.send_message(embed=embed, ephemeral=True)

# helpコマンド
from help import text
def help_text():
    return text[LANG]

@tree.command(name="help", description=tr("このbotの使い方を表示します"))
async def help_command(interaction: discord.Interaction):
    help_text_content = help_text()
    embed = discord.Embed(title=tr("ロールを作るbot - ヘルプ"), description=help_text_content, color=0x00ff00)
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