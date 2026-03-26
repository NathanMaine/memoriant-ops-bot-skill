[English](README.md) | [Deutsch](README.de.md) | [Nederlands](README.nl.md) | [Francais](README.fr.md) | [Russkij](README.ru.md) | [Espanol](README.es.md) | [Portugues](README.pt.md)

<p align="center">
  <img src="docs/images/mops-logo.jpeg" alt="MOPS" width="280">
</p>

<h1 align="center">MOPS</h1>

<p align="center">
  <em>KI-Agenten mit mehreren Anbietern direkt vom Handy steuern.</em>
</p>

<p align="center">
  <a href="#schnellstart">Schnellstart</a> &middot;
  <a href="#so-funktionierts">So funktioniert's</a> &middot;
  <a href="#funktionen">Funktionen</a> &middot;
  <a href="docs/use-cases.md">Anwendungsfälle</a> &middot;
  <a href="docs/installation.md">Installationsanleitung</a> &middot;
  <a href="docs/architecture.md">Architektur</a>
</p>

<p align="center">
  <img src="https://github.com/NathanMaine/memoriant-ops-bot/actions/workflows/tests.yml/badge.svg" alt="Tests">
  <img src="https://img.shields.io/badge/providers-Claude%20%7C%20Codex%20%7C%20Gemini-blue" alt="Anbieter">
  <img src="https://img.shields.io/badge/transport-Telegram%20%7C%20Matrix-green" alt="Transport">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="Lizenz">
  <img src="https://img.shields.io/badge/python-3.11%2B-yellow" alt="Python">
  <img src="https://img.shields.io/pypi/v/memoriant-ops-bot" alt="PyPI">
</p>

---

Starte Claude Code, OpenAI Codex CLI oder Google Gemini CLI von Telegram oder Matrix aus. Nutzt ausschliesslich offizielle CLIs als Subprozesse -- nichts gefaelscht, nichts proxiert. Dein Abo, dein Rechner, deine Daten.

<p align="center">
  <img src="docs/images/mops-demo.gif" alt="MOPS Demo" width="300">
</p>

