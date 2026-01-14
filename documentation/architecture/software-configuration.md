---
project_name: [PROJECT_NAME]
title: Software and dependencies.
description:
last_updated: [YYYY-MM-DD]
clear_doc_version: 2.1.0
status:
keywords: [development, setup, environment, contributing, testing]
---


# {SYSTEM} Software Configuration

This document catalogs all software packages installed on the {SYSTEM}, their purposes, deployment use cases, and future extensibility options.

---

## {SYSTEM}
### Base System
- **OS:**
- **Kernel:**
- **SSH:**
- **Package Manager:**

---

## Supporting Packages

'''
EXAMPLE ENTRY

### Tailscale
Mesh VPN and zero-trust access layer for secure remote connection to the homelab network without exposing services to the internet.

#### Zero-Trust SSH Access
Provides SSH connectivity over encrypted Tailscale subnet (100.x.x.x) with built-in key-based authentication via `tailscale up --ssh`. Replaces direct LAN SSH exposure.

#### Unified Network Mesh
Connects Ubuntu-LLM to Proxmox, TrueNAS, and monitoring stack via a single encrypted virtual network. Simplifies cross-VM communication and remote access from outside the LAN.

#### Other Use Cases
- Site-to-site VPN between multiple homelabs or remote datacenters
- Mobile/laptop access to LLM inference APIs without exposing ports
- DNS resolution within tailnet (MagicDNS)
- Exit node for routing traffic through homelab
'''

---

### {PACKAGE}
{Brief description}

#### {PURPOSE ONE}
{Brief description}

#### {PURPOSE TWO}
{Brief description}

#### Other Use Cases
- {PURPOSE THREE}
- {PURPOSE FOUR}
- ...

---

### {PACKAGE}
{Brief description}

#### {PURPOSE ONE}
{Brief description}

#### {PURPOSE TWO}
{Brief description}

#### Other Use Cases
- {PURPOSE THREE}
- {PURPOSE FOUR}
- ...

---
