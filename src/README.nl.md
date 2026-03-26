[English](README.md) | [Deutsch](README.de.md) | [Nederlands](README.nl.md) | [Francais](README.fr.md) | [Russkij](README.ru.md) | [Espanol](README.es.md) | [Portugues](README.pt.md)

<p align="center">
  <img src="docs/images/mops-logo.jpeg" alt="MOPS" width="280">
</p>

<h1 align="center">MOPS</h1>

<p align="center">
  <em>Multi-provider AI-agentbesturing vanaf je telefoon.</em>
</p>

<p align="center">
  <a href="#snelle-start">Snelle Start</a> &middot;
  <a href="#hoe-het-werkt">Hoe het werkt</a> &middot;
  <a href="#functies">Functies</a> &middot;
  <a href="docs/use-cases.md">Toepassingen</a> &middot;
  <a href="docs/installation.md">Installatiegids</a> &middot;
  <a href="docs/architecture.md">Architectuur</a>
</p>

<p align="center">
  <img src="https://github.com/NathanMaine/memoriant-ops-bot/actions/workflows/tests.yml/badge.svg" alt="Tests">
  <img src="https://img.shields.io/badge/providers-Claude%20%7C%20Codex%20%7C%20Gemini-blue" alt="Providers">
  <img src="https://img.shields.io/badge/transport-Telegram%20%7C%20Matrix-green" alt="Transport">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="Licentie">
  <img src="https://img.shields.io/badge/python-3.11%2B-yellow" alt="Python">
  <img src="https://img.shields.io/pypi/v/memoriant-ops-bot" alt="PyPI">
</p>

---

Gebruik Claude Code, OpenAI Codex CLI of Google Gemini CLI vanuit Telegram of Matrix. Maakt uitsluitend gebruik van officiele CLIs als subprocessen -- niets vervalst, niets geproxied. Jouw abonnement, jouw machine, jouw data.

<p align="center">
  <img src="docs/images/mops-demo.gif" alt="MOPS Demo" width="300">
</p>

