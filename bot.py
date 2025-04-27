import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime, timedelta
import aiohttp

CHECK_TIMEFRAME = 15
MESSAGE_THRESHOLD = 3
server_settings = {}

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_message_logs = {}

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)} comandos.")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

@bot.tree.command(name="iniciar", description="Activa el sistema AntiBoomer en el servidor.")
async def iniciar(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("🚫 No tienes permiso para usar este comando (se requiere ser administrador).", ephemeral=True)
        return
    
    server_settings[interaction.guild.id] = {
        "antiboom_active": True,
        "webhook_url": None
    }
    await interaction.response.send_message("✅ AntiBoomer ACTIVADO para este servidor.", ephemeral=True)
@bot.tree.command(name="avisos", description="Configura el webhook para recibir notificaciones de baneos.")
@app_commands.describe(url="URL del webhook de Discord")
async def avisos(interaction: discord.Interaction, url: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("🚫 No tienes permiso para usar este comando (se requiere ser administrador).", ephemeral=True)
        return

    if interaction.guild.id not in server_settings:
        await interaction.response.send_message("Primero activa AntiBoomer usando /iniciar.", ephemeral=True)
        return

    server_settings[interaction.guild.id]["webhook_url"] = url
    await interaction.response.send_message("✅ Webhook configurado correctamente.", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot or message.guild is None:
        return

    guild_id = message.guild.id

    if guild_id not in server_settings or not server_settings[guild_id]["antiboom_active"]:
        return 

    now = datetime.utcnow()
    user_id = message.author.id

    if user_id not in user_message_logs:
        user_message_logs[user_id] = []

    user_message_logs[user_id].append({
        "content": message.content,
        "channel": message.channel.id,
        "timestamp": now,
    })

    user_message_logs[user_id] = [
        m for m in user_message_logs[user_id]
        if (now - m["timestamp"]).total_seconds() <= CHECK_TIMEFRAME
    ]
    unique_channels = set(m["channel"] for m in user_message_logs[user_id] if m["content"] == message.content)
    if len(unique_channels) >= MESSAGE_THRESHOLD:
        await punish_user(message.author, message.guild, reason="Spam del mismo mensaje en diferentes canales.")
        return

    everyone_mentions = [m for m in user_message_logs[user_id] if "@everyone" in m["content"]]
    if len(everyone_mentions) >= MESSAGE_THRESHOLD:
        await punish_user(message.author, message.guild, reason="Spam de @everyone.")
        return

    free_mentions = [m for m in user_message_logs[user_id] if "FREE" in m["content"].upper()]
    if len(free_mentions) >= MESSAGE_THRESHOLD:
        await punish_user(message.author, message.guild, reason="Spam de FREE.")
        return

    await bot.process_commands(message)

async def punish_user(member, guild, reason):
    try:
        await purge_user_messages(member, guild)
        await guild.ban(member, reason=reason)
        print(f"Baneado {member.name} - {reason}")

        webhook_url = server_settings[guild.id].get("webhook_url")
        if webhook_url:
            await send_webhook_notification(webhook_url, member, reason)
        
    except Exception as e:
        print(f"Error baneando o borrando mensajes: {e}")

async def purge_user_messages(member, guild):
    for channel in guild.text_channels:
        try:
            def check(m):
                return m.author.id == member.id and (datetime.utcnow() - m.created_at) <= timedelta(days=1)
            await channel.purge(limit=1000, check=check, bulk=True)
        except Exception as e:
            print(f"No se pudo purgar en {channel.name}: {e}")

async def send_webhook_notification(webhook_url, member, reason):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        await webhook.send(f"🚨 **{member.name}** ha sido baneado.\n**Razón:** {reason}")

bot.run('TU_TOKEN_AQUI')
