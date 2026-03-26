[English](README.md) | [Deutsch](README.de.md) | [Nederlands](README.nl.md) | [Francais](README.fr.md) | [Russkij](README.ru.md) | [Espanol](README.es.md) | [Portugues](README.pt.md)

<p align="center">
  <img src="docs/images/mops-logo.jpeg" alt="MOPS" width="280">
</p>

<h1 align="center">MOPS</h1>

<p align="center">
  <em>Control de agentes IA multi-proveedor desde tu telefono.</em>
</p>

<p align="center">
  <a href="#inicio-rapido">Inicio rapido</a> &middot;
  <a href="#como-funciona">Como funciona</a> &middot;
  <a href="#caracteristicas">Caracteristicas</a> &middot;
  <a href="docs/use-cases.md">Casos de uso</a> &middot;
  <a href="docs/installation.md">Guia de instalacion</a> &middot;
  <a href="docs/architecture.md">Arquitectura</a>
</p>

<p align="center">
  <img src="https://github.com/NathanMaine/memoriant-ops-bot/actions/workflows/tests.yml/badge.svg" alt="Tests">
  <img src="https://img.shields.io/badge/providers-Claude%20%7C%20Codex%20%7C%20Gemini-blue" alt="Proveedores">
  <img src="https://img.shields.io/badge/transport-Telegram%20%7C%20Matrix-green" alt="Transporte">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="Licencia">
  <img src="https://img.shields.io/badge/python-3.11%2B-yellow" alt="Python">
  <img src="https://img.shields.io/pypi/v/memoriant-ops-bot" alt="PyPI">
</p>

---

Ejecuta Claude Code, OpenAI Codex CLI o Google Gemini CLI desde Telegram o Matrix. Utiliza exclusivamente CLIs oficiales como subprocesos -- nada falsificado, nada proxificado. Tu suscripcion, tu maquina, tus datos.

<p align="center">
  <img src="docs/images/mops-demo.gif" alt="MOPS Demo" width="300">
</p>

