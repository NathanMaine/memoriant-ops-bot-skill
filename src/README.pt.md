[English](README.md) | [Deutsch](README.de.md) | [Nederlands](README.nl.md) | [Francais](README.fr.md) | [Russkij](README.ru.md) | [Espanol](README.es.md) | [Portugues](README.pt.md)

<p align="center">
  <img src="docs/images/mops-logo.jpeg" alt="MOPS" width="280">
</p>

<h1 align="center">MOPS</h1>

<p align="center">
  <em>Controle de agentes IA multi-provedor direto do seu celular.</em>
</p>

<p align="center">
  <a href="#inicio-rapido">Inicio rapido</a> &middot;
  <a href="#como-funciona">Como funciona</a> &middot;
  <a href="#funcionalidades">Funcionalidades</a> &middot;
  <a href="docs/use-cases.md">Casos de uso</a> &middot;
  <a href="docs/installation.md">Guia de instalacao</a> &middot;
  <a href="docs/architecture.md">Arquitetura</a>
</p>

<p align="center">
  <img src="https://github.com/NathanMaine/memoriant-ops-bot/actions/workflows/tests.yml/badge.svg" alt="Tests">
  <img src="https://img.shields.io/badge/providers-Claude%20%7C%20Codex%20%7C%20Gemini-blue" alt="Provedores">
  <img src="https://img.shields.io/badge/transport-Telegram%20%7C%20Matrix-green" alt="Transporte">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="Licenca">
  <img src="https://img.shields.io/badge/python-3.11%2B-yellow" alt="Python">
  <img src="https://img.shields.io/pypi/v/memoriant-ops-bot" alt="PyPI">
</p>

---

Execute Claude Code, OpenAI Codex CLI ou Google Gemini CLI a partir do Telegram ou Matrix. Utiliza exclusivamente CLIs oficiais como subprocessos -- nada falsificado, nada proxificado. Sua assinatura, sua maquina, seus dados.

<p align="center">
  <img src="docs/images/mops-demo.gif" alt="MOPS Demo" width="300">
</p>

