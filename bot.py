import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import time

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 1487986397074952406

# 💎 VIP com tempo (user_id: timestamp)
PREMIUM_USERS = {}

def is_premium(user_id):
    if user_id in PREMIUM_USERS:
        if PREMIUM_USERS[user_id] > time.time():
            return True
        else:
            del PREMIUM_USERS[user_id]  # expirou
    return False

# ================= LIMPAR VIP EXPIRADO =================
@tasks.loop(minutes=10)
async def check_premium():
    now = time.time()
    expired = [user for user, t in PREMIUM_USERS.items() if t <= now]
    for user in expired:
        del PREMIUM_USERS[user]

# ================= VIEW SAY =================
class SayView(discord.ui.View):
    def __init__(self, mensagem):
        super().__init__()
        self.mensagem = mensagem

    @discord.ui.button(label="📨 Send", style=discord.ButtonStyle.primary)
    async def botao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.followup.send(self.mensagem)

# ================= VIEW RAID =================
class RaidView(discord.ui.View):
    @discord.ui.button(label="📨 Send 5 times", style=discord.ButtonStyle.danger)
    async def botao(self, interaction: discord.Interaction, button: discord.ui.Button):

        msg = """⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️
VERTEX NO TOPO

https://discord.gg/357NzPmNW
https://discord.gg/357NzPmNW

⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️⛓️"""

        await interaction.response.defer()

        for _ in range(5):
            await interaction.followup.send(msg)

# ================= VIEW SPAM =================
class SpamView(discord.ui.View):
    def __init__(self, mensagem):
        super().__init__()
        self.mensagem = mensagem

    @discord.ui.button(label="📨 Send 5 times", style=discord.ButtonStyle.primary)
    async def botao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        for _ in range(5):
            await interaction.followup.send(self.mensagem)

# ================= READY =================
@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")
    await bot.tree.sync()
    check_premium.start()

# ================= /ADDPREM =================
@bot.tree.command(name="addprem", description="Dar premium com tempo")
@app_commands.describe(user="Usuário", dias="De 1 a 60 dias")
async def addprem(interaction: discord.Interaction, user: discord.Member, dias: int):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas o dono!", ephemeral=True)

    if dias < 1 or dias > 60:
        return await interaction.response.send_message("❌ Escolha entre 1 e 60 dias!", ephemeral=True)

    tempo = time.time() + dias * 86400
    PREMIUM_USERS[user.id] = tempo

    await interaction.response.send_message(f"✅ {user.name} virou premium por {dias} dias!")

# ================= /REMOVEPREM =================
@bot.tree.command(name="removeprem", description="Remover premium")
@app_commands.describe(user="Usuário")
async def removeprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas o dono!", ephemeral=True)

    PREMIUM_USERS.pop(user.id, None)

    await interaction.response.send_message(f"❌ {user.name} não é mais premium!")

# ================= /SAY =================
@bot.tree.command(name="say", description="Mensagem personalizada")
@app_commands.describe(mensagem="Mensagem")
async def say(interaction: discord.Interaction, mensagem: str):

    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("🔒 Comando premium!", ephemeral=True)

    await interaction.response.send_message(
        "Clique no botão 👇",
        view=SayView(mensagem),
        ephemeral=True
    )

# ================= /RAID =================
@bot.tree.command(name="raid", description="Mensagem pronta")
async def raid(interaction: discord.Interaction):

    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("🔒 Comando premium!", ephemeral=True)

    await interaction.response.send_message(
        "Clique no botão 👇",
        view=RaidView(),
        ephemeral=True
    )

# ================= /SPAM =================
@bot.tree.command(name="spam", description="Enviar mensagem 5x")
@app_commands.describe(mensagem="Mensagem")
async def spam(interaction: discord.Interaction, mensagem: str):

    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("🔒 Comando premium!", ephemeral=True)

    await interaction.response.send_message(
        "Clique no botão 👇",
        view=SpamView(mensagem),
        ephemeral=True
    )

# ================= RUN =================
bot.run(os.getenv("TOKEN"))