> **Lanzado el 12 de marzo de 2026** -- cinco dias antes de que Anthropic lanzara [Claude Dispatch](https://mlq.ai/news/anthropic-launches-claude-dispatch-for-remote-desktop-ai-control/). Mismo concepto, filosofia diferente.

### En que se diferencia de Claude Dispatch?


|  | MOPS | Claude Dispatch |
|---|---|---|
| **Proveedores** | Claude + Codex + Gemini | Solo Claude |
| **Costo** | Gratis -- usa tus suscripciones existentes | Plan Max requerido ($100+/mes) |
| **Control remoto desde** | Telegram, Matrix, cualquier dispositivo | App movil de Claude |
| **Controla** | Cualquier maquina -- servidores, rigs GPU, nube | Solo escritorio Mac |
| **Agentes paralelos** | Ilimitados -- temas, sesiones, sub-agentes | Conversacion unica |
| **Open source** | MIT | Propietario |
| **Tareas en segundo plano** | Si, con delegacion + seguimientos | Si |
| **Sesiones con nombre** | Si | No |
| **Sistema de plugins** | Si -- agrega Discord, Slack, Signal | No |

---

## Inicio rapido

**Paso 1: Instalar Python** (omitir si ya tienes Python 3.11+)

```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Windows — descargar de https://www.python.org/downloads/
# ✅ Marca "Add Python to PATH" durante la instalación
```

**Paso 2: Instalar pipx** (herramienta para aplicaciones Python)

```bash
# macOS
brew install pipx && pipx ensurepath

# Linux
pip install pipx && pipx ensurepath

# Windows
pip install pipx
pipx ensurepath
```

> Después de `pipx ensurepath`, **cierra y vuelve a abrir tu terminal**.

**Paso 3: Instalar MOPS**

```bash
pipx install memoriant-ops-bot
```

**Paso 4: Instalar al menos un CLI de IA** (el agente que MOPS controlará)

```bash
# Elige uno o más:
npm install -g @anthropic-ai/claude-code && claude auth     # Claude
npm install -g @openai/codex && codex auth                   # Codex
npm install -g @google/gemini-cli                            # Gemini
```

> ¿No tienes Node.js? Instálalo primero: `brew install node` (macOS) o `sudo apt install nodejs npm` (Linux) o descarga de [nodejs.org](https://nodejs.org)

**Paso 5: Crear un token de bot de Telegram** — ver [Configuración de Telegram](docs/telegram-setup.md)

**Paso 6: Ejecutar MOPS**

```bash
mops
```

El asistente te guía por la configuración del transporte (Telegram o Matrix), zona horaria, sandbox Docker opcional e instalación del servicio.

---

## Como funciona

MOPS ejecuta binarios CLI oficiales como subprocesos y los conecta a tu plataforma de mensajeria. Sin claves API, sin parches de SDK, sin encabezados falsificados. Cuando envias un mensaje en Telegram, MOPS lo pasa al CLI exactamente como si lo hubieras escrito en tu terminal.

```
Telefono (Telegram/Matrix)
  |
  v
Daemon MOPS (tu maquina)
  |
  +---> claude     (subproceso)
  +---> codex      (subproceso)
  +---> gemini     (subproceso)
  |
  v
Respuesta transmitida en vivo al telefono
```

Todo el estado se almacena en `~/.mops/` como JSON y Markdown simples. Sin base de datos, sin servicios externos.

---

## Modos de chat

MOPS te ofrece cinco niveles de interaccion. Empieza simple, escala segun necesites.

### 1 &mdash; Chat individual

Tu conversacion principal 1:1. Cada mensaje va al CLI activo, las respuestas se transmiten en vivo.

```
Tu:    "Explica el flujo de auth en esta codebase"
Bot:   [transmite respuesta de Claude Code]

Tu:    /model
Bot:   [cambiar a Codex o Gemini]
```

### 2 &mdash; Temas de grupo

Crea un grupo de Telegram con temas habilitados. Cada tema obtiene su propio contexto CLI aislado. Cinco temas = cinco conversaciones paralelas, todo en un grupo.

```
Mis Proyectos/
  General        -- contexto propio
  Auth           -- contexto propio, modelo propio
  Frontend       -- contexto propio
  Base de datos  -- contexto propio
  Refactorizacion -- contexto propio
```

### 3 &mdash; Sesiones con nombre

Inicia una conversacion lateral sin perder tu contexto actual. Como abrir una segunda terminal.

```
Tu:    "Trabajemos en la autenticacion"
Bot:   [responde sobre auth]

/session Arreglar la exportacion CSV rota
Bot:   [trabaja en CSV en contexto separado]

Tu:    "Volvamos a auth -- agregar limitacion de tasa"
Bot:   [retoma exactamente donde lo dejaste]
```

### 4 &mdash; Tareas en segundo plano

Delega trabajo de larga duracion. Tu sigues chateando, la tarea se ejecuta de forma autonoma, los resultados llegan cuando terminan.

```
Tu:    "Investiga los 5 principales competidores y escribe un resumen"
Bot:   -> delega, tu sigues trabajando
Bot:   -> listo, el resumen aparece en tu chat
```

### 5 &mdash; Sub-agentes

Segundo bot completamente aislado -- workspace propio, memoria propia, CLI propio, configuracion propia. Se ejecuta en otro proveedor si quieres.

```bash
mops agents add codex-agent
```

Ahora tienes Claude en tu chat principal y Codex en un chat separado, trabajando en paralelo con contextos independientes. Pueden delegarse tareas mutuamente.

<details>
<summary><strong>Tabla comparativa de modos</strong></summary>
<br>

|  | Individual | Temas | Sesiones | Tareas | Sub-agentes |
|---|---|---|---|---|---|
| **Que** | 1:1 principal | Un tema = un chat | Contexto lateral | "Haz esto en segundo plano" | Bot separado |
| **Contexto** | Uno por proveedor | Uno por tema | Propio por sesion | Propio, resultado regresa | Completamente aislado |
| **Workspace** | `~/.mops/` | Compartido | Compartido | Compartido | Propio en `agents/` |
| **Configuracion** | Automatica | Crear grupo + temas | `/session <prompt>` | Automatica | `mops agents add` |

</details>

---

## Caracteristicas

**Multi-proveedor** &mdash; Cambia entre Claude, Codex y Gemini con `/model`. Por tema, por sesion.

**Multi-transporte** &mdash; Telegram y Matrix se ejecutan simultaneamente. Sistema de plugins para Discord, Slack, Signal.

**Streaming en tiempo real** &mdash; Edicion de mensajes en vivo en Telegram, basada en segmentos en Matrix.

**Memoria persistente** &mdash; Archivos Markdown simples que sobreviven a sesiones y reinicios.

**Cron y webhooks** &mdash; Programa tareas recurrentes con soporte de zonas horarias. Triggers de webhook para integraciones externas.

**Sandbox Docker** &mdash; Contenedor sidecar opcional con montajes de host configurables para ejecucion segura de codigo.

**Servicio en segundo plano** &mdash; Instalable como systemd (Linux), launchd (macOS) o Task Scheduler (Windows).

**Sincronizacion de habilidades** &mdash; Habilidades compartidas entre `~/.claude/`, `~/.codex/`, `~/.gemini/`.

**Configuracion hot-reload** &mdash; Cambia idioma, modelo, permisos, escena -- sin reiniciar.

**7 idiomas** &mdash; English, Deutsch, Nederlands, Francais, Russkij, Espanol, Portugues.

---

## Soporte de transporte

| Plataforma | Estado | Streaming | Interaccion | Instalacion |
|---|---|---|---|---|
| **Telegram** | Principal | Edicion de mensajes en vivo | Teclados inline | Integrado |
| **Matrix** | Soportado | Basado en segmentos | Reacciones emoji | `mops install matrix` |

Ambos se ejecutan en paralelo en el mismo agente. Agregar un nuevo mensajero implica implementar `BotProtocol` en un sub-paquete -- el nucleo es completamente agnostico al transporte.

---

## Seguridad

Modelo de doble lista de permisos. Cada mensaje debe pasar ambas verificaciones:

| Tipo de chat | Requisito |
|---|---|
| **Privado** | ID de usuario en la lista de permisos |
| **Grupo** | ID de grupo en la lista de permisos Y ID de usuario en la lista de permisos |

Las listas de permisos soportan recarga en caliente. Los grupos no autorizados activan salida automatica. Todo el estado es local -- nada sale de tu maquina.

---

## Comandos

| Comando | Que hace |
|---|---|
| `/model` | Cambiar proveedor/modelo |
| `/new` | Reiniciar sesion |
| `/stop` | Detener actual + en cola |
| `/session <prompt>` | Iniciar sesion con nombre |
| `/tasks` | Ver tareas en segundo plano |
| `/cron` | Gestionar tareas programadas |
| `/agents` | Estado multi-agente |
| `/status` | Info de sesion/proveedor |
| `/diagnose` | Diagnosticos de runtime |
| `/memory` | Ver memoria persistente |

<details>
<summary><strong>Comandos CLI</strong></summary>

```bash
mops                    # Iniciar (auto-onboarding)
mops onboarding         # Re-ejecutar configuracion
mops stop               # Detener bot
mops restart            # Reiniciar
mops upgrade            # Actualizar + reiniciar
mops status             # Estado de runtime
mops uninstall          # Eliminar todo

mops service install    # Servicio en segundo plano
mops service start|stop|logs

mops docker enable      # Sandbox Docker
mops docker rebuild
mops docker mount /path

mops agents list        # Sub-agentes
mops agents add NAME
mops agents remove NAME

mops install matrix     # Transporte Matrix
mops install api        # WebSocket API
```

</details>

---

## Espacio de trabajo

```
~/.mops/
  config/config.json          # Configuracion
  sessions.json               # Estado del chat
  named_sessions.json         # Sesiones con nombre
  tasks.json                  # Tareas en segundo plano
  cron_jobs.json              # Tareas programadas
  agents.json                 # Registro de sub-agentes
  SHAREDMEMORY.md             # Conocimiento inter-agentes
  workspace/
    memory_system/            # Memoria persistente
    cron_tasks/               # Scripts cron
    skills/ tools/            # Herramientas compartidas
    tasks/                    # Carpetas por tarea
  agents/<name>/              # Espacios de trabajo aislados de sub-agentes
```

---

## Por que este enfoque

Otros proyectos parchean SDKs, falsifican encabezados o proxifican llamadas API. Eso es fragil y arriesga violar los terminos de servicio de los proveedores.

MOPS ejecuta CLIs oficiales como subprocesos. Nada mas. Tu suscripcion, tu maquina, tu autenticacion. El bot es simplemente un puente entre tu telefono y tu terminal.

---

## Documentacion

| Guia | Contenido |
|---|---|
| [Instalacion](docs/installation.md) | Guia de configuracion |
| [Vision general del sistema](docs/system_overview.md) | Runtime de extremo a extremo |
| [Arquitectura](docs/architecture.md) | Enrutamiento, streaming, callbacks |
| [Configuracion](docs/config.md) | Referencia completa de configuracion |
| [Casos de uso](docs/use-cases.md) | 10 ejemplos prácticos con comandos |
| [FAQ](docs/FAQ.md) | Preguntas frecuentes |
| [Solución de problemas](docs/troubleshooting.md) | Pasos de diagnóstico por síntoma |
| [Guía de plugins](docs/plugin-guide.md) | Agregar transportes y proveedores |
| [Configuración de Telegram](docs/telegram-setup.md) | Token del bot + configuración de grupo |
| [Configuracion de Matrix](docs/matrix-setup.md) | Transporte Matrix |
| [Automatizacion](docs/automation.md) | Cron, webhooks, heartbeat |
| [Gestion de servicios](docs/modules/service_management.md) | systemd / launchd / Task Scheduler |

---

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para configuración, requisitos de calidad y directrices de contribución.

```bash
git clone https://github.com/NathanMaine/memoriant-ops-bot.git
cd memoriant-ops-bot
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff format . && ruff check . && mypy memoriant_ops_bot
```

---

[Política de seguridad](SECURITY.md) · [Registro de cambios](CHANGELOG.md)

<p align="center">
  <strong>Licencia MIT</strong><br>
  Creado por <a href="https://github.com/NathanMaine">Memoriant Inc.</a>
</p>
