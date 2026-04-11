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
- `docs/cloudflare-tunnel.md` Tunnel- und Hostname-Setup fuer Beta und Produktion
- `docs/data-migration.md` Datenmigration von SQLite nach PostgreSQL

## Schnellstart

1. Repositories fuer `tt-auth`, `tt-agenda` und spaeter `tt-analytics` lokal neben dieses Repo legen oder als externe Images verwenden.
2. `.env.example` nach `.env` kopieren und Werte setzen.
3. Pfade oder Image-Namen im `docker-compose.yml` anpassen.
4. Lokalen Direktzugriff starten:

```bash
docker compose --profile analytics -f docker-compose.yml -f docker-compose.local.yml up -d --build
```

## Deployment-Modi

- `docker-compose.yml`: gemeinsamer Basis-Stack ohne oeffentliche App-Ports
- `docker-compose.local.yml`: lokaler Direktzugriff ueber `localhost:8085/8086/8087`
- `docker-compose.edge.yml`: Ingress ueber Traefik plus `cloudflared`

### Beta auf dem Entwickler-Laptop

```bash
cp .env.beta.example .env
docker compose --profile analytics -f docker-compose.yml -f docker-compose.edge.yml up -d --build
```

### Produktion auf Proxmox

```bash
cp .env.prod.example .env
docker compose --profile analytics -f docker-compose.yml -f docker-compose.edge.yml up -d --build
```

Beta und Produktion laufen als getrennte Deployments ueber unterschiedliche `COMPOSE_PROJECT_NAME`-, Hostname- und Tunnel-Konfigurationen.

## Hinweise

- Die Compose-Dateien verwenden fuer `tt-auth`, `tt-agenda` und `tt-analytics` relative Build-Pfade in benachbarte Repositories.
- Feste `container_name`-Eintraege wurden bewusst entfernt, damit Beta und Produktion parallel als getrennte Compose-Projekte betrieben werden koennen.
- Fuer Edge-Betrieb uebernimmt Cloudflare den externen Zugang, waehrend Traefik intern per Hostname an die Services weiterleitet.
