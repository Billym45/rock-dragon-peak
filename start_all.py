import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home()))
from ai_rock_dragon_evolution import run_with_handshake


def run_cmd(args: list[str], label: str) -> None:
    print(f"=== {label} ===")
    subprocess.run(args, check=True)


def main() -> None:
    run_with_handshake(task="start_all_boot", energy="peak", cycles=1, log_to_ledger=True)

    test_script = Path.home() / "test_peak_handshake.sh"
    if test_script.exists():
        run_cmd(["bash", str(test_script)], "Handshake Test Suite")

    optional_scripts = [
        Path.home() / "spirit_monitor.py",
        Path.home() / "builds/constant_pulse.py",
        Path.home() / "builds/master.py",
    ]
    for script in optional_scripts:
        if script.exists():
            run_cmd(["python3", str(script)], f"Running {script.name}")
        else:
            print(f"[skip] {script} not found")


if __name__ == "__main__":
    main()
