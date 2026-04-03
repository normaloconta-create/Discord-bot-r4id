import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 1487986397074952406
PREMIUM_USERS = []


def is_premium(user_id):
    return user_id in PREMIUM_USERS


# ===================== READY =====================
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

        @discord.ui.button(label="📨 Send", style=discord.ButtonStyle.primary)
        async def button(self, i: discord.Interaction, button: discord.ui.Button):

            if i.user.id != self.user_id:
                return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

            channel = i.channel or i.guild.get_channel(i.channel_id)
            await channel.send(mensagem)

            await i.response.send_message("✅ Enviado!", ephemeral=True)

    await interaction.response.send_message(
        "Clique no botão para enviar:",
        view=SayView(interaction.user.id),
        ephemeral=True
    )


# ===================== SPAM =====================
@bot.tree.command(name="spam")
async def spam(interaction: discord.Interaction, mensagem: str):

    if interaction.user.id not in PREMIUM_USERS:
        return await interaction.response.send_message("🔒 Você não é premium!", ephemeral=True)

    class SpamView(discord.ui.View):
        def __init__(self, user_id):
            super().__init__(timeout=None)
            self.user_id = user_id

        @discord.ui.button(label="📨 Send", style=discord.ButtonStyle.danger)
        async def button(self, i: discord.Interaction, button: discord.ui.Button):

            if i.user.id != self.user_id:
                return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

            channel = i.channel or i.guild.get_channel(i.channel_id)
            await channel.send(mensagem)

            await i.response.send_message("✅ Enviado!", ephemeral=True)

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

    async def safe_send(self, i, msg, premium=False):

        if i.user.id != self.user_id:
            return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

        if premium and not is_premium(i.user.id):
            return await i.response.send_message("🔒 Você não é premium!", ephemeral=True)

        channel = i.channel or i.guild.get_channel(i.channel_id)

        await channel.send(msg)
        await i.response.send_message("✅ Enviado!", ephemeral=True)


    @discord.ui.button(label="ℜ𝔞𝔦𝔡", style=discord.ButtonStyle.primary)
    async def raid1(self, i: discord.Interaction, button: discord.ui.Button):

        msg = "⛓️ Mensagem do sistema 1"
        await self.safe_send(i, msg)


    @discord.ui.button(label="ℜ𝔞𝔦𝔡 2", style=discord.ButtonStyle.secondary)
    async def raid2(self, i: discord.Interaction, button: discord.ui.Button):

        msg = "⛓️ Mensagem do sistema 2"
        await self.safe_send(i, msg)


    @discord.ui.button(label="🔒 ℜ𝔞𝔦𝔡 3", style=discord.ButtonStyle.success)
    async def raid3(self, i: discord.Interaction, button: discord.ui.Button):

        msg = "⛓️ Mensagem premium"
        await self.safe_send(i, msg, premium=True)


# ===================== VERTEX =====================
@bot.tree.command(name="vertex")
async def vertex(interaction: discord.Interaction):

    embed = discord.Embed(
        title="Menu",
        description="Bot funcionando corretamente",
        color=discord.Color.dark_red()
    )

    await interaction.response.send_message(
        embed=embed,
        view=VertexView(interaction.user.id),
        ephemeral=False
    )


# ===================== PREMIUM =====================
@bot.tree.command(name="addprem")
async def addprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas owner!", ephemeral=True)

    if user.id not in PREMIUM_USERS:
        PREMIUM_USERS.append(user.id)

    await interaction.response.send_message(f"✅ {user.name} virou premium!")


@bot.tree.command(name="removeprem")
async def removeprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas owner!", ephemeral=True)

    if user.id in PREMIUM_USERS:
        PREMIUM_USERS.remove(user.id)

    await interaction.response.send_message(f"❌ {user.name} removido premium!")


# ===================== RUN =====================
bot.run(os.getenv("TOKEN"))
