# src/agenda/bot.py
import logging
import os

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from . import mensajes
from .categorias import EMOJIS_CAPTURA, EMOJIS_MENU, por_emoji
from .semana import TZ, hoy, lunes_viernes
from .store import Store

log = logging.getLogger("agenda")


class Agenda(discord.Client):
    def __init__(self, channel_id: int, store: Store):
        intents = discord.Intents.default()   # incluye guild_reactions; no hace falta message_content
        super().__init__(intents=intents)
        self.channel_id = channel_id
        self.store = store
        self.scheduler = AsyncIOScheduler(timezone=TZ)

    async def setup_hook(self) -> None:
        # Se ejecuta una vez, antes de conectar. Aquí se arma el reloj.
        self.scheduler.add_job(self.enviar_menu,
                               CronTrigger(day_of_week="mon-fri", hour=17, minute=0))
        self.scheduler.add_job(self.enviar_captura,
                               CronTrigger(day_of_week="mon-fri", hour=21, minute=0))
        self.scheduler.start()

    async def on_ready(self) -> None:
        log.info("conectado como %s", self.user)

    # --- emisión -------------------------------------------------------

    async def _canal(self) -> discord.TextChannel:
        return self.get_channel(self.channel_id) or await self.fetch_channel(self.channel_id)

    async def _enviar(self, tipo: str, texto: str, emojis: list[str]) -> discord.Message:
        canal = await self._canal()
        msg = await canal.send(texto)
        for e in emojis:              # pre-poner las reacciones = respuesta de un tap
            await msg.add_reaction(e)
        self.store.guardar_mensaje(hoy(), tipo, msg.id)
        return msg

    async def enviar_menu(self) -> None:
        await self._enviar("menu", mensajes.menu(), EMOJIS_MENU)

    async def enviar_captura(self) -> None:
        await self._enviar("captura", mensajes.captura(), EMOJIS_CAPTURA)
        if hoy().weekday() == 4:      # viernes: el resumen va pegado a la captura
            lunes, viernes = lunes_viernes(hoy())
            conteos = self.store.conteos(lunes, viernes)
            canal = await self._canal()
            await canal.send(mensajes.resumen(lunes, viernes, conteos))

    # --- captura por reacciones ---------------------------------------

    def _categoria_de(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.user.id:          # nuestras propias pre-reacciones
            return None
        fecha = self.store.fecha_de_captura(payload.message_id)
        if fecha is None:                            # no es una captura (p.ej. es el menú)
            return None
        cat = por_emoji(str(payload.emoji))
        return (fecha, cat.clave) if cat else None

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        if hit := self._categoria_de(payload):
            self.store.registrar(*hit)

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent) -> None:
        if hit := self._categoria_de(payload):
            self.store.quitar(*hit)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    token = os.environ["DISCORD_TOKEN"]
    channel_id = int(os.environ["CHANNEL_ID"])
    store = Store(os.environ.get("DB_PATH", "agenda.db"))
    Agenda(channel_id, store).run(token, log_handler=None)