> **Uitgebracht op 12 maart 2026** -- vijf dagen voordat Anthropic [Claude Dispatch](https://mlq.ai/news/anthropic-launches-claude-dispatch-for-remote-desktop-ai-control/) lanceerde. Zelfde concept, andere filosofie.

### Hoe verschilt dit van Claude Dispatch?


|  | MOPS | Claude Dispatch |
|---|---|---|
| **Providers** | Claude + Codex + Gemini | Alleen Claude |
| **Kosten** | Gratis -- gebruikt je bestaande abonnementen | Max-abonnement vereist ($100+/maand) |
| **Bediening vanaf** | Telegram, Matrix, elk apparaat | Claude mobiele app |
| **Bestuurt** | Elke machine -- servers, GPU-rigs, cloud | Alleen Mac-desktop |
| **Parallelle agenten** | Onbeperkt -- onderwerpen, sessies, sub-agenten | Enkel gesprek |
| **Open source** | MIT | Proprietary |
| **Achtergrondtaken** | Ja, met delegatie + opvolgingen | Ja |
| **Benoemde sessies** | Ja | Nee |
| **Plugin-systeem** | Ja -- voeg Discord, Slack, Signal toe | Nee |

---

## Snelle Start

**Stap 1: Python installeren** (overslaan als je Python 3.11+ hebt)

```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Windows — download van https://www.python.org/downloads/
# ✅ Vink "Add Python to PATH" aan tijdens installatie
```

**Stap 2: pipx installeren** (hulpmiddel voor Python-apps)

```bash
# macOS
brew install pipx && pipx ensurepath

# Linux
pip install pipx && pipx ensurepath

# Windows
pip install pipx
pipx ensurepath
```

> Na `pipx ensurepath`, **sluit je terminal en open opnieuw**.

**Stap 3: MOPS installeren**

```bash
pipx install memoriant-ops-bot
```

**Stap 4: Minstens één AI-CLI installeren** (de agent die MOPS aanstuurt)

```bash
# Kies een of meer:
npm install -g @anthropic-ai/claude-code && claude auth     # Claude
npm install -g @openai/codex && codex auth                   # Codex
npm install -g @google/gemini-cli                            # Gemini
```

> Node.js niet geïnstalleerd? Eerst installeren: `brew install node` (macOS) of `sudo apt install nodejs npm` (Linux) of download van [nodejs.org](https://nodejs.org)

**Stap 5: Telegram-bot-token aanmaken** — zie [Telegram-instelling](docs/telegram-setup.md)

**Stap 6: MOPS starten**

```bash
mops
```

De wizard begeleidt je door transport-setup (Telegram of Matrix), tijdzone, optionele Docker-sandbox en installatie als achtergronddienst.

---

## Hoe het werkt

MOPS start officiele CLI-binaries als subprocessen en koppelt ze aan je berichtenplatform. Geen API-sleutels, geen SDK-patches, geen vervalste headers. Wanneer je een bericht stuurt op Telegram, geeft MOPS het precies zo door aan het CLI alsof je het in je terminal had getypt.

```
Telefoon (Telegram/Matrix)
  |
  v
MOPS-daemon (jouw machine)
  |
  +---> claude     (subproces)
  +---> codex      (subproces)
  +---> gemini     (subproces)
  |
  v
Antwoord wordt live teruggestreamd naar telefoon
```

Alle toestand staat in `~/.mops/` als gewoon JSON en Markdown. Geen database, geen externe diensten.

---

## Chatmodi

MOPS biedt vijf interactieniveaus. Begin eenvoudig, schaal op wanneer nodig.

### 1 &mdash; Enkele Chat

Je directe 1:1-gesprek. Elk bericht gaat naar het actieve CLI, antwoorden worden live teruggestreamd.

```
Jij:   "Leg de auth-flow in deze codebase uit"
Bot:   [streamt Claude Code-antwoord]

Jij:   /model
Bot:   [wissel naar Codex of Gemini]
```

### 2 &mdash; Groepsonderwerpen

Maak een Telegram-groep aan met onderwerpen ingeschakeld. Elk onderwerp krijgt zijn eigen geisoleerde CLI-context. Vijf onderwerpen = vijf parallelle gesprekken, allemaal in een groep.

```
Mijn Projecten/
  Algemeen       -- eigen context
  Auth           -- eigen context, eigen model
  Frontend       -- eigen context
  Database       -- eigen context
  Refactoring    -- eigen context
```

### 3 &mdash; Benoemde Sessies

Start een zijgesprek zonder je huidige context te verliezen. Alsof je een tweede terminal opent.

```
Jij:   "Laten we aan authenticatie werken"
Bot:   [antwoordt over auth]

/session Fix de kapotte CSV-export
Bot:   [werkt aan CSV in aparte context]

Jij:   "Terug naar auth -- voeg rate limiting toe"
Bot:   [pakt het precies op waar je gebleven was]
```

### 4 &mdash; Achtergrondtaken

Delegeer langlopend werk. Je blijft chatten, de taak draait autonoom, resultaten verschijnen wanneer ze klaar zijn.

```
Jij:   "Onderzoek de top 5 concurrenten en schrijf een samenvatting"
Bot:   -> delegeert, jij werkt verder
Bot:   -> klaar, samenvatting verschijnt in je chat
```

### 5 &mdash; Sub-Agenten

Volledig geisoleerde tweede bot -- eigen workspace, eigen geheugen, eigen CLI, eigen configuratie. Draait op een andere provider als je wilt.

```bash
mops agents add codex-agent
```

Nu heb je Claude in je hoofdchat en Codex in een aparte chat, werkend in parallel met onafhankelijke contexten. Ze kunnen taken aan elkaar delegeren.

<details>
<summary><strong>Vergelijkingstabel modi</strong></summary>
<br>

|  | Enkel | Onderwerpen | Sessies | Taken | Sub-agenten |
|---|---|---|---|---|---|
| **Wat** | Hoofd-1:1 | Een onderwerp = een chat | Zijcontext | "Doe dit op achtergrond" | Aparte bot |
| **Context** | Een per provider | Een per onderwerp | Eigen per sessie | Eigen, resultaat vloeit terug | Volledig geisoleerd |
| **Workspace** | `~/.mops/` | Gedeeld | Gedeeld | Gedeeld | Eigen onder `agents/` |
| **Setup** | Automatisch | Groep + onderwerpen aanmaken | `/session <prompt>` | Automatisch | `mops agents add` |

</details>

---

## Functies

**Multi-provider** &mdash; Wissel tussen Claude, Codex en Gemini met `/model`. Per onderwerp, per sessie.

**Multi-transport** &mdash; Telegram en Matrix draaien gelijktijdig. Plugin-systeem voor Discord, Slack, Signal.

**Realtime streaming** &mdash; Live berichtbewerking op Telegram, segmentgebaseerd op Matrix.

**Persistent geheugen** &mdash; Gewone Markdown-bestanden die sessies en herstarts overleven.

**Cron & webhooks** &mdash; Plan terugkerende taken met tijdzone-ondersteuning. Webhook-triggers voor externe integraties.

**Docker-sandbox** &mdash; Optionele sidecar-container met configureerbare host-mounts voor veilige code-uitvoering.

**Achtergronddienst** &mdash; Installeerbaar als systemd (Linux), launchd (macOS) of Task Scheduler (Windows).

**Skill-synchronisatie** &mdash; Gedeelde skills over `~/.claude/`, `~/.codex/`, `~/.gemini/`.

**Hot-reload configuratie** &mdash; Wijzig taal, model, rechten, scene -- geen herstart nodig.

**7 talen** &mdash; English, Deutsch, Nederlands, Francais, Russkij, Espanol, Portugues.

---

## Transportondersteuning

| Platform | Status | Streaming | Interactie | Installatie |
|---|---|---|---|---|
| **Telegram** | Primair | Live berichtbewerking | Inline keyboards | Ingebouwd |
| **Matrix** | Ondersteund | Segmentgebaseerd | Emoji-reacties | `mops install matrix` |

Beide draaien parallel op dezelfde agent. Een nieuwe messenger toevoegen betekent `BotProtocol` implementeren in een sub-package -- de kern is volledig transport-agnostisch.

---

## Beveiliging

Dubbel allowlist-model. Elk bericht moet beide controles doorstaan:

| Chattype | Vereiste |
|---|---|
| **Prive** | Gebruikers-ID in allowlist |
| **Groep** | Groeps-ID in allowlist EN gebruikers-ID in allowlist |

Allowlists zijn hot-reloadbaar. Ongeautoriseerde groepen activeren automatisch verlaten. Alle toestand is lokaal -- niets verlaat jouw machine.

---

## Commando's

| Commando | Functie |
|---|---|
| `/model` | Provider/model wisselen |
| `/new` | Sessie resetten |
| `/stop` | Huidige + wachtende taken stoppen |
| `/session <prompt>` | Benoemde sessie starten |
| `/tasks` | Achtergrondtaken bekijken |
| `/cron` | Geplande taken beheren |
| `/agents` | Multi-agent-status |
| `/status` | Sessie-/provider-info |
| `/diagnose` | Runtime-diagnostiek |
| `/memory` | Persistent geheugen bekijken |

<details>
<summary><strong>CLI-commando's</strong></summary>

```bash
mops                    # Starten (auto-onboarding)
mops onboarding         # Setup opnieuw uitvoeren
mops stop               # Bot stoppen
mops restart            # Herstarten
mops upgrade            # Upgraden + herstarten
mops status             # Runtime-status
mops uninstall          # Alles verwijderen

mops service install    # Achtergronddienst
mops service start|stop|logs

mops docker enable      # Docker-sandbox
mops docker rebuild
mops docker mount /path

mops agents list        # Sub-agenten
mops agents add NAME
mops agents remove NAME

mops install matrix     # Matrix-transport
mops install api        # WebSocket API
```

</details>

---

## Werkruimte

```
~/.mops/
  config/config.json          # Configuratie
  sessions.json               # Chattoestand
  named_sessions.json         # Benoemde sessies
  tasks.json                  # Achtergrondtaken
  cron_jobs.json              # Geplande taken
  agents.json                 # Sub-agent-register
  SHAREDMEMORY.md             # Agent-overschrijdende kennis
  workspace/
    memory_system/            # Persistent geheugen
    cron_tasks/               # Cron-scripts
    skills/ tools/            # Gedeeld gereedschap
    tasks/                    # Taakmappen
  agents/<name>/              # Geisoleerde sub-agent-werkruimtes
```

---

## Waarom deze aanpak

Andere projecten patchen SDKs, vervalsen headers of proxyen API-aanroepen. Dat is fragiel en riskeert schending van de gebruiksvoorwaarden van providers.

MOPS draait officiele CLIs als subprocessen. Meer niet. Jouw abonnement, jouw machine, jouw authenticatie. De bot is slechts een brug tussen je telefoon en je terminal.

---

## Documentatie

| Gids | Inhoud |
|---|---|
| [Installatie](docs/installation.md) | Installatiehandleiding |
| [Systeemoverzicht](docs/system_overview.md) | End-to-end runtime |
| [Architectuur](docs/architecture.md) | Routing, streaming, callbacks |
| [Configuratie](docs/config.md) | Volledige configuratiereferentie |
| [Toepassingen](docs/use-cases.md) | 10 praktijkvoorbeelden met commando's |
| [FAQ](docs/FAQ.md) | Veelgestelde vragen |
| [Probleemoplossing](docs/troubleshooting.md) | Diagnosestappen per symptoom |
| [Plugin-gids](docs/plugin-guide.md) | Transports & providers toevoegen |
| [Telegram-instelling](docs/telegram-setup.md) | Bot-token + groepsinstelling |
| [Matrix-setup](docs/matrix-setup.md) | Matrix-transport |
| [Automatisering](docs/automation.md) | Cron, webhooks, heartbeat |
| [Dienstbeheer](docs/modules/service_management.md) | systemd / launchd / Task Scheduler |

---

## Bijdragen

Zie [CONTRIBUTING.md](CONTRIBUTING.md) voor setup, kwaliteitseisen en bijdragerichtlijnen.

```bash
git clone https://github.com/NathanMaine/memoriant-ops-bot.git
cd memoriant-ops-bot
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff format . && ruff check . && mypy memoriant_ops_bot
```

---

[Beveiligingsbeleid](SECURITY.md) · [Wijzigingslogboek](CHANGELOG.md)

<p align="center">
  <strong>MIT-licentie</strong><br>
  Gebouwd door <a href="https://github.com/NathanMaine">Memoriant Inc.</a>
</p>
