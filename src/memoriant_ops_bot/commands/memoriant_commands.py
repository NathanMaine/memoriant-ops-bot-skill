"""
Memoriant-specific commands -- unique to this fork.
Configured via environment variables for infrastructure endpoints.

Commands:
    /spark       - DGX Spark health check
    /braintrust  - Search Brain Trust knowledge base
    /nas         - NAS disk usage summary
    /report      - Today's ops report summary
    /models      - List Ollama models on Spark
    /chunks      - Qdrant chunk count
    /experts     - List Brain Trust experts
    /health      - Full system health check
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import platform
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# -- Infrastructure constants (configured via env vars) ------------------------

SPARK_HOST = os.environ.get("MOPS_SPARK_HOST", "user@localhost")
SPARK_IP = os.environ.get("MOPS_SPARK_IP", "localhost")
QDRANT_URL = os.environ.get("MOPS_QDRANT_URL", f"http://{SPARK_IP}:6333")
SSH_TIMEOUT = 10  # seconds
HTTP_TIMEOUT = 10  # seconds

OPS_REPORT_PATH = os.environ.get("MOPS_OPS_REPORT_PATH", "REPORT.md")


# -- Helpers -------------------------------------------------------------------


async def _ssh_command(cmd: str, timeout: int = SSH_TIMEOUT) -> tuple[bool, str]:
    """Run an SSH command against DGX Spark. Returns (success, output)."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "ssh",
            "-o",
            "ConnectTimeout=5",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "BatchMode=yes",
            SPARK_HOST,
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        if proc.returncode == 0:
            return True, stdout.decode("utf-8", errors="replace").strip()
        return False, stderr.decode("utf-8", errors="replace").strip()
    except asyncio.TimeoutError:
        return False, "SSH connection timed out"
    except Exception as e:
        return False, f"SSH error: {e}"


