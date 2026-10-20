"""Run the whole project, in order: raw data in, tables and figures out.

    uv run python run.py           # every step
    uv run python run.py build     # only steps whose path contains "build"
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))
from lib.paths import DATA, LOGS, ensure_dirs  # noqa: E402

# Every script in the order it runs, Python and Stata alike.
# A script that is not listed here is not part of the project.
STEPS = [
    "code/00_check_setup.py",
    # "code/01_build/01_import_census.py",
    # "code/01_build/02_merge_counties.do",
    # "code/02_analysis/01_main_regressions.do",
]


def environment():
    env = dict(os.environ)  # lib.paths has already loaded .env into os.environ
    env["DATA_DIR"] = str(DATA)  # absolute, so Stata reads the same folder
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT / "code"), env.get("PYTHONPATH")]))
    return env


def run_python(step, env):
    subprocess.run([sys.executable, str(ROOT / step)], cwd=ROOT, env=env, check=True)


def run_stata(step, env):
    stata = env.get("STATA_PATH")
    if not stata:
        sys.exit(f"{step} is a Stata script, but STATA_PATH is not set in .env")
    flag = "/e" if os.name == "nt" else "-b"
    subprocess.run([stata, flag, "do", str(ROOT / step)], cwd=ROOT, env=env, check=True)
    # Batch mode writes <name>.log into the project root; keep it in output/logs.
    log = ROOT / (Path(step).stem + ".log")
    if log.exists():
        log = log.replace(LOGS / log.name)
        # Stata can exit with code 0 even after an error, so read the log.
        if re.search(r"^r\(\d+\);", log.read_text(errors="replace"), re.MULTILINE):
            sys.exit(f"{step} stopped with an error; see {log.relative_to(ROOT)}")


def main():
    ensure_dirs()
    env = environment()
    wanted = sys.argv[1:]
    steps = [s for s in STEPS if not wanted or any(w in s for w in wanted)]
    if not steps:
        sys.exit("No step matches " + " ".join(wanted))
    for step in steps:
        if not (ROOT / step).exists():
            sys.exit(f"{step} is listed in run.py but does not exist")
        print(f"▸ {step}", flush=True)
        start = time.time()
        try:
            if step.endswith(".py"):
                run_python(step, env)
            elif step.endswith(".do"):
                run_stata(step, env)
            else:
                sys.exit(f"Don't know how to run {step}")
        except subprocess.CalledProcessError:
            sys.exit(f"✗ {step} failed (see the message above). Later steps were not run.")
        print(f"  done in {time.time() - start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
