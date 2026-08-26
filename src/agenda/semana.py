# src/agenda/semana.py
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Dublin")

def hoy() -> date:
    return datetime.now(TZ).date()

def lunes_viernes(d: date) -> tuple[date, date]:
    lunes = d - timedelta(days=d.weekday())
    return lunes, lunes + timedelta(days=4)