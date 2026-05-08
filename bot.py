import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot en ligne : {bot.user}")

@bot.tree.command(name="avis", description="Laisser un avis sur une commande")
@app_commands.describe(
    note="Ta note de 1 à 5",
    commentaire="Ton commentaire (ex: x1 McMenu merci @staff)",
    staff="Le membre du staff concerné"
)
async def avis(
    interaction: discord.Interaction,
    note: app_commands.Range[int, 1, 5],
    commentaire: str,
    staff: discord.Member
):
    stars = "★" * note + "☆" * (5 - note)

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

    embed = discord.Embed(color=0xe74c3c)

    embed.set_author(
        name=interaction.user.name,
        icon_url=interaction.user.display_avatar.url
    )

    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    embed.add_field(
        name="Commentaire",
        value=f"{commentaire} {staff.mention}",
        inline=False
    )

    embed.add_field(
        name="Note",
        value=f"{stars}  {note}/5 — {label}",
        inline=True
    )

    embed.set_footer(
        text=f"O'Food — Avis certifié • {(interaction.created_at + __import__('datetime').timedelta(hours=2)).strftime('%d/%m/%Y %H:%M')}"
    )

    print(f"CHANNEL_ID utilisé : {os.getenv('CHANNEL_ID')}")
    channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))

    if channel is None:
        await interaction.response.send_message(
            "❌ Erreur : channel introuvable. Vérifie le CHANNEL_ID dans les variables.",
            ephemeral=True
        )
        return

    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Ton avis a bien été envoyé !", ephemeral=True)

bot.run(os.getenv("TOKEN"))
