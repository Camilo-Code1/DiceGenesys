import random

# ==================================================
# CONFIGURACIÓN DE LOS DADOS GENESYS
# ==================================================
#
# Cada cara se representa mediante la tupla:
# (éxitos, fallos, ventajas, amenazas, triunfos, desesperaciones)
# ==================================================

DICE = {
    "b": {
        "name": "Bonus",
        "color": "🔵",
        "faces": [
            (0, 0, 0, 0, 0, 0),  # Vacía (33.33%)
            (0, 0, 0, 0, 0, 0),  # Vacía (33.33%)
            (1, 0, 0, 0, 0, 0),  # Éxito (16.67%)
            (0, 0, 1, 0, 0, 0),  # Ventaja (16.67%)
            (0, 0, 2, 0, 0, 0),  # Doble Ventaja (16.67%)
            (1, 0, 1, 0, 0, 0),  # Éxito + Ventaja (16.67%)
        ],
    },
    "g": {
        "name": "Habilidad",
        "color": "🟢",
        "faces": [
            (0, 0, 0, 0, 0, 0),  # Vacía (12.5%)
            (1, 0, 0, 0, 0, 0),  # Éxito (25%)
            (1, 0, 0, 0, 0, 0),  # Éxito (25%)
            (2, 0, 0, 0, 0, 0),  # Doble Éxito (12.5%)
            (0, 0, 1, 0, 0, 0),  # Ventaja (25%)
            (0, 0, 1, 0, 0, 0),  # Ventaja (25%)
            (1, 0, 1, 0, 0, 0),  # Éxito + Ventaja (12.5%)
            (0, 0, 2, 0, 0, 0),  # Doble Ventaja (12.5%)
        ],
    },
    "y": {
        "name": "Competencia",
        "color": "🟡",
        "faces": [
            (0, 0, 0, 0, 0, 0),  # Vacía (8.33%)
            (1, 0, 0, 0, 0, 0),  # Éxito (16.67%)
            (1, 0, 0, 0, 0, 0),  # Éxito (16.67%)
            (2, 0, 0, 0, 0, 0),  # Doble Éxito (25%)
            (2, 0, 0, 0, 0, 0),  # Doble Éxito (25%)
            (2, 0, 0, 0, 0, 0),  # Doble Éxito (25%)
            (0, 0, 1, 0, 0, 0),  # Ventaja (8.33%)
            (1, 0, 1, 0, 0, 0),  # Éxito + Ventaja (25%)
            (1, 0, 1, 0, 0, 0),  # Éxito + Ventaja (25%)
            (1, 0, 1, 0, 0, 0),  # Éxito + Ventaja (25%)
            (0, 0, 2, 0, 0, 0),  # Doble Ventaja (16.67%)
            (0, 0, 2, 0, 0, 0),  # Doble Ventaja (16.67%)
            (1, 0, 0, 0, 1, 0),  # Triunfo (8.33%)
        ],
    },
    "k": {
        "name": "Desventaja",
        "color": "⚫",
        "faces": [
            (0, 0, 0, 0, 0, 0),  # Vacía (33.33%)
            (0, 0, 0, 0, 0, 0),  # Vacía (33.33%)
            (0, 1, 0, 0, 0, 0),  # Fallo (33.33%)
            (0, 1, 0, 0, 0, 0),  # Fallo (33.33%)
            (0, 0, 0, 1, 0, 0),  # Amenaza (33.33%)
            (0, 0, 0, 1, 0, 0),  # Amenaza (33.33%)
        ],
    },
    "p": {
        "name": "Dificultad",
        "color": "🟣",
        "faces": [
            (0, 0, 0, 0, 0, 0),  # Vacía (12.5%)
            (0, 1, 0, 0, 0, 0),  # Fallo (12.5%)
            (0, 2, 0, 0, 0, 0),  # Doble Fallo (12.5%)
            (0, 0, 0, 1, 0, 0),  # Amenaza (37.5%)
            (0, 0, 0, 1, 0, 0),  # Amenaza (37.5%)
            (0, 0, 0, 1, 0, 0),  # Amenaza (37.5%)
            (0, 0, 0, 2, 0, 0),  # Doble Amenaza (12.5%)
            (0, 1, 0, 1, 0, 0),  # Fallo + Amenaza (12.5%)
        ],
    },
    "r": {
        "name": "Desafío",
        "color": "🔴",
        "faces": [
            (0, 0, 0, 0, 0, 0),  # Vacía (8.33%)
            (0, 1, 0, 0, 0, 0),  # Fallo (16.67%)
            (0, 1, 0, 0, 0, 0),  # Fallo (16.67%)
            (0, 2, 0, 0, 0, 0),  # Doble Fallo (16.67%)
            (0, 2, 0, 0, 0, 0),  # Doble Fallo (16.67%)
            (0, 0, 0, 1, 0, 0),  # Amenaza (16.67%)
            (0, 0, 0, 1, 0, 0),  # Amenaza (16.67%)
            (0, 1, 0, 1, 0, 0),  # Fallo + Amenaza (16.67%)
            (0, 1, 0, 1, 0, 0),  # Fallo + Amenaza (16.67%)
            (0, 0, 0, 2, 0, 0),  # Doble Amenaza (16.67%)
            (0, 0, 0, 2, 0, 0),  # Doble Amenaza (16.67%)
            (0, 1, 0, 0, 0, 1),  # Desesperación (8.33%)
        ],
    },
}

# ==================================================
# SÍMBOLOS (Actualizados con emojis de Discord)
# ==================================================

SYMBOLS = {
    "success": ":white_check_mark:",
    "failure": ":x:",
    "advantage": ":sparkles:",
    "threat": ":warning:",
    "triumph": ":star2:",
    "despair": ":skull:",
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

    # Cálculo de resultados netos
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