> **Veroeffentlicht am 12. Maerz 2026** -- fuenf Tage bevor Anthropic [Claude Dispatch](https://mlq.ai/news/anthropic-launches-claude-dispatch-for-remote-desktop-ai-control/) herausbrachte. Gleiches Konzept, andere Philosophie.

### Wie unterscheidet sich das von Claude Dispatch?


|  | MOPS | Claude Dispatch |
|---|---|---|
| **Anbieter** | Claude + Codex + Gemini | Nur Claude |
| **Kosten** | Kostenlos -- nutzt deine bestehenden Abos | Max-Tarif erforderlich (100+ $/Monat) |
| **Fernzugriff von** | Telegram, Matrix, jedem Geraet | Claude Mobile App |
| **Steuert** | Jeden Rechner -- Server, GPU-Rigs, Cloud | Nur Mac-Desktop |
| **Parallele Agenten** | Unbegrenzt -- Themen, Sitzungen, Sub-Agenten | Einzelnes Gespraech |
| **Open Source** | MIT | Proprietaer |
| **Hintergrundaufgaben** | Ja, mit Delegation + Rueckmeldungen | Ja |
| **Benannte Sitzungen** | Ja | Nein |
| **Plugin-System** | Ja -- Discord, Slack, Signal erweiterbar | Nein |

---

## Schnellstart

**Schritt 1: Python installieren** (ueberspringen, wenn Python 3.11+ bereits vorhanden)

```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Windows — herunterladen von https://www.python.org/downloads/
# ✅ "Add Python to PATH" bei der Installation aktivieren
```

**Schritt 2: pipx installieren** (ein Werkzeug fuer Python-Apps)

```bash
# macOS
brew install pipx && pipx ensurepath

# Linux
pip install pipx && pipx ensurepath

# Windows
pip install pipx
pipx ensurepath
```

> Nach `pipx ensurepath` das **Terminal schliessen und neu oeffnen**.

**Schritt 3: MOPS installieren**

```bash
pipx install memoriant-ops-bot
```

**Schritt 4: Mindestens ein AI-CLI installieren** (der Agent, den MOPS steuert)

```bash
# Eines oder mehrere:
npm install -g @anthropic-ai/claude-code && claude auth     # Claude
npm install -g @openai/codex && codex auth                   # Codex
npm install -g @google/gemini-cli                            # Gemini
```

> Node.js fehlt? Zuerst installieren: `brew install node` (macOS) oder `sudo apt install nodejs npm` (Linux) oder von [nodejs.org](https://nodejs.org)

**Schritt 5: Telegram-Bot-Token erstellen** — siehe [Telegram-Einrichtung](docs/telegram-setup.md)

**Schritt 6: MOPS starten**

```bash
mops
```

Der Einrichtungsassistent fuehrt dich durch Transport-Setup (Telegram oder Matrix), Zeitzone, optionale Docker-Sandbox und Installation als Hintergrunddienst.

---

## So funktioniert's

MOPS startet offizielle CLI-Binaries als Subprozesse und verbindet sie mit deiner Messaging-Plattform. Keine API-Schluessel, keine SDK-Patches, keine gefaelschten Header. Wenn du eine Nachricht auf Telegram sendest, gibt MOPS sie genau so an das CLI weiter, als haettest du sie in dein Terminal getippt.

```
Handy (Telegram/Matrix)
  |
  v
MOPS-Daemon (dein Rechner)
  |
  +---> claude     (Subprozess)
  +---> codex      (Subprozess)
  +---> gemini     (Subprozess)
  |
  v
Antwort wird live zum Handy gestreamt
```

Der gesamte Zustand liegt in `~/.mops/` als einfaches JSON und Markdown. Keine Datenbank, keine externen Dienste.

---

## Chat-Modi

MOPS bietet dir fuenf Interaktionsebenen. Fang einfach an, skaliere nach Bedarf.

### 1 &mdash; Einzelchat

Dein direktes 1:1-Gespraech. Jede Nachricht geht an das aktive CLI, Antworten werden live zurueckgestreamt.

```
Du:    "Erklaere den Auth-Flow in dieser Codebase"
Bot:   [streamt Claude-Code-Antwort]

Du:    /model
Bot:   [wechsel zu Codex oder Gemini]
```

### 2 &mdash; Gruppenthemen

Erstelle eine Telegram-Gruppe mit aktivierten Themen. Jedes Thema bekommt seinen eigenen isolierten CLI-Kontext. Fuenf Themen = fuenf parallele Gespraeche, alles in einer Gruppe.

```
Meine Projekte/
  Allgemein      -- eigener Kontext
  Auth           -- eigener Kontext, eigenes Modell
  Frontend       -- eigener Kontext
  Datenbank      -- eigener Kontext
  Refactoring    -- eigener Kontext
```

### 3 &mdash; Benannte Sitzungen

Starte ein Nebengespraech, ohne deinen aktuellen Kontext zu verlieren. Wie ein zweites Terminal oeffnen.

```
Du:    "Lass uns an der Authentifizierung arbeiten"
Bot:   [antwortet ueber Auth]

/session Fix den kaputten CSV-Export
Bot:   [arbeitet an CSV in separatem Kontext]

Du:    "Zurueck zu Auth -- Ratenbegrenzung hinzufuegen"
Bot:   [macht genau da weiter, wo du aufgehoert hast]
```

### 4 &mdash; Hintergrundaufgaben

Delegiere langwierige Arbeit. Du chattest weiter, die Aufgabe laeuft autonom, Ergebnisse kommen zurueck, wenn sie fertig sind.

```
Du:    "Recherchiere die Top-5-Wettbewerber und schreib eine Zusammenfassung"
Bot:   -> delegiert, du arbeitest weiter
Bot:   -> fertig, Zusammenfassung erscheint in deinem Chat
```

### 5 &mdash; Sub-Agenten

Vollstaendig isolierter zweiter Bot -- eigener Workspace, eigener Speicher, eigenes CLI, eigene Konfiguration. Laeuft auf einem anderen Anbieter, wenn du willst.

```bash
mops agents add codex-agent
```

Jetzt hast du Claude in deinem Hauptchat und Codex in einem separaten Chat, die parallel mit unabhaengigen Kontexten arbeiten. Sie koennen sich gegenseitig Aufgaben delegieren.

<details>
<summary><strong>Vergleichstabelle der Modi</strong></summary>
<br>

|  | Einzelchat | Themen | Sitzungen | Aufgaben | Sub-Agenten |
|---|---|---|---|---|---|
| **Was** | Haupt-1:1 | Ein Thema = ein Chat | Nebenkontext | "Mach das im Hintergrund" | Separater Bot |
| **Kontext** | Einer pro Anbieter | Einer pro Thema | Eigener pro Sitzung | Eigener, Ergebnis fliesst zurueck | Vollstaendig isoliert |
| **Workspace** | `~/.mops/` | Geteilt | Geteilt | Geteilt | Eigener unter `agents/` |
| **Einrichtung** | Automatisch | Gruppe + Themen erstellen | `/session <prompt>` | Automatisch | `mops agents add` |

</details>

---

## Funktionen

**Multi-Anbieter** &mdash; Wechsle zwischen Claude, Codex und Gemini mit `/model`. Pro Thema, pro Sitzung.

**Multi-Transport** &mdash; Telegram und Matrix laufen gleichzeitig. Plugin-System fuer Discord, Slack, Signal.

**Echtzeit-Streaming** &mdash; Live-Nachrichtenbearbeitung auf Telegram, segmentbasiert auf Matrix.

**Persistenter Speicher** &mdash; Einfache Markdown-Dateien, die Sitzungen und Neustarts ueberleben.

**Cron & Webhooks** &mdash; Plane wiederkehrende Aufgaben mit Zeitzonen-Unterstuetzung. Webhook-Trigger fuer externe Integrationen.

**Docker-Sandbox** &mdash; Optionaler Sidecar-Container mit konfigurierbaren Host-Mounts fuer sichere Code-Ausfuehrung.

**Hintergrunddienst** &mdash; Als systemd (Linux), launchd (macOS) oder Task Scheduler (Windows) installierbar.

**Skill-Synchronisation** &mdash; Geteilte Skills ueber `~/.claude/`, `~/.codex/`, `~/.gemini/`.

**Hot-Reload-Konfiguration** &mdash; Aendere Sprache, Modell, Berechtigungen, Szene -- kein Neustart noetig.

**7 Sprachen** &mdash; English, Deutsch, Nederlands, Francais, Russkij, Espanol, Portugues.

---

## Transport-Unterstuetzung

| Plattform | Status | Streaming | Interaktion | Installation |
|---|---|---|---|---|
| **Telegram** | Primaer | Live-Nachrichtenbearbeitung | Inline-Keyboards | Integriert |
| **Matrix** | Unterstuetzt | Segmentbasiert | Emoji-Reaktionen | `mops install matrix` |

Beide laufen parallel auf demselben Agenten. Einen neuen Messenger hinzuzufuegen bedeutet, `BotProtocol` in einem Sub-Package zu implementieren -- der Kern ist vollstaendig transport-agnostisch.

---

## Sicherheit

Duales Allowlist-Modell. Jede Nachricht muss beide Pruefungen bestehen:

| Chat-Typ | Anforderung |
|---|---|
| **Privat** | Benutzer-ID in der Allowlist |
| **Gruppe** | Gruppen-ID in der Allowlist UND Benutzer-ID in der Allowlist |

Allowlists sind hot-reloadbar. Nicht autorisierte Gruppen loesen automatisches Verlassen aus. Der gesamte Zustand ist lokal -- nichts verlaesst deinen Rechner.

---

## Befehle

| Befehl | Funktion |
|---|---|
| `/model` | Anbieter/Modell wechseln |
| `/new` | Sitzung zuruecksetzen |
| `/stop` | Aktuelle + wartende Aufgaben stoppen |
| `/session <prompt>` | Benannte Sitzung starten |
| `/tasks` | Hintergrundaufgaben anzeigen |
| `/cron` | Geplante Jobs verwalten |
| `/agents` | Multi-Agenten-Status |
| `/status` | Sitzungs-/Anbieter-Info |
| `/diagnose` | Laufzeit-Diagnose |
| `/memory` | Persistenten Speicher anzeigen |

<details>
<summary><strong>CLI-Befehle</strong></summary>

```bash
mops                    # Starten (Auto-Onboarding)
mops onboarding         # Setup erneut ausfuehren
mops stop               # Bot stoppen
mops restart            # Neustarten
mops upgrade            # Aktualisieren + Neustarten
mops status             # Laufzeitstatus
mops uninstall          # Alles entfernen

mops service install    # Hintergrunddienst
mops service start|stop|logs

mops docker enable      # Docker-Sandbox
mops docker rebuild
mops docker mount /path

mops agents list        # Sub-Agenten
mops agents add NAME
mops agents remove NAME

mops install matrix     # Matrix-Transport
mops install api        # WebSocket API
```

</details>

---

## Arbeitsverzeichnis

```
~/.mops/
  config/config.json          # Konfiguration
  sessions.json               # Chat-Zustand
  named_sessions.json         # Benannte Sitzungen
  tasks.json                  # Hintergrundaufgaben
  cron_jobs.json              # Geplante Jobs
  agents.json                 # Sub-Agenten-Verzeichnis
  SHAREDMEMORY.md             # Agentenuebergreifendes Wissen
  workspace/
    memory_system/            # Persistenter Speicher
    cron_tasks/               # Cron-Skripte
    skills/ tools/            # Geteilte Werkzeuge
    tasks/                    # Aufgabenordner
  agents/<name>/              # Isolierte Sub-Agenten-Workspaces
```

---

## Warum dieser Ansatz

Andere Projekte patchen SDKs, faelschen Header oder proxieren API-Aufrufe. Das ist fragil und riskiert Verstoesse gegen die Nutzungsbedingungen der Anbieter.

MOPS fuehrt offizielle CLIs als Subprozesse aus. Nicht mehr. Dein Abo, dein Rechner, deine Authentifizierung. Der Bot ist nur eine Bruecke zwischen deinem Handy und deinem Terminal.

---

## Dokumentation

| Anleitung | Inhalt |
|---|---|
| [Installation](docs/installation.md) | Einrichtungsanleitung |
| [Systemuebersicht](docs/system_overview.md) | End-to-End-Laufzeit |
| [Architektur](docs/architecture.md) | Routing, Streaming, Callbacks |
| [Konfiguration](docs/config.md) | Vollstaendige Konfigurationsreferenz |
| [Anwendungsfälle](docs/use-cases.md) | 10 Praxisbeispiele mit Befehlen |
| [FAQ](docs/FAQ.md) | Häufig gestellte Fragen |
| [Fehlerbehebung](docs/troubleshooting.md) | Diagnoseschritte nach Symptom |
| [Plugin-Anleitung](docs/plugin-guide.md) | Transports & Provider hinzufügen |
| [Telegram-Einrichtung](docs/telegram-setup.md) | Bot-Token + Gruppensetup |
| [Matrix-Setup](docs/matrix-setup.md) | Matrix-Transport |
| [Automatisierung](docs/automation.md) | Cron, Webhooks, Heartbeat |
| [Dienstverwaltung](docs/modules/service_management.md) | systemd / launchd / Task Scheduler |

---

## Mitmachen

Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Setup, Qualitätsanforderungen und Beitragsrichtlinien.

```bash
git clone https://github.com/NathanMaine/memoriant-ops-bot.git
cd memoriant-ops-bot
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff format . && ruff check . && mypy memoriant_ops_bot
```

---

[Sicherheitsrichtlinie](SECURITY.md) · [Änderungsprotokoll](CHANGELOG.md)

<p align="center">
  <strong>MIT-Lizenz</strong><br>
  Entwickelt von <a href="https://github.com/NathanMaine">Memoriant Inc.</a>
</p>
