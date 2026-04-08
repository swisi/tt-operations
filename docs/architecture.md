# Architektur

## Rolle des Repositories

`tt-operations` ist das zentrale Plattform-Repository fuer Infrastruktur, Deployment und Betriebsdokumentation.

## Repositories

- `tt-auth` zentrale Benutzerverwaltung und Service-Zugriff
- `tt-agenda` Trainings- und Agenda-Service
- `tt-analytics` Analytics- und Reporting-Service
- `tt-operations` Compose, Ops, Deployment, Doku

## Zielarchitektur

- zentrale Anmeldung in `tt-auth`
- Service-Start ueber `tt-auth`
- kurzlebige SSO-Tokens fuer Zielservices
- je Service eigene Postgres-Datenbank
- spaeter optional Reverse Proxy, Redis, Monitoring

Die ausfuehrliche Version liegt in `docs/stack-architecture.md`.

## Datenbankstrategie

Jeder Service bekommt seine eigene Datenbank:

- `tt-postgres-auth`
- `tt-postgres-agenda`
- `tt-postgres-analytics`

Dadurch bleiben Datenmodell, Migrationen und Deployments entkoppelt.

## Netzwerk

Alle Container laufen im internen Docker-Netz `tigers-internal`. Exponiert werden nur benoetigte Ports oder spaeter ausschliesslich der Reverse Proxy.