async def _http_get(url: str, timeout: int = HTTP_TIMEOUT) -> tuple[bool, str]:
    """HTTP GET via curl. Returns (success, body)."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "curl",
            "-s",
            "--connect-timeout",
            "5",
            "--max-time",
            str(timeout),
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout + 2)
        if proc.returncode == 0:
            return True, stdout.decode("utf-8", errors="replace").strip()
        return False, stderr.decode("utf-8", errors="replace").strip()
    except asyncio.TimeoutError:
        return False, "HTTP request timed out"
    except Exception as e:
        return False, f"HTTP error: {e}"


def _format_bytes(size_str: str) -> str:
    """Pass through human-readable size strings from df."""
    return size_str


def _status_icon(ok: bool) -> str:
    """Return a status indicator."""
    return "OK" if ok else "FAIL"


def _usage_warning(percent_str: str) -> str:
    """Return warning level based on disk usage percentage."""
    try:
        pct = int(percent_str.rstrip("%"))
        if pct >= 95:
            return " [CRITICAL]"
        if pct >= 90:
            return " [WARNING]"
        return ""
    except (ValueError, TypeError):
        return ""


# -- Command implementations --------------------------------------------------


async def cmd_spark() -> str:
    """DGX Spark quick health check."""
    lines = ["*DGX Spark Status*\n"]

    # Docker containers
    ok, output = await _ssh_command(
        'docker ps --format "{{.Names}}: {{.Status}}" 2>/dev/null | head -15'
    )
    if ok and output:
        lines.append("*Containers:*")
        for line in output.splitlines():
            lines.append(f"  `{line}`")
    elif ok:
        lines.append("*Containers:* none running")
    else:
        lines.append(f"*Containers:* {_status_icon(False)} {output}")

    lines.append("")

    # GPU status
    ok, output = await _ssh_command(
        "nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total "
        "--format=csv,noheader,nounits 2>/dev/null"
    )
    if ok and output:
        lines.append("*GPU:*")
        for line in output.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 5:
                name, temp, util, mem_used, mem_total = parts[:5]
                lines.append(f"  `{name}` | {temp}C | {util}% util | {mem_used}/{mem_total} MB")
            else:
                lines.append(f"  `{line}`")
    else:
        lines.append(f"*GPU:* {_status_icon(False)} {output}")

    lines.append("")

    # Disk usage
    ok, output = await _ssh_command("df -h $HOME --output=size,used,avail,pcent | tail -1")
    if ok and output:
        parts = output.split()
        if len(parts) >= 4:
            lines.append(
                f"*Disk (/home):* {parts[1]} / {parts[0]} ({parts[3]} used, {parts[2]} free)"
            )
        else:
            lines.append(f"*Disk:* `{output}`")
    else:
        lines.append(f"*Disk:* {_status_icon(False)} {output}")

    return "\n".join(lines)


async def cmd_braintrust(query: str = "") -> str:
    """Search the Brain Trust knowledge base via Qdrant."""
    if not query.strip():
        return (
            "*Brain Trust Search*\n\n"
            "Usage: `/braintrust <query>`\n"
            "Example: `/braintrust CMMC level 2 requirements`"
        )

    # Get collections first
    ok, body = await _http_get(f"{QDRANT_URL}/collections")
    if not ok:
        return f"*Brain Trust*\n\n{_status_icon(False)} Qdrant unreachable: {body}"

    try:
        data = json.loads(body)
        collections = [c["name"] for c in data.get("result", {}).get("collections", [])]
    except (json.JSONDecodeError, KeyError):
        return f"*Brain Trust*\n\n{_status_icon(False)} Invalid Qdrant response"

    if not collections:
        return "*Brain Trust*\n\nNo collections found in Qdrant."

    # Search the first collection (brain_trust or similar)
    target = next((c for c in collections if "brain" in c.lower()), collections[0])

    # Use scroll to get points (simple text search without embeddings)
    ok, body = await _http_get(
        f"{QDRANT_URL}/collections/{target}/points/scroll",
    )
    if not ok:
        return f"*Brain Trust*\n\n{_status_icon(False)} Search failed: {body}"

    try:
        data = json.loads(body)
        points = data.get("result", {}).get("points", [])
    except (json.JSONDecodeError, KeyError):
        points = []

    # Simple text-based filtering
    query_lower = query.lower()
    matches = []
    for point in points[:100]:
        payload = point.get("payload", {})
        text = str(payload.get("content", "") or payload.get("text", ""))
        creator = str(payload.get("creator", "") or payload.get("expert", "unknown"))
        title = str(payload.get("title", "") or payload.get("source", ""))
        if query_lower in text.lower() or query_lower in title.lower():
            snippet = text[:200].replace("\n", " ")
            matches.append(f"  *{creator}* - {title}\n  `{snippet}...`")
            if len(matches) >= 3:
                break

    if not matches:
        return f"*Brain Trust*\n\nNo results for: `{query}`\nSearched collection: `{target}`"

    result_text = "\n\n".join(matches)
    return f"*Brain Trust Results* ({len(matches)} hits)\n\n{result_text}"


async def cmd_nas() -> str:
    """NAS disk usage summary."""
    lines = ["*NAS Disk Usage*\n"]

    nas_base = os.environ.get("MOPS_NAS_MOUNT", "/mnt/nas")
    volumes = [
        ("ai-models", f"{nas_base}/ai-models"),
        ("additional-ai-models", f"{nas_base}/additional-ai-models"),
        ("projects", f"{nas_base}/projects"),
    ]

    for name, path in volumes:
        ok, output = await _ssh_command(
            f"df -h {path} --output=size,used,avail,pcent 2>/dev/null | tail -1"
        )
        if ok and output:
            parts = output.split()
            if len(parts) >= 4:
                warning = _usage_warning(parts[3])
                lines.append(f"*{name}:* {parts[1]} / {parts[0]} ({parts[3]} used){warning}")
            else:
                lines.append(f"*{name}:* `{output}`")
        else:
            lines.append(f"*{name}:* {_status_icon(False)} unreachable")

    return "\n".join(lines)


async def cmd_report() -> str:
    """Show current ops report summary."""
    report_path = Path(OPS_REPORT_PATH)

    if not report_path.exists():
        return f"*Ops Report*\n\n{_status_icon(False)} Report not found at:\n`{OPS_REPORT_PATH}`"

    try:
        content = await asyncio.to_thread(report_path.read_text, encoding="utf-8")
    except OSError as e:
        return f"*Ops Report*\n\n{_status_icon(False)} Read error: {e}"

    # Extract key sections
    lines_out = ["*Ops Report Summary*\n"]

    # Find program status
    in_section = False
    section_lines: list[str] = []
    priority_lines: list[str] = []

    for line in content.splitlines():
        if "## Program Status" in line or "## Status" in line:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            in_section = False
            continue
        if in_section and line.strip():
            section_lines.append(line.strip())

        if "Priority 1" in line or "P1" in line or "CRITICAL" in line.upper():
            priority_lines.append(line.strip())

    if section_lines:
        lines_out.append("*Status:*")
        for sl in section_lines[:5]:
            lines_out.append(f"  {sl}")
        lines_out.append("")

    if priority_lines:
        lines_out.append("*Priority Items:*")
        for pl in priority_lines[:5]:
            lines_out.append(f"  {pl}")
        lines_out.append("")

    # Show last modified time
    mtime = report_path.stat().st_mtime
    from datetime import datetime

    mod_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    lines_out.append(f"_Last updated: {mod_time}_")

    return "\n".join(lines_out)


async def cmd_models() -> str:
    """List all Ollama models on Spark."""
    ok, output = await _ssh_command(
        "docker exec ollama ollama list 2>/dev/null",
        timeout=15,
    )

    if not ok:
        # Try direct ollama
        ok, output = await _ssh_command("ollama list 2>/dev/null", timeout=15)

    if not ok:
        return f"*Ollama Models*\n\n{_status_icon(False)} {output}"

    if not output.strip():
        return "*Ollama Models*\n\nNo models installed."

    lines = ["*Ollama Models*\n"]
    for i, line in enumerate(output.splitlines()):
        if i == 0:
            # Header row
            lines.append(f"`{line}`")
        else:
            parts = line.split()
            if parts:
                name = parts[0]
                size = parts[-2] if len(parts) >= 3 else ""
                lines.append(f"  `{name}` ({size})")

    return "\n".join(lines)


async def cmd_chunks() -> str:
    """Qdrant chunk count and collection status."""
    ok, body = await _http_get(f"{QDRANT_URL}/collections")
    if not ok:
        return f"*Qdrant Status*\n\n{_status_icon(False)} Unreachable: {body}"

    try:
        data = json.loads(body)
        collections = data.get("result", {}).get("collections", [])
    except (json.JSONDecodeError, KeyError):
        return f"*Qdrant Status*\n\n{_status_icon(False)} Invalid response"

    if not collections:
        return "*Qdrant Status*\n\nNo collections found."

    lines = ["*Qdrant Collections*\n"]
    total_points = 0

    for coll in collections:
        name = coll.get("name", "unknown")
        # Get collection info
        ok2, info_body = await _http_get(f"{QDRANT_URL}/collections/{name}")
        if ok2:
            try:
                info = json.loads(info_body)
                result = info.get("result", {})
                points = result.get("points_count", 0)
                status = result.get("status", "unknown")
                total_points += points
                lines.append(f"  `{name}`: {points:,} chunks ({status})")
            except (json.JSONDecodeError, KeyError):
                lines.append(f"  `{name}`: info unavailable")
        else:
            lines.append(f"  `{name}`: unreachable")

    lines.append(f"\n*Total:* {total_points:,} chunks across {len(collections)} collection(s)")
    return "\n".join(lines)


async def cmd_experts() -> str:
    """List Brain Trust experts from Qdrant."""
    ok, body = await _http_get(f"{QDRANT_URL}/collections")
    if not ok:
        return f"*Brain Trust Experts*\n\n{_status_icon(False)} Qdrant unreachable: {body}"

    try:
        data = json.loads(body)
        collections = data.get("result", {}).get("collections", [])
    except (json.JSONDecodeError, KeyError):
        return f"*Brain Trust Experts*\n\n{_status_icon(False)} Invalid response"

    target = next(
        (c["name"] for c in collections if "brain" in c.get("name", "").lower()),
        None,
    )
    if not target:
        if collections:
            target = collections[0]["name"]
        else:
            return "*Brain Trust Experts*\n\nNo collections found."

    # Scroll through points and group by creator
    ok, body = await _http_get(f"{QDRANT_URL}/collections/{target}/points/scroll")
    if not ok:
        return f"*Brain Trust Experts*\n\n{_status_icon(False)} {body}"

    try:
        data = json.loads(body)
        points = data.get("result", {}).get("points", [])
    except (json.JSONDecodeError, KeyError):
        points = []

    experts: dict[str, int] = {}
    for point in points:
        payload = point.get("payload", {})
        creator = str(
            payload.get("creator", "")
            or payload.get("expert", "")
            or payload.get("author", "unknown")
        )
        if creator:
            experts[creator] = experts.get(creator, 0) + 1

    if not experts:
        return f"*Brain Trust Experts*\n\nNo expert data found in `{target}`."

    lines = [f"*Brain Trust Experts* ({target})\n"]
    for name, count in sorted(experts.items(), key=lambda x: -x[1]):
        lines.append(f"  *{name}*: {count} nodes")

    return "\n".join(lines)


async def cmd_health() -> str:
    """Full system health check combining all subsystems."""
    lines = ["*System Health Dashboard*\n"]

    # 1. DGX Spark
    spark_ok, _ = await _ssh_command("echo ok", timeout=5)
    lines.append(f"*DGX Spark:* {_status_icon(spark_ok)}")

    # 2. GPU
    if spark_ok:
        gpu_ok, gpu_out = await _ssh_command(
            "nvidia-smi --query-gpu=utilization.gpu,temperature.gpu "
            "--format=csv,noheader,nounits 2>/dev/null"
        )
        if gpu_ok and gpu_out:
            parts = [p.strip() for p in gpu_out.split(",")]
            if len(parts) >= 2:
                lines.append(f"  GPU: {parts[0]}% util, {parts[1]}C")
        else:
            lines.append(f"  GPU: {_status_icon(False)}")
    else:
        lines.append("  GPU: unreachable")

    # 3. NAS
    if spark_ok:
        nas_ok, _ = await _ssh_command("ls /mnt/nas/ai-models >/dev/null 2>&1 && echo ok")
        lines.append(f"*NAS:* {_status_icon(nas_ok)}")
    else:
        lines.append("*NAS:* unreachable (via Spark)")

    # 4. Qdrant
    qdrant_ok, qdrant_body = await _http_get(f"{QDRANT_URL}/collections")
    qdrant_detail = ""
    if qdrant_ok:
        try:
            data = json.loads(qdrant_body)
            n = len(data.get("result", {}).get("collections", []))
            qdrant_detail = f" ({n} collections)"
        except (json.JSONDecodeError, KeyError):
            pass
    lines.append(f"*Qdrant:* {_status_icon(qdrant_ok)}{qdrant_detail}")

    # 5. Ollama
    if spark_ok:
        ollama_ok, ollama_out = await _ssh_command(
            "docker exec ollama ollama list 2>/dev/null | wc -l"
        )
        if ollama_ok:
            try:
                n_models = max(0, int(ollama_out.strip()) - 1)
                lines.append(f"*Ollama:* {_status_icon(True)} ({n_models} models)")
            except ValueError:
                lines.append(f"*Ollama:* {_status_icon(True)}")
        else:
            lines.append(f"*Ollama:* {_status_icon(False)}")
    else:
        lines.append("*Ollama:* unreachable")

    # 6. Local machine
    load = os.getloadavg()
    lines.append(
        f"\n*Local ({platform.node()}):*\n  Load: {load[0]:.1f} / {load[1]:.1f} / {load[2]:.1f}"
    )

    return "\n".join(lines)


# -- Command registry for Telegram integration --------------------------------

MEMORIANT_COMMANDS: dict[str, tuple[str, str]] = {
    "spark": ("DGX Spark status", "Check DGX Spark health"),
    "braintrust": ("Brain Trust search", "Search expert knowledge"),
    "nas": ("NAS disk usage", "Show NAS storage status"),
    "report": ("Ops report", "Today's ops report summary"),
    "models": ("Ollama models", "List models on Spark"),
    "chunks": ("Qdrant stats", "Show chunk counts"),
    "experts": ("Brain Trust experts", "List expert contributors"),
    "health": ("System health", "Full system health check"),
}


async def dispatch_memoriant_command(command: str, args: str = "") -> str | None:
    """Dispatch a Memoriant-specific command. Returns response text or None."""
    handlers = {
        "spark": lambda: cmd_spark(),
        "braintrust": lambda: cmd_braintrust(args),
        "nas": lambda: cmd_nas(),
        "report": lambda: cmd_report(),
        "models": lambda: cmd_models(),
        "chunks": lambda: cmd_chunks(),
        "experts": lambda: cmd_experts(),
        "health": lambda: cmd_health(),
    }

    handler = handlers.get(command)
    if handler is None:
        return None

    try:
        return await handler()
    except Exception:
        logger.exception("Memoriant command /%s failed", command)
        return f"*/{command}*\n\nCommand failed. Check logs for details."
