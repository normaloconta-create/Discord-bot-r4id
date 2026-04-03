import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 1487986397074952406
PREMIUM_USERS = []


def is_premium(user_id):
    return user_id in PREMIUM_USERS


# ===================== ON READY =====================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logado como {bot.user}")


# ===================== SAY =====================
@bot.tree.command(name="say")
async def say(interaction: discord.Interaction, mensagem: str):

    class SayView(discord.ui.View):
        def __init__(self, user_id):
            super().__init__(timeout=None)
            self.user_id = user_id

        @discord.ui.button(label="📨 Send 1 time", style=discord.ButtonStyle.primary)
        async def button(self, i: discord.Interaction, b: discord.ui.Button):

            if i.user.id != self.user_id:
                return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

            await i.response.defer()
            await i.channel.send(mensagem)

    await interaction.response.send_message(
        "Clique no botão para enviar:",
        view=SayView(interaction.user.id),
        ephemeral=True
    )


# ===================== SPAM (PREMIUM) =====================
@bot.tree.command(name="spam")
async def spam(interaction: discord.Interaction, mensagem: str):

    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("🔒 Você não é premium!", ephemeral=True)

    class SpamView(discord.ui.View):
        def __init__(self, user_id):
            super().__init__(timeout=None)
            self.user_id = user_id

        @discord.ui.button(label="📨 Send 5 times", style=discord.ButtonStyle.danger)
        async def button(self, i: discord.Interaction, b: discord.ui.Button):

            if i.user.id != self.user_id:
                return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

            await i.response.defer()

            for _ in range(5):
                await i.channel.send(mensagem)

    await interaction.response.send_message(
        "Clique no botão:",
        view=SpamView(interaction.user.id),
        ephemeral=True
    )


# ===================== VERTEX VIEW =====================
class VertexView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    async def send_msgs(self, i, msg, premium=False):

        if i.user.id != self.user_id:
            return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

        if premium and not is_premium(i.user.id):
            return await i.response.send_message("🔒 Você não é premium!", ephemeral=True)

        await i.response.defer()

        for _ in range(5):
            await i.channel.send(msg)

    # ================= RAID =================
    @discord.ui.button(label="ℜ𝔞𝔦𝔡", style=discord.ButtonStyle.primary)
    async def raid1(self, i: discord.Interaction, b: discord.ui.Button):

        msg = """⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️
ADQUIRA A VERSÃO VIP EM https://discord.gg/5zs6tj7mbD
⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️"""

        await self.send_msgs(i, msg)


    # ================= RAID 2 =================
    @discord.ui.button(label="ℜ𝔞𝔦𝔡 2", style=discord.ButtonStyle.secondary)
    async def raid2(self, i: discord.Interaction, b: discord.ui.Button):

        msg = """⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️

SUA MODERAÇÃO É UM LIXO, VERTEX ACIMA DE TODOS

⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️"""

        await self.send_msgs(i, msg)


    # ================= RAID 3 PREMIUM =================
    @discord.ui.button(label="🔒 ℜ𝔞𝔦𝔡 3", style=discord.ButtonStyle.success)
    async def raid3(self, i: discord.Interaction, b: discord.ui.Button):

        msg = """⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️
||@everyone @here||
https://media.discordapp.net/attachments/1488943346813763828/1489631468480368773/VID_20260403_102310.mp4
⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️"""

        await self.send_msgs(i, msg, premium=True)


# ===================== VERTEX COMMAND =====================
@bot.tree.command(name="vertex")
async def vertex(interaction: discord.Interaction):

    embed = discord.Embed(
        title="ℜ𝔞𝔦𝔡",
        description="""
ℜ𝔞𝔦𝔡 → envia uma mensagem 5x  
ℜ𝔞𝔦𝔡 2 → envia uma mensagem 5x  
🔒 ℜ𝔞𝔦𝔡 3 → premium  
""",
        color=discord.Color.dark_red()
    )

    await interaction.response.send_message(
        embed=embed,
        view=VertexView(interaction.user.id),
        ephemeral=False
    )


# ===================== ADDPREM =====================
@bot.tree.command(name="addprem")
async def addprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas owner!", ephemeral=True)

    if user.id not in PREMIUM_USERS:
        PREMIUM_USERS.append(user.id)

    await interaction.response.send_message(f"✅ {user.name} virou premium!")


# ===================== REMOVEPREM =====================
@bot.tree.command(name="removeprem")
async def removeprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas owner!", ephemeral=True)

    if user.id in PREMIUM_USERS:
        PREMIUM_USERS.remove(user.id)

    await interaction.response.send_message(f"❌ {user.name} não é mais premium!")


# ===================== RUN =====================
bot.run(os.getenv("TOKEN"))
