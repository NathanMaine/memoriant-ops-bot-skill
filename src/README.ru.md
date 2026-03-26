[English](README.md) | [Deutsch](README.de.md) | [Nederlands](README.nl.md) | [Francais](README.fr.md) | [Russkij](README.ru.md) | [Espanol](README.es.md) | [Portugues](README.pt.md)

<p align="center">
  <img src="docs/images/mops-logo.jpeg" alt="MOPS" width="280">
</p>

<h1 align="center">MOPS</h1>

<p align="center">
  <em>Upravlenie AI-agentami ot neskolkih provajderov prjamo s telefona.</em>
</p>

<p align="center">
  <a href="#bystryj-start">Bystryj start</a> &middot;
  <a href="#kak-eto-rabotaet">Kak eto rabotaet</a> &middot;
  <a href="#vozmozhnosti">Vozmozhnosti</a> &middot;
  <a href="docs/use-cases.md">Primery ispolzovanija</a> &middot;
  <a href="docs/installation.md">Rukovodstvo po ustanovke</a> &middot;
  <a href="docs/architecture.md">Arhitektura</a>
</p>

<p align="center">
  <img src="https://github.com/NathanMaine/memoriant-ops-bot/actions/workflows/tests.yml/badge.svg" alt="Tests">
  <img src="https://img.shields.io/badge/providers-Claude%20%7C%20Codex%20%7C%20Gemini-blue" alt="Provajdery">
  <img src="https://img.shields.io/badge/transport-Telegram%20%7C%20Matrix-green" alt="Transport">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="Licenzija">
  <img src="https://img.shields.io/badge/python-3.11%2B-yellow" alt="Python">
  <img src="https://img.shields.io/pypi/v/memoriant-ops-bot" alt="PyPI">
</p>

---

Zapuskajte Claude Code, OpenAI Codex CLI ili Google Gemini CLI iz Telegram ili Matrix. Ispolzuet tolko oficialnye CLI kak subprocessy -- nichego poddelnogo, nichego proksirovanogo. Vasha podpiska, vasha mashina, vashi dannye.

<p align="center">
  <img src="docs/images/mops-demo.gif" alt="MOPS Demo" width="300">
</p>

