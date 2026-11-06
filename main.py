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
from dice import roll_pool, SYMBOLS


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
        # Embed de ayuda cuando no se especifican dados
        embed_help = discord.Embed(
            title="🎲 Ayuda de Tiradas - Genesys RPG",
            description="¡Necesitas indicar qué dados quieres lanzar!\n\n**Ejemplo:**\n`!roll yyggkkrr`",
            color=discord.Color.blue()
        )
        embed_help.add_field(
            name="Dados Disponibles",
            value=(
                "🔵 `b` — Bonus\n"
                "🟢 `g` — Habilidad\n"
                "🟡 `y` — Competencia\n"
                "⚫ `k` — Desventaja\n"
                "🟣 `p` — Dificultad\n"
                "🔴 `r` — Desafío"
            ),
            inline=False
        )
        await ctx.send(embed=embed_help)
        return

    try:
        result = roll_pool(pool)

        net_success = result["net_success"]
        net_advantage = result["net_advantage"]
        totals = result["totals"]

        # Determinar color de la barra lateral del Embed según prioridad temática:
        # 1. Desesperación (Morado)
        # 2. Triunfo (Amarillo / Dorado)
        # 3. Éxito neto (Verde)
        # 4. Fallo neto (Rojo)
        # 5. Solo Ventajas (Azul)
        # 6. Solo Amenazas (Naranja)
        # 7. Marrón o por defecto para otros casos neutros
        
        brown_color = discord.Color.from_rgb(139, 69, 19) # Tono marrón madera/desventaja

        if totals["despair"] > 0:
            embed_color = discord.Color.purple()
        elif totals["triumph"] > 0:
            embed_color = discord.Color.gold()
        elif net_success > 0:
            embed_color = discord.Color.green()
        elif net_success < 0:
            embed_color = discord.Color.red()
        elif net_success == 0 and net_advantage > 0:
            embed_color = discord.Color.blue()
        elif net_success == 0 and net_advantage < 0:
            embed_color = discord.Color.orange()
        else:
            embed_color = brown_color

        embed = discord.Embed(
            title="Tirada",
            color=embed_color
        )

        # 1. Agrupar tiradas individuales para mostrarlas de forma compacta
        grouped_counts = {}
        for die in result["dice"]:
            key = (die["color"], die["name"])
            grouped_counts[key] = grouped_counts.get(key, 0) + 1

        dice_summary_lines = []
        for (color, name), count in grouped_counts.items():
            dice_summary_lines.append(f"{color} {name} (×{count})")

        # 2. Recopilar totales netos y especiales en una sola lista
        net_lines = []
        
        # Éxitos / Fallos / Triunfos netos
        has_success_source = totals["success"] > 0 or totals["triumph"] > 0
        has_failure_source = totals["failure"] > 0 or totals["despair"] > 0

        if net_success > 0:
            net_lines.append(f"{SYMBOLS['success']} Éxitos: **{net_success}**")
        elif net_success < 0:
            net_lines.append(f"{SYMBOLS['failure']} Fallos: **{abs(net_success)}**")
        elif has_success_source or has_failure_source:
            net_lines.append("⚖️ Éxitos y fallos cancelados")

        # Ventajas / Amenazas netas
        has_advantage_source = totals["advantage"] > 0
        has_threat_source = totals["threat"] > 0

        if net_advantage > 0:
            net_lines.append(f"{SYMBOLS['advantage']} Ventajas: **{net_advantage}**")
        elif net_advantage < 0:
            net_lines.append(f"{SYMBOLS['threat']} Amenazas: **{abs(net_advantage)}**")
        elif has_advantage_source or has_threat_source:
            net_lines.append("⚖️ Ventajas y amenazas canceladas")

        # Triunfos y Desesperaciones absolutas
        if totals["triumph"] > 0:
            net_lines.append(f"{SYMBOLS['triumph']} Triunfos: **{totals['triumph']}**")
        if totals["despair"] > 0:
            net_lines.append(f"{SYMBOLS['despair']} Desesperaciones: **{totals['despair']}**")

        # Si no hubo ningún símbolo relevante
        if not net_lines:
            net_lines.append("🎲 ¡Tirada completamente vacía!")

        # 3. Construir la descripción uniendo los dados tirados y el resultado final
        full_description = (
            "\n".join(dice_summary_lines)
            + "\n### Resultado\n"
            + "\n".join(net_lines)
        )

        embed.description = full_description

        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=avatar_url)

        await ctx.send(embed=embed)

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