> **Lancado em 12 de marco de 2026** -- cinco dias antes da Anthropic lancar o [Claude Dispatch](https://mlq.ai/news/anthropic-launches-claude-dispatch-for-remote-desktop-ai-control/). Mesmo conceito, filosofia diferente.

### Como isso se compara ao Claude Dispatch?


|  | MOPS | Claude Dispatch |
|---|---|---|
| **Provedores** | Claude + Codex + Gemini | Apenas Claude |
| **Custo** | Gratuito -- usa suas assinaturas existentes | Plano Max necessario ($100+/mes) |
| **Controle remoto de** | Telegram, Matrix, qualquer dispositivo | App movel do Claude |
| **Controla** | Qualquer maquina -- servidores, rigs GPU, nuvem | Apenas desktop Mac |
| **Agentes paralelos** | Ilimitados -- topicos, sessoes, sub-agentes | Conversa unica |
| **Open source** | MIT | Proprietario |
| **Tarefas em segundo plano** | Sim, com delegacao + acompanhamentos | Sim |
| **Sessoes nomeadas** | Sim | Nao |
| **Sistema de plugins** | Sim -- adicione Discord, Slack, Signal | Nao |

---

## Inicio rapido

**Passo 1: Instalar Python** (pular se já tem Python 3.11+)

```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Windows — baixar de https://www.python.org/downloads/
# ✅ Marque "Add Python to PATH" durante a instalação
```

**Passo 2: Instalar pipx** (ferramenta para aplicações Python)

```bash
# macOS
brew install pipx && pipx ensurepath

# Linux
pip install pipx && pipx ensurepath

# Windows
pip install pipx
pipx ensurepath
```

> Após `pipx ensurepath`, **feche e reabra o terminal**.

**Passo 3: Instalar MOPS**

```bash
pipx install memoriant-ops-bot
```

**Passo 4: Instalar pelo menos um CLI de IA** (o agente que MOPS controlará)

```bash
# Escolha um ou mais:
npm install -g @anthropic-ai/claude-code && claude auth     # Claude
npm install -g @openai/codex && codex auth                   # Codex
npm install -g @google/gemini-cli                            # Gemini
```

> Não tem Node.js? Instale primeiro: `brew install node` (macOS) ou `sudo apt install nodejs npm` (Linux) ou baixe de [nodejs.org](https://nodejs.org)

**Passo 5: Criar um token de bot do Telegram** — veja o [Guia de Configuração do Telegram](docs/telegram-setup.md)

**Passo 6: Executar MOPS**

```bash
mops
```

O assistente guia você pela configuração de transporte (Telegram ou Matrix), fuso horário, sandbox Docker opcional e instalação do serviço.

---

## Como funciona

MOPS executa binarios CLI oficiais como subprocessos e os conecta a sua plataforma de mensagens. Sem chaves API, sem patches de SDK, sem cabecalhos falsificados. Quando voce envia uma mensagem no Telegram, MOPS a passa para o CLI exatamente como se voce a tivesse digitado no seu terminal.

```
Celular (Telegram/Matrix)
  |
  v
Daemon MOPS (sua maquina)
  |
  +---> claude     (subprocesso)
  +---> codex      (subprocesso)
  +---> gemini     (subprocesso)
  |
  v
Resposta transmitida em tempo real para o celular
```

Todo o estado fica em `~/.mops/` como JSON e Markdown simples. Sem banco de dados, sem servicos externos.

---

## Modos de chat

MOPS oferece cinco niveis de interacao. Comece simples, escale conforme necessario.

### 1 &mdash; Chat individual

Sua conversa principal 1:1. Cada mensagem vai para o CLI ativo, respostas sao transmitidas em tempo real.

```
Voce:  "Explique o fluxo de auth nesta codebase"
Bot:   [transmite resposta do Claude Code]

Voce:  /model
Bot:   [trocar para Codex ou Gemini]
```

### 2 &mdash; Topicos de grupo

Crie um grupo no Telegram com topicos habilitados. Cada topico recebe seu proprio contexto CLI isolado. Cinco topicos = cinco conversas paralelas, tudo em um grupo.

```
Meus Projetos/
  Geral          -- contexto proprio
  Auth           -- contexto proprio, modelo proprio
  Frontend       -- contexto proprio
  Banco de dados -- contexto proprio
  Refatoracao    -- contexto proprio
```

### 3 &mdash; Sessoes nomeadas

Inicie uma conversa paralela sem perder seu contexto atual. Como abrir um segundo terminal.

```
Voce:  "Vamos trabalhar na autenticacao"
Bot:   [responde sobre auth]

/session Corrigir a exportacao CSV quebrada
Bot:   [trabalha no CSV em contexto separado]

Voce:  "Voltar ao auth -- adicionar limitacao de taxa"
Bot:   [retoma exatamente de onde voce parou]
```

### 4 &mdash; Tarefas em segundo plano

Delegue trabalhos de longa duracao. Voce continua conversando, a tarefa roda de forma autonoma, resultados aparecem quando concluidos.

```
Voce:  "Pesquise os 5 principais concorrentes e escreva um resumo"
Bot:   -> delega, voce continua trabalhando
Bot:   -> pronto, resumo aparece no seu chat
```

### 5 &mdash; Sub-agentes

Segundo bot completamente isolado -- workspace proprio, memoria propria, CLI proprio, configuracao propria. Roda em outro provedor se voce quiser.

```bash
mops agents add codex-agent
```

Agora voce tem Claude no seu chat principal e Codex em um chat separado, trabalhando em paralelo com contextos independentes. Eles podem delegar tarefas entre si.

<details>
<summary><strong>Tabela comparativa dos modos</strong></summary>
<br>

|  | Individual | Topicos | Sessoes | Tarefas | Sub-agentes |
|---|---|---|---|---|---|
| **O que** | 1:1 principal | Um topico = um chat | Contexto paralelo | "Faca isso em segundo plano" | Bot separado |
| **Contexto** | Um por provedor | Um por topico | Proprio por sessao | Proprio, resultado retorna | Completamente isolado |
| **Workspace** | `~/.mops/` | Compartilhado | Compartilhado | Compartilhado | Proprio em `agents/` |
| **Configuracao** | Automatica | Criar grupo + topicos | `/session <prompt>` | Automatica | `mops agents add` |

</details>

---

## Funcionalidades

**Multi-provedor** &mdash; Alterne entre Claude, Codex e Gemini com `/model`. Por topico, por sessao.

**Multi-transporte** &mdash; Telegram e Matrix rodam simultaneamente. Sistema de plugins para Discord, Slack, Signal.

**Streaming em tempo real** &mdash; Edicao de mensagens ao vivo no Telegram, baseada em segmentos no Matrix.

**Memoria persistente** &mdash; Arquivos Markdown simples que sobrevivem a sessoes e reinicializacoes.

**Cron e webhooks** &mdash; Agende tarefas recorrentes com suporte a fusos horarios. Gatilhos de webhook para integracoes externas.

**Sandbox Docker** &mdash; Container sidecar opcional com montagens de host configuraveis para execucao segura de codigo.

**Servico em segundo plano** &mdash; Instalavel como systemd (Linux), launchd (macOS) ou Task Scheduler (Windows).

**Sincronizacao de habilidades** &mdash; Habilidades compartilhadas entre `~/.claude/`, `~/.codex/`, `~/.gemini/`.

**Configuracao hot-reload** &mdash; Mude idioma, modelo, permissoes, cena -- sem reiniciar.

**7 idiomas** &mdash; English, Deutsch, Nederlands, Francais, Russkij, Espanol, Portugues.

---

## Suporte de transporte

| Plataforma | Status | Streaming | Interacao | Instalacao |
|---|---|---|---|---|
| **Telegram** | Principal | Edicao de mensagens ao vivo | Teclados inline | Integrado |
| **Matrix** | Suportado | Baseado em segmentos | Reacoes emoji | `mops install matrix` |

Ambos rodam em paralelo no mesmo agente. Adicionar um novo mensageiro significa implementar `BotProtocol` em um sub-pacote -- o nucleo e completamente agnostico ao transporte.

---

## Seguranca

Modelo de dupla lista de permissoes. Cada mensagem deve passar por ambas as verificacoes:

| Tipo de chat | Requisito |
|---|---|
| **Privado** | ID do usuario na lista de permissoes |
| **Grupo** | ID do grupo na lista de permissoes E ID do usuario na lista de permissoes |

As listas de permissoes suportam recarga a quente. Grupos nao autorizados acionam saida automatica. Todo o estado e local -- nada sai da sua maquina.

---

## Comandos

| Comando | O que faz |
|---|---|
| `/model` | Trocar provedor/modelo |
| `/new` | Reiniciar sessao |
| `/stop` | Parar atual + na fila |
| `/session <prompt>` | Iniciar sessao nomeada |
| `/tasks` | Ver tarefas em segundo plano |
| `/cron` | Gerenciar tarefas agendadas |
| `/agents` | Status multi-agente |
| `/status` | Info da sessao/provedor |
| `/diagnose` | Diagnosticos de runtime |
| `/memory` | Ver memoria persistente |

<details>
<summary><strong>Comandos CLI</strong></summary>

```bash
mops                    # Iniciar (auto-onboarding)
mops onboarding         # Re-executar configuracao
mops stop               # Parar bot
mops restart            # Reiniciar
mops upgrade            # Atualizar + reiniciar
mops status             # Status de runtime
mops uninstall          # Remover tudo

mops service install    # Servico em segundo plano
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

## Espaco de trabalho

```
~/.mops/
  config/config.json          # Configuracao
  sessions.json               # Estado do chat
  named_sessions.json         # Sessoes nomeadas
  tasks.json                  # Tarefas em segundo plano
  cron_jobs.json              # Tarefas agendadas
  agents.json                 # Registro de sub-agentes
  SHAREDMEMORY.md             # Conhecimento inter-agentes
  workspace/
    memory_system/            # Memoria persistente
    cron_tasks/               # Scripts cron
    skills/ tools/            # Ferramentas compartilhadas
    tasks/                    # Pastas por tarefa
  agents/<name>/              # Espacos de trabalho isolados dos sub-agentes
```

---

## Por que esta abordagem

Outros projetos fazem patches em SDKs, falsificam cabecalhos ou proxificam chamadas API. Isso e fragil e arrisca violar os termos de servico dos provedores.

MOPS executa CLIs oficiais como subprocessos. Nada mais. Sua assinatura, sua maquina, sua autenticacao. O bot e apenas uma ponte entre seu celular e seu terminal.

---

## Documentacao

| Guia | Conteudo |
|---|---|
| [Instalacao](docs/installation.md) | Guia de configuracao |
| [Visao geral do sistema](docs/system_overview.md) | Runtime de ponta a ponta |
| [Arquitetura](docs/architecture.md) | Roteamento, streaming, callbacks |
| [Configuracao](docs/config.md) | Referencia completa de configuracao |
| [Casos de uso](docs/use-cases.md) | 10 exemplos práticos com comandos |
| [FAQ](docs/FAQ.md) | Perguntas frequentes |
| [Solução de problemas](docs/troubleshooting.md) | Passos de diagnóstico por sintoma |
| [Guia de plugins](docs/plugin-guide.md) | Adicionar transportes e provedores |
| [Configuração do Telegram](docs/telegram-setup.md) | Token do bot + configuração de grupo |
| [Configuracao Matrix](docs/matrix-setup.md) | Transporte Matrix |
| [Automacao](docs/automation.md) | Cron, webhooks, heartbeat |
| [Gerenciamento de servicos](docs/modules/service_management.md) | systemd / launchd / Task Scheduler |

---

## Contribuir

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para configuração, requisitos de qualidade e diretrizes de contribuição.

```bash
git clone https://github.com/NathanMaine/memoriant-ops-bot.git
cd memoriant-ops-bot
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff format . && ruff check . && mypy memoriant_ops_bot
```

---

[Política de segurança](SECURITY.md) · [Registro de alterações](CHANGELOG.md)

<p align="center">
  <strong>Licenca MIT</strong><br>
  Criado por <a href="https://github.com/NathanMaine">Memoriant Inc.</a>
</p>
