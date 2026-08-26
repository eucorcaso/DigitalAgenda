# src/agenda/store.py
import sqlite3
from datetime import date

_SCHEMA = """
CREATE TABLE IF NOT EXISTS mensajes (
    fecha TEXT NOT NULL,
    tipo TEXT NOT NULL,
    message_id INTEGER PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS capturas (
    fecha TEXT NOT NULL,
    categoria TEXT NOT NULL,
    PRIMARY KEY (fecha, categoria)
);
"""

class Store:
    def __init__(self, path: str):
        self._db = sqlite3.connect(path)
        self._db.executescript(_SCHEMA)

    def guardar_mensaje(self, fecha: date, tipo: str, message_id: int) -> None:
        with self._db:
            self._db.execute(
                "INSERT OR REPLACE INTO mensajes VALUES (?, ?, ?)",
                (fecha.isoformat(), tipo, message_id))

    def fecha_de_captura(self, message_id: int) -> date | None:
        row = self._db.execute(
            "SELECT fecha FROM mensajes WHERE message_id = ? AND tipo = 'captura'",
            (message_id,)).fetchone()
        return date.fromisoformat(row[0]) if row else None

    def registrar(self, fecha: date, categoria: str) -> None:
        with self._db:
            self._db.execute(
                "INSERT OR IGNORE INTO capturas VALUES (?, ?)",
                (fecha.isoformat(), categoria))

    def quitar(self, fecha: date, categoria: str) -> None:
        with self._db:
            self._db.execute(
                "DELETE FROM capturas WHERE fecha = ? AND categoria = ?",
                (fecha.isoformat(), categoria))

    def conteos(self, desde: date, hasta: date) -> dict[str, int]:
        rows = self._db.execute(
            "SELECT categoria, COUNT(DISTINCT fecha) FROM capturas "
            "WHERE fecha BETWEEN ? AND ? GROUP BY categoria",
            (desde.isoformat(), hasta.isoformat())).fetchall()
        return {cat: n for cat, n in rows}