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

## Persistenz und Backups

Die Datenbanken laufen in eigenen Docker-Volumes:

- `postgres-auth-data`
- `postgres-agenda-data`
- `postgres-analytics-data`

Dadurch bleiben die Daten getrennt von den Applikationscontainern persistent. Fuer regelmaessige Backups sollte nicht das App-Dateisystem, sondern das jeweilige Postgres-Volume bzw. ein `pg_dump`-Prozess gesichert werden.

Empfohlener Weg:

- regelmaessige logische Dumps mit `pg_dump`
- zusaetzlich optional volumenbasierte Snapshots auf Host- oder Storage-Ebene
- Restore nicht in der App, sondern ueber `psql` oder `pg_restore`

## Aktivierung von Analytics

```bash
docker compose --profile analytics up -d
```

## Naechste Plattform-Schritte

- Reverse Proxy mit Traefik oder Nginx hinzufuegen
- Redis fuer Rate Limiting und Jobs hinzufuegen
- produktionsreife Secret-Verwaltung einfuehren
- CI/CD fuer Compose-Validierung und Deployment ergaenzen
