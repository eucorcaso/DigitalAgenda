# src/agenda/mensajes.py
from datetime import date
from .categorias import CATEGORIAS

_MESES = ["ene", "feb", "mar", "abr", "may", "jun",
          "jul", "ago", "sep", "oct", "nov", "dic"]

def _linea(cats) -> str:
    return " · ".join(f"{c.emoji} {c.etiqueta}" for c in cats)

def menu() -> str:
    cats = [c for c in CATEGORIAS if not c.solo_captura]
    return f"{_linea(cats)} · resto: proyecto"

def captura() -> str:
    return f"¿Qué tocaste hoy? {_linea(CATEGORIAS)}"

def resumen(lunes: date, viernes: date, conteos: dict[str, int]) -> str:
    # Sin comparar, sin objetivo, sin flechas: solo contar.
    cabecera = f"Semana {lunes.day}–{viernes.day} {_MESES[viernes.month - 1]}"
    partes = [f"{c.etiqueta} {conteos.get(c.clave, 0)}" for c in CATEGORIAS]
    return f"{cabecera}\n{' · '.join(partes)}"