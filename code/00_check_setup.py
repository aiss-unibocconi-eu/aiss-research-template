"""First step of run.py: check that this machine is set up. Writes nothing.

Keep it as step one, or delete it once everyone on the project is set up.
"""
import os
import sys
from pathlib import Path

from lib.paths import DATA, RAW, ROOT

problems, notes = [], []

if not (ROOT / ".env").exists():
    problems.append("No .env file. Copy .env.example to .env and fill it in.")

if not RAW.exists() or not any(RAW.iterdir()):
    notes.append(f"data/raw is empty ({RAW}). Fine for a new project; otherwise check DATA_DIR in .env.")

stata = os.environ.get("STATA_PATH")
uses_stata = any((ROOT / "code").rglob("*.do"))
if uses_stata and stata and not Path(stata).exists():
    problems.append(f"STATA_PATH points to {stata}, which does not exist.")
elif uses_stata and not stata:
    notes.append("STATA_PATH is not set. Needed only to run .do files.")

print(f"  project root  {ROOT}")
print(f"  data folder   {DATA}")
print(f"  python        {sys.version.split()[0]}")
for note in notes:
    print(f"  note: {note}")
if problems:
    for problem in problems:
        print(f"  PROBLEM: {problem}")
    sys.exit(1)
print("  setup looks good")