> **Vypushhen 12 marta 2026** -- za pjat dnej do togo, kak Anthropic vypustila [Claude Dispatch](https://mlq.ai/news/anthropic-launches-claude-dispatch-for-remote-desktop-ai-control/). Ta zhe koncepcija, drugaja filosofija.

### Chem eto otlichaetsja ot Claude Dispatch?


|  | MOPS | Claude Dispatch |
|---|---|---|
| **Provajdery** | Claude + Codex + Gemini | Tolko Claude |
| **Stoimost** | Besplatno -- ispolzuet vashi sushhestvujushhie podpiski | Nuzhen tarif Max ($100+/mes.) |
| **Udalennyj dostup s** | Telegram, Matrix, ljubogo ustrojstva | Mobilnoe prilozhenie Claude |
| **Upravljaet** | Ljuboj mashinoj -- servery, GPU-stojki, oblako | Tolko Mac-rabochij stol |
| **Parallelnye agenty** | Neogranicheno -- temy, sessii, sub-agenty | Odin razgovor |
| **Open source** | MIT | Proprietarnyj |
| **Fonovye zadachi** | Da, s delegirovaniem + otchetami | Da |
| **Imenovannye sessii** | Da | Net |
| **Sistema plaginov** | Da -- dobavte Discord, Slack, Signal | Net |

---

## Bystryj start

**Shag 1: Ustanovite Python** (propustite, esli Python 3.11+ uzhe ustanovlen)

```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Windows — skachajte s https://www.python.org/downloads/
# ✅ Otmetjte "Add Python to PATH" pri ustanovke
```

**Shag 2: Ustanovite pipx** (instrument dlja Python-prilozhenij)

```bash
# macOS
brew install pipx && pipx ensurepath

# Linux
pip install pipx && pipx ensurepath

# Windows
pip install pipx
pipx ensurepath
```

> Posle `pipx ensurepath` **zakrojte i zanovo otkrojte terminal**.

**Shag 3: Ustanovite MOPS**

```bash
pipx install memoriant-ops-bot
```

**Shag 4: Ustanovite hotja by odin AI CLI** (agent, kotorym MOPS budet upravljat)

```bash
# Vyberite odin ili neskolko:
npm install -g @anthropic-ai/claude-code && claude auth     # Claude
npm install -g @openai/codex && codex auth                   # Codex
npm install -g @google/gemini-cli                            # Gemini
```

> Net Node.js? Snachala ustanovite: `brew install node` (macOS) ili `sudo apt install nodejs npm` (Linux) ili skachajte s [nodejs.org](https://nodejs.org)

**Shag 5: Sozdajte token Telegram-bota** — sm. [Nastrojka Telegram](docs/telegram-setup.md)

**Shag 6: Zapustite MOPS**

```bash
mops
```

Pomoshhnik po nastrojke provodit vas cherez nastrojku transporta (Telegram ili Matrix), chasovoj pojas, Docker-sandbox i ustanovku servisa.

---

## Kak eto rabotaet

MOPS zapuskaet oficialnye CLI-fajly kak subprocessy i svjazyvaet ih s vashej platformoj obmenа soobshhenijami. Nikаkih API-kljuchej, nikаkih pаtchej SDK, nikаkih poddelnyh zаgolovkov. Kogdа vy otprаvljaete soobshhenie v Telegram, MOPS peredaet ego v CLI tochno tak zhe, kak esli by vy nabRAli ego v terminale.

```
Telefon (Telegram/Matrix)
  |
  v
Demon MOPS (vasha mashina)
  |
  +---> claude     (subprocesss)
  +---> codex      (subprocess)
  +---> gemini     (subprocess)
  |
  v
Otvet transliruetsja obratno na telefon
```

Vsjo sostojanie hranitsja v `~/.mops/` v vide obychnogo JSON i Markdown. Nikаkoj bazy dаnnyh, nikаkih vneshnih servisov.

---

## Rezhimy chata

MOPS predlagaet pjat urovnej vzaimodejstvija. Nachinajte prosto, masshtabirujte po mere neobhodimosti.

### 1 &mdash; Lichnyj chat

Vash osnovnoj razgovor 1:1. Kazhdoe soobshhenie idet v aktivnyj CLI, otvety transliirujutsja v realnom vremeni.

```
Vy:    "Objasni potok autentifikacii v etoj kodovoj baze"
Bot:   [transliruet otvet Claude Code]

Vy:    /model
Bot:   [perekljuchenie na Codex ili Gemini]
```

### 2 &mdash; Gruppovye temy

Sozdajte gruppu Telegram s vkljuchennymi temami. Kazhdaja tema poluchaet sobstvennyj izolirovannyj kontekst CLI. Pjat tem = pjat parallelnyh razgovorov, vsjo v odnoj gruppe.

```
Moi Proekty/
  Obshhee        -- sobstvennyj kontekst
  Auth           -- sobstvennyj kontekst, svoja model
  Frontend       -- sobstvennyj kontekst
  Baza dannyh    -- sobstvennyj kontekst
  Refaktoring    -- sobstvennyj kontekst
```

### 3 &mdash; Imenovannye sessii

Zapustite pobochnyj razgovor, ne terjaja tekushhij kontekst. Kak otkryt vtoroj terminal.

```
Vy:    "Davaj porabotaem nad autentifikaciej"
Bot:   [otvechaet pro auth]

/session Ispravit slomannуj eksport CSV
Bot:   [rabotaet s CSV v otdelnom kontekste]

Vy:    "Nazad k auth -- dobavit ogranichenie skorosti"
Bot:   [prodolzhaet imenno s togo mesta, gde vy ostanovilis]
```

### 4 &mdash; Fonovye zadachi

Delegirujte dolgosrochnuju rabotu. Vy prodolzhaete obshhatsjа, zadachа rabotaet avtonomno, rezultaty pоjavljajutsja po zavershenii.

```
Vy:    "Issleduj top-5 konkurentov i napishi reZJUme"
Bot:   -> delegiruet, vy prodolzhaete rabotat
Bot:   -> gotovo, reZJUme pojavljaetsja v vashem chate
```

### 5 &mdash; Sub-agenty

Polnostju izolirovannyj vtoroj bot -- sobstvennyj workspace, sobstvennaja pamjat, sobstvennyj CLI, sobstvennaja konfiguracija. Mozhet rabotat na drugom provajdere.

```bash
mops agents add codex-agent
```

Teper u vas Claude v osnovnom chate i Codex v otdelnom chate, rabotajushhie parallelnо s nezavisimymi kontekstami. Oni mogut delegirovat zadachi drug drugu.

<details>
<summary><strong>Sravnitelnaja tablica rezhimov</strong></summary>
<br>

|  | Lichnyj | Temy | Sessii | Zadachi | Sub-agenty |
|---|---|---|---|---|---|
| **Chto** | Osnovnoj 1:1 | Odna tema = odin chat | Pobochnyj kontekst | "Sdelaj eto v fone" | Otdelnyj bot |
| **Kontekst** | Odin na provajdera | Odin na temu | Sobstvennyj na sessiju | Sobstvennyj, rezultat vozvrashhaetsja | Polnostju izolirovannyj |
| **Workspace** | `~/.mops/` | Obshhij | Obshhij | Obshhij | Sobstvennyj v `agents/` |
| **Nastrojka** | Avtomaticheskaja | Sozdat gruppu + temy | `/session <prompt>` | Avtomaticheskaja | `mops agents add` |

</details>

---

## Vozmozhnosti

**Multi-provajder** &mdash; Perekljuchajtes mezhdu Claude, Codex i Gemini cherez `/model`. Na temu, na sessiju.

**Multi-transport** &mdash; Telegram i Matrix rabotajut odnovremenno. Sistema plaginov dlja Discord, Slack, Signal.

**Streaming v realnom vremeni** &mdash; Redaktirovanie soobshhenij v realnom vremeni v Telegram, posegmentno v Matrix.

**Postojannaja pamjat** &mdash; Prostye fajly Markdown, kotorye sohranjaajutsja mezhdu sessijami i perezagruzkami.

**Cron i webhooks** &mdash; Planirujte povtorjajushhiesja zadachi s podderzhkoj chasovyh pojasov. Webhook-triggery dlja vneshnih integracij.

**Docker-sandbox** &mdash; Opcionalnyj sidecar-kontejner s nastrzaivaemymi montirovanijami hosta dlja bezopasnogo vypolnenija koda.

**Fonovyj servis** &mdash; Ustanavlivaetsja kak systemd (Linux), launchd (macOS) ili Task Scheduler (Windows).

**Sinhronizacija navykov** &mdash; Obshhie navyki cherez `~/.claude/`, `~/.codex/`, `~/.gemini/`.

**Gorjachaja perezagruzka konfiguracii** &mdash; Menjajte jazyk, model, prava, scenu -- bez perezapuska.

**7 jazykov** &mdash; English, Deutsch, Nederlands, Francais, Russkij, Espanol, Portugues.

---

## Podderzhka transportov

| Platforma | Status | Streaming | Vzaimodejstvie | Ustanovka |
|---|---|---|---|---|
| **Telegram** | Osnovnoj | Redaktirovanie soobshhenij v realnom vremeni | Inline-klaviatury | Vstroennyj |
| **Matrix** | Podderzhivaetsja | Posegmentnyj | Emoji-reakcii | `mops install matrix` |

Oba rabotajut parallelnо na odnom agente. Dobavlenie novogo messendzhera oznachaet realizaciju `BotProtocol` v sub-pakete -- jadro polnostju ne zavisit ot transporta.

---

## Bezopasnost

Model dvojnogo spiska razreshenij. Kazhdoe soobshhenie dolzhno projti obe proverki:

| Tip chata | Trebovanie |
|---|---|
| **Lichnyj** | ID polzovatelja v spiske razreshenij |
| **Gruppa** | ID gruppy v spiske razreshenij I ID polzovatelja v spiske razreshenij |

Spiski razreshenij podderzhivajut gorjachuju perezagruzku. Nerazreshennye gruppy vyzvivajut avtomaticheskij vyhod. Vsjo sostojanie lokalnoe -- nichto ne pokidaet vashu mashinu.

---

## Komandy

| Komanda | Chto delaet |
|---|---|
| `/model` | Smenit provajdera/model |
| `/new` | Sbrosit sessiju |
| `/stop` | Ostanovit tekushhie + v ocheredi |
| `/session <prompt>` | Zapustit imenovannuju sessiju |
| `/tasks` | Posmotret fonovye zadachi |
| `/cron` | Upravljat zapplanirovannymi zadachami |
| `/agents` | Status multi-agentov |
| `/status` | Info o sessii/provajdere |
| `/diagnose` | Diagnostika vremeni vypolnenija |
| `/memory` | Posmotret postojannuju pamjat |

<details>
<summary><strong>Komandy CLI</strong></summary>

```bash
mops                    # Zapustit (avto-onboarding)
mops onboarding         # Perezapustit nastrojku
mops stop               # Ostanovit bota
mops restart            # Perezapustit
mops upgrade            # Obnovit + perezapustit
mops status             # Status vremeni vypolnenija
mops uninstall          # Udalit vsjo

mops service install    # Fonovyj servis
mops service start|stop|logs

mops docker enable      # Docker-sandbox
mops docker rebuild
mops docker mount /path

mops agents list        # Sub-agenty
mops agents add NAME
mops agents remove NAME

mops install matrix     # Matrix-transport
mops install api        # WebSocket API
```

</details>

---

## Rabochee prostranstvo

```
~/.mops/
  config/config.json          # Konfiguracija
  sessions.json               # Sostojanie chata
  named_sessions.json         # Imenovannye sessii
  tasks.json                  # Fonovye zadachi
  cron_jobs.json              # Zaplanirovannye zadachi
  agents.json                 # Reestr sub-agentov
  SHAREDMEMORY.md             # Mezhagentye znanija
  workspace/
    memory_system/            # Postojannaja pamjat
    cron_tasks/               # Cron-skripty
    skills/ tools/            # Obshhie instrumenty
    tasks/                    # Papki zadach
  agents/<name>/              # Izolirovannye rabochie prostranstva sub-agentov
```

---

## Pochemu imenno takoj podhod

Drugie proekty patchat SDK, poddelvajut zagolovki ili proksirujut API-vyzovy. Eto nenadezhno i riskovano s tochki zrenija narushenija uslovij ispolzovanija provajderov.

MOPS zapuskaet oficialnye CLI kak subprocessy. Ni bolshe, ni menshe. Vasha podpiska, vasha mashina, vasha autentifikacija. Bot -- eto prosto most mezhdu vashim telefonom i vashim terminalom.

---

## Dokumentacija

| Rukovodstvo | Soderzhanie |
|---|---|
| [Ustanovka](docs/installation.md) | Poshagovaja nastrojka |
| [Obzor sistemy](docs/system_overview.md) | Runtime ot nachala do konca |
| [Arhitektura](docs/architecture.md) | Marshrutizacija, streaming, callbacki |
| [Konfiguracija](docs/config.md) | Polnaja spravka po konfigurацii |
| [Primery ispolzovanija](docs/use-cases.md) | 10 prakticheskikh scenariev s komandami |
| [FAQ](docs/FAQ.md) | Chasto zadavaemye voprosy |
| [Ustranenie nepoladok](docs/troubleshooting.md) | Diagnostika po simptomu |
| [Rukovodstvo po plaginam](docs/plugin-guide.md) | Dobavlenie transportov i provajderov |
| [Nastrojka Telegram](docs/telegram-setup.md) | Token bota + nastrojka grupp |
| [Nastrojka Matrix](docs/matrix-setup.md) | Transport Matrix |
| [Avtomatizacija](docs/automation.md) | Cron, webhooks, heartbeat |
| [Upravlenie servisami](docs/modules/service_management.md) | systemd / launchd / Task Scheduler |

---

## Uchastie v razrabotke

Sm. [CONTRIBUTING.md](CONTRIBUTING.md) — nastrojka, trebovanija kachestva i pravila uchastija.

```bash
git clone https://github.com/NathanMaine/memoriant-ops-bot.git
cd memoriant-ops-bot
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff format . && ruff check . && mypy memoriant_ops_bot
```

---

[Politika bezopasnosti](SECURITY.md) · [Zhurnal izmenenij](CHANGELOG.md)

<p align="center">
  <strong>Licenzija MIT</strong><br>
  Sozdano <a href="https://github.com/NathanMaine">Memoriant Inc.</a>
</p>
