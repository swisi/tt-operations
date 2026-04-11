# Cloudflare Tunnel mit Traefik

Dieses Dokument beschreibt die empfohlene Ingress-Struktur fuer den Tigers-Stack mit zwei getrennten Deployments:

- `beta` auf dem Entwickler-Laptop
- `prod` auf dem Proxmox-Host

## Zielbild

Die Kette lautet:

- Internet
- Cloudflare DNS und Edge
- `cloudflared`
- Traefik
- `tt-auth`, `tt-agenda`, `tt-analytics`

Cloudflare und Traefik sind dabei nicht doppelt.

- Cloudflare ist fuer DNS, TLS, WAF und Tunnel-Zugang zustaendig.
- Traefik ist fuer das interne Hostname-Routing im Docker-Stack zustaendig.

## Hostname-Modell

### Beta

- `auth-beta.thun-tigers.net`
- `agenda-beta.thun-tigers.net`
- `analytics-beta.thun-tigers.net`

### Produktion

- `auth.thun-tigers.net`
- `agenda.thun-tigers.net`
- `analytics.thun-tigers.net`

## Warum zwei getrennte Deployments

Beta und Produktion sollen nicht nur unterschiedliche Domains haben, sondern wirklich getrennte Laufzeitumgebungen:

- eigener `COMPOSE_PROJECT_NAME`
- eigener Cloudflare-Tunnel
- eigene Secrets
- eigene Datenbanken und Volumes
- eigene Host-Maschine oder mindestens eigener Deployment-Kontext

Fuer euren Fall bedeutet das:

- Beta: Entwickler-Laptop
- Produktion: Proxmox-Docker-Host

## Cloudflare-Vorbereitung

Pro Umgebung wird ein eigener Tunnel empfohlen.

### Beta-Tunnel

Beispielhafte Hostname-Zuordnung im Cloudflare-Tunnel:

- `auth-beta.thun-tigers.net` -> `http://traefik:80`
- `agenda-beta.thun-tigers.net` -> `http://traefik:80`
- `analytics-beta.thun-tigers.net` -> `http://traefik:80`

### Produktions-Tunnel

Beispielhafte Hostname-Zuordnung im Cloudflare-Tunnel:

- `auth.thun-tigers.net` -> `http://traefik:80`
- `agenda.thun-tigers.net` -> `http://traefik:80`
- `analytics.thun-tigers.net` -> `http://traefik:80`

Wichtig:

- Die Weiterleitung geht immer auf Traefik, nicht direkt auf die einzelnen Apps.
- Die eigentliche Service-Zuordnung uebernimmt Traefik dann anhand des `Host`-Headers.

## Beta auf dem Entwickler-Laptop

1. `.env.beta.example` nach `.env` kopieren.
2. `CLOUDFLARE_TUNNEL_TOKEN` fuer den Beta-Tunnel eintragen.
3. Falls noetig lokale Secrets und Passwoerter ersetzen.
4. Stack starten:

```bash
docker compose --profile analytics -f docker-compose.yml -f docker-compose.edge.yml up -d --build
```

5. In Cloudflare pruefen, dass die Beta-Hostnames auf den Beta-Tunnel zeigen.
6. Danach im Browser testen:

```text
https://auth-beta.thun-tigers.net
https://agenda-beta.thun-tigers.net
https://analytics-beta.thun-tigers.net
```

## Produktion auf Proxmox

1. Repository auf dem Proxmox-Host bereitstellen.
2. `.env.prod.example` nach `.env` kopieren.
3. `CLOUDFLARE_TUNNEL_TOKEN` fuer den Produktions-Tunnel eintragen.
4. Produktive Secrets, Datenbank-Passwoerter und Admin-Passwoerter setzen.
5. Stack starten:

```bash
docker compose --profile analytics -f docker-compose.yml -f docker-compose.edge.yml up -d --build
```

6. In Cloudflare pruefen, dass die Produktiv-Hostnames auf den Produktions-Tunnel zeigen.
7. Danach im Browser testen:

```text
https://auth.thun-tigers.net
https://agenda.thun-tigers.net
https://analytics.thun-tigers.net
```

## Was du hier lokal wirklich brauchst

Auf deinem aktuellen Entwickler-Laptop brauchst du fuer den extern erreichbaren Testbetrieb die Beta-Umgebung.

Das heisst konkret:

- `cp .env.beta.example .env`
- echten Beta-Tunnel-Token eintragen
- Beta-Domains in Cloudflare auf den Beta-Tunnel legen
- Edge-Compose mit Traefik und `cloudflared` starten

Wenn du dagegen nur lokal ohne Cloudflare entwickeln willst, bleibst du bei `.env.example` plus `docker-compose.local.yml`.

## Was spaeter auf Proxmox gebraucht wird

Auf dem Proxmox-Host nutzt du die Produktionsumgebung.

Das heisst konkret:

- `cp .env.prod.example .env`
- echten Produktions-Tunnel-Token eintragen
- produktive Domains in Cloudflare auf den Produktions-Tunnel legen
- Edge-Compose starten

## Empfohlene Reihenfolge

1. Beta lokal mit Cloudflare Tunnel lauffaehig machen.
2. Hostname-Routing und SSO-Endpunkte pruefen.
3. Dokumentierte `.env.prod.example` fuer Proxmox mit echten Secrets befuellen.
4. Produktionsdeployment getrennt aufsetzen.
5. Erst danach DNS fuer Produktion final aktivieren.