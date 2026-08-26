# tests/test_store.py
from datetime import date
import pytest
from agenda.store import Store

@pytest.fixture
def store(tmp_path):
    return Store(str(tmp_path / "t.db"))

def test_mensaje_de_captura(store):
    store.guardar_mensaje(date(2026, 8, 24), "captura", 111)
    store.guardar_mensaje(date(2026, 8, 24), "menu", 222)
    assert store.fecha_de_captura(111) == date(2026, 8, 24)
    assert store.fecha_de_captura(222) is None   # el menú no es captura
    assert store.fecha_de_captura(999) is None

def test_registrar_es_idempotente(store):
    d = date(2026, 8, 24)
    store.registrar(d, "paseo")
    store.registrar(d, "paseo")
    assert store.conteos(d, d) == {"paseo": 1}

def test_quitar(store):
    d = date(2026, 8, 24)
    store.registrar(d, "paseo")
    store.quitar(d, "paseo")
    assert store.conteos(d, d) == {}

def test_conteos_cuenta_dias_no_reacciones(store):
    store.registrar(date(2026, 8, 24), "dibujar")
    store.registrar(date(2026, 8, 25), "dibujar")
    store.registrar(date(2026, 8, 25), "casa")
    store.registrar(date(2026, 8, 31), "dibujar")   # fuera de rango
    assert store.conteos(date(2026, 8, 24), date(2026, 8, 28)) == {"dibujar": 2, "casa": 1}