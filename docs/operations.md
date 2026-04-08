# Operations

## Lokale Entwicklung

Voraussetzungen:

- Docker und Docker Compose
- lokale Checkouts von `tt-auth` und `tt-agenda` neben diesem Repository

## Start

```bash
cp .env.example .env
docker compose up -d --build
```

## Erwartete Struktur

```text
tigers/
  tt-auth/
  tt-agenda/
  tt-operations/
```

## Wichtige Hinweise

- `tt-auth` und `tt-agenda` muessen auf `SQLALCHEMY_DATABASE_URI` aus der Umgebung reagieren.
- `tt-agenda` enthaelt aktuell noch SQLite-spezifische Backup-Logik und muss fuer Postgres weiter angepasst werden.
- `tt-analytics` ist im Compose-Stack als Platzhalter vorbereitet und wird ueber das Profil `analytics` aktiviert.

## Aktivierung von Analytics

```bash
docker compose --profile analytics up -d
```

## Naechste Plattform-Schritte

- Reverse Proxy mit Traefik oder Nginx hinzufuegen
- Redis fuer Rate Limiting und Jobs hinzufuegen
- produktionsreife Secret-Verwaltung einfuehren
- CI/CD fuer Compose-Validierung und Deployment ergaenzen
