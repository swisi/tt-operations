# Operations

## Lokale Entwicklung

Voraussetzungen:

- Docker und Docker Compose
- lokale Checkouts von `tt-auth` und `tt-agenda` neben diesem Repository

## Start

```bash
cp .env.example .env
docker compose --profile analytics -f docker-compose.yml -f docker-compose.local.yml up -d --build
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

## Deployment-Modi

### Lokale Direktnutzung

Fuer lokale Entwicklung ohne Reverse Proxy:

```bash
cp .env.example .env
docker compose --profile analytics -f docker-compose.yml -f docker-compose.local.yml up -d --build
```

### Beta via Traefik und Cloudflare Tunnel

Beta ist fuer den Entwickler-Laptop oder einen dedizierten Test-Host gedacht:

```bash
cp .env.beta.example .env
docker compose --profile analytics -f docker-compose.yml -f docker-compose.edge.yml up -d --build
```

### Produktion via Traefik und Cloudflare Tunnel

Produktion ist fuer den separaten Proxmox-Host gedacht:

```bash
cp .env.prod.example .env
docker compose --profile analytics -f docker-compose.yml -f docker-compose.edge.yml up -d --build
```

Die Umgebungen werden ueber unterschiedliche Werte fuer `COMPOSE_PROJECT_NAME`, Tunnel-Token, Domains und Secrets sauber getrennt.

## Aktivierung von Analytics

```bash
docker compose --profile analytics -f docker-compose.yml -f docker-compose.local.yml up -d
```

## Naechste Plattform-Schritte

- Redis fuer Rate Limiting und Jobs hinzufuegen
- produktionsreife Secret-Verwaltung einfuehren
- CI/CD fuer Compose-Validierung und Deployment ergaenzen

## Reverse Proxy und Tunnel

- Cloudflare bleibt der externe Edge-Layer fuer DNS, TLS, WAF und Tunnel-Terminierung.
- `cloudflared` bringt den Traffic in den Docker-Stack.
- Traefik bleibt intern sinnvoll und ist nicht doppelt: es uebernimmt Hostname-Routing, Docker-Service-Discovery und Ingress-Logik zwischen `tt-auth`, `tt-agenda` und `tt-analytics`.
- Pfadbasiertes Routing wurde bewusst nicht als Standardmodell gewaehlt, weil die bestehenden Apps sauberer ueber eigene Subdomains betrieben werden koennen.
- Eine konkrete Schritt-fuer-Schritt-Anleitung fuer Beta und Produktion steht in `docs/cloudflare-tunnel.md`.
