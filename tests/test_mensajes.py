from agenda.categorias import CATEGORIAS, por_emoji, EMOJIS_MENU, EMOJIS_CAPTURA

def test_categorias_fijas():
    assert [c.clave for c in CATEGORIAS] == ["paseo", "casa", "dibujar", "proyecto"]

def test_proyecto_solo_en_captura():
    assert len(EMOJIS_MENU) == 3
    assert len(EMOJIS_CAPTURA) == 4

def test_por_emoji():
    assert por_emoji("1️⃣").clave == "paseo"
    assert por_emoji("🍕") is None

from datetime import date
from agenda.mensajes import menu, captura, resumen

def test_menu():
    assert menu() == "1️⃣ paseo · 2️⃣ casa · 3️⃣ dibujar · resto: proyecto"

def test_captura():
    assert captura() == "¿Qué tocaste hoy? 1️⃣ paseo · 2️⃣ casa · 3️⃣ dibujar · 4️⃣ solo proyecto"

def test_resumen_formato():
    txt = resumen(date(2026, 8, 24), date(2026, 8, 28),
                  {"paseo": 2, "casa": 1, "dibujar": 3, "proyecto": 1})
    assert txt == "Semana 24–28 ago\npaseo 2 · casa 1 · dibujar 3 · solo proyecto 1"

def test_resumen_sin_datos_no_juzga():
    txt = resumen(date(2026, 8, 24), date(2026, 8, 28), {})
    assert txt == "Semana 24–28 ago\npaseo 0 · casa 0 · dibujar 0 · solo proyecto 0"