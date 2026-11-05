
import random

# ==================================================
# CONFIGURACIÓN DE LOS DADOS GENESYS
# ==================================================
#
# Cada cara se representa mediante:
# (éxitos, fallos, ventajas, amenazas, triunfos, desesperaciones)
#
# ==================================================

DICE = {
    "b": {
        "name": "Impulso",
        "color": "🔵",
        "faces": [
            (0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 0),
            (1, 0, 1, 0, 0, 0),
            (0, 0, 2, 0, 0, 0),
            (0, 0, 1, 0, 0, 0),
        ],
    },

    "g": {
        "name": "Habilidad",
        "color": "🟢",
        "faces": [
            (0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 0),
            (2, 0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0, 0),
            (0, 0, 1, 0, 0, 0),
            (1, 0, 1, 0, 0, 0),
            (0, 0, 2, 0, 0, 0),
        ],
    },

    "y": {
        "name": "Pericia",
        "color": "🟡",
        "faces": [
            (0, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 0),
            (1, 0, 0, 0, 0, 0),
            (2, 0, 0, 0, 0, 0),
            (2, 0, 0, 0, 0, 0),
            (0, 0, 1, 0, 0, 0),
            (1, 0, 1, 0, 0, 0),
            (1, 0, 1, 0, 0, 0),
            (1, 0, 1, 0, 0, 0),
            (0, 0, 2, 0, 0, 0),
            (0, 0, 2, 0, 0, 0),
            (1, 0, 0, 0, 1, 0),
        ],
    },

    "k": {
        "name": "Contratiempo",
        "color": "⚫",
        "faces": [
            (0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0),
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0, 0),
        ],
    },

    "p": {
        "name": "Dificultad",
        "color": "🟣",
        "faces": [
            (0, 0, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0),
            (0, 2, 0, 0, 0, 0),
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 2, 0, 0),
            (0, 1, 0, 1, 0, 0),
        ],
    },

    "r": {
        "name": "Desafío",
        "color": "🔴",
        "faces": [
            (0, 0, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0),
            (0, 2, 0, 0, 0, 0),
            (0, 2, 0, 0, 0, 0),
            (0, 0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0, 0),
            (0, 1, 0, 1, 0, 0),
            (0, 1, 0, 1, 0, 0),
            (0, 0, 0, 2, 0, 0),
            (0, 0, 0, 2, 0, 0),
            (0, 1, 0, 0, 0, 1),
        ],
    },
}


# ==================================================
# SÍMBOLOS
# ==================================================

SYMBOLS = {
    "success": "✔",
    "failure": "✖",
    "advantage": "✧",
    "threat": "⚠",
    "triumph": "🌟",
    "despair": "💀",
}


# ==================================================
# LANZAMIENTO DE DADOS
# ==================================================

def roll_pool(pool):
    """Lanza los dados indicados y calcula sus resultados."""

    pool = pool.lower().replace(" ", "")

    if not pool:
        raise ValueError("Debes indicar al menos un dado.")

    for letter in pool:
        if letter not in DICE:
            raise ValueError(f"Dado desconocido: '{letter}'")

    totals = {
        "success": 0,
        "failure": 0,
        "advantage": 0,
        "threat": 0,
        "triumph": 0,
        "despair": 0,
    }

    results = []

    for letter in pool:
        die = DICE[letter]
        face = random.choice(die["faces"])

        names = list(totals.keys())

        for name, amount in zip(names, face):
            totals[name] += amount

        symbols = [
            f"{SYMBOLS[name]} ×{amount}"
            for name, amount in zip(names, face)
            if amount > 0
        ]

        results.append({
            "name": die["name"],
            "color": die["color"],
            "symbols": symbols,
            "blank": not symbols,
        })

    # Cálculo de resultados netos.
    # Triunfos cuentan como éxitos.
    # Desesperaciones cuentan como fallos.

    net_success = (
        totals["success"]
        + totals["triumph"]
        - totals["failure"]
        - totals["despair"]
    )

    net_advantage = (
        totals["advantage"]
        - totals["threat"]
    )

    return {
        "dice": results,
        "totals": totals,
        "net_success": net_success,
        "net_advantage": net_advantage,
    }


# ==================================================
# FORMATEAR RESULTADO
# ==================================================


def format_result(result):
    """Presentación compacta de la tirada."""

    output = [
        "🎲 **DICEDGENESYS**",
        "|| Tirada completada ||",
        ""
    ]

    grouped = {}

    for die in result["dice"]:
        name = die["name"]

        if name not in grouped:
            grouped[name] = {
                "color": die["color"],
                "results": []
            }

        if die["blank"]:
            symbols = "—"
        else:
            symbols = " ".join(die["symbols"])

        grouped[name]["results"].append(symbols)

    for name, data in grouped.items():
        rolls = " / ".join(data["results"])

        output.append(
            f"{data['color']} **{name} ×{len(data['results'])}**"
            f" · {rolls}"
        )

    success = result["net_success"]
    advantage = result["net_advantage"]
    totals = result["totals"]

    output.append("")
    output.append("━━━━━━━━━━━━━━━━")
    output.append("⚔️ **RESULTADO FINAL**")

    if success > 0:
        output.append(f"✔ Éxitos: **{success}**")
    elif success < 0:
        output.append(f"✖ Fallos: **{abs(success)}**")
    else:
        output.append("⚖️ Éxitos cancelados")

    if advantage > 0:
        output.append(f"✧ Ventajas: **{advantage}**")
    elif advantage < 0:
        output.append(f"⚠ Amenazas: **{abs(advantage)}**")
    else:
        output.append("⚖️ Ventajas canceladas")

    # Los símbolos especiales siempre se muestran
    output.append("━━━━━━━━━━━━━━━━")

    if totals["triumph"] > 0:
        output.append(
            f"🌟 **TRIUNFOS: {totals['triumph']}**"
        )

    if totals["despair"] > 0:
        output.append(
            f"💀 **DESESPERACIONES: {totals['despair']}**"
        )

    return "\n".join(output)



# ==================================================
# PRUEBA INDEPENDIENTE DE DISCORD
# ==================================================

if __name__ == "__main__":

    print("\n🎲 SISTEMA DE DADOS GENESYS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━")
    print("b = Impulso")
    print("g = Habilidad")
    print("y = Pericia")
    print("k = Contratiempo")
    print("p = Dificultad")
    print("r = Desafío")
    print("━━━━━━━━━━━━━━━━━━━━━━━━")

    pool = input("\nIntroduce los dados: ")

    try:
        result = roll_pool(pool)

        print()
        print(format_result(result))

    except ValueError as error:
        print(f"\n❌ Error: {error}")