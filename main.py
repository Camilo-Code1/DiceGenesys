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

        # Construcción del Embed de resultados
        net_success = result["net_success"]
        net_advantage = result["net_advantage"]
        totals = result["totals"]

        # Determinar color del Embed según el resultado neto de éxitos
        if net_success > 0:
            embed_color = discord.Color.green()
        elif net_success < 0:
            embed_color = discord.Color.red()
        else:
            embed_color = discord.Color.gold()

        # El título principal del Embed ya es más grande por defecto en Discord,
        # pero le añadimos formato para resaltarlo aún más.
        embed = discord.Embed(
            title="⚔️ Resultado de la Tirada",
            color=embed_color
        )

        # 1. Agrupar tiradas individuales por tipo de dado
        grouped = {}
        for die in result["dice"]:
            name = die["name"]
            if name not in grouped:
                grouped[name] = {
                    "color": die["color"],
                    "results": []
                }
            
            if die["blank"]:
                symbols_str = "— (Vacío)"
            else:
                symbols_str = " ".join(die["symbols"])
            
            grouped[name]["results"].append(symbols_str)

        # Añadir detalle de dados lanzados
        for name, data in grouped.items():
            rolls_text = "\n".join([f"• {res}" for res in data["results"]])
            embed.add_field(
                name=f"{data['color']} {name} (×{len(data['results'])})",
                value=rolls_text,
                inline=False
            )

        # 2. Resumen neto
        net_lines = []
        
        # Evaluación de Éxitos / Fallos
        has_success_source = totals["success"] > 0 or totals["triumph"] > 0
        has_failure_source = totals["failure"] > 0 or totals["despair"] > 0

        if net_success > 0:
            net_lines.append(f"{SYMBOLS['success']} Éxitos: **{net_success}**")
        elif net_success < 0:
            net_lines.append(f"{SYMBOLS['failure']} Fallos: **{abs(net_success)}**")
        elif has_success_source or has_failure_source:
            net_lines.append("⚖️ Éxitos y fallos cancelados")

        # Evaluación de Ventajas / Amenazas
        has_advantage_source = totals["advantage"] > 0
        has_threat_source = totals["threat"] > 0

        if net_advantage > 0:
            net_lines.append(f"{SYMBOLS['advantage']} Ventajas: **{net_advantage}**")
        elif net_advantage < 0:
            net_lines.append(f"{SYMBOLS['threat']} Amenazas: **{abs(net_advantage)}**")
        elif has_advantage_source or has_threat_source:
            net_lines.append("⚖️ Ventajas y amenazas canceladas")

        # Si no hubo ningún símbolo relevante
        if not net_lines:
            net_lines.append("🎲 ¡Tirada completamente vacía!")

        embed.add_field(
        name="**RESULTADO**",
        value="\n".join(net_lines),
        inline=False
)



        # 3. Símbolos especiales (Triunfos / Desesperaciones) si los hay
        special_lines = []
        if totals["triumph"] > 0:
            special_lines.append(f"{SYMBOLS['triumph']} **TRIUNFOS: {totals['triumph']}**")
        if totals["despair"] > 0:
            special_lines.append(f"{SYMBOLS['despair']} **DESESPERACIONES: {totals['despair']}**")

        if special_lines:
            embed.add_field(
                name="",
                value="\n".join(special_lines),
                inline=False
            )

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