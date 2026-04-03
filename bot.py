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


# ===================== SELECT MENU =====================
class VertexSelect(discord.ui.Select):
    def __init__(self, user_id):
        self.user_id = user_id

        options = [
            discord.SelectOption(label="ℜ𝔞𝔦𝔡", description="Envia mensagem 5x"),
            discord.SelectOption(label="ℜ𝔞𝔦𝔡 2", description="Mensagem diferente"),
            discord.SelectOption(label="ℜ𝔞𝔦𝔡 3", description="VIP"),
        ]

        super().__init__(
            placeholder="Escolha uma opção...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        # só você pode usar
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message(
                "❌ Você não pode usar esse painel!",
                ephemeral=True
            )

        choice = self.values[0]

        # ================= RAID 1 =================
        if choice == "ℜ𝔞𝔦𝔡":
            msg = """⛓️⛓️⛓️⛓️⛓️
ADQUIRA A VERSÃO VIP EM https://discord.gg/5zs6tj7mbD
⛓️⛓️⛓️⛓️⛓️"""

            for _ in range(5):
                await interaction.channel.send(msg)

        # ================= RAID 2 =================
        elif choice == "ℜ𝔞𝔦𝔡 2":
            msg = """⛓️⛓️⛓️⛓️⛓️
SUA MODERAÇÃO É UM LIXO
VERTEX ACIMA DE TODOS
⛓️⛓️⛓️⛓️⛓️"""

            for _ in range(5):
                await interaction.channel.send(msg)

        # ================= RAID 3 =================
        elif choice == "ℜ𝔞𝔦𝔡 3":

            if not is_premium(interaction.user.id):
                return await interaction.response.send_message(
                    "🔒 Você não é premium!",
                    ephemeral=True
                )

            msg = """⛓️⛓️⛓️⛓️⛓️
||@everyone @here||
https://media.discordapp.net/attachments/1488943346813763828/1489631468480368773/VID_20260403_102310.mp4
⛓️⛓️⛓️⛓️⛓️"""

            for _ in range(5):
                await interaction.channel.send(msg)

        await interaction.response.send_message("✅ Executado!", ephemeral=True)


# ===================== VIEW =====================
class VertexView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.add_item(VertexSelect(user_id))


# ===================== VERTEX COMMAND =====================
@bot.tree.command(name="vertex")
async def vertex(interaction: discord.Interaction):

    embed = discord.Embed(
        title="ℜ𝔞𝔦𝔡",
        description="""
ℜ𝔞𝔦𝔡 → envia mensagem 5x
ℜ𝔞𝔦𝔡 2 → mensagem diferente
ℜ𝔞𝔦𝔡 3 → VIP
""",
        color=discord.Color.dark_red()
    )

    # 🔒 só você vê o painel
    await interaction.response.send_message(
        embed=embed,
        view=VertexView(interaction.user.id),
        ephemeral=True
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
