
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# ==========================================
# CONFIGURACIÓN
# ==========================================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# Importar motor de dados
from dice import roll_pool, format_result


# ==========================================
# EVENTOS
# ==========================================

@bot.event
async def on_ready():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🎲 Bot conectado: {bot.user}")
    print("⚔️ Sistema Genesys RPG preparado")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


# ==========================================
# COMANDO DE TIRADAS
# ==========================================

@bot.command(name="roll")
async def roll(ctx, *, pool: str = None):

    if not pool:
        await ctx.send(
            "🎲 **¡Necesitas indicar los dados!**\n\n"
            "Ejemplo:\n"
            "`!roll yyggkkrr`\n\n"
            "**Dados disponibles:**\n"
            "🔵 `b` — Impulso\n"
            "🟢 `g` — Habilidad\n"
            "🟡 `y` — Pericia\n"
            "⚫ `k` — Contratiempo\n"
            "🟣 `p` — Dificultad\n"
            "🔴 `r` — Desafío"
        )
        return

    try:
        result = roll_pool(pool)

        message = format_result(result)

        await ctx.send(message)

    except ValueError as error:
        await ctx.send(f"❌ **Error en la tirada:** {error}")


# ==========================================
# INICIAR BOT
# ==========================================

if not TOKEN:
    raise ValueError(
        "❌ No se ha encontrado DISCORD_TOKEN en el archivo .env"
    )

bot.run(TOKEN)
