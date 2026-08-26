# tests/test_semana.py
from datetime import date
from agenda.semana import lunes_viernes

def test_lunes_viernes_desde_miercoles():
    assert lunes_viernes(date(2026, 8, 26)) == (date(2026, 8, 24), date(2026, 8, 28))

def test_lunes_viernes_desde_viernes():
    assert lunes_viernes(date(2026, 8, 28)) == (date(2026, 8, 24), date(2026, 8, 28))