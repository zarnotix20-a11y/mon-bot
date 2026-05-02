import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

# Charge les secrets depuis le fichier .env
load_dotenv()

# Démarre le bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Quand le bot se connecte à Discord
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot en ligne : {bot.user}")

# La commande /avis
@bot.tree.command(name="avis", description="Laisser un avis sur une commande")
@app_commands.describe(
    note="Ta note de 1 à 5",
    commentaire="Ton commentaire (ex: x1 basic fit merci)",
    staff="Le membre du staff concerné"
)
async def avis(
    interaction: discord.Interaction,
    note: app_commands.Range[int, 1, 5],
    commentaire: str,
    staff: discord.Member
):
    # Génère les étoiles
    stars = "⭐" * note + "☆" * (5 - note)

    if note == 5:
        label = "Excellent"
    elif note == 4:
        label = "Très bien"
    elif note == 3:
        label = "Bien"
    elif note == 2:
        label = "Moyen"
    else:
        label = "Mauvais"

    # Crée la carte stylisée (embed)
    embed = discord.Embed(color=0xFFA500)

    embed.set_author(
        name=f"{interaction.user.name} laisse un avis",
        icon_url=interaction.user.display_avatar.url
    )

    embed.add_field(
        name="Note",
        value=f"{stars} {note}/5 — {label}",
        inline=False
    )

    embed.add_field(
        name="Commentaire",
        value=f"{commentaire} {staff.mention}",
        inline=False
    )

    embed.set_footer(
        text=f"O'FOOD | {interaction.created_at.strftime('%d/%m/%Y %H:%M')}"
    )

    # Envoie l'avis dans le channel configuré
    channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))

    if channel is None:
        await interaction.response.send_message(
            "❌ Erreur : channel introuvable. Vérifie le CHANNEL_ID dans le fichier .env",
            ephemeral=True
        )
        return

    await channel.send(embed=embed)

    # Répond à l'utilisateur (seulement visible par lui)
    await interaction.response.send_message(
        "✅ Ton avis a bien été envoyé !",
        ephemeral=True
    )

# Lance le bot
bot.run(os.getenv("TOKEN"))
