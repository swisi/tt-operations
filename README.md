# tt-operations

Operations- und Plattform-Repository fuer den Tigers Microservice-Stack.

## Zweck

Dieses Repository enthaelt die zentrale Infrastruktur fuer:

- Docker Compose Stack
- Umgebungsvariablen
- Betriebsdokumentation
- Architekturuebersichten
- Deployment-Vorbereitung

Die fachlichen Anwendungen bleiben in separaten Repositories:

- `tt-auth`
- `tt-agenda`
- `tt-analytics`

## Zielbild

`tt-auth` ist der zentrale Identity- und Access-Service. Fachliche Anwendungen wie `tt-agenda` und `tt-analytics` werden als eigenstaendige Services betrieben und ueber den zentralen Stack orchestriert.

## Struktur

- `docker-compose.yml` zentraler Compose-Stack
- `.env.example` Beispiel fuer benoetigte Umgebungsvariablen
- `docs/architecture.md` Zielarchitektur
- `docs/stack-architecture.md` detaillierte Plattform-Architektur
- `docs/operations.md` Betriebs- und Deployment-Hinweise
- `docs/data-migration.md` Datenmigration von SQLite nach PostgreSQL

## Schnellstart

1. Repositories fuer `tt-auth`, `tt-agenda` und spaeter `tt-analytics` lokal neben dieses Repo legen oder als externe Images verwenden.
2. `.env.example` nach `.env` kopieren und Werte setzen.
3. Pfade oder Image-Namen im `docker-compose.yml` anpassen.
4. Stack starten:

```bash
docker compose up -d --build
```

## Hinweise

- Die Compose-Datei verwendet fuer `tt-auth` und `tt-agenda` zunaechst relative Build-Pfade `../tt-auth` und `../tt-agenda`.
- `tt-analytics` ist als Platzhalter vorbereitet.
- Fuer Produktion sollten HTTPS, Reverse Proxy, Redis und vernuenftiges Secret-Handling ergaenzt werden.
