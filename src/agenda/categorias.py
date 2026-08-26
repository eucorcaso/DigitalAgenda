# src/agenda/categorias.py
from dataclasses import dataclass

# Los "keycap" de Discord son el dígito + U+FE0F + U+20E3.
def _keycap(n: int) -> str:
    return f"{n}️⃣"

@dataclass(frozen=True)
class Categoria:
    numero: int
    clave: str
    etiqueta: str
    emoji: str
    solo_captura: bool = False

CATEGORIAS: list[Categoria] = [
    Categoria(1, "paseo", "paseo", _keycap(1)),
    Categoria(2, "casa", "casa", _keycap(2)),
    Categoria(3, "dibujar", "dibujar", _keycap(3)),
    Categoria(4, "proyecto", "solo proyecto", _keycap(4), solo_captura=True),
]

EMOJIS_MENU = [c.emoji for c in CATEGORIAS if not c.solo_captura]
EMOJIS_CAPTURA = [c.emoji for c in CATEGORIAS]

def por_emoji(emoji: str) -> Categoria | None:
    for c in CATEGORIAS:
        if c.emoji == emoji:
            return c
    return None