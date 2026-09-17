"""Run every check listed in checks.txt and report which claims pass.

    python run_checks.py

Exits with an error if any check fails.
"""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
here = Path(__file__).resolve().parent
failed = 0
total = 0

for line in (here / "checks.txt").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    ids, folder, command = (part.strip() for part in line.split("|", 2))
    cwd = Path(folder) if Path(folder).is_absolute() else (here / folder).resolve()
    total += 1
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    ok = result.returncode == 0
    failed += not ok
    print("%-4s  %-14s  %s  (in %s)" % ("PASS" if ok else "FAIL", ids, command, folder))
    if not ok:
        print((result.stdout + result.stderr)[-2000:])

print("\n%d of %d checks passed" % (total - failed, total))
sys.exit(1 if failed else 0)
