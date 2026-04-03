import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 1487986397074952406
PREMIUM_USERS = []


def is_premium(user_id):
    return user_id in PREMIUM_USERS


@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")
    await bot.tree.sync()


# ===================== /say =====================
@bot.tree.command(name="say")
async def say(interaction: discord.Interaction, mensagem: str):

    class SayView(discord.ui.View):
        def __init__(self, user_id):
            super().__init__(timeout=None)
            self.user_id = user_id

        @discord.ui.button(label="📨 Enviar 1x", style=discord.ButtonStyle.primary)
        async def button(self, i: discord.Interaction, b: discord.ui.Button):

            if i.user.id != self.user_id:
                return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

            await i.response.defer()

            await i.channel.send(mensagem)

    await interaction.response.send_message(
        "Clique no botão:",
        view=SayView(interaction.user.id),
        ephemeral=True
    )


# ===================== /spam =====================
@bot.tree.command(name="spam")
async def spam(interaction: discord.Interaction, mensagem: str):

    if not is_premium(interaction.user.id):
        return await interaction.response.send_message("❌ Você não é premium!", ephemeral=True)

    class SpamView(discord.ui.View):
        def __init__(self, user_id):
            super().__init__(timeout=None)
            self.user_id = user_id

        @discord.ui.button(label="📨 Enviar 5x", style=discord.ButtonStyle.danger)
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


# ===================== /addprem =====================
@bot.tree.command(name="addprem")
async def addprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas o dono!", ephemeral=True)

    if user.id not in PREMIUM_USERS:
        PREMIUM_USERS.append(user.id)

    await interaction.response.send_message(f"✅ {user.name} virou Premium")


# ===================== /removeprem =====================
@bot.tree.command(name="removeprem")
async def removeprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas o dono!", ephemeral=True)

    if user.id in PREMIUM_USERS:
        PREMIUM_USERS.remove(user.id)

    await interaction.response.send_message(f"❌ {user.name} perdeu Premium")


bot.run(os.getenv("TOKEN")) 
