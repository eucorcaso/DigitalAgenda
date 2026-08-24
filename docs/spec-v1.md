# DigitalAgenda v1 — Spec

Destilada de la conversación de diseño del 2026-08-24.

## Problema

La tarde libre (18:00–21:00, 3h) se va íntegra a proyectos → cena tarde → cama
tarde → sedentarismo. El tiempo existe; falta un reparto a la entrada.

## Qué es

Un bot de Discord que **ofrece y registra**. No planifica, no exige, no juzga.

## Ciclo (lunes a viernes, hora de Madrid)

| hora | mensaje | respuesta |
|---|---|---|
| 17:00 | **Menú**: `1) paseo · 2) casa · 3) dibujar · resto: proyecto` | reacción opcional 1/2/3. Ignorar es legítimo. No insiste. |
| 21:00 | **Captura** (sobre el ancla de la cena): "¿qué tocaste hoy?" mismos números + `4) solo proyecto` | multi-reacción. Todas las combinaciones son válidas. Tocar cuenta, sin duraciones. |
| viernes 21:00 | **Resumen** tras la captura: conteo de días por categoría en la semana | ninguna |

- Fin de semana: silencio total.
- Lo que pasa después de cenar no se registra.
- El texto que Corco escriba en el canal es feedback; el bot lo ignora, queda en el historial.

## Categorías (fijas en v1)

| nº | clave | etiqueta |
|---|---|---|
| 1 | paseo | paseo |
| 2 | casa | casa (limpiar, ordenar) |
| 3 | dibujar | dibujar |
| 4 | proyecto | solo proyecto (solo en captura) |

## Invariantes

1. **No castiga.** Sin rachas, sin rojo, sin recordatorios repetidos, sin comparar con
   la semana anterior. Mide variedad, no cumplimiento.
2. **Un solo ancla real:** cena a las 21:00. Todo lo demás es oferta.
3. **Cero LLM en el ciclo diario.** Determinista y gratis.
4. **Sin dashboard.** El historial del canal es la consulta.
5. **Fuera de v1:** second brain, dieta, gestión de proyectos, fin de semana, duraciones,
   menú variable.

## Resumen del viernes (formato)

```
Semana 24–28 ago
paseo 2 · casa 1 · dibujar 3 · solo proyecto 1
```

Un día cuenta en una categoría si tuvo esa reacción en la captura. Un día sin reacción no
aparece en ningún conteo ni se menciona.

## Técnica

- Python ≥3.12, `discord.py`, `APScheduler`, SQLite, `uv`.
- Bot propio (token propio), un único canal privado `#agenda` en servidor de Corco.
- Permisos mínimos: enviar mensajes, añadir reacciones, leer reacciones en ese canal.
- Corre como servicio `systemd` en el VPS de Corco.
- Config por variables de entorno: `DISCORD_TOKEN`, `CHANNEL_ID`, `TZ=Europe/Madrid`.
- Datos: SQLite `agenda.db`, tabla `capturas(fecha, categoria)`, y `mensajes(fecha, tipo,
  message_id)` para reconciliar reacciones tras reinicios.

## Criterio de éxito de la semana 1

Contestar la captura de las 21:00 **4 de 5 días**, con cualquier reacción. Menos → se
rediseña el toque (hora, forma, canal), no se añade nada. Más el feedback en el canal.
