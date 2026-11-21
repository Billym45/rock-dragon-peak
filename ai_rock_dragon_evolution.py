import json
import os
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def gemini_live_check(prompt: str = "Reply with ONLY: ROCK_DRAGON_ONLINE") -> dict[str, str]:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return {"gemini_status": "LOCAL_ONLY", "gemini_reply": "GEMINI_API_KEY not set"}

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={api_key}"
    )
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )
        return {"gemini_status": "ONLINE", "gemini_reply": text or "EMPTY_RESPONSE"}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"gemini_status": "OFFLINE_FALLBACK", "gemini_reply": str(exc)}


def run_peak_algorithm(
    task: str = "rock_dragon_evolution",
    energy: str = "peak",
    script_path: str = "~/gemini_peak_alg.sh",
) -> list[dict[str, str]]:
    script = Path(script_path).expanduser()
    if not script.exists():
        raise FileNotFoundError(f"Missing script: {script}")

    proc = subprocess.run(
        ["bash", str(script), task, energy],
        capture_output=True,
        text=True,
        check=True,
    )

    stages: list[dict[str, str]] = []
    for line in proc.stdout.strip().splitlines():
        if "->" in line and "]" in line:
            _, after_time = line.split("]", 1)
            stage, detail = after_time.split("->", 1)
            stages.append({
                "stage": stage.strip(),
                "detail": detail.strip(),
            })
    return stages


def append_ledger(
    task: str,
    energy: str,
    stages: list[dict[str, str]],
    gemini_info: dict[str, str],
    ledger_path: str = "~/builds/rock_dragon_peak_project/rock_dragon_peak_ledger.jsonl",
) -> Path:
    path = Path(ledger_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project": "rock_dragon_peak",
        "task": task,
        "energy": energy,
        "status": "PASS",
        "handshake": "ACK_ACTIVE",
        "motion": "MOTION_ACTIVE",
        "gemini": gemini_info,
        "stages": {s["stage"]: s["detail"] for s in stages},
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return path


def run_with_handshake(
    task: str = "rock_dragon_evolution",
    energy: str = "peak",
    cycles: int = 1,
    log_to_ledger: bool = True,
) -> list[dict[str, str]]:
    last_stages: list[dict[str, str]] = []
    for cycle in range(1, cycles + 1):
        cycle_task = f"{task}_c{cycle}"
        stages = run_peak_algorithm(task=cycle_task, energy=energy)
        handshake_ok = any(
            s["stage"] == "HANDSHAKE" and "ACK_ACTIVE" in s["detail"]
            for s in stages
        )
        motion_ok = any(
            s["stage"] == "MOTION" and "MOTION_ACTIVE" in s["detail"]
            for s in stages
        )
        if not handshake_ok:
            raise RuntimeError(f"Handshake missing on cycle {cycle}")
        if not motion_ok:
            raise RuntimeError(f"Motion status missing on cycle {cycle}")

        gemini_info = gemini_live_check()
        print(f"[cycle {cycle}] GEMINI_LINK: {gemini_info['gemini_status']} | {gemini_info['gemini_reply']}")
        for item in stages:
            print(f"[cycle {cycle}] {item['stage']}: {item['detail']}")

        if log_to_ledger:
            append_ledger(task=cycle_task, energy=energy, stages=stages, gemini_info=gemini_info)
        last_stages = stages
    return last_stages


def main() -> None:
    run_with_handshake(task="rock_dragon_evolution", energy="peak", cycles=1)


if __name__ == "__main__":
    main()
