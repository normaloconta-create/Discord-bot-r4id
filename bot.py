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

        @discord.ui.button(label="📨 Send", style=discord.ButtonStyle.primary)
        async def button(self, i: discord.Interaction, button: discord.ui.Button):

            if i.user.id != self.user_id:
                return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

            # 🔥 TODO MUNDO VÊ
            await i.channel.send(mensagem)

            # 🔒 SÓ QUEM CLICOU VÊ
            await i.response.send_message("✅ Mensagem enviada!", ephemeral=True)

    await interaction.response.send_message(
        "Clique no botão para enviar a mensagem:",
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

        @discord.ui.button(label="📨 Send", style=discord.ButtonStyle.danger)
        async def button(self, i: discord.Interaction, button: discord.ui.Button):

            if i.user.id != self.user_id:
                return await i.response.send_message("❌ Não é seu botão!", ephemeral=True)

            await i.channel.send(mensagem)
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

        await i.channel.send(msg)
        await i.response.send_message("✅ Enviado!", ephemeral=True)


    # ================= RAID 1 =================
    @discord.ui.button(label="ℜ𝔞𝔦𝔡", style=discord.ButtonStyle.primary)
    async def raid1(self, i: discord.Interaction, button: discord.ui.Button):

        msg = "⛓️ Mensagem do sistema 1"
        await self.safe_send(i, msg)


    # ================= RAID 2 =================
    @discord.ui.button(label="ℜ𝔞𝔦𝔡 2", style=discord.ButtonStyle.secondary)
    async def raid2(self, i: discord.Interaction, button: discord.ui.Button):

        msg = "⛓️ Mensagem do sistema 2"
        await self.safe_send(i, msg)


    # ================= RAID 3 PREMIUM =================
    @discord.ui.button(label="🔒 ℜ𝔞𝔦𝔡 3", style=discord.ButtonStyle.success)
    async def raid3(self, i: discord.Interaction, button: discord.ui.Button):

        msg = "⛓️ Mensagem premium do sistema"
        await self.safe_send(i, msg, premium=True)


# ===================== VERTEX COMMAND =====================
@bot.tree.command(name="vertex")
async def vertex(interaction: discord.Interaction):

    embed = discord.Embed(
        title="Menu",
        description="Sistema de botões funcionando",
        color=discord.Color.dark_red()
    )

    await interaction.response.send_message(
        embed=embed,
        view=VertexView(interaction.user.id),
        ephemeral=False
    )


# ===================== ADD PREMIUM =====================
@bot.tree.command(name="addprem")
async def addprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas owner!", ephemeral=True)

    if user.id not in PREMIUM_USERS:
        PREMIUM_USERS.append(user.id)

    await interaction.response.send_message(f"✅ {user.name} virou premium!")


# ===================== REMOVE PREMIUM =====================
@bot.tree.command(name="removeprem")
async def removeprem(interaction: discord.Interaction, user: discord.Member):

    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Apenas owner!", ephemeral=True)

    if user.id in PREMIUM_USERS:
        PREMIUM_USERS.remove(user.id)

    await interaction.response.send_message(f"❌ {user.name} não é mais premium!")


# ===================== RUN =====================
bot.run(os.getenv("TOKEN"))
