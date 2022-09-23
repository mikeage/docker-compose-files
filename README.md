# Docker Compose Repository Documentation

## Overview
This repository contains a collection of Docker Compose configurations for managing various services and applications. Deployments are managed with `doco-cd`, with one host-specific deployment target per machine.

## Repository Structure
Each subdirectory contains the files needed to deploy a specific stack, typically including:
- `compose.yaml`: Service configuration
- `.env` or `*.env`: Environment variables when needed
- Supporting files such as `Dockerfile`, scripts, configs, or application assets for stacks that need them

## Configuration Files
- `.doco-cd.g4-gpu.yaml`, `.doco-cd.openmediavault.yaml`, `.doco-cd.vm1.yaml`: Host-specific deployment targets for `doco-cd`
- `doco-cd/`: Stack for running `doco-cd` itself in polling mode against this repository
- Service-specific `.env` files: Contain environment variables needed for each service

  ## Services

  | Service | Description |
  |---------|-------------|
  | **Media Management** ||
  | jellyfin | Media server for movies, TV, music, and more |
  | navidrome | Music server and streamer compatible with Subsonic/Airsonic |
  | photoprism | Photo management with AI features |
  | piwigo | Photo gallery management system |
  | immich | Self-hosted photo and video backup platform |
  | photo-gallery | Lightweight photo gallery stack |
  | **\*Arr Applications** ||
  | bazarr | Subtitle downloader for Radarr and Sonarr |
  | lidarr | Music collection manager |
  | prowlarr | Indexer manager and proxy |
  | radarr | Movie collection manager |
  | readarr | Book collection manager |
  | sonarr | TV series management |
  | search-not-foundarr | Search helper for missing media |
  | **Content Libraries & Tools** ||
  | audiobookshelf | Self-hosted audiobook and podcast server |
  | calibre-web | Web app for browsing, reading, and downloading eBooks |
  | kapowarr | Comic book management and reading |
  | komga | Media server for comics and manga |
  | picard | Music tagger and metadata organizer |
  | pinchflat | YouTube downloader and media archiver |
  | bentopdf | Web-to-PDF conversion service |
  | **File Sharing & Storage** ||
  | nextcloud | File hosting and collaboration platform |
  | paperless-ngx | Document management system |
  | paperless-ngx-gavriel | Separate Paperless-ngx deployment for Gavriel |
  | psitransfer | Simple file sharing service |
  | wordpress | Content management system |
  | vaultwarden | Self-hosted Bitwarden-compatible password manager |
  | **Torrenting & Downloads** ||
  | autobrr | Automation for tracker-driven download workflows |
  | cross-seed | Tool for cross-seeding torrents across trackers |
  | myanonamouse | Automatically update MAM_ID cookie for MyAnonamouse |
  | qbittorrent | qBittorrent stack with multiple dedicated instances |
  | transmission | BitTorrent client |
  | qui | Lightweight UI for Autobrr |
  | **Home Automation & IoT** ||
  | frigate | NVR with real-time object detection for IP cameras |
  | homeassistant | Open source home automation platform |
  | mosquitto | MQTT broker for IoT applications |
  | room-assistant | Presence detection for home automation |
  | octoeverywhere | Remote access for 3D printers |
  | **Aviation & Tracking** ||
  | fr24feed | ADS-B client for Flightradar24 |
  | ultrafeeder | ADS-B and aircraft tracking feeder stack |
  | ultrafeederPF | PlaneFence-oriented feeder stack |
  | **Dashboards & Monitoring** ||
  | cyd-monitor | Host metrics exporter |
  | homarr | Dashboard for self-hosted services |
  | patchmon | Patch and package monitoring stack |
  | uptime-kuma | Uptime monitoring tool |
  | whatsrunning | Container status dashboard |
  | **Productivity & Organization** ||
  | escher | Custom gallery application |
  | freshrss | RSS feed aggregator and reader |
  | joplin | Note-taking and to-do application |
  | karakeep | Bookmarking and knowledge capture tool |
  | seerr | Media request management |
  | **Mail, Network, and Access** ||
  | consul | Service networking and discovery |
  | dovecot | Mail server components |
  | getmail6 | Mail retrieval service |
  | headscale | Self-hosted Tailscale control server |
  | registrator | Dynamic service registration helper |
  | roundcube | Webmail interface |
  | rspamd | Mail filtering stack |
  | tailscale-router | Tailscale-based routing container |
  | traefik-kop | Reverse proxy and ingress stack |
  | **System Tools** ||
  | autoheal | Automatically restarts unhealthy containers |
  | rsyslog-dockerlogs | Centralized Docker log forwarding |
## Deployment
Deployments are organized per host with `doco-cd` target files at the repository root:

- `.doco-cd.g4-gpu.yaml`
- `.doco-cd.openmediavault.yaml`
- `.doco-cd.vm1.yaml`

The `doco-cd` stack lives in [doco-cd/README.md](/Users/mikemi/src/docker-compose-files/doco-cd/README.md). It polls this repository over SSH and selects the correct host target with `DOCO_TARGET`.
