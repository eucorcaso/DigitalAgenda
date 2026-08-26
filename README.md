# DigitalAgenda v1

Bot de Discord que ofrece (17:00) y registra (21:00), lunes a viernes. Spec: `docs/spec-v1.md`.

## Crear el bot en Discord
1. https://discord.com/developers/applications → New Application → Bot → Reset Token → copiar a `.env`.
2. OAuth2 → URL Generator: scope `bot`; permisos `View Channel`, `Send Messages`, `Add Reactions`, `Read Message History`. Abrir la URL e invitarlo a tu servidor.
3. Crear canal privado `#agenda`; dar acceso al bot. Modo desarrollador en Discord → clic derecho en el canal → Copy Channel ID → `CHANNEL_ID` en `.env`.

## Local

    cp .env.example .env   # rellenar
    uv sync
    uv run pytest
    uv run --env-file .env python -m agenda

## VPS (Linux con systemd)

    # una vez: usuario de servicio y uv
    sudo useradd -r -m -d /opt/agenda -s /bin/bash agenda
    sudo -iu agenda bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'

    # código y dependencias
    sudo -iu agenda git clone https://github.com/eucorcaso/DigitalAgenda.git /opt/agenda/app
    sudo -iu agenda bash -c 'cd /opt/agenda/app && ~/.local/bin/uv sync --no-dev'

    # secretos
    sudo -iu agenda cp /opt/agenda/app/.env.example /opt/agenda/app/.env
    sudo -iu agenda nano /opt/agenda/app/.env

    # servicio
    sudo cp /opt/agenda/app/deploy/agenda.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now agenda
    journalctl -u agenda -f      # debe decir: conectado como <bot>

Actualizar tras un push:

    sudo -iu agenda bash -c 'cd /opt/agenda/app && git pull && ~/.local/bin/uv sync --no-dev'
    sudo systemctl restart agenda
