from agenda.categorias import CATEGORIAS, por_emoji, EMOJIS_MENU, EMOJIS_CAPTURA

def test_categorias_fijas():
    assert [c.clave for c in CATEGORIAS] == ["paseo", "casa", "dibujar", "proyecto"]

def test_proyecto_solo_en_captura():
    assert len(EMOJIS_MENU) == 3
    assert len(EMOJIS_CAPTURA) == 4

def test_por_emoji():
    assert por_emoji("1️⃣").clave == "paseo"
    assert por_emoji("🍕") is None