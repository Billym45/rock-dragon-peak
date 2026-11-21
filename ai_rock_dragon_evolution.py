import subprocess
from pathlib import Path


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


def run_with_handshake(
    task: str = "rock_dragon_evolution",
    energy: str = "peak",
    cycles: int = 1,
) -> None:
    for cycle in range(1, cycles + 1):
        stages = run_peak_algorithm(task=f"{task}_c{cycle}", energy=energy)
        handshake_ok = any(
            s["stage"] == "HANDSHAKE" and "ACK_ACTIVE" in s["detail"]
            for s in stages
        )
        if not handshake_ok:
            raise RuntimeError(f"Handshake missing on cycle {cycle}")

        for item in stages:
            print(f"[cycle {cycle}] {item['stage']}: {item['detail']}")


def main() -> None:
    run_with_handshake(task="rock_dragon_evolution", energy="peak", cycles=1)


if __name__ == "__main__":
    main()
