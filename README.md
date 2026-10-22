# Cross-Domain Guard Service

A multi-tier, containerized security microservice built with **Python (FastAPI)**, **PostgreSQL/SQLite**, and **Docker/Podman** using Red Hat Enterprise Linux base images (**RHEL UBI 9**). 

Designed to model cross-domain security controls for naval surface and submarine command-and-control networks by enforcing automated access policies, non-bypassable information flow controls, and comprehensive audit logging.

---

## Key Features & Security Controls

* **Identification & Authentication**: Token-based client authentication mapping API credentials to security clearances (`UNCLASS`, `SECRET`).
* **Cross-Domain Flow Engine**: Non-bypassable policy engine enforcing high-to-low leakage prevention (low-to-high data transfer permitted; high-to-low blocked).
* **Audit Logging**: SQLite/PostgreSQL-backed operational log recording decision timestamps, client identities, attempted cross-domain flows, and pass/fail reasons.
* **Red Hat Container Security**: Built on `ubi9/python-311` base images to align with Red Hat Enterprise Linux (RHEL) security requirements.

---

## Architecture & Data Flow

```text
 Client Request (API Key)
        │
        ▼
 ┌──────────────┐
 │ FastAPI App  │ ──► Auth Check (Validate clearance vs. payload label)
 └──────┬───────┘
        │
        ▼
 ┌──────────────┐
 │ Guard Engine │ ──► Flow Validation (Ensure low-to-high flow direction)
 └──────┬───────┘
        │
        ▼
 ┌──────────────┐
 │ Database Log │ ──► Audit Record (Timestamp, client ID, status, reason)
 └──────────────┘
